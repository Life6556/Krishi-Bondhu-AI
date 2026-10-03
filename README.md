# 🌾 KrishiBondhu AI — Single Input UI

Google Gemini API powered agriculture assistant.

## UI

একটি ChatGPT-style composer:
- Text
- 📎 Image attachment
- 🎙️ Voice message
- Send

Text + image + voice একই message-এ পাঠানো যায়।

## Setup

```bash
pip install -r requirements.txt
```

Set API key on Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Run:

```bash
streamlit run app.py
```

You can also use `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "YOUR_API_KEY"
```

Never commit your real API key to GitHub.
