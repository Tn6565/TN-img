from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("TNSYSTEM1")
client = OpenAI(api_key=api_key)

def analyze_theme(text):
    prompt = f"""
以下は市場調査の分析結果です。
この内容をもとに、Stable Diffusion向けの画像生成プロンプトを作成してください。
出力は英語で、カンマ区切りのキーワード形式で返してください。
---
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたはプロのアートディレクター兼プロンプトエンジニアです。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()
