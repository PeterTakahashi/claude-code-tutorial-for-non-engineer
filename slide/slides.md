---
marp: true
theme: default
paginate: true
size: 16:9
title: はじめてのClaude Code 〜手を動かして“動くもの”を作る4時間〜
author: Seiya
---

<style>
:root{
  --ink:#1F2933; --paper:#FAF9F6; --accent:#D97757; --accent2:#2A9D8F;
  --muted:#6B7280; --line:#E7E3DC; --soft:#F0EDE7;
}
section{
  background:var(--paper); color:var(--ink);
  font-family:-apple-system,"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic",sans-serif;
  font-size:26px; padding:54px 64px; line-height:1.55;
}
h1{ font-size:46px; border-bottom:4px solid var(--accent); padding-bottom:.18em; letter-spacing:.01em;}
h2{ font-size:33px; }
h3{ font-size:27px; color:var(--accent2); margin:.2em 0;}
strong{ color:var(--accent); }
a{ color:var(--accent2); }
code{ background:var(--soft); padding:.08em .35em; border-radius:6px; font-size:.88em;}
pre{ background:var(--ink); color:#F6F8FA; padding:.85em 1.1em; border-radius:12px; font-size:20px;}
pre code{ background:transparent; color:inherit;}
ul,ol{ margin-top:.2em;} li{ margin:.22em 0;}
blockquote{ border-left:5px solid var(--accent2); margin:0; padding:.25em 1em;
  background:#EFF6F4; border-radius:0 10px 10px 0;}
.eyebrow{ font-size:19px; letter-spacing:.18em; color:var(--accent); font-weight:800;}
.term{ display:inline-block; background:#fff; border:2px solid var(--accent); color:var(--accent);
  border-radius:999px; padding:.02em .7em; font-weight:800; font-size:.8em; margin-right:.2em;}
.gloss{ color:var(--muted);}
.small{ font-size:.78em; color:var(--muted);}
.do{ background:#EAF6F3; border-left:6px solid var(--accent2); padding:.5em .9em; border-radius:0 12px 12px 0;}
.warn{ background:#FBEEE8; border-left:6px solid var(--accent); padding:.5em .9em; border-radius:0 12px 12px 0;}
.cols{ display:flex; gap:24px;}
.col{ flex:1; background:#fff; border:1px solid var(--line); border-radius:14px; padding:.7em .9em;}
.diagram{ display:flex; gap:10px; align-items:stretch; margin-top:.4em;}
.box{ flex:1; background:#fff; border:2px solid var(--line); border-radius:14px; padding:.6em .4em; text-align:center; font-size:.82em;}
.box b{ display:block; color:var(--accent); font-size:1.0em; margin-bottom:.15em;}
.arrow{ display:flex; align-items:center; color:var(--muted); font-size:26px;}
.split{ display:flex; gap:30px; align-items:center;}
.split>.t{ flex:1; min-width:0;}
.split>img{ flex:none; width:300px; border-radius:18px; box-shadow:0 8px 24px rgba(31,41,51,.13); background:#fff;}
.split.sm>img{ width:240px;}
.split.lg>img{ width:340px;}
section.title{ background:linear-gradient(135deg,#1F2933,#2b3a47); color:var(--paper); justify-content:center;}
section.title h1{ color:#fff; border:none; font-size:58px;}
section.title h2{ color:#E9C3B4; font-weight:500;}
section.section{ background:var(--ink); color:var(--paper); justify-content:center;}
section.section h1{ color:#fff; border:none; font-size:52px;}
section.section .eyebrow{ color:var(--accent);}
section::after{ color:var(--muted); font-size:15px;}
</style>

<!-- _class: title -->
<!-- _paginate: false -->

<span class="eyebrow">CLAUDE CODE 勉強会 / 4時間</span>

# はじめてのClaude Code

## 手を動かして“動くもの”を作る4時間

by Seiya

<!-- 最初の10分：自己紹介＋今日の流れ。気楽に、専門知識ゼロ前提で話す。 -->

---

## 自己紹介（テンプレ・自由に書き換え）

- 名前 / ふだんやっていること
- なぜこの会を開いたのか（ひとことで）
- 今日のスタンス：**「全部わからなくてOK。動けば勝ち」**

<div class="do">

今日は“エンジニアになる会”ではありません。**AIに頼んで、自分のアイデアを動く形にする**会です。

</div>

---

## 今日のゴール

<div class="do" style="font-size:1.05em">

**自分のパソコンで動く「お店の予約サイト」を作って、<br>ngrokで“友達に送れるURL”にするところまで。**

</div>

- むずかしいサーバー契約・公開設定はしません
- 途中で迷っても大丈夫。あとで見返せる記事も用意しています
- 遅れて来た人も、記事の途中から合流できます

---

## 今日の流れ（4時間）

| 時間 | 内容 |
|---|---|
| 0:00–0:10 | 自己紹介・今日の流れ・**完成形デモ** |
| 0:10–0:45 | みんなで準備（アプリ・ログイン・**Docker**・ngrok） |
| 0:45–1:05 | 最低限の地図（言葉と仕組み） |
| 1:05–1:15 | 休憩 |
| 1:15–2:00 | ハンズオン①：AIにブラウザで調べ物→表に |
| 2:00–3:35 | ハンズオン②：予約サイトを作って公開 |
| 3:35–4:00 | まとめ・自分のアイデアを試す・質問 |

---

## まず完成形を見てもらいます（デモ）

<div class="do">

これから30秒。**「予約サイトが動いて、URLを友達に送れる」**ところまでを先に見せます。

</div>

- ゴールが見えていると、途中の作業が迷子になりません
- 「あれを自分で作るのか」という感覚を持って始めましょう

<!-- ここでSeiyaが実際にローカル起動→ngrok→スマホで開く、までライブ。 -->

---

## 準備でいれるもの（始める前に）

- **Claude Desktop アプリ**<span class="gloss">今日の作業場（Codeタブを使う）</span>
- **Docker**<span class="gloss">アプリを“箱ごと”動かす道具（あとで予約システムで使用）</span>
- **ngrok**<span class="gloss">あとでURLを公開する道具（authtokenは準備済み）</span>

<div class="do">

ここでみんなで一緒にインストール＆ログイン。**詰まっても大丈夫、声をかけてください。**

</div>

<div class="small">

※ Windowsの人は **Git** も。git を使うためではなく、**Claude Code がコマンドを動かす土台**として必要（Macは標準装備）。

</div>

---

## Docker（ドッカー）とは

<div class="split sm">
<div class="t">

<span class="term">Docker</span><span class="gloss">アプリを“箱（コンテナ）”ごと、そのまま動かす仕組み</span>

- ふつう、ソフトは使う前に**面倒なインストール**が必要
- Dockerなら、**必要なものが箱に入った状態**で来る → 動かすだけ
- PC（Mac / Windows）の違いで「自分だけ動かない」が起きにくい

</div>
<img src="img/docker.png" alt="アプリを箱（コンテナ）ごと動かすDockerのイラスト">
</div>

<div class="do">

今日は、予約システムの **データベース（PostgreSQL）** や **Go** を動かすのに使います。<br>
<span class="small">（Node.js / npm は Claude が各自のPCに入れてくれるので、そちらはDocker不要）</span>

</div>

<div class="warn small">

注意：Docker Desktopは**アプリを開いて動かしたまま**にしておく必要があります（閉じると中の箱も止まる）。

</div>

---

<!-- _class: section -->
<!-- _paginate: false -->

<span class="eyebrow">PART 1</span>

# 最低限の地図
### 〜言葉は“使う直前に1個ずつ”〜

---

## そもそもClaude Codeって何？

<div class="split lg">
<div class="t">

<span class="term">LLM</span><span class="gloss">ネットの文章を大量に読んだ“物知りな助手”</span>

<span class="term">Claude</span><span class="gloss">その助手のひとり（Anthropic社製）</span>

<span class="term">Claude Code</span><span class="gloss">その助手に“手”を付けたもの</span>

> ふつうのAIは「答えを言う」だけ。**Claude Codeは、あなたのPCを実際に操作して、ファイルを作ったり動かしたりできる。**

</div>
<img src="img/llm.png" alt="たくさんの本に囲まれた物知りな助手のイラスト">
</div>

---

## なぜ今、こんなに急に広まった？

- **言葉で頼める**：呪文のようなコードを覚えなくていい
- **自分で手を動かす**：提案だけでなく、実際に作って・試して・直す
- **失敗を自分で直す**：エラーが出たら自分で原因を探して修正
- **道具につながる**：あとで出てくる<span class="term">MCP</span>で世界中のサービスと接続

<div class="do">

要するに「**作れる人の条件**」が、“コードが書ける”から“**やりたいことを言葉にできる**”に変わった。

</div>

---

## Webサービスを“レストラン”でイメージ

<div class="diagram">
  <div class="box"><b>客席・メニュー</b>フロントエンド<br><span class="small">見える画面</span></div>
  <div class="arrow">→</div>
  <div class="box"><b>ウェイター</b>API<br><span class="small">注文を運ぶ窓口</span></div>
  <div class="arrow">→</div>
  <div class="box"><b>厨房</b>バックエンド<br><span class="small">実際の調理＝処理</span></div>
  <div class="arrow">→</div>
  <div class="box"><b>食材庫</b>データベース<br><span class="small">データの保管</span></div>
</div>

<div class="split sm">
<div class="t">

- <span class="term">サーバー</span><span class="gloss">この“お店”そのもの（動かす場所）</span>
- <span class="term">クラウドサーバー</span><span class="gloss">店を買わずに借りる</span>

</div>
<img src="img/restaurant.png" alt="客席・ウェイター・厨房・食材庫を並べたレストランの断面イラスト">
</div>

---

## 今日の“サーバー”は怖くない

<div class="do">

今日の「サーバー」は、**あなたのPCの中で一時的に動くだけ**。<br>
クラウド契約も難しい設定もナシ。Claude Codeが起動してくれます。

</div>

- <span class="term">ngrok</span><span class="gloss">そのPCに“公開の住所”を一本だけ通す道具</span>
- だから**友達がスマホからアクセスできる**
- <span class="term">インターネット</span>＝そのお店に世界中からアクセスできる道

---

## Claude Codeが得意なこと

- 小さなWebアプリ・ツール・自動化を**ゼロから形にする**
- 既にあるものの**修正・改善・説明**
- **調べ物**や**面倒な手作業**の自動化（後でやります）
- 「とりあえず動く試作（モック）」を**速く**作る

<div class="warn">

苦手：あいまいな丸投げ、正確さが命の計算の検算なし運用、最新すぎる情報。<br>
→ **具体的に頼む・結果を自分で確認する**のが大事。

</div>

---

<!-- _class: section -->
<!-- _paginate: false -->

<span class="eyebrow">PART 2</span>

# Claude Codeの基本機能
### 画面・remote-control・MCP・Skills

---

## 画面の使い方（Claude Desktop）

- **Code**タブを開く → **Local** → 作業フォルダを選ぶ
- 頼みごとを書くと、Claudeが**変更案**を出す
- <span class="term">差分（diff）</span><span class="gloss">どこが変わるかの表示</span>を見て **Accept / Reject**
- **Preview**：作ったアプリをアプリ内で起動して見られる

<div class="do">

ポイント：**いつでも止められる・言い直せる**。気軽に試してOK。

</div>

---

## remote-control（リモート操作）

<div class="split sm">
<div class="t">

<span class="term">remote-control</span><span class="gloss">スマホからPCのClaude Codeに指示を送る</span>

- 外出先からスマホで「これやっといて」と投げる
- PC側のClaude Codeが受け取って作業
- “PCの前にいなくても進む”感覚

</div>
<img src="img/remote_control.png" alt="スマホから自宅のPCに指示を送るイラスト">
</div>

<div class="small">

※ 新しめの機能です。今日は概念の紹介まで（時間が余れば触ります）。

</div>

---

## MCP（コネクタ）とは

<div class="split sm">
<div class="t">

<span class="term">MCP</span><span class="gloss">AI用の“USB端子”。外部サービスに挿す仕組み</span>

- Claude Code単体は「自分のPCの中」が基本
- **MCPを挿す**と、外の世界（地図・メール・カレンダー等）につながる
- 「コネクタ」という言い方もします

</div>
<img src="img/mcp.png" alt="USB端子で外部の道具につながるAIのイラスト">
</div>

<div class="do">

今日のハンズオン①で、**ブラウザを操作するMCP（Playwright MCP）**を実際に使います。

</div>

---

## MCPの活用例（今日はやらない・紹介だけ）

<div class="cols">
<div class="col">

### 📧 Gmail
メールを読み取って<br>**下書き・自動返信**を作る

</div>
<div class="col">

### 💬 Slack
チャンネルを読み取って<br>**返信案**を用意する

</div>
<div class="col">

### 📅 Googleカレンダー
予定を読み込んで<br>**今日の予定を把握**

</div>
</div>

<br>

> 「自分の道具に“挿す”だけで、AIができることが一気に広がる」── これがMCPの面白さ。

<div class="warn small">

メールやチャットの**自動送信**は事故のもと。実運用では「**下書きまで**＝人が最後に確認」が安全。

</div>

---

## Skills（スキル）とは

<div class="split sm">
<div class="t">

<span class="term">Skills</span><span class="gloss">よく使う“作業手順書”をまとめたパック</span>

- Claude Codeに「この手順でやって」と覚えさせておけるもの
- 画面で **`/`** を打つと呼び出せる
- 毎回ゼロから説明しなくてよくなる

</div>
<img src="img/skills.png" alt="手順書（レシピ集）を持つロボットのイラスト">
</div>

<div class="do">

今日は **`idea-to-mockup`** というスキルを用意しました。<br>
質問に答えるだけで、**自分のアイデアの試作**ができます（最後に使います）。

</div>

---

## Agentic loop（自分で回す仕組み）

<span class="term">Agentic loop</span><span class="gloss">考える→やる→結果を見る→直す、を自分で繰り返す</span>

<div class="diagram">
  <div class="box"><b>考える</b><span class="small">何をすべきか</span></div>
  <div class="arrow">→</div>
  <div class="box"><b>やる</b><span class="small">ファイル作成・実行</span></div>
  <div class="arrow">→</div>
  <div class="box"><b>確認</b><span class="small">結果・エラー</span></div>
  <div class="arrow">→</div>
  <div class="box"><b>直す</b><span class="small">必要なら修正</span></div>
</div>

<div class="split sm">
<div class="t">

- 人が一手ずつ指示しなくても、ある程度**自走**する
- だから「止める・確認する」操作が大事になる

</div>
<img src="img/agentic_loop.png" alt="考える→やる→確認→直すをぐるぐる繰り返すループのイラスト">
</div>

---

<!-- _class: section -->
<!-- _paginate: false -->

<span class="eyebrow">HANDS-ON 1</span>

# AIにブラウザで調べ物
### 結果を表（CSV）に書き出す

---

## ハンズオン①でやること

<div class="split sm">
<div class="t">

<span class="term">Playwright MCP</span><span class="gloss">人の代わりにブラウザを自動操作する道具</span>

1. Claude Codeに **Playwright MCP** をつなぐ
2. 「○○を調べて一覧にして」とお願いする<br><span class="small">例：近所のカフェをGoogleマップで10件（名前・住所・評価）</span>
3. Claudeが**ブラウザを自動で動かして**集める（画面で見える！）
4. <span class="term">CSV</span><span class="gloss">表計算で開ける、カンマ区切りの表ファイル</span>に書き出す
5. **スプレッドシート**（Excel / Googleスプレッドシート）で開く

</div>
<img src="img/playwright_robot.png" alt="ロボットが自動でブラウザを操作して情報を集めるイラスト">
</div>

---

## ハンズオン①の進め方

<div class="do">

頼み方の例：<br>
「Googleマップで“渋谷 カフェ”を調べて、上位10件の**店名・住所・評価**を集めて、`cafes.csv` に保存して」

</div>

- うまくいかない → 件数を減らす／条件を具体的にする
- 集まったら **`cafes.csv` をスプレッドシートで開く**
- 「人が30分かける作業をAIがやる」体験

<div class="warn small">

マナー：**少量・学習目的**で。相手サイトの規約・回数制限に配慮（大量取得はしない）。

</div>

---

<!-- _class: section -->
<!-- _paginate: false -->

<span class="eyebrow">HANDS-ON 2</span>

# 予約サイトを作って
### 友達に送れるURLにする

---

## これから作るもの

- お店の**トップページ**（名前・写真・営業時間）
- **予約フォーム**（名前・日時・人数）
- 送信された予約の**一覧表示**（**管理者だけ**が見られる）

<div class="do">

完成イメージ：フォームから予約 → 一覧に増える → そのURLを友達に送れる

</div>

---

## 作る順番（STEP 0〜9）

1. **STEP0** 「お店の予約サイトを作りたい」と伝える <span class="small">→ セッション / Agentic loop</span>
2. **STEP1** トップページ <span class="small">→ フロントエンド</span>
3. **STEP2** 予約フォーム
4. **STEP3** 予約を受け取って保存 <span class="small">→ バック / API / データベース</span>
5. **STEP4** 予約一覧で確認 ← ここで“動いた！”
6. **STEP5** **管理者ログイン** <span class="small">→ 一覧は管理者だけが見られる（作成は今は誰でも可）</span>
7. **STEP6** 自動チェック <span class="small">→ ユニットテスト</span>
8. **STEP7** お客さん目線の自動チェック <span class="small">→ E2Eテスト / Playwright</span>
9. **STEP8** 自分のPCで起動（Previewでも確認）
10. **STEP9** **ngrokで公開 → URLを友達に送る** 🎉

---

## テストってなに？（STEP6–7で登場）

<div class="split sm">
<div class="t">

- <span class="term">ユニットテスト</span><span class="gloss">部品ひとつが正しく動くかの確認</span>
- <span class="term">E2Eテスト</span><span class="gloss">お客さんの一連の流れを丸ごと確認</span>
- <span class="term">Playwright</span><span class="gloss">お客さんの代わりに画面を操作するロボット</span>

> 「フォームに入力 → 送信 → 完了画面が出る」を**自動で**やってくれる。

</div>
<img src="img/test_rehearsal.png" alt="味見（ユニット）と通しリハーサル（E2E）を並べたイラスト">
</div>

---

## STEP9：ngrokで公開する

<div class="split sm">
<div class="t">

- 出てくる住所は `〜.ngrok-free.app`（無料）
- そのURLを**友達に送れば、スマホから予約できる**

</div>
<img src="img/ngrok_tunnel.png" alt="自宅PCから外の友達のスマホへ一本のトンネルが伸びるイラスト">
</div>

<div class="warn">

注意：無料版のURLは**一時的**。**PCやngrokを閉じると止まります**。<br>
＝“今この瞬間に生きているリンク”。常時公開したいなら、本当はサーバーに置く（今日はやらない）。

</div>

<div class="small">

※ ngrokは無料登録して**authtoken**を取得します（準備でやりました）。

</div>

---

## うまくいかない時のコツ

- **止める**：暴走しそうなら停止ボタン
- **言い直す**：「さっきのを、こう変えて」でOK
- **差分を見る**：何が変わるか必ず確認してからAccept
- **小さく頼む**：一度に大きく頼まず、1ステップずつ

<div class="do">

エラーは“失敗”ではなく**会話のきっかけ**。そのままClaudeに見せて「直して」でOK。

</div>

---

<!-- _class: section -->
<!-- _paginate: false -->

<span class="eyebrow">WRAP UP</span>

# まとめと次の一歩

---

## 今日さわった言葉（チェック）

<div class="cols">
<div class="col">

**仕組み**
LLM / Claude / Claude Code
フロント / バック / DB / API
サーバー / クラウド / インターネット

</div>
<div class="col">

**道具**
MCP（コネクタ）/ Skills
remote-control / Playwright MCP
CSV / ngrok / テスト

</div>
</div>

<br>

> 全部を“説明できる”必要はありません。**“見て驚かない”**ようになれば十分。

---

## 次の一歩：自分のアイデアを試す

<div class="do">

スキル **`idea-to-mockup`** を呼び出して、<br>
質問に答えるだけで**あなたのアイデアの試作**を作ってみましょう。

</div>

- 「○○できるやつが欲しい」と言うだけでOK
- 今日の予約サイトと同じ流れで、自分専用に

---

<!-- _class: title -->
<!-- _paginate: false -->

# ありがとうございました 🙌

## 質問タイム

<span class="gloss" style="color:#E9C3B4">困ったら、その画面のまま聞いてください。一緒に直します。</span>
