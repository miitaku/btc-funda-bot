import streamlit as st
from datetime import datetime
import pandas as pd

# デモ用の価格変化データ（API連携は未実装）
price_changes = {
    "15分前比": "+0.8%",
    "30分前比": "-0.2%",
    "1時間前比": "+1.1%",
    "1日前比": "-0.6%",
    "1週間前比": "+3.5%"
}

# Streamlitページ設定
st.set_page_config(page_title="BTCファンダBOT", layout="wide")

# タイトル
st.title("📊 BTCファンダメンタルBOT")

# 現在価格
st.header("💰 現在のBTC価格")
st.metric(label="USD", value="$68,500", delta="+1.2%")

# Fear & Greed Index 表示
st.header("🧠 Fear & Greed Index")
fg_index = 71
if fg_index >= 75:
    fg_label = "🔴 Greed／売り傾向"
elif fg_index >= 50:
    fg_label = "🟡 中立〜やや売り傾向"
else:
    fg_label = "🟢 Fear／買い傾向"
st.markdown(f"**現在の指数：{fg_index}（{fg_label}）**")

# BTC価格変化
with st.expander("🕒 BTC価格の変化を見る（15分〜1週間）"):
    cols = st.columns(len(price_changes))
    for i, (label, value) in enumerate(price_changes.items()):
        cols[i].metric(label, value)

# 関連ニュース（仮のデータ）
st.header("📰 関連ニュース・イベント")
news_data = [
    {"title": "ビットコインETF承認に前進", "impact": "high"},
    {"title": "マイニング難易度が過去最高に", "impact": "medium"},
    {"title": "SECが暗号資産規制に言及", "impact": "high"},
    {"title": "主要取引所が新機能リリース", "impact": "low"},
    {"title": "ビットコイン週次リポート発表", "impact": "medium"},
]
for item in news_data:
    icon = "🚨" if item["impact"] == "high" else "🔍" if item["impact"] == "medium" else "📄"
    st.markdown(f"- {icon} {item['title']}")

st.caption("※データはすべてデモ表示です。")
