"""日本語まじりテキストの整形ユーティリティ（ハンズオン用）。

各関数は入力を変更せず、新しい文字列を返す純関数として書く。
"""

# 制御文字 (タブ・改行 LF/CR を除く) を削除する str.translate 用テーブル
_CONTROL_TABLE = {c: None for c in range(0x00, 0x20) if c not in (0x09, 0x0A, 0x0D)}
_CONTROL_TABLE[0x7F] = None


def strip_control(text: str) -> str:
    """制御文字を取り除く。タブと改行 (LF / CR) は残す。"""
    return text.translate(_CONTROL_TABLE)


def normalize_spaces(text: str) -> str:
    """連続する空白（半角・全角・タブ）を半角スペース1つに畳み、行頭行末の空白を落とす。

    改行は保持する。行単位で処理するので、段落構造は壊れない。
    """
    lines = []
    for line in text.split("\n"):
        parts = line.replace("　", " ").replace("\t", " ").split()
        lines.append(" ".join(parts))
    return "\n".join(lines)
