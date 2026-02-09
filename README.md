#  Real Estate RAG Research Tool

Ask questions about real estate articles using AI. Get accurate answers with sources.

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## What Does This Do?

This tool lets you:
1. Add URLs to real estate news articles
2. Ask questions about the content
3. Get AI-generated answers with source links

**Example:**
- Add article about mortgage rates
- Ask: "What is the current 30-year mortgage rate?"
- Get instant answer with source citation

---

## Installation

1. **Clone the repo**
```bash
git clone https://github.com/jsuryanm/real-estate-rag.git
cd real-estate-rag
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Add your API key**

Create a `.env` file:
```
GROQ_API_KEY=your_api_key_here
```

Get a free API key from [Groq](https://console.groq.com)

---

## Usage

**Run the app:**
```bash
streamlit run main.py
```

**Then:**
1. Paste URLs in the sidebar (1-3 articles)
2. Click "Process URLs"
3. Ask your question
4. Get your answer!

---

## Example URLs to Try
```
https://www.cnbc.com/2024/12/21/how-the-federal-reserves-rate-policy-affects-mortgages.html
https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html
```

---

## How It Works
```
URLs → Scrape Content → Split into Chunks → Store in Database
                                                    ↓
Question → Find Relevant Chunks → Ask AI → Get Answer + Sources
```

---

## Tech Stack

- **LLM**: Groq (openai/gpt-oss-120b)
- **Framework**: LangChain
- **Database**: ChromaDB
- **UI**: Streamlit

---

## Common Issues

**"Access Denied" when loading URLs?**
- Some sites block bots. Try different URLs.

**"Vector database not initialized"?**
- Process URLs first before asking questions.

**Module not found errors?**
- Run `pip install -r requirements.txt`

---

## License

MIT License - see [LICENSE](LICENSE) file

---

## Contact

Made by [Surya](https://github.com/jsuryanm)

⭐ Star this repo if you find it useful!
