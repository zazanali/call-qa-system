# 📞 AI-Powered Call Quality Assurance System

An intelligent, multilingual call quality assurance (QA) tool that transcribes, analyzes, and summarizes customer support calls using OpenAI's Whisper and Gemini LLM. The tool automatically detects predefined and custom intents, assigns quality scores, and generates structured summaries—helping QA teams audit calls efficiently and at scale.

---

## 🚀 Features

- 🎧 **Audio Transcription**: High-accuracy transcription using [OpenAI Whisper].
- 🧠 **Intent Detection**: Extracts multiple relevant intent snippets using [Gemini LLM] and advanced prompt engineering.
- 🌐 **Multilingual Support**: Supports English, Urdu, Hindi, French, and more with automatic language fallback responses.
- 📊 **Intent-wise QA Scoring**: Generates intent flags and quality scores based on detected utterances.
- 📝 **Structured Call Summary**: View detailed summaries with all matching sentences grouped under each intent.
- 📥 **Batch Upload & Report Export**: Upload multiple files and export results to Excel (`.xlsx`) format.
- 🧩 **Custom Intents**: Add new intents dynamically at runtime.
- 💻 **Interactive Dashboard**: Built with Streamlit for a seamless user interface.

---

## 📁 Project Structure

```
├── app/
│   ├── main_app.py              # Streamlit frontend
│   ├── processor.py             # Core processing logic
│   ├── prompts.py               # Prompt templates and intent definitions
│   ├── utils.py                 # Utility functions (audio conversion, model loading)
│   ├── requirements.txt         # Dependencies
│   ├── README.md                # You're here
│   ├── .env                     # where you put api key
```

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/zazanali/call-qa-system.git
cd call-qa-system
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app/main_app.py
```

---

## 🛠️ Tech Stack

| Component         | Technology                         |
|------------------|-------------------------------------|
| Transcription     | [Whisper (medium)] by OpenAI        |
| LLM               | [Gemini 2.5 Flash] via Langchain    |
| Language Detection| `langdetect` Python package         |
| Audio Handling    | `ffmpeg` for conversion to `.wav`   |
| Frontend          | Streamlit                           |
| Report Export     | Pandas + Excel (`xlsxwriter`)       |

---

## 📄 Usage Guide

1. **Upload Audio**: Accepts `.mp3`, `.wav`, or `.m4a` files.
2. **Select Intents**: Choose predefined intents or add custom ones.
3. **Run Analysis**: Click the "🚀 Run Analysis" button.
4. **View Summary**: Click "📝 Summary" next to any file to view all matched snippets by intent.
5. **Download Report**: Export the analysis in Excel format with all flags and scores.

---

## ✅ Supported Intents (Predefined)

```text
Greetings, Playmusic, AddtoPlaylist, RateBook,
```

You can also define custom intents during runtime input.

---

## 📌 Call Summary Example

```
Listen to Westbam album Allergic on Google Music
Playmusic
Add 'Step to Me' to the 50 clásicos playlist
AddtoPlaylist
I give this current textbook a rating of 1 and best rating of 6
RateBook
Play the song 'Little Robin Redbreast'
Playmusic
Please add Iris Dement to my playlist
AddtoPlaylist
Add Slimm Cutta Calhoun to my playlist
AddtoPlaylist
I want to listen to seventies music
Playmusic
Good Morning
Greetings
Play a popular chant by Brian Epstein
Playmusic
```

---

## 📤 Output Report (Excel)

The Excel file includes the following columns:

- `File Name`
- `Language`
- One column per intent (`1` if detected, else `0`)
- `Score (%)` — Percentage of detected intents
- `Call Summary` — Intent-wise grouped utterances

---

## 🛡️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

PRs and suggestions are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📬 Contact

For questions or feedback, feel free to reach out via [LinkedIn](https://www.linkedin.com/zazanali) or 
email (alizazan3@gmail.com).

## 🙋‍♂️ Author

Developed by Zazan Ali – feel free to reach out for collaboration or questions!
