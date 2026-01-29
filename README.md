🎓 英単語学習アプリ Pro (Supabase連携版)

StreamlitとSupabaseを組み合わせた、データの消えない本格的な英単語学習アプリケーションです。300問の英単語を4択クイズ形式で学び、ブックマーク機能を使って苦手な単語を効率的に復習できます。
URL

このURLで試すことができます（スリープ状態のときは青色の起動ボタンを押してください）：

https://blank-app-e44ycfxrbgq.streamlit.app/
🌟 主な機能

    4択クイズモード: 300問の英単語からランダムに出題。直感的な選択肢形式でスピーディに学習できます。

    ブックマーク機能: 覚えにくい単語をボタン一つで保存。データはクラウド（Supabase）に永続保存されます。

    集中復習モード: ブックマークした単語だけを抽出して、繰り返しクイズに挑戦できます。

    学習履歴の記録: 過去の正解数や進捗がデータベースに保存され、アプリを閉じても履歴を確認可能です。

🛠 セットアップ方法
1. 依存ライブラリのインストール
Bash

pip install streamlit pandas supabase

2. Supabaseの設定

    Supabaseでプロジェクトを作成し、learning_logs と bookmarks テーブルを作成します。

    .streamlit/secrets.toml に以下の情報を設定してください。

Ini, TOML

SUPABASE_URL = "あなたのプロジェクトURL"
SUPABASE_KEY = "あなたのanonキー"

3. アプリの起動
Bash

streamlit run streamlit_app.py

📊 データの仕組み

このアプリは Supabase (PostgreSQL) を使用して、アプリが休止状態になってもデータが消えないように設計されています。

    learning_logs: 学習ごとの正解数、進捗数、日時を保存。

    bookmarks: ブックマークした単語のIDを保存し、復習モードで使用。

💻 使用技術

    Frontend/UI: Streamlit

    Backend/DB: Supabase (PostgreSQL)

    Data Handling: Pandas

💡 今回の改良ポイント（課題への対応）

    データの永続化: SQLite3等の簡易DBではなく、クラウドDBのSupabaseを採用することで、サーバー休止時もデータが保持されるようにしました。

    セキュリティ: Streamlitの secrets 機能を活用し、DBの認証情報を安全に管理しています。

    UXの向上: 記述式から選択式へ変更し、学習のハードルを下げるとともに、後から見返せる復習機能を実装しました。
