import streamlit as st
import requests
import os

# --- APIキー読み込み ---
CRYPTO_API_KEY = st.secrets["CRYPTO_API_KEY"]
DEEPL_API_KEY = st.secrets["DEEPL_API_KEY"]

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

# --- ニュース取得 (CryptoPanic) ---
def get_btc_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&currencies=BTC"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get("results", [])
    return []

# --- DeepL翻訳 ---
def translate_text(text):
    url = "https://api-free.deepl.com/v2/translate"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": "JA"
    }
    res = requests.post(url, headers=headers, data=data)
    if res.status_code == 200:
        return res.json()["translations"][0]["text"]
    return text

# ========================
#         表示開始
# ========================

st.markdown("# 📊 **BTCファンダレーダー**")
st.markdown("---")

# --- BTC価格表示 ---
st.subheader("💰 BTC価格")
usd, jpy = get_btc_price()
st.metric(label="USD", value=f"${usd:,}")
st.metric(label="JPY", value=f"¥{jpy:,}")
st.markdown("---")

# --- Fear & Greed Index表示 ---
st.subheader("🧠 Fear & Greed Index")
fg_index = get_fear_and_greed_index()
st.write(f"現在の指数：**{fg_index}**")

# 診断
if fg_index <= 25:
    signal = "🟢 **Fear（買い傾向）**"
    comment = "市場は恐怖状態。買い場の可能性あり。"
elif fg_index >= 75:
    signal = "🔴 **Greed（売り傾向）**"
    comment = "市場は過熱気味。利確の検討タイミング。"
else:
    signal = "🟡 **Neutral（中立）**"
    comment = "市場は安定中。明確な買い/売り傾向はなし。"

st.markdown(signal)
st.info(comment)
st.markdown("---")

# --- ニュース表示 ---
st.subheader("📰 BTC関連ニュース・イベント")

posts = get_btc_news()
if posts:
    for post in posts[:5]:  # 最新5件表示
        published = post.get("published_at", "")[:10]
        title_en = post.get("title", "")
        title_ja = translate_text(title_en)
        url = post.get("url", "#")

        st.write(f"📅 {published}")
        st.write(f"**{title_ja}**")
        st.markdown(f"[続きを読む]({url})")
        st.markdown("---")
else:
    st.warning("ニュースが取得できませんでした。")
