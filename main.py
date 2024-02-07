#main.py

#windows
#import sqlite3
#Linux systemの場合はrequirements.txt に pysqlite3-binary を指定
import pysqlite3.dbapi2 as sqlite3

import sys
sys.modules['sqlite3'] = sqlite3

from fastapi import FastAPI
from pydantic import BaseModel

import os
import openai

#必要なライブラリをインポート
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb
from chromadb.config import Settings

# OpenAI を使うためのインポート
from langchain_openai import ChatOpenAI

# 質問と回答の取得に使用するチェーンをインポート
from langchain.chains import RetrievalQA

app = FastAPI()
class Question(BaseModel):
    text: str

#import os
#key = 'key'
#os.environ['OPENAI_API_KEY'] = key


# openai.api_keyにOpenAIのAPIキーを入れる
openai.api_key = os.environ['OPENAI_API_KEY']

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

# LLM ラッパーの初期化
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, max_tokens=500)

# チェーンを作り、それを使って質問に答える
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

@app.post("/answer")
def get_answer(question: Question):
    # ここでモデルに質問を渡し、応答を取得するロジックを追加
    query = question.text
    answer = qa.run(query)
    return {"answer": answer}