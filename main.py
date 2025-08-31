import re
import streamlit as st
from langchain_helper import get_few_shot_db_chain

st.title("Retail Database: Q&A")

# Pressing Enter in this input triggers a rerun, so we can answer immediately.
question = st.text_input("Ask a question and press Enter:")

if question.strip():
    result_text = get_few_shot_db_chain(question)

    # Pull out SQL / Value / Answer if present in the returned text
    def grab(label, text):
        # capture everything after "<Label>:" up to the next label or end
        pattern = rf"{label}:\s*(.*?)(?=\s*(?:SQL|Value|Answer):|$)"
        m = re.search(pattern, text, re.S)
        return m.group(1).strip() if m else None

    sql = grab("SQL", result_text)
    value = grab("Value", result_text)
    answer = grab("Answer", result_text)

    if sql or value or answer:
        if sql:
            st.markdown("**SQL:**")
            st.code(sql, language="sql")
        if value:
            st.markdown("**Value:**")
            st.write(value)
        if answer:
            st.markdown("**Answer:**")
            st.write(answer)
    else:
        # Fallback to raw text if labels are not present
        st.write(result_text)
