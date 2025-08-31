from langchain_google_genai import GoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
import os
from few_shots import FEW_SHOTS

from dotenv import load_dotenv
load_dotenv()

def get_few_shot_db_chain(question):

    llm = GoogleGenerativeAI(model="models/gemini-2.5-flash", google_api_key=os.environ["GOOGLE_API_KEY"])
    db_user="root"
    db_password="Yourpassword"
    db_host="localhost"
    db_name="atliq_tshirts"

    db=SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",sample_rows_in_table_info=3)

    FEW_SHOTS_FOR_SELECTOR = [
        {"input": ex["question"], "answer": ex["answer"]} for ex in FEW_SHOTS
    ]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
        model_kwargs={"device": "cpu"}
    )

    selector = SemanticSimilarityExampleSelector.from_examples(
        examples=FEW_SHOTS_FOR_SELECTOR,  # <-- now keyed by "input"
        embeddings=embeddings,
        vectorstore_cls=FAISS,
        k=1,
        input_keys=["input"],  # <-- chain will supply {input}; selector uses it
    )

    example_prompt = PromptTemplate(
        input_variables=["input", "answer"],  # <-- "input", not "question"
        template="Q: {input}\nSQL: {answer}"
    )

    dynamic_fewshot_prompt = FewShotPromptTemplate(
        example_selector=selector,
        example_prompt=example_prompt,
        # MUST include exactly what the SQL chain expects to inject:
        input_variables=["input", "table_info", "top_k"],  # ✅ required by create_sql_query_chain
        prefix=(
            "You are an expert SQL generator.\n"
            "Use the semantically selected example below as guidance for style and schema usage.\n\n"
            "Example:\n"
        ),
        suffix=(
            "\n\nGiven the database schema:\n{table_info}\n\n"
            "Write a syntactically correct {dialect} SQL query that answers the user's question.\n"
            "Return ONLY the SQL (no markdown/backticks/prose). If a LIMIT is sensible, use {top_k}.\n\n"
            "Question: {input}"
        ),
    )
    SQL_STARTS = ("SELECT", "WITH", "INSERT", "UPDATE", "DELETE")

    sql_chain = create_sql_query_chain(llm, db, prompt=dynamic_fewshot_prompt)

    sql = sql_chain.invoke({"question": question})


    if isinstance(sql, str) and sql.strip().upper().startswith("SQLQUERY:"):
        sql = sql.split(":", 1)[1].strip()

    if sql.strip().upper().startswith(SQL_STARTS):
        rows = db.run(sql)
        value = rows[0][0] if isinstance(rows, list) and rows and isinstance(rows[0], (tuple, list)) and len(
            rows[0]) == 1 else rows
        prompt = (
            f"Question: {question}\n"
            f"Raw result: {rows}\n\n"
            "Write a brief, friendly answer for a non-technical user. "
            "If relevant, include brand, size, and color."
        )
        answer = StrOutputParser().invoke(llm.invoke(prompt))
        return f"SQL: {sql}\nValue: {value}\nAnswer: {answer}"
    else:
        return (f"LLM did not return SQL. Got: {sql!r}")


if __name__=="__main__":

    print(get_few_shot_db_chain("How many t-shirts do we have left for Nike in extra small size and white color?"))
