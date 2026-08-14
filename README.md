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

リポジトリで配布する場合、参加者への案内はこの3行:

```bash
git clone https://github.com/kudouatushi/step3-handson.git
cp -R step3-handson/handson ~/handson-try
cd ~/handson-try   # 以降は README.md（手順書）の「準備」から
```

- **Claude Code を起動するのはコピーした `~/handson-try` だけ**。clone した
  リポジトリ側では起動しない（一度実行すると task-101 の答えが焼き込まれるため、
  原本は触らずコピーを使い捨てる。やり直しもコピーの作り直しで済む）
- ハンズオン中に参加者が対話する Claude Code は T3 の1つだけ。worker は
  バックグラウンドセッションとして都度起動・都度片付けされ、ターミナルを占有しない
- リポジトリは private のため、事前に参加者の招待（または公開への変更、zip 配布）が必要

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
- **worker が「This background session hasn't isolated its changes yet」で
  failed を返す**: 同梱の `.claude/settings.json`（bgIsolation 無効化）が
  配布物から欠落している。zip の展開範囲に隠しファイルが含まれているか確認する。
  なお、この設定は**稼働中の worker にも反映される**（再起動不要。実測 2026-08-14）
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

## ドライラン結果（2026-08-14）

Ex1〜Ex4 をコピー環境で通し確認済み（観測セッションが T3 役をヘッドレス代行）:

- Ex1: 即時返り → 約50秒で完了。分析係は仕込んだテスト空白（0x7F DEL 未テスト）を
  発見しファイル無変更で報告
- Ex3: 初回 ref 要求 → ref 再送で配達 → 返信受領（罠が教材どおり再現）
- Ex4: worker が仕様どおり実装（11 tests OK・未コミット・src と tests のみ変更）、
  done 通知も正しい形式で到着
- **未検証のまま残るもの**: 対話 T3 での体験（trust ダイアログ・done 通知の
  承認プロンプトの見え方）と Agent View の TUI 表示

## この教材の設計判断

- **zellij 等の多重化ツールを使わない**: 導入障壁をゼロにするため素の
  ターミナル3枚で構成
- **Python 標準ライブラリのみ**: 環境構築での脱落者を出さないため
- **worker はコミットしない**: 統合判断（diff と reports を見て commit）を
  人間の手に残すことで、Step3 の役割分担を体験の中心に置く
- **罠（ref 要求・success≠配達・trust 不可視）をあえて踏ませる**: 実運用で
  最初に混乱する3点を、安全な教材の中で先に経験させる
- **`.claude/settings.json`（bgIsolation 無効化）を同梱する**: bg セッションは
  既定で git 作業ツリーの直接編集を隔離ガードに止められる（実測 2026-08-14）。
  教材は「worker の diff を人間がそのまま検証する」体験を優先して無効化した。
  実運用では worktree 分離が基本形であることを手順書・スライド両方に明記している
- **配布物自身に `.gitignore` を同梱する**: 無いと参加者の `git add -A` が
  `__pycache__/*.pyc` を初期コミットに取り込む（ドライランで実際に混入した）
