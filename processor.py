import os
from langdetect import detect
from utils import ffmpeg_to_wav
from prompts import PER_INTENT_PROMPT, FALLBACK_MAP

def process_call(
    audio_path: str,
    whisper_model,
    gemini_llm,
    selected_intents: list[str],
    debug: bool = False
):
    # 1) Convert & transcribe
    wav = ffmpeg_to_wav(audio_path)
    os.remove(audio_path)
    result = whisper_model.transcribe(
        wav,
        fp16=(whisper_model.device.type == "cuda")
    )
    transcript = result["text"].strip()
    os.remove(wav)

    # 2) Detect language & fallback
    lang = detect(transcript) if transcript else "en"
    fallback = FALLBACK_MAP.get(lang, FALLBACK_MAP["en"])

    # 3) Initialize storage for each intent
    summary_map: dict[str, list[str]] = { intent: [] for intent in selected_intents }

    # 4) For each intent, ask Gemini to list *all* matching utterances
    for intent in selected_intents:
        prompt_str = PER_INTENT_PROMPT.format(
            lang=lang,
            transcript=transcript,
            intent=intent,
            fallback=fallback
        )
        if debug:
            print(f"\n--- Prompt for {intent} ---\n{prompt_str}")

        response = gemini_llm.invoke(prompt_str)
        raw_lines = response.content.splitlines()
        if debug:
            print(f"--- Raw response for {intent} ---\n{raw_lines}")

        # 5) Collect every non-fallback line
        for line in raw_lines:
            ln = line.strip().lstrip("-•* ").strip()
            if ln and ln != fallback:
                summary_map[intent].append(ln)

    # 6) Remove intents with no matches
    summary_map = { intent: snippets for intent,snippets in summary_map.items() if snippets }

    # 7) Build binary flags & score
    flags = { intent: int(intent in summary_map) for intent in selected_intents }
    score = round(sum(flags.values()) / len(selected_intents) * 100, 2)

    # 8) Build the final summary text
    lines = []
    for intent, snippets in summary_map.items():
        for snippet in snippets:
            lines.append(f"{intent}: {snippet}")
    summary_text = "\n".join(lines)

    # 9) Assemble result row
    row = {
        "File Name": os.path.basename(audio_path),
        "Language": lang,
        **flags,
        "Score (%)": score,
        "Call Summary": summary_text
    }

    return row, summary_text
