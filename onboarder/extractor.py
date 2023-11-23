import os
import PyPDF2
from pptx import Presentation
from docx import Document

from .pdf import extract_text_from_pdf
from .ppt import extract_text_from_ppt
from .doc import extract_text_from_doc
from .text import extract_text_from_text


def extract_text(file_path, extract_funcs):
    # ファイルの拡張子を取得する
    _, ext = os.path.splitext(file_path)
    ext = ext.lstrip(".")  # 先頭の「.」を削除する

    # 拡張子に対応する抽出関数を取得する
    for func_name, exts in extract_funcs.items():
        if ext in exts:
            extract_func = globals()[func_name]  # 関数名から関数を取得する
            break
    else:
        # 抽出関数が見つからなかった場合は、空文字列を返す
        return ""

    # 抽出関数を呼び出して、テキストを抽出する
    return extract_func(file_path)
