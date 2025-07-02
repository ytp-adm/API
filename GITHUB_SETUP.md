# GitHub リポジトリセットアップガイド

## 手順1: GitHubでリポジトリを作成

1. **GitHub.com にアクセス**
   - https://github.com にログイン

2. **新しいリポジトリを作成**
   - 右上の「+」ボタン → 「New repository」をクリック
   - Repository name: `seo-fastapi-dify` (または任意の名前)
   - Description: `SEO見出し抽出API - Dify統合用FastAPIサービス`
   - Public または Private を選択
   - **重要**: 「Initialize this repository with a README」はチェックしない
   - 「Create repository」をクリック

## 手順2: ローカルリポジトリとGitHubを接続

GitHubリポジトリ作成後、以下のコマンドを実行してください：

```bash
# GitHubリポジトリをリモートとして追加
git remote add origin https://github.com/[あなたのユーザー名]/[リポジトリ名].git

# メインブランチをプッシュ
git push -u origin main
```

### 例（実際のユーザー名とリポジトリ名に置き換えてください）:
```bash
git remote add origin https://github.com/yourusername/seo-fastapi-dify.git
git push -u origin main
```

## 手順3: 認証設定（必要に応じて）

### Personal Access Token を使用する場合:
1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 「Generate new token」で新しいトークンを作成
3. 必要な権限: `repo` (フルアクセス)
4. プッシュ時にユーザー名とトークンを使用

### SSH キーを使用する場合:
```bash
# SSH キーを生成（まだない場合）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 公開キーをGitHubに追加
# ~/.ssh/id_ed25519.pub の内容をGitHub Settings → SSH and GPG keys に追加

# SSH URLを使用
git remote set-url origin git@github.com:[ユーザー名]/[リポジトリ名].git
```

## 手順4: プッシュ実行

```bash
git push -u origin main
```

## 推奨リポジトリ設定

### リポジトリ名の候補:
- `seo-fastapi-dify`
- `dify-seo-heading-extractor`
- `fastapi-heading-extraction`

### 説明文の例:
```
SEO見出し抽出API - 複数URLからH1/H2/H3タグを階層構造で一括抽出するFastAPIサービス。Google Cloud Run対応、Dify統合用。
```

### トピック（タグ）の推奨:
- `fastapi`
- `seo`
- `web-scraping`
- `dify`
- `google-cloud-run`
- `heading-extraction`
- `api`

## セキュリティ注意事項

⚠️ **重要**: 以下のファイルは絶対にGitHubにプッシュしないでください：
- `dify-service-account-key.json` (既に.gitignoreに追加済み)
- その他の認証情報やAPIキー

現在の`.gitignore`設定により、これらのファイルは自動的に除外されます。

## 完了後の確認

GitHubリポジトリが正常に作成されたら：
1. リポジトリページでファイル構造を確認
2. README.mdが正しく表示されることを確認
3. DIFY_INTEGRATION.mdが含まれていることを確認

---

**次のステップ**: GitHubリポジトリ作成後、上記のコマンドを実行してプッシュしてください。