import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# --- APIキー（.streamlit/secrets.toml から取得） ---
CRYPTO_API_KEY = st.secrets["CRYPTO_API_KEY"]
DEEPL_API_KEY = st.secrets["DEEPL_API_KEY"]

# --- ヘッダー ---
st.set_page_config(page_title="BTCファンダBOT", layout="wide")
st.title("📊 BTCファンダメンタルBOT")
st.markdown("Bitcoinの価格、心理、ニュースを1ページでチェック！")

# --- レイアウトの列設定 ---
col1, col2, col3 = st.columns(3)

# --- BTC価格表示 ---
def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,jpy"
    response = requests.get(url)
    return response.json()

price = get_btc_price()
with col1:
    st.subheader("💰 BTC価格")
    st.metric(label="USD", value=f"${price['bitcoin']['usd']:,}")
    st.metric(label="JPY", value=f"¥{price['bitcoin']['jpy']:,}")

# --- Fear & Greed Index 表示 ---
def get_fear_and_greed_index():
    url = "https://api.alternative.me/fng/"
    response = requests.get(url).json()
    value = int(response["data"][0]["value"])
    if value <= 25:
        label = "🟢 恐怖（買い時）"
    elif value >= 75:
        label = "🔴 欲望（売り時）"
    else:
        label = "🟡 中立"
    return value, label

fng_value, fng_label = get_fear_and_greed_index()
with col2:
    st.subheader("🧠 市場心理")
    st.markdown(f"**現在の指数：{fng_value}（{fng_label}）**")

# --- BTC価格チャート（30日） ---
def get_btc_history():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30"
    response = requests.get(url).json()
    prices = response["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

btc_df = get_btc_history()
with col3:
    st.subheader("📈 30日間の価格推移")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=btc_df["date"], y=btc_df["price"], mode="lines", name="BTC Price"))
    fig.update_layout(height=250, margin=dict(l=0, r=0, t=30, b=0), xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)

# --- ニュース取得＋翻訳 ---
st.divider()
st.subheader("📰 BTCニュース（CryptoPanic）")

def get_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&currencies=BTC"
    response = requests.get(url).json()
    return response["results"][:5]

def translate_text(text):
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": "JA"
    }
    res = requests.post(url, data=data).json()
    return res["translations"][0]["text"]

news_items = get_crypto_news()

for item in news_items:
    title = item["title"]
    url = item["url"]
    highlight = "🔥 " if any(x in title.lower() for x in ["etf", "halving", "inflation", "approval", "interest", "regulation"]) else ""
    translated_title = translate_text(title)
    st.markdown(f"{highlight}**{translated_title}**  \n[→ 記事を見る]({url})")
