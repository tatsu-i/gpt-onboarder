from docx import Document


def extract_text_from_doc(doc_path):
    # Wordの文書を開く
    try:
        doc = Document(doc_path)
        # パラグラフごとにテキストを抽出する
        text = ""
        for para in doc.paragraphs:
            text += para.text
        return text
    except FileNotFoundError:
        print("Wordファイルが見つかりませんでした")
    except ValueError:
        print("Wordファイルを読み込めませんでした")
    return ""
