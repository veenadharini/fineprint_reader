# 🕵️ FinePrintFinder

**Automatically extract and analyze “fine print” (Terms & Conditions, policies, etc.) from any webpage or pasted text, flag hidden risks, and get actionable recommendations—in clean JSON.**

---

## 🔍 Overview

FinePrintFinder is a Streamlit-based MVP that helps users uncover the hidden “gotchas” buried in terms & conditions, subscription policies, and legal fine-print. Powered by:

- **CloudRift’s DeepSeek-V3** LLM (via OpenAI-compatible API)  
- **BeautifulSoup** HTML scraping for auto-extracting T&C sections  
- **Streamlit** UI for paste-or-scan workflows

It returns an **MCP-style JSON payload** containing:

```json
{
  "context":   "Brief summary of the fine print",
  "red_flags": ["…"], 
  "recommendations": ["…"]
}
```

---

## 🚀 Features

- **Manual Paste**: Paste any policy text into a textbox  
- **Auto-Extract**: Enter a URL → the scraper finds & follows “Terms of Use” links → extracts only that text  
- **LLM Analysis**: CloudRift’s DeepSeek-V3 identifies up to 3 red-flag clauses and 3 recommendations  
- **Robust JSON Parsing**: Auto-completes truncated JSON, falls back to raw display  
- **Downloadable Output**: One-click download of analysis as `.json`  

---

## 📐 Architecture

```
[ User ]  
   |  
   |--- Streamlit UI (app.py)  
         |                             ↳ .env reads CloudRift key  
    [ Paste OR Scan URL ]              ↳ stagehand_reader.py (requests + BS4)  
         |                                                ↳ Finds & follows T&C link  
         |  
         +--> get_fineprint_text(url) --------------------> Extracted text  
         |  
         +--> analyze_fine_print(text) -------------------> CloudRift LLM  
                                                ↳ deepseek-ai/DeepSeek-V3  
         |  
         +--> JSON cleanup, display & download  
```

---

## 🛠 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/fineprintfinder.git
cd fineprintfinder
```

### 2. Install dependencies

No virtualenv required—just install globally or with `--user`:

```bash
pip install streamlit openai python-dotenv requests beautifulsoup4
```

### 3. Configure your CloudRift key

Create a file named `.env` in the root:

```env
CLOUDRIFT_API_KEY=rift_your_actual_key_here
```

---

## ⚡ Usage

### 1. Run the app

```bash
streamlit run app.py
```

Your browser opens at `http://localhost:8501`.

### 2. Paste any fine-print

- **Paste**: Enter policy text in the “✍️ Paste Terms & Conditions” box  
- **Analyze**: Click “🔍 Analyze Fine Print”  

### 3. Auto-Extract from a URL

- **Scan**: Enter a T&C page URL (e.g. `https://temu.com`)  
- Click **“🔎 Scan Webpage for Fine Print”** to fetch & extract  
- Then click **“🔍 Analyze Fine Print”**  

### 4. View & Download

- **Raw Response**: See the unprocessed JSON from the model  
- **Parsed Result**: Structured red flags & recommendations  
- **Download**: Click “📥 Download JSON” to save results  

---

## 📂 File Structure

```
fineprint_reader/
├── app.py               # Streamlit frontend  
├── fineprint_agent.py   # CloudRift LLM integration  
├── stagehand_reader.py  # HTTP scraper (requests + BeautifulSoup)  
├── .env                 # Your CLOUDRIFT_API_KEY  
└── README.md            # This file  
```

---

## 🛠 Troubleshooting

- **No extraction?**  
  - Make sure the URL is correct and reachable  
  - Terms link selectors look for headers containing “term”, “condition”, “policy”, etc.

- **LLM errors or timeouts?**  
  - Verify `CLOUDRIFT_API_KEY` in `.env`  
  - Check network connectivity to `https://inference.cloudrift.ai/v1`

- **Malformed JSON?**  
  - The app auto-patches common truncations  
  - You can adjust `analyze_fine_print` prompt to shorten output  

---

## 🚀 Future Improvements

- **Browser Extension**: Click-to-analyze on any page without copying URLs  
- **Multi-lingual support**: Detect and translate non-English fine print  
- **PDF / DOCX input**: Upload contracts directly  
- **User accounts & history**: Save past analyses in a database  

---

## 🤝 Contributing

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/xyz`)  
3. Commit your changes (`git commit -m "Add xyz"`)  
4. Push to the branch (`git push origin feature/xyz`)  
5. Open a Pull Request  

Please adhere to existing code style and include tests for new features.

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

> **FinePrintFinder** — Because nobody reads the fine print… until now. 🚀  
