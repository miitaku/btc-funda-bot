import streamlit as st
import requests
import os

st.set_page_config(page_title="BTCファンダBOT", layout="centered")

# --- BTC価格取得 ---
def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,jpy"
    res = requests.get(url)
    data = res.json()["bitcoin"]
    return data["usd"], data["jpy"]

# --- Fear & Greed Index取得 ---
def get_fear_and_greed_index():
    url = "https://api.alternative.me/fng/"
    res = requests.get(url)
    return int(res.json()["data"][0]["value"])

# --- CryptoPanicニュース取得 ---
def get_btc_news():
    API_KEY = os.environ.get("CRYPTO_API_KEY")
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={API_KEY}&currencies=BTC"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get("results", [])
    else:
        return []

# --- 表示開始 ---
st.title("🤖 BTCファンダBOT")
st.divider()

# --- BTC価格 ---
usd, jpy = get_btc_price()
st.subheader("📊 BTC価格")
st.write(f"USD: **${usd:,}**")
st.write(f"JPY: **¥{jpy:,}**")
st.divider()

# --- Fear & Greed Index ---
fg_index = get_fear_and_greed_index()
st.subheader("📊 Fear & Greed Index")
st.write(f"現在の指数：**{fg_index}**")

if fg_index <= 25:
    signal = "🟢 **Fear（買い傾向）**"
    comment = "市場は恐怖状態。**買い場の可能性**あり。"
elif fg_index >= 75:
    signal = "🔴 **Greed（売り傾向）**"
    comment = "市場は過熱気味。**利益確定の検討**を。"
else:
    signal = "🟡 **Neutral（中立）**"
    comment = "市場は安定中。明確な買い/売り傾向はなし。"

st.markdown(signal)
st.info(comment)
st.divider()

# --- ニュース表示 ---
st.subheader("📊 BTC関連ニュース・イベント")
posts = get_btc_news()

if posts:
    for post in posts[:5]:
        st.markdown(f"📅 {post['published_at'][:10]}")
        st.markdown(f"**{post['title']}**")
        st.markdown(f"[続きを読む]({post['url']})")
        st.write("---")
else:
    st.warning("📰 ニュースが取得できませんでした。")
