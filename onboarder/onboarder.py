import os
import sys
import yaml
import tiktoken
import click
from fnmatch import fnmatch
from .extractor import extract_text


def get_ignored_files():
    """.gitignoreに記述されたファイルやディレクトリを取得する"""
    ignored_files = [".git/*", ".git", ".gitignore"]
    try:
        with open(".gitignore") as f:
            for line in f:
                # 空行やコメント行を除外する
                line = line.strip()
                if line == "" or line.startswith("#"):
                    continue
                # **/を使用して、任意のディレクトリ深さにマッチするように修正する
                ignored_files.append(line.replace("/", "*/*"))
    except OSError:
        # .gitignoreが存在しない場合は、何もしない
        pass
    return ignored_files


def tree(dir_path, level=0, ignored_files=[]):
    text = ""
    """dir_path以下のツリー構造を表示する"""
    # ファイルやディレクトリを一つずつ処理する
    for name in os.listdir(dir_path):
        # フルパスを取得する
        full_path = os.path.join(dir_path, name)

        # .gitignoreで除外されるファイルやディレクトリをスキップする
        if any(fnmatch(full_path.replace("./", ""), p) for p in ignored_files):
            continue

        # ファイルかどうかを判定する
        if os.path.isfile(full_path):
            text += "  " * level + "- " + name + "\n"
        else:
            text += "  " * level + "+ " + name + "\n"
            # 再帰的にツリー構造を表示する
            text += tree(full_path, level + 1, ignored_files)
    return text


def calculate_token_size(text):
    # TikTokのAPIやライブラリを使用して実際のトークンサイズを計算
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text, allowed_special="all"))


ext_map = {".py": "python", ".yaml": "yaml", ".yml": "yaml", ".sh": "bash", ".json": "json", ".txt": "text"}


@click.command()
@click.option('-c', '--config', default='config.yaml', help='設定ファイル')
@click.option('-d', '--dir', default='.', help='検索ディレクトリ')
@click.option('-o', '--output', default='output', help='出力ディレクトリ')
@click.option('-t', '--types', default='py,yaml,ipynb,sh,txt', help='ファイル拡張子')
def main(config, dir, output, types):
    extract_funcs = yaml.safe_load(open(config, "r"))
    current_dir = os.getcwd()
    os.chdir(dir)
    ignored_files = get_ignored_files()
    output_dir = output

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    md_text = "# Gitリポジトリの情報\n"
    md_text += "## ディレクトリ構造\n```\n"
    md_text += tree(dir, level=0, ignored_files=ignored_files)
    md_text += "```\n\n"

    file_count = 0
    token_size = 0
    max_token_size = 2000000

    types = [f'.{type}' for type in types.split(',')]
    print(types)

    for root, dirs, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file_path)
            if ext in [".md"]:
                continue

            if not ext in types:
                continue

            if any(fnmatch(file_path.replace("./", ""), p) for p in ignored_files):
                continue

            try:
                text = extract_text(file_path, extract_funcs)

                if len(text) > 0:
                    file_type = ext_map.get(ext, "text")
                    section_text = f"## ファイル名: {file_path}\n内容:\n```{file_type}\n{text}\n```\n\n"
                    section_token_size = calculate_token_size(section_text)

                    if token_size + section_token_size > max_token_size:
                        output_path = os.path.join(output_dir, f"project_files_{file_count}.md")
                        with open(output_path, "w") as f:
                            f.write(md_text)
                        md_text = ""
                        file_count += 1
                        token_size = 0

                    md_text += section_text
                    token_size += section_token_size
            except Exception as e:
                pass

    os.chdir(current_dir)
    output_path = os.path.join(output_dir, f"project_files_{file_count}.md")
    with open(output_path, "w") as f:
        f.write(md_text)


if __name__ == "__main__":
    main()
