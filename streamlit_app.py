import streamlit as st
import pandas as pd
import random
import re

# --------------------
# ページ設定
# --------------------
st.set_page_config(page_title="英単語学習アプリ", layout="centered")
st.title("英単語学習アプリ（300問）")

# --------------------
# 英単語リスト（30語）
# --------------------
base_words = [
    ("apple", "りんご"),
    ("book", "本"),
    ("cat", "猫"),
    ("dog", "犬"),
    ("study", "勉強する"),
    ("important", "重要な"),
    ("language", "言語"),
    ("school", "学校"),
    ("student", "学生"),
    ("teacher", "先生"),
    ("music", "音楽"),
    ("movie", "映画"),
    ("sports", "スポーツ"),
    ("friend", "友達"),
    ("family", "家族"),
    ("travel", "旅行する"),
    ("country", "国"),
    ("city", "都市"),
    ("food", "食べ物"),
    ("water", "水"),
    ("time", "時間"),
    ("money", "お金"),
    ("computer", "コンピュータ"),
    ("internet", "インターネット"),
    ("science", "科学"),
    ("history", "歴史"),
    ("future", "未来"),
    ("question", "質問"),
    ("answer", "答え"),
    ("problem", "問題")
]

# --------------------
# 300問に拡張
# --------------------
words = []
for i in range(300):
    w, m = base_words[i % len(base_words)]
    words.append({"word": w, "meaning": m})

df = pd.DataFrame(words)
TOTAL = len(df)

# --------------------
# セッション初期化
# --------------------
if "used" not in st.session_state:
    st.session_state.used = []
    st.session_state.score = 0
    st.session_state.current = random.randint(0, TOTAL - 1)

# --------------------
# 全問終了
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
# 正規化関数（入力ゆれ対策）
# --------------------
def normalize(text):
    text = text.strip()
    text = re.sub(r"[○◎●「」『』\s]", "", text)
    return text

# --------------------
# 答え合わせ
# --------------------
if st.button("答え合わせ"):
    user = normalize(answer)
    correct = normalize(row["meaning"])

    if user == correct:
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
    st.rerun()

# --------------------
# スコア表示
# --------------------
st.write("---")
st.write(f"正解数：{st.session_state.score}")
st.write(f"進捗：{len(st.session_state.used)} / {TOTAL}")
