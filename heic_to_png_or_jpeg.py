import streamlit as st
from PIL import Image
import pillow_heif
from io import BytesIO
import os
import zipfile

def convert_heic_to_image(heic_bytes, output_format, jpeg_quality=95):
    """HEICファイルを指定されたフォーマットに変換する関数"""
    try:
        # BytesIOオブジェクトを作成
        heic_buffer = BytesIO(heic_bytes)
        
        # HEICファイルを読み込む
        heif_file = pillow_heif.read_heif(heic_buffer)
        
        # PIL Imageに変換
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
        )
        
        # 指定されたフォーマットでBytesIOに保存
        output_buffer = BytesIO()
        
        if output_format == "JPEG":
            # JPEGの場合、品質設定を適用
            image = image.convert('RGB')  # JPEGはRGBAをサポートしないため
            image.save(output_buffer, format=output_format, quality=jpeg_quality)
        else:
            image.save(output_buffer, format=output_format)
            
        output_buffer.seek(0)
        return output_buffer
    
    except Exception as e:
        st.error(f"変換エラー: {str(e)}")
        return None

def create_zip_file(converted_files):
    """変換したファイルをZIPにまとめる関数"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for filename, file_content in converted_files.items():
            zip_file.writestr(filename, file_content.getvalue())
    
    zip_buffer.seek(0)
    return zip_buffer

def main():
    st.title("HEIC画像変換アプリ")
    st.write("HEICファイルをPNGまたはJPEG形式に一括変換します。")
    
    # サイドバーで変換設定
    with st.sidebar:
        st.header("変換設定")
        output_format = st.selectbox(
            "出力フォーマット",
            options=["PNG", "JPEG"],
            help="変換後の画像フォーマットを選択してください"
        )
        
        # JPEG選択時のみ品質設定を表示
        jpeg_quality = None
        if output_format == "JPEG":
            jpeg_quality = st.slider(
                "JPEG品質",
                min_value=1,
                max_value=100,
                value=95,
                help="JPEGの圧縮品質を設定します。高い値ほど品質が良くなりますがファイルサイズも大きくなります"
            )
    
    # 複数ファイルアップロード
    uploaded_files = st.file_uploader(
        "HEICファイルを選択してください（複数選択可）", 
        type=["heic", "HEIC"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.write(f"選択されたファイル数: {len(uploaded_files)}個")
        
        # 変換開始ボタン
        if st.button("変換開始"):
            converted_files = {}
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, uploaded_file in enumerate(uploaded_files):
                # 進捗状況の更新
                progress = (i + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                status_text.text(f"変換中... ({i + 1}/{len(uploaded_files)})")
                
                # オリジナルのファイル名を取得（拡張子を除く）
                original_filename = os.path.splitext(uploaded_file.name)[0]
                
                # ファイルを読み込んで変換
                file_bytes = uploaded_file.getvalue()
                converted_buffer = convert_heic_to_image(
                    file_bytes, 
                    output_format, 
                    jpeg_quality
                )
                
                if converted_buffer:
                    # 新しい拡張子でファイル名を設定
                    new_ext = ".jpg" if output_format == "JPEG" else ".png"
                    converted_files[f"{original_filename}{new_ext}"] = converted_buffer
            
            # 変換完了後の処理
            if converted_files:
                status_text.text("変換完了！")
                
                # ZIPファイルの作成
                zip_buffer = create_zip_file(converted_files)
                
                # ダウンロードボタンの表示
                st.download_button(
                    label=f"変換したファイルをZIPでダウンロード（{output_format}形式）",
                    data=zip_buffer,
                    file_name=f"converted_images_{output_format.lower()}.zip",
                    mime="application/zip"
                )
                
                # プレビューの表示（最大5枚まで）
                st.write("変換後のプレビュー（最大5枚）:")
                preview_files = list(converted_files.items())[:5]
                cols = st.columns(len(preview_files))
                
                for col, (filename, buffer) in zip(cols, preview_files):
                    with col:
                        st.image(buffer, caption=filename, use_column_width=True)
                
                if len(converted_files) > 5:
                    st.info(f"残り{len(converted_files) - 5}枚の画像はZIPファイル内でご確認ください。")
                
                # 変換情報の表示
                st.success(f"全{len(converted_files)}個のファイルを{output_format}形式に変換しました！")
                if output_format == "JPEG":
                    st.info(f"JPEG品質設定: {jpeg_quality}")
            else:
                st.error("変換に失敗したファイルがありました。")

if __name__ == "__main__":
    main()