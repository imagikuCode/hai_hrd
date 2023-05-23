import streamlit as st
import pandas as pd
from loguru import logger

from base_pdf_v1 import KnowledgeBase

st.set_page_config(page_title="HAI HRD", page_icon="")
st.title("HAI HRD")

st.markdown(
    """
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
""",
    unsafe_allow_html=True,
)
st.markdown("#### Human AI HRD")
st.markdown("## Ask")

query = st.text_input("Apa yang mau kamu tanya?")
source = "1Cmat7LIISE4E6gsqtm6Ywa4-nLo6dazG"


@st.cache_resource
def get_knowledge_base(source):
    return KnowledgeBase(
        source=source,
    )

@st.cache_resource
def get_answer(source,query):
    kb = get_knowledge_base(source)
    return kb.ask(query)

#query = st.text_input("Question", value="")

if query:
    with st.spinner("Mengumpulkan jawaban...."):
        print("Source: ", source) # <-- Add this line
        result = get_answer(source,query)

    st.markdown("### Answer")
    st.markdown(result["answer"])
    st.markdown("### Sources")
    st.markdown("\n ".join([f"- {x}" for x in result["sources"].split("\n")]))
logger.info("Proses query selesai")