# 🎓 英単語学習アプリ Pro (Supabase連携版)

**StreamlitとSupabaseを組み合わせた、データの消えない本格的な英単語学習アプリケーションです。** 300問の英単語を4択クイズ形式で学び、ブックマーク機能を使って苦手な単語をクラウド上に保存、効率的に復習することができます。


## 🔗 URL

このURLで試すことができます（スリープ状態のときは青色の起動ボタンを押してください）：  
https://blank-app-e44ycfxrbgq.streamlit.app/


## 🌟 主な機能

* **4択クイズモード** 300問の英単語データからランダムに出題。直感的なインターフェースでスピーディに学習を進められます。
* **ブックマーク（🌟マーク）機能** 覚えにくい単語や間違えた単語をボタン一つで「お気に入り」として保存。データはクラウドDBへ永続的に記録されます。
* **ブックマーク復習モード** 保存した単語だけを抽出して集中的に解き直すことができ、苦手克服に特化した学習が可能です。
* **学習履歴の永続化** これまでの正解数や解答進捗を保存し、アプリを再起動しても過去の記録をいつでも確認できます。


## 🛠 セットアップ方法

### 1. 依存ライブラリのインストール

```bash
pip install streamlit pandas supabase
```
### 2. Supabaseの設定（重要）

Supabaseでプロジェクトを作成します。

SQL Editor で以下のテーブルを作成し、RLSをDisableに設定してください。

learning_logs (学習履歴用)

bookmarks (ブックマーク保存用)

Streamlit Cloudの Secrets に、SUPABASE_URL と SUPABASE_KEY を登録してください。

### 3. アプリの起動
```bash

streamlit run streamlit_app.py
```

### 📊 データの仕組み

本アプリは、通常のSQLite3等の簡易データベースではなく、外部クラウドデータベースの Supabase (PostgreSQL) を利用しています。

learning_logs: ユーザーのスコアや学習進捗を保存。

bookmarks: ブックマークした単語のIDを管理。

英単語データ: 内部のDataFrameで300問の単語を動的に管理。


### 💻 使用技術

* **Frontend/UI**: [Streamlit](https://streamlit.io/)
* **Database/Backend**: [Supabase](https://supabase.com/) (PostgreSQL)
* **Data Handling**: [Pandas](https://pandas.pydata.org/)


### 💡 今回の改良ポイント（課題への対応）

クラウドDB連携: アプリがスリープしてもデータが消えないようにSupabaseへ書き換えを実施。

セキュリティ対応: APIキーなどの機密情報を st.secrets で安全に管理。

UI/UXの刷新: 記述式から4択選択式へ変更し、学習のハードルを下げ、ブックマーク機能による復習効率を向上させました。
