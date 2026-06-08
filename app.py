import streamlit as st
import pandas as pd
import os

# ページの設定
st.set_page_config(page_title="地域区分＆日射A区分 検索ツール", layout="centered")

st.title("Webプログラム専用：地域区分＆日射A区分 検索ツール")
st.write("Webプログラムの入力に必要な「地域区分」と「日射地域A区分」を検索できます。")

csv_filepath = 'Area2026.csv'

# CSVファイルの存在確認
if not os.path.exists(csv_filepath):
    st.error(f"エラー: '{csv_filepath}' が見つかりません。プログラムと同じフォルダに配置してください。")
else:
    # データの読み込み（キャッシュ化して高速化）
    @st.cache_data
    def load_data():
        # cp932で読み込み
        df = pd.read_csv(csv_filepath, encoding='cp932')
        # 必要に応じて列名を調整してください（CSVの列順に合わせてインデックスで指定）
        # 列数安全対策
        if df.shape[1] >= 5:
            df = df.iloc[:, [0, 2, 3, 4]]
            df.columns = ['都道府県名', '市区町村名', '地域区分', '日射地域A区分']
        return df

    try:
        df = load_data()

        # 検索入力
        keyword = st.text_input("検索する地域（都道府県または市区町村）を入力してください:").strip()

        if keyword:
            # 都道府県名または市区町村名にキーワードが含まれる行を抽出
            results = df[df['都道府県名'].str.contains(keyword, na=False) | 
                         df['市区町村名'].str.contains(keyword, na=False)]

            if results.empty:
                st.warning(f"「{keyword}」に一致する地域は見つかりませんでした。")
            else:
                st.success(f"検索結果: '{keyword}' （{len(results)}件ヒット）")
                
                # テーブル表示
                st.dataframe(results, use_container_width=True, hide_index=True)
                
                st.info("💡 上記の数値をそのままWebプログラムの基本情報に入力してください。")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
