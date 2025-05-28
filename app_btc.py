# -*- coding: utf-8 -*-
import streamlit as st
import requests
from datetime import datetime

# APIキー設定
CRYPTO_API_KEY = "3acb16112aa28f59897d2ac014e0560fd117c41a"
DEEPL_API_KEY = "52d6d0a8-eb79-4b60-86c1-9bee83cde1cf:fx"

# --- タイトル ---
st.title("🤖 BTCファンダBOT")
st.markdown("---")

# --- BTC価格取得 ---
def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,jpy"
    res = requests.get(url).json()
    usd = res["bitcoin"]["usd"]
    jpy = res["bitcoin"]["jpy"]
    return usd, jpy

usd, jpy = get_btc_price()
st.subheader("💰 BTC価格")
st.write(f"USD: ${usd:,}")
st.write(f"JPY: ¥{jpy:,}")

# --- Fear & Greed Index取得 ---
def get_fear_greed_index():
    url = "https://api.alternative.me/fng/"
    res = requests.get(url).json()
    index = res['data'][0]['value']
    state = res['data'][0]['value_classification']
    return index, state

index, state = get_fear_greed_index()
st.subheader("😱 Fear & Greed Index")
st.metric("現在の指数", index, state)

# --- CryptoPanicニュース取得 ---
def get_btc_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&currencies=BTC"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get("results", [])
    else:
        return []

# --- DeepL翻訳 ---
def translate_to_japanese(text):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": "JA"
    }
    res = requests.post(url, data=params)
    if res.status_code == 200:
        return res.json()["translations"][0]["text"]
    else:
        return text + "（翻訳失敗）"

# --- ニュース表示 ---
st.subheader("📰 BTC関連ニュース・イベント")
posts = get_btc_news()

if posts:
    for post in posts[:5]:  # 最新5件のみ
        dt = post['published_at'][:10]
        title_en = post['title']
        title_ja = translate_to_japanese(title_en)
        st.markdown(f"📅 {dt}")
        st.markdown(f"**{title_ja}**")
        st.markdown(f"[続きを読む]({post['url']})")
        st.write("---")
else:
    st.warning("ニュースが取得できませんでした。")
