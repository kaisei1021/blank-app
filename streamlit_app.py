import streamlit as st
import pandas as pd
import random

# --------------------
# ページ設定
# --------------------
st.set_page_config(page_title="英単語学習アプリ", layout="centered")
st.title("英単語学習アプリ（300問）")

# --------------------
# 300問分の単語データを生成
# --------------------
words = []
for i in range(1, 301):
    words.append({
        "word": f"EnglishWord{i}",
        "meaning": f"意味{i}"
    })

df = pd.DataFrame(words)
TOTAL = len(df)

# --------------------
# セッション状態の初期化
# --------------------
if "used" not in st.session_state:
    st.session_state.used = []
    st.session_state.score = 0
    st.session_state.current = random.randint(0, TOTAL - 1)
    st.session_state.checked = False

# --------------------
# 全問終了時
# --------------------
if len(st.session_state.used) == TOTAL:
    st.success("🎉 300問すべて終了しました！")
    st.write(f"最終スコア：{st.session_state.score} / {TOTAL}")
    st.stop()

# --------------------
# 問題表示
# --------------------
row = df.iloc[st.session_state.current]

st.write(f"### 問題 {len(st.session_state.used) + 1} / {TOTAL}")
st.write(f"## {row['word']}")

answer = st.text_input("日本語の意味を入力してください")

# --------------------
# 答え合わせ
# --------------------
if st.button("答え合わせ"):
    st.session_state.checked = True
    if answer == row["meaning"]:
        st.success("正解！")
        st.session_state.score += 1
    else:
        st.error(f"不正解… 正解は「{row['meaning']}」です")

# --------------------
# 次の問題
# --------------------
if st.button("次の単語"):
    st.session_state.used.append(st.session_state.current)

    remaining = list(set(range(TOTAL)) - set(st.session_state.used))
    st.session_state.current = random.choice(remaining)

    st.session_state.checked = False
    st.experimental_rerun()

# --------------------
# スコア表示
# --------------------
st.write("---")
st.write(f"正解数：{st.session_state.score}")
st.write(f"進捗：{len(st.session_state.used)} / {TOTAL}")


    
