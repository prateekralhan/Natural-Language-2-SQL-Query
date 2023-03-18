import re
import os
import json
import openai
import pathlib
import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="SQL Query Generator",
    page_icon="✨",
    layout= "wide",
    initial_sidebar_state="expanded",
    menu_items={
    'Get Help': 'https://github.com/prateekralhan',
    'Report a bug': "mailto:ralhanprateek@gmail.com",
    'About': "## A minimalistic application to generate SQL queries using OpenAI APIs built with Python and Streamlit"
    } )

@st.cache_data()
def lottie_local(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

@st.cache_data()
def hide_footer():
    hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("Natural Language <2> SQL Query 🚀")
hide_footer()

col1, col2 = st.columns(2)
with col1:
    anim = lottie_local(r"./assets/animation.json")
    st_lottie(anim,
            speed=1,
            reverse=False,
            loop=True,
            height = 700,
            width = 700,
            quality="high",
            key=None)

with col2:
    st.markdown("-----------------------------")
    query = st.text_area("Please enter the desired question and see the magic 💫", height = 250)
    openai.api_key = os.environ["OpenAI_API_Key_v2"]
    prompt = f"Translate this natural language query into syntactically correct SQL:\n\n{query}\n\nSQL Query:"
    st.markdown("-----------------------------")
    ch = st.checkbox("Table Schema")
    if ch:
        schema = st.text_area("Enter Table Schema 📝")
        prompt = f"Translate this natural language query into syntactically correct SQL:\n\n{query}\n\nUse this table schema:\n\n{schema}\n\n{prompt}"
        st.markdown("-----------------------------")
    if st.button("Generate SQL Query ✨", use_container_width=True):
        with st.spinner("Working.. 💫"):
            try:
                completion = openai.Completion.create(
                            engine="text-davinci-003",
                            prompt=prompt,
                            max_tokens=2048,
                            n=1,
                            stop = "\\n",
                            temperature=0.5,
                            frequency_penalty = 0.5,
                            presence_penalty = 0.5,
                            logprobs = 10)

                response = completion.choices[0].text
                st.balloons()
                st.markdown("### Output:")
                st.success(f"{response}")
            except Exception as e:
                st.error(f"Error: {e}")
