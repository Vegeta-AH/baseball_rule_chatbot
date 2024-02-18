# app.py
import streamlit as st
import requests

st.title("野球ルールAIチャットボット")

# 想定される質問の提示
st.sidebar.header("質問例:")
st.sidebar.markdown("""
- 投手板から本塁の距離は？
- 野球でピッチャーの役割を教えて？
- プロ野球では、金属製バットは使用できる？
- 試合中、ベンチに入れる人は？
- ２人の走者が同一のフェアボールに触れた場合に2人ともアウトになるのか？
""")

# Streamlit UIの構築
user_input = st.text_input("Enter a question:")
button = st.button("Get Answer")

# ボタンがクリックされたときの処理
if button:
    # FastAPIサーバーに質問を送信し、応答を取得 ローカル環境 http://localhost:8000/answer
    #response = requests.post("http://localhost:8000/answer", json={"text": user_input})
    response = requests.post("https://baseball-rule-chatbot.onrender.com/answer", json={"text": user_input})
    answer = response.json().get("answer", "No answer available.")
    docs = response.json().get("docs", [])

    #バーンを表示
    st.balloons()
    
    # 応答を表示
    st.subheader("回答:")
    st.write(f"Answer: {answer['result']}")

    # 関連文書を表示、もし存在する場合
    if docs:
        st.subheader("以下の関連文書を参考に回答しています：")
        for doc in docs:
            st.markdown(f"**文書{doc['doc_num']}**: {doc['content']}")
    else:
        st.write("関連する文書が見つかりませんでした。")