import PyPDF2


def extract_text_from_pdf(pdf_path):
    # PDFを開く
    try:
        with open(pdf_path, "rb") as f:
            # PDFを読み込む
            pdf = PyPDF2.PdfFileReader(f)
            # PDFのページ数を取得する
            num_pages = pdf.getNumPages()
            # ページごとにテキストを抽出する
            text = ""
            for i in range(num_pages):
                page = pdf.getPage(i)
                text += page.extractText()
            return text
    except FileNotFoundError:
        print("PDFファイルが見つかりませんでした")
    except PyPDF2.PdfReadError:
        print("PDFファイルを読み込めませんでした")
    return ""
