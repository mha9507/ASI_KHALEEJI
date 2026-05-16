# 🕌 KHALEEJI-MIND

**A Gulf Arabic Social Cognition Benchmark for Theory of Mind Evaluation**

> CS-UH 3260 · Artificial Social Intelligence · NYU Abu Dhabi  
> Author: Meera Alzaabi

---

## Overview

Theory of Mind (ToM) benchmarks are often developed in English-language and WEIRD-context settings. **KHALEEJI-MIND** is a Gulf Arabic social cognition benchmark designed to evaluate how language models reason about Emirati cultural norms, سنع, and socially embedded misunderstandings.

The benchmark contains **80 multiple-choice scenarios** grounded in five Emirati cultural norm categories:

| Category | Description |
|---|---|
| `diyafa` | Hospitality norms, hosting obligations, qahwa etiquette, and majlis behavior |
| `hierarchy` | Age, rank, seniority, and status-based interaction rules |
| `gender_interaction` | Cross-gender interaction, modesty boundaries, and respectful conduct |
| `religious_observance` | Islamic practice, Ramadan/Eid etiquette, and observance-related norms |
| `community_obligation` | Collective duty, neighborhood responsibility, and سنع etiquette |

The benchmark evaluates **GPT-4**, **Gemini 2.5 Flash**, **Mistral-7B**, and a **random baseline** across three prompting conditions:

1. Zero-shot prompting  
2. Chain-of-thought prompting  
3. Norm-in-context prompting  

---

## Dataset

| Property | Value |
|---|---|
| Total scenarios | 80 |
| Norm categories | 5 |
| Language: English | 30 |
| Language: Bilingual EN/AR | 26 |
| Language: Arabic only | 24 |
| First-order ToM scenarios | 41 |
| Second-order ToM scenarios | 39 |
| Correct answer balance | A = 20, B = 20, C = 20, D = 20 |

Each scenario includes:

- A social situation in English, Arabic, or bilingual Arabic-English text
- A Theory of Mind question about a named character
- Four answer options
- One culturally correct answer
- Plausible distractors, including one non-local or culturally external misreading
- A `cultural_explanation` field used in the norm-in-context condition
- A `severity` rating from **0–5**

Severity is coded from **0 to 5**, where **0** means no local norm violation occurs; instead, the scenario tests whether an outsider or model misreads culturally appropriate behavior.

The dataset stores the non-local distractor field as `common_western_misreading`, but in the report and analysis this is interpreted more broadly as a culturally external or non-local misunderstanding.

---

## Key Results

### Zero-Shot Accuracy

| Model | Overall | Diyafa | Hierarchy | Gender | Religious | Comm. Obl. | EN | Bilingual | AR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GPT-4 | 93.8% | 87.0% | 100.0% | 100.0% | 100.0% | 81.8% | 96.7% | 88.5% | 95.8% |
| Gemini | 95.0% | 91.3% | 93.3% | 100.0% | 100.0% | 90.9% | 96.7% | 92.3% | 95.8% |
| Mistral-7B | 65.0% | 65.2% | 73.3% | 66.7% | 56.2% | 63.6% | 56.7% | 76.9% | 62.5% |
| Random | 27.5% | — | — | — | — | — | — | — | — |

### Three-Condition Comparison

| Model | Zero-Shot | Chain-of-Thought | Norm-in-Context | Norm-Context Δ |
|---|---:|---:|---:|---:|
| GPT-4 | 93.8% | 93.8% | 96.2% | +2.5pp |
| Gemini | 95.0% | 96.2% | 96.2% | +1.2pp |
| Mistral-7B | 65.0% | 70.0% | 80.0% | **+15.0pp** |

Norm-in-context prompting produced the strongest gain for **Mistral-7B**, which improved from **65.0%** to **80.0%**. This suggests that smaller models struggle more when Emirati cultural norms must be inferred implicitly, but improve when the relevant سنع rule is made explicit. GPT-4 and Gemini already performed strongly in zero-shot, so their smaller gains suggest that remaining errors are more likely due to subtle reasoning, ambiguity, or answer-option confusion.

---

## Repository Structure

```text
khaleeji-mind/
│
├── README.md
├── app.py                                  # Flask demo backend
├── dataset.csv                             # Dataset used by the Flask app
├── KHALEEJI_MIND_Pipeline_cleaned.ipynb    # Main notebook: full evaluation pipeline
├── KHALEEJI_MIND_final_80.csv              # Final benchmark dataset: 80 scenarios
├── khaleeji_mind_full_results.csv          # Full results: 800 rows
├── khaleeji_mind_results.png               # Zero-shot/category results visualization
├── khaleeji_mind_prompting_conditions.png  # Prompting-condition comparison figure
├── requirements.txt                        # Python dependencies
├── .gitignore
│
└── templates/
    └── index.html                          # Flask frontend interface
```

---

## How to Reproduce the Model Evaluation

### Step 1: Open the notebook

Open the notebook in Google Colab:

```text
KHALEEJI_MIND_Pipeline_cleaned.ipynb
```

### Step 2: Install dependencies

Run the install cell in Step 0. Then restart the session when Colab asks you to.

### Step 3: Add your API key

In the configuration section, paste your own OpenRouter API key:

```python
OPENROUTER_API_KEY = "your-key-here"

GEMINI_MODEL = "google/gemini-2.5-flash"
GPT4_MODEL = "openai/gpt-4"
MISTRAL_MODEL = "mistralai/mistral-7b-instruct-v0.1"
```

Do **not** commit real API keys to GitHub.

### Step 4: Load the dataset

Upload the dataset to Google Drive and update the path:

