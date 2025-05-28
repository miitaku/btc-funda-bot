import streamlit as st
import requests

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

# --- Fear & Greed Index取得 ---
def get_fear_and_greed_index():
    url = "https://api.alternative.me/fng/"
    res = requests.get(url).json()
    index = int(res["data"][0]["value"])
    return index

# --- CryptoPanic ニュース取得 ---
def get_btc_news(api_key):
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={api_key}&currencies=BTC"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get("results", [])
    else:
        return []

# --- DeepL翻訳 ---
def translate_text(text, api_key):
    url = "https://api-free.deepl.com/v2/translate"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "auth_key": api_key,
        "text": text,
        "target_lang": "JA"
    }
    res = requests.post(url, headers=headers, data=data)
    if res.status_code == 200:
        return res.json()["translations"][0]["text"]
    else:
        return text

# --- 表示エリア ---
usd, jpy = get_btc_price()
st.subheader("💰 BTC価格")
st.write(f"USD: ${usd:,}")
st.write(f"JPY: ¥{jpy:,}")

fg_index = get_fear_and_greed_index()
st.subheader("🧠 Fear & Greed Index")
st.write(f"現在の指数：**{fg_index}**")

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

# --- ニュース表示 ---
st.subheader("📰 BTC関連ニュース・イベント")

api_key_crypto = st.secrets["CRYPTO_API_KEY"]
api_key_deepl = st.secrets["DEEPL_API_KEY"]

posts = get_btc_news(api_key_crypto)

if posts:
    for post in posts[:5]:  # 最新5件
        date = post['published_at'][:10]
        title = post['title']
        url = post['url']
        jp_title = translate_text(title, api_key_deepl)
        st.markdown(f"📅 {date}")
        st.markdown(f"**{jp_title}**")
        st.markdown(f"[続きを読む]({url})")
        st.write("---")
else:
    st.warning("ニュースが取得できませんでした。")
