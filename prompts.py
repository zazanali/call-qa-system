# prompts.py

from langchain_core.prompts import PromptTemplate

PREDEFINED_INTENTS = [
    "Greetings", "Playmusic", "AddtoPlaylist", "RateBook"
]

# ── Bulk Intent Summary ─────────────────────────────────────────
# Use this if you want a one‐shot summary for all intents (only first snippet each)
SUMMARY_PROMPT = PromptTemplate(
    input_variables=["lang", "transcript", "intents", "fallback"],
    template="""
You are a call QA assistant. The transcript language is **{lang}**.
For each of these intents, output either:

- IntentName: 'exact snippet'
or
- IntentName: {fallback}

Intents to check:
{intents}

Transcript:
\"\"\"{transcript}\"\"\"
"""
)

# ── Per‐Intent Full Extraction ───────────────────────────────────
# Use this when you need to list *all* utterances for one specific intent
PER_INTENT_PROMPT = PromptTemplate(
    input_variables=["lang", "transcript", "intent", "fallback"],
    template="""
You are a call QA assistant. The transcript language is **{lang}**.
List *all* utterances from this transcript that correspond to the intent **{intent}**.
If none are found, respond exactly with: {fallback}

Transcript:
\"\"\"{transcript}\"\"\"
"""
)

# ── Fallback Messages by Language ────────────────────────────────
FALLBACK_MAP = {
    "ur": "اِس اِیشو کے لیے مُتعَلِقہ مَتن موجُود نہیں ہے۔",
    "en": "No relevant content found for this issue.",
    "hi": "इस मुद्दे के लिए कोई प्रासंगिक सामग्री उपलब्ध नहीं है।",
    "fr": "Aucun contenu pertinent n’a been trouvé pour ce sujet.",
    "es": "No se encontró contenido relevante para este विषय।"
}
