# GPTs Onboarder

GPTs Onboarderは、Gitリポジトリの情報を抽出し、Markdown形式で出力するツールです。このツールは、リポジトリのディレクトリ構造を表示し、指定された種類のファイルからテキストを抽出します。
出力されたテキストファイルをGPTsのナレッジファイルに登録しコードに関するインストラクションを与えてください。

## インストール

このツールはPythonで書かれており、setup.pyを使用してインストールできます。
```bash
python setup.py install
```

## 使用方法

以下のコマンドを使用して、GPTs Onboarderを実行します。
```bash
onboarder -c extract_funcs.yml -d ./work -o ./docs/
```

ここで、`extract_funcs.yml`は抽出関数の設定ファイル、`./work`は検索ディレクトリ、`./docs`は出力ディレクトリを指定します。

## 抽出関数

抽出関数は、extract_funcs.ymlファイルで定義します。このファイルでは、各抽出関数がどのファイル拡張子に対応しているかを指定します。

```yaml
extract_text_from_pdf:
  - pdf
extract_text_from_ppt:
  - ppt
  - pptx
extract_text_from_doc:
  - doc
  - docx
extract_text_from_text:
  - py
  - txt
  - md
  - js
  - conf
  - yml
  - yaml
```

## .gitignore

.gitignoreファイルに記述されたファイルやディレクトリは無視されます。.gitignoreファイルが存在しない場合、デフォルトで.git/*, .git, .gitignoreが無視されます。

## 注意事項

- ファイルのサイズが大きい場合、抽出されたテキストはトークンサイズに制限されます。デフォルトの最大トークンサイズは2000000です。
- 抽出エラーが発生したファイルは無視されます。