# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    text: str

#import os
#key = 'key'
#os.environ['OPENAI_API_KEY'] = key

import os
import openai
# openai.api_keyにOpenAIのAPIキーを入れる
openai.api_key = os.environ['OPENAI_API_KEY']

#必要なライブラリをインポート
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import chromadb
from chromadb.config import Settings

persist_directory = 'persist_directory'
client = chromadb.PersistentClient(path=persist_directory)

embeddings= OpenAIEmbeddings()

# persistされたデータベースを使用するとき
db2 = Chroma(
    collection_name="langchain_store",
    embedding_function=embeddings,
    client=client,
)

# データベースからretriever作成
retriever = db2.as_retriever(search_kwargs={"k": 3}) # Topkもここの引数で指定できる

# OpenAI を使うためのインポート
from langchain.llms import OpenAI

# LLM ラッパーの初期化
llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0, max_tokens=500)

# 質問と回答の取得に使用するチェーンをインポート
from langchain.chains import RetrievalQA

# チェーンを作り、それを使って質問に答える
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

@app.post("/answer")
def get_answer(question: Question):
    # ここでモデルに質問を渡し、応答を取得するロジックを追加
    query = question.text
    answer = qa.run(query)
    return {"answer": answer}