import streamlit as st
import os
from datetime import datetime
from prompt_builder import analyze_theme
from image_generator import generate_images
from utils import save_images, load_gallery, get_today_count, add_today_count
import pyperclip
import torch

st.set_page_config(page_title="🎨 画像生成スタジオ", page_icon="🖼️", layout="wide")
st.markdown("<h1 style='text-align:center;'>🎨 市場調査連携 画像生成スタジオ</h1>", unsafe_allow_html=True)

col_input, col_gallery = st.columns([1.2, 1.8])

with col_input:
    st.markdown("### 📝 市場調査結果をペースト")
    user_text = st.text_area("市場調査レポート内容", height=200, placeholder="市場調査アプリの出力を貼り付けてください。")

    st.markdown("### ⚙️ 生成設定")
    num_images = st.slider("生成する画像枚数", 1, 5, 2)
    steps = st.slider("生成ステップ数（品質）", 10, 100, 30)
    width = st.number_input("幅 (px)", value=512, step=64)
    height = st.number_input("高さ (px)", value=512, step=64)

    if not torch.cuda.is_available():
        st.warning("⚠️ GPUが見つかりません。生成速度が遅くなります。")

    # --- 生成制限チェック ---
    today_count = get_today_count()
    remaining = 5 - today_count
    st.markdown(f"**本日残り生成可能枚数: {remaining} 枚**")

    if remaining <= 0:
        st.warning("⚠️ 本日の生成上限（5枚）に達しました。明日までお待ちください。")
    else:
        if st.button("🚀 画像を生成する", use_container_width=True):
            if not user_text.strip():
                st.warning("市場調査結果を入力してください。")
            elif num_images > remaining:
                st.warning(f"⚠️ 今日残り生成可能枚数は {remaining} 枚です。")
            else:
                try:
                    # --- プロンプト生成 ---
                    with st.spinner("🎨 プロンプトを生成中..."):
                        prompt = analyze_theme(user_text)
                        st.success("プロンプト生成完了！")
                    
                    with st.expander("🧠 生成されたプロンプト（英語）", expanded=False):
                        st.code(prompt, language="markdown")
                        if st.button("📋 プロンプトをコピー"):
                            pyperclip.copy(prompt)
                            st.toast("コピーしました！")

                    # --- 画像生成 ---
                    with st.spinner("🪄 画像生成中..."):
                        images = generate_images(prompt, num_images=num_images, steps=steps, width=width, height=height)
                        folder = os.path.join("generated_images", datetime.now().strftime("%Y%m%d_%H%M%S"))
                        paths = save_images(images, folder=folder)
                        add_today_count(len(images))
                        st.balloons()
                        st.success(f"🎉 {len(paths)}枚の画像を生成し保存しました！")

                except Exception as e:
                    st.error("❌ エラーが発生しました。Replicate APIが起動していない可能性があります。")
                    st.text(f"詳細: {e}")

with col_gallery:
    st.markdown("### 🖼️ ギャラリー")
    gallery = load_gallery()
    if gallery:
        cols = st.columns(3)
        for i, img_path in enumerate(gallery):
            timestamp = datetime.fromtimestamp(os.path.getmtime(img_path)).strftime("%m/%d %H:%M")
            with cols[i % 3]:
                st.image(img_path, caption=f"{timestamp}", use_container_width=True)
    else:
        st.info("まだ保存済み画像はありません。")
