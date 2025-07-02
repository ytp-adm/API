# SEO見出し抽出API - プロジェクトクリーンアップ

## 概要
SEO見出し抽出APIプロジェクトの整理とGoogle Cloud Runへのデプロイ完了に伴う、本番用構成への移行です。

## 変更内容

### 🗑️ 削除されたファイル
- `debug_headings.py` - デバッグ用スクリプト
- `test_*.py` - 開発・テスト用スクリプト（10ファイル）
- `main_original.py`, `main_with_apikey.py` - バックアップファイル

### 📝 更新されたファイル
- **README.md**: 本番環境情報、認証方法、Dify統合手順を含む完全なガイドに更新
- **.gitignore**: セキュリティファイル（`*.json`、テストファイル等）の除外を強化

### ➕ 追加されたファイル
- **DIFY_INTEGRATION.md**: Dify統合専用の詳細ガイド
- **GITHUB_SETUP.md**: GitHubリポジトリセットアップ手順

## 本番環境情報

- **API URL**: https://seo-fastapi-449500499475.asia-northeast1.run.app
- **プロジェクト**: dify-seo-api-2025
- **認証**: Google Cloud IDトークン + APIキー (`dify-seo-api-key-2025`)
- **デプロイ先**: Google Cloud Run (asia-northeast1)

## 機能

✅ 複数URLからH1/H2/H3タグの階層構造抽出  
✅ 並列処理による高速化  
✅ 個別エラーハンドリング  
✅ APIキー認証によるセキュア化  
✅ Dify統合対応  

## セキュリティ対策

- Google Cloud サービスアカウントキーをGit履歴から完全削除
- `.gitignore`でセキュリティファイルの除外を強化
- 組織ポリシーに準拠したアクセス制御

## テスト結果

✅ API動作確認済み（200 OK）  
✅ 認証機能確認済み（APIキー検証）  
✅ 複数URL処理確認済み  
✅ エラーハンドリング確認済み  

## 次のステップ

1. このプルリクエストをマージ
2. Difyワークフローでの統合テスト
3. 本番運用開始

## 関連ドキュメント

- [README.md](README.md) - プロジェクト全体のガイド
- [DIFY_INTEGRATION.md](DIFY_INTEGRATION.md) - Dify統合詳細手順
- [GITHUB_SETUP.md](GITHUB_SETUP.md) - GitHubセットアップガイド

---

**レビュー観点**:
- ファイル構成の整理が適切か
- ドキュメントの内容が正確か
- セキュリティ対策が十分か