#main.py

#windows
#import sqlite3
#Linux systemの場合はrequirements.txt に pysqlite3-binary を指定
import pysqlite3.dbapi2 as sqlite3

import sys
sys.modules['sqlite3'] = sqlite3

from fastapi import FastAPI
from pydantic import BaseModel
import openai

#必要なライブラリをインポート
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# OpenAI を使うためのインポート
from langchain_openai import ChatOpenAI

# 質問と回答の取得に使用するチェーンをインポート
from langchain.chains import RetrievalQA

# 本書の説明に合わせて少し変更しています
from langchain.prompts import PromptTemplate

app = FastAPI()
class Question(BaseModel):
    text: str

#import os
#key = 'key'
#os.environ['OPENAI_API_KEY'] = key

import os
# openai.api_keyにOpenAIのAPIキーを入れる
openai.api_key = os.environ['OPENAI_API_KEY']

embeddings= OpenAIEmbeddings()

# persistされたデータベースを使用するとき
db2 = Chroma(
    collection_name="langchain_store",
    embedding_function=embeddings,
    persist_directory = 'persist_directory',
)

# データベースからretriever作成
#retriever = db2.as_retriever(search_kwargs={"k": 3}) # Topkもここの引数で指定できる
retriever = db2.as_retriever(search_type="similarity_score_threshold",search_kwargs={"score_threshold": .8}) #類似度の閾値を設定する。

# LLM ラッパーの初期化
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, max_tokens=1000)

#promptを追加
prompt_template = """Use the following pieces of context to answer the question at the end.
If you don't get the answer, just say that you don't know.
Don't try to make up an answer. And Answer in Japanese.

 {context}

Question: {question}:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# チェーンを作り、それを使って質問に答える
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,chain_type_kwargs={"prompt": PROMPT},
        # 参考にした文書もレスポンスに含める
        return_source_documents=True,
        verbose=True
        )

@app.post("/answer")
def get_answer(question: Question):
    # ここでモデルに質問を渡し、応答を取得するロジックを追加
    query = question.text
    answer = qa.invoke(query)
    docs = retriever.get_relevant_documents(query)
    # docsの内容を整形してレスポンスに含める
    formatted_docs = [{"doc_num": num + 1, "content": doc.page_content} for num, doc in enumerate(docs)]

    return {"answer": answer, "docs": formatted_docs}
    #return {"docs": formatted_docs}