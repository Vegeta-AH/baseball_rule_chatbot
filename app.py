# app.py
import streamlit as st
import requests

st.title("野球AIチャットボット")

# Streamlit UIの構築
user_input = st.text_input("Enter a question:")
button = st.button("Get Answer")

# ボタンがクリックされたときの処理
if button:
    # FastAPIサーバーに質問を送信し、応答を取得
    response = requests.post("http://localhost:8000/answer", json={"text": user_input})
    answer = response.json().get("answer", "No answer available.")
    
    # 応答を表示
    st.write(f"Answer: {answer}")