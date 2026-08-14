# step3-handson — Step3 入門教材（進行者向け）

Claude Code の公式3機能（Background Session / Agent View / Cross Session
Messaging）を、45分のハンズオンで体感してもらう教材一式。

## 構成

```
step3-handson/
├── README.md            # このファイル（進行者向け）
├── slides/
│   └── step3-intro.md   # Marp スライド（16枚）
└── handson/             # 参加者に配布するプロジェクト
    ├── README.md        # 参加者向け手順書（コピペ可能なコマンド付き）
    ├── CLAUDE.md        # プロジェクト規約（worker が読む）
    ├── src/textutil.py  # 題材: テキスト整形ユーティリティ（関数2つ）
    ├── tests/test_textutil.py  # 既存テスト5件
    └── tasks/task-101.md       # Ex4 で worker に渡すタスク仕様
```

## 想定時間

| パート | 時間 |
|---|---|
| 講義（スライド） | 20分 |
| ハンズオン Ex1〜Ex4 | 45分 |
| 質疑・バッファ | 10分 |
| **合計** | **75分（確保する枠は90分推奨）** |

スライドのみの発表なら 20〜25分。

バッファを推奨する理由: 初回 trust 承認・messaging の ref 再送・worker の
実装時間（2〜5分）など、**教材の狙いどおりの「つまずき」で個人差が出る**ため。

## 参加者の前提

- Claude Code を日常利用しているエンジニア
- **Claude Code 2.1.224 以降**（cross-session messaging の要件。
  `claude --version` で確認させる）
- macOS / Linux、`python3` が使えること（追加インストール不要。
  テストは標準ライブラリの unittest のみ）
- 1人1台。ハンズオンは各自のマシン内で完結する
  （messaging は同一マシンの Unix ソケット経由）

## 配布方法

`handson/` フォルダを zip か リポジトリで配布する。
**`.git` は含めない**（Ex4 の冒頭で参加者自身に `git init` させる手順になっており、
これが裏取りで使う `git diff` の基準づくりを兼ねている）。

## スライドの表示

```bash
# VS Code: Marp for VS Code 拡張でプレビュー / エクスポート
# CLI:
npx @marp-team/marp-cli slides/step3-intro.md -o slides/step3-intro.html
npx @marp-team/marp-cli slides/step3-intro.md -o slides/step3-intro.pdf
```

## 進行のポイント・トラブルシュート

- **最初に T3（対話セッション）で trust を承認させる**。手順書にも書いてあるが、
  飛ばした参加者の bg セッションは trust ダイアログ待ちで止まり、
  ListAgents にも出ない（「いない」ように見える）。その場合は
  そのフォルダで対話 `claude` を一度起動して承認させれば復旧する
- **Ex3 の ref 要求エラーは「教材の仕様」**。エラーが出たら成功、と先に言って
  おくと会場が落ち着く。2回目以降は名前だけで通ることまで確認させる
- **Ex4 の worker が動かない**: ほぼ `--settings` のコピペミス（シングルクォート
  の欠落で JSON が壊れる）。手順書のコマンドをそのまま貼り直させる
- **worker の実装が終わらない**: 2〜5分は正常。Agent View で busy なら待つ。
  10分以上 idle のままなら `claude logs <id>` で状況を見る
- **片付け忘れ**: 各 Ex の最後に stop + rm を必ず実行させる。残った bg
  セッションは次の Ex の ListAgents を汚す
- **worker の done 通知が T3 に「承認プロンプト」として出ることがある**
  （T3 は受信許可を明示していないため）。承認すれば届く。これも
  「success≠配達」の実例として使える
- **Ex1 の `claude logs` の表示品質はドライランで要確認**。非 TTY で
  キャプチャするとスピナーの再描画しか見えないことがある。実ターミナルで
  読みにくい場合は Agent View からの確認・attach に誘導する
- 参加者マシンに他の Claude Code セッションがあると Agent View や ListAgents に
  混ざって見える。「マシン全体が見えるのも学び」として扱う

## この教材の設計判断

- **zellij 等の多重化ツールを使わない**: 導入障壁をゼロにするため素の
  ターミナル3枚で構成
- **Python 標準ライブラリのみ**: 環境構築での脱落者を出さないため
- **worker はコミットしない**: 統合判断（diff と reports を見て commit）を
  人間の手に残すことで、Step3 の役割分担を体験の中心に置く
- **罠（ref 要求・success≠配達・trust 不可視）をあえて踏ませる**: 実運用で
  最初に混乱する3点を、安全な教材の中で先に経験させる
