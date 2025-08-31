# 🧠 Retail Database: AI-Powered SQL Q&A  

This project is an **AI-driven SQL Assistant** that allows users to query a retail database using **natural language**.  
Powered by **LangChain + Google Gemini + HuggingFace Embeddings + MySQL**, it translates plain English into **SQL queries**, executes them, and returns **friendly human-readable answers**.  

---

## 🚀 Features  
- 🗨️ **Natural Language → SQL** query generation  
- 🔎 **Few-Shot Semantic Example Selection** (FAISS + HuggingFace embeddings)  
- ⚡ **Google Gemini 2.5 Flash LLM** for fast reasoning  
- 🗄️ **MySQL Integration** via LangChain `SQLDatabase`  
- 🤖 **Friendly Explanations** of raw DB results  

---

## 📸 Screenshots  

### ✅ Example: Successful SQL Generation  
User asks: *"How many small size Levi t-shirts?"*  
The system generates SQL, executes it, and gives a clean answer.  

![Retail DB Query Example](./assets/633a0b9c-33b6-4c45-98c3-61be7f41f11a.png)  

---

### ❌ Example: Failed SQL Generation  
If the schema doesn’t support the question, the LLM gracefully declines.  

![Retail DB Failure Example](./assets/74d1cd8f-1c13-452a-bd20-e1533eef87c5.png)  

---

## 🏗️ Tech Stack  

- **[LangChain](https://www.langchain.com/)** – LLM orchestration  
- **[Google Gemini 2.5 Flash](https://ai.google/)** – Natural language → SQL generation  
- **[MySQL](https://www.mysql.com/)** – Retail database backend  
- **[HuggingFace Embeddings](https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L3-v2)** – Semantic similarity for few-shot selection  
- **[FAISS](https://github.com/facebookresearch/faiss)** – Vector search for example retrieval  
- **Python 3.12**  

---

## ⚙️ Installation  

```bash
# Clone repo
git clone https://github.com/yourusername/retail-sql-assistant.git



# Install requirements
pip install -r requirements.txt

#Run:
streamlit run main.py
