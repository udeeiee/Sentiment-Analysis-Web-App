from flask import Flask, render_template, request, jsonify
import re
import math
from collections import Counter

app = Flask(__name__)

# ── Simple built-in sentiment lexicon (no external downloads needed) ──────────
POSITIVE_WORDS = set([
    "good","great","excellent","amazing","wonderful","fantastic","outstanding",
    "brilliant","superb","perfect","love","loved","like","liked","enjoy","enjoyed",
    "happy","happiness","joy","joyful","pleased","pleasure","beautiful","best",
    "awesome","magnificent","incredible","positive","nice","lovely","delightful",
    "glad","grateful","thankful","exciting","excited","impressive","recommend",
    "recommended","helpful","useful","easy","simple","clean","fast","fun","funny",
    "interesting","smart","intelligent","creative","innovative","quality","worth",
    "affordable","friendly","comfortable","smooth","reliable","powerful","strong",
    "effective","efficient","productive","satisfied","satisfying","remarkable","fresh"
])

NEGATIVE_WORDS = set([
    "bad","terrible","horrible","awful","dreadful","poor","worst","hate","hated",
    "dislike","disliked","ugly","boring","slow","difficult","hard","confusing",
    "confused","frustrating","frustrated","annoying","annoyed","disappointing",
    "disappointed","useless","waste","expensive","overpriced","broken","buggy",
    "crash","crashes","fail","failed","failure","problem","issue","error","wrong",
    "sad","unhappy","angry","upset","negative","painful","pain","sick","tired",
    "weak","stupid","dumb","lazy","fake","scam","fraud","dangerous","harmful",
    "toxic","unreliable","unstable","complicated","messy","dirty","noisy","ugly",
    "regret","regrets","avoid","never","worst","pathetic","ridiculous","unacceptable"
])

NEGATION_WORDS = {"not","no","never","neither","nor","cannot","can't","don't",
                  "doesn't","didn't","won't","wouldn't","shouldn't","couldn't","isn't","wasn't"}

INTENSIFIERS = {"very","extremely","really","absolutely","totally","completely",
                "highly","incredibly","so","quite","super","truly","deeply"}

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s']", " ", text)
    tokens = text.split()
    return tokens

def analyze_sentiment(text):
    tokens = preprocess(text)
    pos_score = 0
    neg_score = 0
    matched_words = {"positive": [], "negative": []}
    
    i = 0
    while i < len(tokens):
        word = tokens[i]
        multiplier = 1.5 if (i > 0 and tokens[i-1] in INTENSIFIERS) else 1.0
        negated = any(tokens[max(0,i-3):i][j] in NEGATION_WORDS for j in range(min(3, i)))
        
        if word in POSITIVE_WORDS:
            if negated:
                neg_score += 1.0 * multiplier
                matched_words["negative"].append(f"(not) {word}")
            else:
                pos_score += 1.0 * multiplier
                matched_words["positive"].append(word)
        elif word in NEGATIVE_WORDS:
            if negated:
                pos_score += 0.5 * multiplier
                matched_words["positive"].append(f"(not) {word}")
            else:
                neg_score += 1.0 * multiplier
                matched_words["negative"].append(word)
        i += 1

    total = pos_score + neg_score
    if total == 0:
        sentiment = "Neutral"
        confidence = 50
        emoji = "😐"
        color = "neutral"
    else:
        ratio = pos_score / total
        if ratio >= 0.6:
            sentiment = "Positive"
            confidence = int(50 + ratio * 50)
            emoji = "😊"
            color = "positive"
        elif ratio <= 0.4:
            sentiment = "Negative"
            confidence = int(50 + (1 - ratio) * 50)
            emoji = "😞"
            color = "negative"
        else:
            sentiment = "Neutral"
            confidence = 50
            emoji = "😐"
            color = "neutral"

    word_count = len(tokens)
    sentiment_density = round((total / word_count) * 100, 1) if word_count > 0 else 0

    return {
        "sentiment": sentiment,
        "confidence": min(confidence, 97),
        "emoji": emoji,
        "color": color,
        "pos_score": round(pos_score, 2),
        "neg_score": round(neg_score, 2),
        "matched_positive": matched_words["positive"],
        "matched_negative": matched_words["negative"],
        "word_count": word_count,
        "sentiment_density": sentiment_density
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Please enter some text."}), 400
    if len(text) > 2000:
        return jsonify({"error": "Text too long (max 2000 characters)."}), 400
    result = analyze_sentiment(text)
    return jsonify(result)

if __name__ == "__main__":
    print("=" * 50)
    print("  Sentiment Analysis Web App")
    print("  Running at: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True)
