const SAMPLES = {
  pos: "This product is absolutely amazing! I love everything about it. The quality is outstanding and the customer service was incredibly helpful and friendly. Highly recommend to everyone!",
  neg: "This was the worst experience I have ever had. The product broke after one day, customer support was useless and rude. Total waste of money. I regret buying this. Never again.",
  neu: "The package arrived on Tuesday. It contains three items as described. The manual is included in English and Hindi. Dimensions are listed on the back of the box."
};

const textInput = document.getElementById('textInput');
const charCount  = document.getElementById('charCount');

textInput.addEventListener('input', () => {
  charCount.textContent = `${textInput.value.length} / 2000`;
});

textInput.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.key === 'Enter') analyzeSentiment();
});

function setSample(type) {
  textInput.value = SAMPLES[type];
  charCount.textContent = `${textInput.value.length} / 2000`;
  analyzeSentiment();
}

async function analyzeSentiment() {
  const text = textInput.value.trim();
  const btn  = document.getElementById('analyzeBtn');
  const btnText   = document.getElementById('btnText');
  const btnLoader = document.getElementById('btnLoader');
  const resultCard = document.getElementById('resultCard');
  const errorMsg   = document.getElementById('errorMsg');

  errorMsg.classList.add('hidden');

  if (!text) {
    showError('Please enter some text to analyze.');
    return;
  }

  btnText.textContent = 'Analyzing…';
  btnLoader.classList.remove('hidden');
  btn.disabled = true;

  try {
    const res  = await fetch('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await res.json();

    if (data.error) { showError(data.error); return; }

    displayResult(data);

  } catch (err) {
    showError('Something went wrong. Make sure the Flask server is running.');
  } finally {
    btnText.textContent = 'Analyze';
    btnLoader.classList.add('hidden');
    btn.disabled = false;
  }
}

function displayResult(data) {
  const resultCard = document.getElementById('resultCard');

  document.getElementById('resultEmoji').textContent      = data.emoji;
  const label = document.getElementById('resultLabel');
  label.textContent  = data.sentiment;
  label.className    = `result-label ${data.color}`;
  document.getElementById('resultConfidence').textContent = `Confidence: ${data.confidence}%`;

  // Progress bar: 0% = all negative, 100% = all positive
  const total = data.pos_score + data.neg_score;
  const fillPct = total === 0 ? 50 : Math.round((data.pos_score / total) * 100);
  document.getElementById('progressFill').style.width = `${fillPct}%`;

  document.getElementById('statWords').textContent   = data.word_count;
  document.getElementById('statPos').textContent     = data.pos_score;
  document.getElementById('statNeg').textContent     = data.neg_score;
  document.getElementById('statDensity').textContent = `${data.sentiment_density}%`;

  // Keywords
  const posEl = document.getElementById('posKeywords');
  const negEl = document.getElementById('negKeywords');
  posEl.innerHTML = data.matched_positive.map(w => `<span class="keyword-tag pos">${w}</span>`).join('');
  negEl.innerHTML = data.matched_negative.map(w => `<span class="keyword-tag neg">${w}</span>`).join('');

  resultCard.classList.remove('hidden');
  resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(msg) {
  const el = document.getElementById('errorMsg');
  el.textContent = msg;
  el.classList.remove('hidden');
  document.getElementById('resultCard').classList.add('hidden');
}
