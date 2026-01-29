import streamlit as st
import pandas as pd
import random
import re
from supabase import create_client, Client

# --------------------
# 1. Supabase接続設定 (注意1: Secretsを利用)
# --------------------
# StreamlitのSecretsから設定を読み込みます
try:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("SupabaseのURLまたはKeyが設定されていません。Secretsを確認してください。")
    st.stop()

# --------------------
# 2. ページ設定
# --------------------
st.set_page_config(page_title="英単語学習アプリ Pro", layout="centered")
st.title("英単語学習アプリ（Supabase連携版）")

# --------------------
# 3. 英単語リスト・データ準備 (変更なし)
# --------------------
base_words = [
    ("apple", "りんご"), ("book", "本"), ("cat", "猫"), ("dog", "犬"), ("study", "勉強する"),
    ("important", "重要な"), ("language", "言語"), ("school", "学校"), ("student", "学生"),
    ("teacher", "先生"), ("music", "音楽"), ("movie", "映画"), ("sports", "スポーツ"),
    ("friend", "友達"), ("family", "家族"), ("travel", "旅行する"), ("country", "国"),
    ("city", "都市"), ("food", "食べ物"), ("water", "水"), ("time", "時間"),
    ("money", "お金"), ("computer", "コンピュータ"), ("internet", "インターネット"),
    ("science", "科学"), ("history", "歴史"), ("future", "未来"), ("question", "質問"),
    ("answer", "答え"), ("problem", "問題")
]

words = []
for i in range(300):
    w, m = base_words[i % len(base_words)]
    words.append({"word": w, "meaning": m})

df = pd.DataFrame(words)
TOTAL = len(df)

# --------------------
# 4. データベース操作関数 (改良ポイント)
# --------------------
def save_score_to_supabase(score, progress):
    """学習結果をSupabaseに保存する"""
    data = {
        "score": score, 
        "progress": progress, 
        "user_name": "User1" # 必要に応じて変更
    }
    supabase.table("learning_logs").insert(data).execute()

def get_history_from_supabase():
    """過去の学習履歴を最新5件取得する"""
    response = supabase.table("learning_logs").select("*").order("created_at", desc=True).limit(5).execute()
    return response.data

# --------------------
# 5. セッション初期化
# --------------------
if "used" not in st.session_state:
    st.session_state.used = []
    st.session_state.score = 0
    st.session_state.current = random.randint(0, TOTAL - 1)

# --------------------
# 6. 全問終了時の処理
# --------------------
if len(st.session_state.used) == TOTAL:
    st.success("🎉 300問すべて終了しました！")
    st.write(f"最終スコア：{st.session_state.score} / {TOTAL}")
    
    # データを保存するボタン
    if st.button("学習結果をデータベースに保存"):
        save_score_to_supabase(st.session_state.score, len(st.session_state.used))
        st.toast("Supabaseに保存しました！")
    
    if st.button("最初からやり直す"):
        st.session_state.used = []
        st.session_state.score = 0
        st.rerun()
    st.stop()

# --------------------
# 7. 問題表示・解答ロジック
# --------------------
row = df.iloc[st.session_state.current]
st.write(f"### 問題 {len(st.session_state.used) + 1} / {TOTAL}")
st.write(f"## {row['word']}")

answer = st.text_input("日本語の意味を入力してください", key="ans_input")

def normalize(text):
    text = text.strip()
    text = re.sub(r"[○◎●「」『』\s]", "", text)
    return text

col1, col2 = st.columns(2)
with col1:
    if st.button("答え合わせ"):
        user = normalize(answer)
        correct = normalize(row["meaning"])
        if user == correct:
            st.success("正解！")
            st.session_state.score += 1
        else:
            st.error(f"不正解… 正解は「{row['meaning']}」です")

with col2:
    if st.button("次の単語"):
        st.session_state.used.append(st.session_state.current)
        remaining = list(set(range(TOTAL)) - set(st.session_state.used))
        if remaining:
            st.session_state.current = random.choice(remaining)
            st.rerun()

# --------------------
# 8. 履歴表示 (注意3: データの永続化を可視化)
# --------------------
st.write("---")
st.subheader("📊 過去の学習履歴 (Supabaseから取得)")

# 履歴データを取得して表示
history_data = get_history_from_supabase()
if history_data:
    # データを表形式で表示
    h_df = pd.DataFrame(history_data)
    # 列名の整理と時間のフォーマット調整
    h_df = h_df[['created_at', 'score', 'progress']]
    h_df.columns = ['学習日時', '正解数', '解答数']
    st.dataframe(h_df, use_container_width=True)
else:
    st.info("まだ保存された履歴はありません。")

st.write(f"現在のセッション正解数：{st.session_state.score}")
