# HEIC Image Converter

HEICファイルをPNGまたはJPEG形式に一括変換できるStreamlitアプリケーションです。


## 機能

- 複数のHEICファイルを一括変換
- PNG/JPEG形式を選択可能
- JPEG変換時の品質設定
- プログレスバーによる進捗表示
- 変換後画像のプレビュー表示
- 変換済みファイルのZIPダウンロード

## インストール方法

1. リポジトリのクローン
```bash
git clone https://github.com/yourusername/heic-converter.git
cd heic-converter
```

2. 仮想環境の作成（推奨）
```bash
python -m venv venv
```

3. 仮想環境の有効化
- Windows:
```bash
.\venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```

4. 必要なパッケージのインストール
```bash
pip install -r requirements.txt
```

## 使用方法

1. アプリケーションの起動
```bash
streamlit run app.py
```

2. ブラウザが自動で開き、アプリケーションにアクセスできます（通常はhttp://localhost:8501）

3. 使用手順
   - サイドバーで出力フォーマット（PNGまたはJPEG）を選択
   - JPEGを選択した場合は、品質設定（1-100）を調整
   - 「ファイルを選択」ボタンをクリックしてHEICファイルを選択（複数選択可能）
   - 「変換開始」ボタンをクリック
   - 変換完了後、ZIPファイルでダウンロード可能

## 必要要件

- Python 3.7以上
- 必要なPythonパッケージ:
  - streamlit
  - pillow
  - pillow-heif

requirements.txtの内容:
```
streamlit
pillow
pillow-heif
```

## 対応環境

- Windows 10/11
- macOS 10.15以降
- Linux (Ubuntu 20.04以降)

## 注意事項

- 大量のファイルを一度に変換する場合、メモリ使用量に注意してください
- HEIC形式はAppleデバイスで撮影された写真の標準フォーマットです
- 変換時間はファイルサイズと数、およびマシンのスペックに依存します

## トラブルシューティング

### よくある問題と解決方法

1. インストールエラー
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

2. HEICファイルが認識されない場合
- ファイル拡張子が正しいか確認してください（.heicまたは.HEIC）
- ファイルが破損していないか確認してください

3. メモリエラーが発生する場合
- 一度に変換するファイル数を減らしてください
- システムのメモリ使用状況を確認してください

