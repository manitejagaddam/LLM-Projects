# 🧠 AI Tool & LLM Suggestor

A developer-focused AI assistant that helps you choose the right **LLM**, **API**, or **tool** for your specific task — no guessing, no trial-and-error.

> Think of it as your personalized AI tech radar 📡

---

## 🚀 Features

* 🔍 **Searchable Tool/LLM Knowledge Base**

  * Compare models like GPT-4o, Claude, Gemini, LLaMA, and more
  * Explore APIs like Notion, DuckDuckGo, Groq, and custom endpoints

* 🧠 **Smart Matching Engine**

  * Match your use-case to the best-suited AI model/tool
  * Use filters like input type, latency, cost, context length, capabilities

* 📊 **Side-by-side Comparisons**

  * Tokens, pricing, API limits, fine-tuning support, modality (text/image/audio), etc.

* 🧰 **Dev-Centric Data**

  * GitHub links, SDKs, request/response formats, usage examples

---

## 🏗️ Tech Stack

* **Backend:** Python, FastAPI
* **LLM Integrations:** OpenAI, Anthropic, Mistral, Google, Meta (via OpenRouter / direct APIs)
* **Data Source:** Manual + Web scraping + API docs parsing (TBD)
* **Frontend:** (Coming soon) React + Tailwind (planned)
* **Storage:** JSON / SQLite (MVP) → PostgreSQL or vector DB (later)
* **Auth & API Routing:** OpenRouter / Custom API Gateway (in-progress)

---

## 📦 Setup

If uv is not installed in your device then install it

```bash
pip install uv
```


```bash
git clone https://github.com/manitejagaddam/AI-Tool-Segregator.git
cd AI-Tool-Segregator
uv init .
uv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
uv add -r requirements.txt
```

> 🔑 Don’t forget to set your API keys in a `.env` file:

```
OPENROUTER_API_KEY=your_key
OPENAI_API_KEY=optional
...
```

---

## 📡 Sample Usage

```python
from suggestor import get_best_llm

task = "i want to build a sportness apllication which can track my fitness journey"
best_options = get_best_llm(task)
print(best_options)
```

Expected Output:

```
Recommended Tools:
- Firebase
- Strava API
- Fitbit Web API
- Apple HealthKit
- Google Fitness API

Recommended LLMs:
- GPT-4
- GPT-3.5 Turbo
- Gemini Pro
```

---

## 🔮 Roadmap

### Phase 1: MVP (Done ✅)

* [x] CLI interface for querying best LLM/tool
* [x] API structure with OpenRouter integration
* [x] Basic metadata for tools stored in JSON

### Phase 2: UI & Interactivity (WIP 🛠️)

* [ ] Web frontend with React + Tailwind
* [ ] Filtering, comparison view, and tool cards
* [ ] Tag-based tool exploration (e.g., "image input", "low latency")

### Phase 3: Data Expansion

* [ ] Auto-scraping of tool/API data
* [ ] Manual curation + source attributions
* [ ] Community contributions & admin review

### Phase 4: Smart Recommender

* [ ] Use-case based model reasoning ("Why Claude over Gemini?")
* [ ] Context-aware suggestion engine
* [ ] Simple prompt-to-tool matching (LLM-enhanced)

### Phase 5: Developer Ecosystem

* [ ] Public API with rate-limiting
* [ ] Plugin for VS Code / browser extensions
* [ ] Weekly digest or GitHub Action for changes in top tools


---

## 👨‍💻 Contributing

Pull requests welcome! Ideas? Bugs? [Open an issue](https://github.com/manitejagaddam/AI-Tool-Segregator/issues)

---

## 🙌 Acknowledgements

* [OpenRouter](https://openrouter.ai)

* [OpenAI](https://openai.com)
* ...and the open-source community 💖
