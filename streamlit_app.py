import streamlit as st
import pandas as pd
import random

# --------------------
# 初期設定
# --------------------
st.set_page_config(page_title="英単語学習アプリ", layout="centered")
st.title("英単語学習アプリ（300問）")

# 単語データ読み込み
df = pd.read_csv("words.csv")
TOTAL_QUESTIONS = len(df)

# --------------------
# セッション状態の初期化
# --------------------
if "used_indices" not in st.session_state:
    st.session_state.used_indices = []
    st.session_state.score = 0
    st.session_state.current_index = random.choice(range(TOTAL_QUESTIONS))
    st.session_state.show_answer = False

# --------------------
# 全問終了チェック
# --------------------
if len(st.session_state.used_indices) == TOTAL_QUESTIONS:
    st.success("🎉 300問すべて終了しました！")
    st.write(f"最終スコア：{st.session_state.score} / {TOTAL_QUESTIONS}")
    st.stop()

# --------------------
# 現在の問題
# --------------------
row = df.iloc[st.session_state.current_index]

st.write(f"### 問題 {len(st.session_state.used_indices) + 1} / {TOTAL_QUESTIONS}")
st.write(f"## {row['word']}")

answer = st.text_input("日本語で意味を入力してください")

# --------------------
# 答え合わせ
# --------------------
if st.button("答え合わせ"):
    st.session_state.show_answer = True
    if answer == row["meaning"]:
        st.success("正解！")
        st.session_state.score += 1
    else:
        st.error(f"不正解… 正解は「{row['meaning']}」です")

# --------------------
# 次の問題
# --------------------
if st.button("次の単語"):
    st.session_state.used_indices.append(st.session_state.current_index)

    remaining = list(set(range(TOTAL_QUESTIONS)) - set(st.session_state.used_indices))
    st.session_state.current_index = random.choice(remaining)

    st.session_state.show_answer = False
    st.experimental_rerun()

# --------------------
# スコア表示
# --------------------
st.write("---")
st.write(f"正解数：{st.session_state.score}")
st.write(f"進捗：{len(st.session_state.used_indices)} / {TOTAL_QUESTIONS}")

