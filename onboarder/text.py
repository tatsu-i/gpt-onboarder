def extract_text_from_text(file_path):
    """テキストファイルからテキストを抽出する"""
    with open(file_path, "r") as f:
        return f.read()
