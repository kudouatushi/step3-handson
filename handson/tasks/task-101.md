# task-101: ゼロ幅文字を取り除く strip_zero_width を追加する

## 目的
ゼロ幅文字（コピペや Web 由来のテキストに混入し、目視できないのに文字列比較を
壊す）を取り除く純関数を `textutil` に追加する。

## 対象
- 作業ディレクトリ: このファイルがある `handson/` プロジェクト（worker の cwd）
- ブランチ: 切らない。main の作業ツリーをそのまま編集する

## 触ってよい範囲
- `src/textutil.py`
- `tests/test_textutil.py`
- `reports/task-101/` 配下

## 触ってはいけない範囲
- `tasks/` / `CLAUDE.md` / `README.md`
- 既存の関数（`strip_control` / `normalize_spaces`）の**挙動**
  — 既存テストが1つでも落ちたら仕様違反

## 実装する仕様

`src/textutil.py` に追加する:

```python
def strip_zero_width(text: str) -> str:
```

- 取り除く文字は次の4つだけ:
  - U+200B ZERO WIDTH SPACE (ZWSP)
  - U+200C ZERO WIDTH NON-JOINER (ZWNJ)
  - U+200D ZERO WIDTH JOINER (ZWJ)
  - U+FEFF ZERO WIDTH NO-BREAK SPACE / BOM
- 純関数。入力を破壊的に変更せず、新しい文字列を返す
- docstring は日本語
- U+FEFF は先頭の BOM に限らず、文字列中のどこにあっても取り除く
- U+200D の除去は絵文字 ZWJ シーケンス（例: 家族絵文字）を構成要素に分解する。
  これは**意図した挙動**。docstring に明記し、テストで固定する

## テストの要件

`tests/test_textutil.py` に `TestStripZeroWidth` クラスを追加する。

- Arrange-Act-Assert。1テスト1振る舞い。テスト名は日本語
- **ゼロ幅文字は `chr(0x200B)` のようにコードポイントで組み立てる。**
  目視できない文字をソースに直接貼ると、エディタでの打ち直し・貼り付けで
  静かに壊れるため
- 最低限含める振る舞い:
  1. ZWSP が取り除かれる
  2. BOM が文字列の先頭・途中のどちらにあっても取り除かれる
  3. 対象外の文字（日本語・空白・改行）は残る
  4. 該当文字を含まない入力では入力と等しい文字列が返る

## 完了条件（機械判定できる形）
1. `python3 -m unittest discover -s tests` が**全件成功**する（既存5件 + 新規）
2. `src/textutil.py` に `strip_zero_width` が存在する
3. `tests/test_textutil.py` に `TestStripZeroWidth` が存在する

## 成果物
worker は cwd 配下に書く:
- `reports/task-101/result.md` — 何をしたか。主張には根拠へのポインタ
  （ファイルパス・checks.txt）を付ける
- `reports/task-101/checks.txt` — 次のコマンドの**生の実行出力**:
  ```bash
  mkdir -p reports/task-101
  python3 -m unittest discover -s tests -v > reports/task-101/checks.txt 2>&1
  ```

## 完了通知
- 全チェック完了後、SendMessage で `manager` 宛に
  `done task-101: <result.md の絶対パス>` を送る（失敗時は `failed task-101: <理由>`）
- 名前だけの初回送信は ref を要求されることがある。エラー文中の
  `manager [ref]` 形式をそのままコピーして再送する
- SendMessage の success は配達証明ではない。**正はファイル**。通知が届かなくても
  result.md と checks.txt が書けていれば成果は成立する

## コミット
**しない。** git への取り込み（統合判断）は人間が `git diff` と reports を
確認したうえで行う。これが Step3 の役割分担の練習になっている。