```python
CSV_PATH = "/content/drive/MyDrive/ASI_FINAL_PROJECT/KHALEEJI_MIND_final_80.csv"
```

### Step 5: Run the notebook

Run all cells from top to bottom. The notebook performs:

- Dataset loading and validation
- Dataset balance checks
- Prompt construction
- Zero-shot evaluation
- Chain-of-thought evaluation
- Norm-in-context evaluation
- Accuracy analysis
- Non-local distractor error analysis
- Severity and ToM-order analysis
- Full results export

The final results are saved to:

```text
khaleeji_mind_full_results.csv
```

The full results file contains **800 rows**:

- 80 zero-shot results for GPT-4
- 80 chain-of-thought results for GPT-4
- 80 norm-in-context results for GPT-4
- 80 zero-shot results for Gemini
- 80 chain-of-thought results for Gemini
- 80 norm-in-context results for Gemini
- 80 zero-shot results for Mistral-7B
- 80 chain-of-thought results for Mistral-7B
- 80 norm-in-context results for Mistral-7B
- 80 zero-shot random baseline results

---

## Running the Flask Demo App

The repository also includes a simple Flask web app that lets users answer random KHALEEJI-MIND scenarios interactively.

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the app

```bash
python app.py
```

Then open this link in your browser:

```text
http://127.0.0.1:5000
```

The app randomly samples a scenario from `dataset.csv`, displays the multiple-choice question, checks the selected answer, and returns:

- Whether the answer was correct
- The correct answer
- The cultural explanation
- The violated norm
- The common non-local / culturally external misreading

User responses are saved locally to:

```text
user_responses.csv
```

This file is ignored by Git because it may contain local testing data.

---

## Local Setup

To run the notebook locally:

```bash
git clone https://github.com/mha9507/ASI_KHALEEJI.git
cd ASI_KHALEEJI
pip install -r requirements.txt
jupyter notebook KHALEEJI_MIND_Pipeline_cleaned.ipynb
```

If running locally, set `CSV_PATH` to the local dataset path and remove or comment out the Google Drive mounting cell.

---

## Dependencies

The main dependencies are:

```text
flask
openai
pandas
matplotlib
seaborn
scipy
scikit-learn
statsmodels
numpy>=2.0
requests
jupyter
```

---

## Pipeline Overview

| Step | Description |
|---|---|
| Step 0 | Install packages |
| Step 1 | Configure API keys and model IDs |
| Step 2 | Load dataset, normalize columns, and build option dictionaries |
| Step 2b | Generate dataset overview and balance statistics |
| Step 2c | Map non-local distractor explanations to answer letters |
| Step 3 | Build zero-shot prompts |
| Step 4 | Define evaluation functions and retry logic |
| Step 4b | Run zero-shot evaluation |
| Step 5 | Generate main zero-shot results table |
| Step 6 | Run chain-of-thought evaluation |
| Step 7 | Build and run norm-in-context prompts |
| Step 8 | Generate visualizations |
| Step 9 | Analyze non-local distractor errors, ToM order, and severity |
| Step 10 | Run norm-in-context diagnostic and failure spot-checks |
| Step 11 | Save full results to CSV |

---

## Known Issues and Limitations

- **Single annotator:** The scenarios were authored and validated by one native Emirati speaker, so inter-annotator agreement could not be computed.
- **Jais not integrated:** HuggingFace/API access was unavailable at submission time, so Mistral-7B was used instead. Jais evaluation is a future Phase 2 priority.
- **Construct validity:** Some scenarios may be solvable through general social reasoning rather than Gulf-specific cultural knowledge, especially for frontier models.
- **Non-local distractor mapping:** The dataset stores this field as `common_western_misreading`, but the analysis interprets it more broadly as a non-local or culturally external misunderstanding. The matching heuristic may misassign edge cases with very short or semantically similar answer options.
- **Output parsing:** Some Mistral-7B errors are blank or unparseable outputs, so they should be interpreted partly as formatting failures rather than only reasoning failures.
- **Ambiguous items:** A small number of scenarios, such as KM_D07, KM_D11, KM_H18, and KM_H19, may require further refinement because frontier-model raw responses suggest answer-option ambiguity.

---

## Next Steps

- Expand the dataset to **150+ scenarios** with more adversarial examples.
- Add validation from at least **three native Gulf Arabic annotators** and compute inter-annotator agreement.
- Evaluate **Jais-13B** as an Arabic-native baseline.
- Add **3-shot and 5-shot prompting** conditions.
- Conduct a small human baseline study with Emirati participants.
- Release the dataset and benchmark publicly after further validation.

---

## API Key Safety

API keys are not included in this repository. Users must provide their own API key when running the notebook.

Before uploading or sharing the notebook, search for and remove:

```text
api_key
OPENROUTER_API_KEY
GEMINI_API_KEY
Authorization
Bearer
sk-
```

Do not commit `.env` files or notebook outputs containing private keys.

---

## Submission Checklist

- [x] Final dataset contains 80 scenarios
- [x] Correct answers are balanced across A, B, C, and D
- [x] Full results file contains 800 rows
- [x] Notebook runs end-to-end
- [x] Flask demo app runs locally
- [x] `requirements.txt` included
- [x] `.gitignore` included
- [x] API keys removed before upload

---

## Citation

```text
Alzaabi, M. (2026). KHALEEJI-MIND: A Gulf Arabic Social Cognition Benchmark
for Theory of Mind Evaluation. NYU Abu Dhabi, CS-UH 3260.
```

---

## License

Dataset and code are released for academic use only. Do not redistribute without permission.
