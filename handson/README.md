# Step3 入門ハンズオン — 手順書

Claude Code の3つの公式機能を、手を動かして体感します。

| 機能 | 一言でいうと |
|---|---|
| Background Session (`claude --bg`) | **手を離す** — タスクを裏で走らせる |
| Agent View (`claude agents`) | **見張る** — 複数セッションを1画面で監視 |
| Cross Session Messaging (ListAgents / SendMessage) | **声をかける** — セッション同士が連絡し合う |

所要時間: 約45分（Ex1〜Ex4）

## 準備（5分）

ターミナルを3枚開き、すべてこのフォルダに `cd` します。役割を決めておきます:

- **T1: human** — 起動・確認コマンドを打つ手作業用
- **T2: Agent View** — 監視画面を出しっぱなしにする
- **T3: manager** — 対話の Claude Code（後半で管制塔役になる）

```bash
# 各ターミナルで（バージョンが 2.1.224 以降であることを確認）
cd <このフォルダ>
claude --version
```

**最初に T3 で対話セッションを起動してください**（このフォルダを初めて開くと
trust 確認が出ます。ここで承認しておかないと、後の bg セッションが
ダイアログ待ちで止まります — これも Step3 の重要な性質です）:

```bash
# T3
claude --name manager
```

trust 確認に応答したら、T3 はそのまま置いておきます。

## Ex1: Background Session — 手を離す（10分）

T1 からバックグラウンドセッションを起動します:

```bash
# T1
claude --bg --name "ex1-analyst" "src/textutil.py と tests/test_textutil.py を読んで、テストされていない振る舞いを1つ挙げ、理由を3行で報告して。ファイルは書き換えないこと。"
```

**確認ポイント**:
- コマンドが**すぐ返ってくる**（session id が表示される）。仕事は裏で進んでいる
- 出力を見る: `claude logs <session id>`
- 何度か `logs` を叩いて、進行中 → 完了と変わるのを見る

終わったら片付けます（**stop だけでなく rm まで**が片付け）:

```bash
# T1
claude stop <session id>
claude rm <session id>
```

## Ex2: Agent View — 見張る（5分）

T2 で監視画面を起動し、出しっぱなしにします:

```bash
# T2
claude agents
```

T1 からもう一度 Ex1 と同じ bg セッションを起動し、**T2 の画面に現れて
状態が変わっていく**のを観察してください。

**確認ポイント**:
- 自分が起動した覚えのないセッションも見える（マシン全体のセッション一覧）
- 状態表示（busy / idle など）は目安。**完了の判定には使わない**（後述）
- 確認できたら T1 から stop + rm で片付け

## Ex3: Cross Session Messaging — 声をかける（10分）

T1 から「応答係」の bg セッションを起動します。**`--settings` に注目** —
受信許可（`crossSessionInbound`）と送信権限は起動時に渡します:

```bash
# T1
claude --bg --name "ex3-echo" --settings '{"crossSessionInbound":"accept","permissions":{"allow":["SendMessage","ListAgents"]}}' "あなたは応答テスト係。メッセージが届いたら、送り主宛に SendMessage で『受信しました: <本文の要約>』を返す。それ以外は何もしない。"
```

T3 の manager（対話セッション）に、日本語でこう指示します:

> ListAgents で ex3-echo を探して、SendMessage で「こんにちは、聞こえますか」と送ってください。返信が来たら本文を見せてください。

**確認ポイント（ここが本日の山場です）**:
1. **初回送信は ref を要求されることがある** — エラーに見えるが正常。
   エラー文中の `ex3-echo [ref]` をそのまま使って再送すれば届く
2. **success:true は「送信を受け付けた」であって「届いた」ではない** —
   配達の確認は、返信が来たか（受信側の挙動）で取る
3. T2 の Agent View で、メッセージを受けた ex3-echo が動き出すのが見える

終わったら T1 から stop + rm で片付け。

## Ex4: ミニ manager–worker — Step3 を体験する（20分）

いよいよ役割分担です。**あなた＝人間（目標と統合判断）、T3＝manager（管制塔）、
bg セッション＝worker（実装）** という Step3 の最小構成を回します。

### 4-1. git 初期化（裏取りの基準を作る）

```bash
# T1
git init -b main
git add -A
git commit -m "chore: ハンズオン初期状態"
```

> **同梱の `.claude/settings.json` について**: bg セッションが git リポジトリの
> 作業ツリーを直接編集しようとすると、既定では「まず worktree に隔離せよ」という
> ガードに止められます。本ハンズオンは「worker の diff を人間がそのまま検証する」
> 体験のため、同梱の設定（`"worktree": {"bgIsolation": "none"}`）でこれを
> 無効化しています。**実運用では worktree 分離を使うのが基本形**です。

### 4-2. worker を起動

```bash
# T1
claude --bg --name "w:task-101" --settings '{"crossSessionInbound":"accept","permissions":{"allow":["SendMessage","ListAgents","Write","Edit","Bash"]}}' "待機。タスクは manager から SendMessage で届く。届くまで自発的に作業を始めないこと。届いたら本文中のタスク仕様ファイルを読み、その指示だけに従う。"
```

### 4-3. manager からタスクを投入

T3 の manager にこう指示します:

> tasks/task-101.md の絶対パスを調べて、ListAgents で w:task-101 の出現を確認してから、SendMessage でそのパスと「完了したら manager 宛に done task-101 を送って」という指示を渡してください。

T2 の Agent View で worker が動き出すのを眺めてください（2〜5分かかります）。

### 4-4. 完了通知とファイルでの裏取り

manager に done 通知が届いたら（T3 に表示されます）、**通知を鵜呑みにせず**
ファイルで裏を取ります。T3 の manager にこう指示します:

> reports/task-101/result.md と checks.txt を読み、git diff と突き合わせて、
> タスク仕様の完了条件を満たしているか検証して報告してください。

自分の目でも確認します:

```bash
# T1
git diff --stat
python3 -m unittest discover -s tests -v
cat reports/task-101/result.md
```

### 4-5. 統合判断（人間の仕事）

納得できたら、**自分の手で**コミットします。worker はコミットしません —
取り込みの判断と実行は人間の領分、というのが Step3 の役割分担です:

```bash
# T1
git add src tests
git commit -m "feat: strip_zero_width を追加（worker 実装・人間が検証して取り込み）"
```

最後に片付け:

```bash
# T1
claude stop <w:task-101 の session id>
claude rm <同 id>
```

## 持ち帰ってほしい3原則

1. **正はファイル、メッセージは起床合図** — 完了判定は reports と diff で。
   通知や画面表示を判定材料にしない
2. **権限は起動時に渡す** — bg セッションのダイアログは誰も押せない。
   `--settings` の許可リストが worker の行動範囲を決める
3. **manager は実装せず、worker は統合しない** — 役割の分離が、
   速度（並列化）と安全（検証の独立性）の両方を生む
