# Sentiment Analysis Web App

A Flask-based web application that analyzes the sentiment of any text using NLP techniques.

## Features
- Detects Positive / Negative / Neutral sentiment
- Shows confidence score and progress bar
- Highlights matched positive/negative keywords
- Handles negation ("not good" → negative)
- Handles intensifiers ("very amazing" → stronger signal)
- 3 sample texts to test quickly
- Ctrl+Enter shortcut to analyze

## How to Run

1. **Install dependencies:**
   ```
   pip install flask
   ```

2. **Run the app:**
   ```
   python app.py
   ```

3. **Open in browser:**
   ```
   http://127.0.0.1:5000
   ```

## Project Structure
```
1_sentiment_analysis/
├── app.py                  ← Flask backend + NLP logic
├── requirements.txt
├── templates/
│   └── index.html          ← Frontend UI
└── static/
    ├── css/style.css       ← Styling
    └── js/main.js          ← Frontend logic
```

## Tech Stack
- Python, Flask
- Custom lexicon-based NLP (no downloads needed)
- HTML, CSS, Vanilla JavaScript
