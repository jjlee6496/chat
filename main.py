import streamlit as st
from io import StringIO

# 제목
st.title(':sunglasses: Test app for :blue[LLM]')
st.text('챗 pdf')

# 파일 업로드
uploaded_file = st.file_uploader('PDF 파일을 업로드해주세요', type=['pdf','png','jpg'])


# 질문 부분
prompt = st.chat_input("Say something")
st.chat_message('hi')