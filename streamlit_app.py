import streamlit as st
import pandas as pd
import random
import re
from supabase import create_client, Client

# --- Supabase接続 ---
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- データ準備 ---
base_words = [("apple", "りんご"), ("book", "本"), ("cat", "猫"), ("dog", "犬"), ("study", "勉強する"),
              ("important", "重要な"), ("language", "言語"), ("school", "学校"), ("student", "学生"),
              ("teacher", "先生"), ("music", "音楽"), ("movie", "映画"), ("sports", "スポーツ"),
              ("friend", "友達"), ("family", "家族"), ("travel", "旅行する"), ("country", "国"),
              ("city", "都市"), ("food", "食べ物"), ("water", "水"), ("time", "時間"),
              ("money", "お金"), ("computer", "コンピュータ"), ("internet", "インターネット"),
              ("science", "科学"), ("history", "歴史"), ("future", "未来"), ("question", "質問"),
              ("answer", "答え"), ("problem", "問題")]

words = []
for i in range(300):
    w, m = base_words[i % len(base_words)]
    words.append({"id": i, "word": w, "meaning": m})
df = pd.DataFrame(words)

# --- セッション初期化 ---
if "mode" not in st.session_state:
    st.session_state.mode = "normal"  # "normal" or "bookmark_review"
if "used" not in st.session_state:
    st.session_state.used = []
    st.session_state.score = 0
    st.session_state.current_idx = random.randint(0, len(df) - 1)
    st.session_state.options = []

# --- データベース関数 ---
def add_bookmark(word_id):
    supabase.table("bookmarks").insert({"word_id": word_id}).execute()

def get_bookmarks():
    res = supabase.table("bookmarks").select("word_id").execute()
    return [item["word_id"] for item in res.data]

def clear_bookmarks():
    supabase.table("bookmarks").delete().neq("id", -1).execute()

# --- 選択肢の生成 ---
def generate_options(correct_meaning):
    options = [correct_meaning]
    others = [m for w, m in base_words if m != correct_meaning]
    options.extend(random.sample(list(set(others)), 3))
    random.shuffle(options)
    return options

# --- メインUI ---
st.title("英単語学習 Pro (選択式+復習機能)")

# サイドバーでモード切り替え
st.sidebar.title("メニュー")
if st.sidebar.button("通常モード開始"):
    st.session_state.mode = "normal"
    st.session_state.used = []
    st.rerun()

bookmarked_ids = get_bookmarks()
if st.sidebar.button(f"ブックマーク復習 ({len(bookmarked_ids)}件)"):
    if len(bookmarked_ids) > 0:
        st.session_state.mode = "bookmark_review"
        st.session_state.used = []
        st.session_state.current_idx = random.choice(bookmarked_ids)
        st.rerun()
    else:
        st.sidebar.warning("ブックマークがありません")

if st.sidebar.button("ブックマークを全削除"):
    clear_bookmarks()
    st.rerun()

# --- 問題ロジック ---
current_word = df.iloc[st.session_state.current_idx]

# 選択肢が未生成なら生成
if not st.session_state.options:
    st.session_state.options = generate_options(current_word["meaning"])

st.subheader(f"【{ '復習' if st.session_state.mode == 'bookmark_review' else '通常' }モード】")
st.write(f"## {current_word['word']}")

# 選択肢ボタン
for opt in st.session_state.options:
    if st.button(opt, use_container_width=True):
        if opt == current_word["meaning"]:
            st.success("正解！")
            st.session_state.score += 1
        else:
            st.error(f"不正解... 正解は「{current_word['meaning']}」でした")

# アクションボタン
col1, col2 = st.columns(2)
with col1:
    if st.button("🌟 ブックマークに追加"):
        add_bookmark(int(st.session_state.current_idx))
        st.toast("ブックマークに保存しました")

with col2:
    if st.button("次の問題へ ➔"):
        st.session_state.used.append(st.session_state.current_idx)
        
        # 次の問題の選定
        if st.session_state.mode == "normal":
            remaining = list(set(range(len(df))) - set(st.session_state.used))
        else:
            remaining = list(set(bookmarked_ids) - set(st.session_state.used))
            
        if remaining:
            st.session_state.current_idx = random.choice(remaining)
            st.session_state.options = [] # 選択肢をリセット
            st.rerun()
        else:
            st.balloons()
            st.success("全ての問を終了しました！")

st.divider()
st.write(f"現在のスコア: {st.session_state.score}")
