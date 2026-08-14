# CLAUDE.md — step3 ハンズオンプロジェクト

Step3 入門ハンズオンの練習用プロジェクト。日本語まじりテキストの整形ユーティリティ。

## 言語

返答・コメント・docstring は日本語。コード識別子は英語。

## 前提

- Python 3.9+ / 標準ライブラリのみ（追加インストールなし）
- テストは `python3 -m unittest discover -s tests`
- テストは Arrange-Act-Assert で書く。1テスト1振る舞い
- `src/textutil.py` の関数は純関数。入力を破壊的に変更しない

## 変更禁止

- `tasks/` 配下（タスク仕様。読むのは自由）
- `reports/` 配下は `reports/<task-id>/` のみ書いてよい
