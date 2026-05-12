
# 🕌 KHALEEJI-MIND

**A Gulf Arabic Social Cognition Benchmark for Theory of Mind Evaluation**

> CS-UH 3260 · Artificial Social Intelligence · NYU Abu Dhabi  
> Author: Meera Alzaabi · `mha9507@nyu.edu`

---

## Overview

Theory of Mind (ToM) benchmarks have been developed almost exclusively in English-language, WEIRD (Western, Educated, Industrialized, Rich, Democratic) contexts. **KHALEEJI-MIND** is the first Gulf Arabic social cognition benchmark, consisting of 80 scenarios grounded in five core Emirati cultural norm categories:

| Category | Description |
|---|---|
| `diyafa` | Hospitality norms and hosting obligations |
| `hierarchy` | Age, rank, and status-based interaction rules |
| `gender_interaction` | Cross-gender interaction and modesty norms |
| `religious_observance` | Islamic practice and observance etiquette |
| `community_obligation` | Collective duty, neighbourhood, and سنع etiquette |

The benchmark evaluates GPT-4, Gemini 2.5 Flash, Mistral-7B, and a random baseline across three prompting conditions: zero-shot, chain-of-thought, and norm-in-context.

---

## Dataset

| Property | Value |
|---|---|
| Total scenarios | 80 |
| Norm categories | 5 |
| Language: English | 31 |
| Language: Bilingual EN/AR | 25 |
| Language: Arabic only | 24 |
| ToM Order 1 | 41 |
| ToM Order 2 | 39 |

Each scenario includes:
- A social situation in natural language (English, Arabic, or bilingual)
- A Theory of Mind question about a named character
- Four answer options: one culturally-correct answer, two plausible distractors, and one Western-centric misreading
- A `cultural_explanation` field used in the norm-in-context condition
- A `severity` rating (0–5) indicating the seriousness of the norm violation depicted

---

## Key Results

### Zero-Shot Accuracy

| Model | Overall | Diyafa | Hierarchy | Gender | Religious | Comm. Obl. | EN | Bilingual | AR |
|---|---|---|---|---|---|---|---|---|---|
| GPT-4 | 95.0% | 91.3% | 93.3% | 100.0% | 100.0% | 90.9% | 96.8% | 92.0% | 95.8% |
| Gemini | 95.0% | 91.3% | 86.7% | 100.0% | 100.0% | 100.0% | 96.8% | 96.0% | 91.7% |
| Mistral-7B | 61.3% | 65.2% | 60.0% | 60.0% | 56.2% | 63.6% | 54.8% | 76.0% | 54.2% |
| Random | 27.5% | — | — | — | — | — | — | — | — |

### Three-Condition Comparison

| Model | Zero-Shot | CoT | Norm-in-Context | NIC Δ |
|---|---|---|---|---|
| GPT-4 | 95.0% | 97.5% | 98.8% | +3.8pp |
| Gemini | 95.0% | 96.2% | 96.2% | +1.2pp |
| Mistral-7B | 61.3% | 66.2% | 75.0% | **+13.7pp** |

The norm-in-context gain for Mistral-7B (+13.7pp) vs negligible gains for frontier models indicates that Mistral's failures are knowledge-driven, while frontier model errors reflect persistent reasoning biases.

---

## Repository Structure

```
khaleeji-mind/
│
├── README.md
├── KHALEEJI_MIND_Pipeline_cleaned.ipynb   # Main notebook — all steps end-to-end
├── KHALEEJI_MIND_balanced_100_cleaned.csv # Dataset (80 scenarios, cleaned)
├── khaleeji_mind_full_results.csv         # Full results (800 rows, all models × conditions)
├── khaleeji_mind_results.png              # Accuracy chart
└── requirements.txt                       # Python dependencies
```

---

## How to Reproduce

**Step 1.** Open `KHALEEJI_MIND_Pipeline_cleaned.ipynb` in Google Colab.

**Step 2.** Run the install cell (Step 0), then do **Runtime → Restart session**.

**Step 3.** In Step 1 (Configuration), paste your OpenRouter API key:
```python
OPENROUTER_API_KEY = "your-key-here"
GEMINI_MODEL  = "google/gemini-2.5-flash"
GPT4_MODEL    = "openai/gpt-4"
LLAMA_MODEL   = "mistralai/mistral-7b-instruct-v0.1"
```

**Step 4.** Upload `KHALEEJI_MIND_balanced_100_cleaned.csv` to your Google Drive and update the path in Step 2:
```python
CSV_PATH = "/content/drive/MyDrive/ASI_FINAL_PROJECT/KHALEEJI_MIND_balanced_100_cleaned.csv"
```

**Step 5.** Run all cells top to bottom. All three models will run live — no mock fallback.

---

### Local Setup (Optional)

```bash
git clone https://github.com/mha9507/ASI_KHALEEJI.git
cd ASI_KHALEEJI
pip install -r requirements.txt
jupyter notebook KHALEEJI_MIND_Pipeline_cleaned.ipynb
```

Set `CSV_PATH` to a local path and remove the `drive.mount(...)` call in Step 2.

---

## Dependencies

```
openai
pandas
matplotlib
seaborn
scipy
scikit-learn
statsmodels
numpy>=2.0
requests
```

---

## Pipeline Overview

| Step | Description |
|---|---|
| Step 0 | Install packages |
| Step 1 | Configuration (API keys, model IDs) |
| Step 2 | Load dataset, normalize columns, build options dict |
| Step 2b | Dataset overview and statistics |
| Step 2c | Map western distractor text to answer letter |
| Step 3 | Text preprocessing and prompt construction |
| Step 4 | Model evaluation functions (random baseline + OpenRouter with retry logic) |
| Step 4b | Run zero-shot evaluation (Mistral-7B, Gemini, GPT-4, Random) |
| Step 5 | Main results table |
| Step 6 | Chain-of-thought evaluation |
| Step 7 | Norm-in-context prompts and evaluation |
| Step 8 | Visualisations |
| Step 9 | Error analysis (western-centric error rate, ToM order, severity) |
| Step 10 | Norm-in-context diagnostic and spot-check |
| Step 11 | Save full results to CSV |

---

## Known Issues

- **Single annotator:** Inter-annotator agreement cannot be computed yet; all scenarios were authored and validated by one native Emirati speaker.
- **Jais not integrated:** HuggingFace Inference API access was unavailable at submission. Replaced with Mistral-7B. Jais evaluation via T4 GPU is the first Phase 2 priority.
- **Construct validity:** Many scenarios may be solvable through general social reasoning rather than Gulf-specific cultural knowledge, limiting diagnostic power for frontier models.
- **Western distractor mapping:** Word-overlap heuristic may misassign edge cases with very short option texts.

---

## Citation

```
Alzaabi, M. (2026). KHALEEJI-MIND: A Gulf Arabic Social Cognition Benchmark
for Theory of Mind Evaluation. NYU Abu Dhabi, CS-UH 3260.
```

---

## License

Dataset and code released for academic use only. Do not redistribute without permission.

