# Dify統合ガイド（最新版）

## 🚀 デプロイ済みAPI情報

**API URL**: https://seo-fastapi-449500499475.asia-northeast1.run.app/

## 📋 現在の状況（2025/1/7 17:26 更新）

### ✅ 完全動作確認済み
- ✅ **パブリックアクセス**: 認証なしでアクセス可能
- ✅ **API機能**: 見出し抽出が正常動作
- ✅ **CORS対応**: Difyからのアクセス対応済み
- ✅ **正しいレスポンス形式**: 有効なJSONレスポンス
- ✅ **組織ポリシー**: 制限を解除済み

### 🔧 解決済み問題
- ~~403 Forbidden エラー~~ → **解決済み**
- ~~組織ポリシー制限~~ → **削除済み**
- ~~パブリックアクセス制限~~ → **利用可能**

## 🔧 Dify統合設定

### 推奨設定: パブリックアクセス

```json
{
  "url": "https://seo-fastapi-449500499475.asia-northeast1.run.app/extract-headings",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "urls": ["https://example.com/", "https://another-site.com"]
  }
}
```

### オプション設定: APIキー付きアクセス

```json
{
  "url": "https://seo-fastapi-449500499475.asia-northeast1.run.app/extract-headings",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json",
    "X-API-Key": "dify-seo-api-key-2025"
  },
  "body": {
    "urls": ["https://example.com/"]
  }
}
```

## 📊 レスポンス形式

### 成功時のレスポンス
```json
{
  "processing_time_seconds": 0.31,
  "results": [
    {
      "url": "https://example.com/",
      "status": "success",
      "headings": {
        "h1": ["Example Domain"],
        "h2_sections": [
          {
            "h2_text": "セクション1",
            "h3_tags": ["サブセクション1", "サブセクション2"]
          }
        ]
      },
      "error": null
    }
  ]
}
```

### エラー時のレスポンス
```json
{
  "processing_time_seconds": 0.15,
  "results": [
    {
      "url": "https://invalid-url.com/",
      "status": "error",
      "headings": null,
      "error": "HTTPエラー: 404 Client Error: Not Found for url"
    }
  ]
}
```

## 🔍 トラブルシューティング

### 1. 403 Forbidden エラー
- **原因**: Google Cloud組織ポリシーによる制限
- **解決済み**: `iam.allowedPolicyMemberDomains`制約を削除済み
- **確認方法**: `curl https://seo-fastapi-449500499475.asia-northeast1.run.app/health`

### 2. CORS エラー
- **原因**: ブラウザからの直接アクセス時のCORS制限
- **解決済み**: CORSMiddlewareを設定済み
- **設定**: `allow_origins=["*"]`で全ドメイン許可

### 3. APIキー認証エラー
- **パブリック版**: APIキーは**オプション**（提供しなくても動作）
- **認証版**: `X-API-Key: dify-seo-api-key-2025`が必須

### 4. Dify「Failed to parse JSON」エラーの解決方法

**✅ API動作確認済み**: APIは正常にJSONを返しています
```bash
# テスト結果（2025/1/7 17:26 確認済み）
curl -X POST "https://seo-fastapi-449500499475.asia-northeast1.run.app/extract-headings" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com/"]}'

# レスポンス: 200 OK
{"processing_time_seconds":0.31,"results":[{"url":"https://example.com/","status":"success","headings":{"h1":["Example Domain"],"h2_sections":[]},"error":null}]}
```

**Difyでの対処法**:

1. **HTTPツールノードの設定確認**:
   ```
   URL: https://seo-fastapi-449500499475.asia-northeast1.run.app/extract-headings
   Method: POST
   Headers: Content-Type: application/json
   Body: {"urls": ["https://example.com/"]}
   ```

2. **レスポンス処理の設定**:
   - **Output Variable**: `response`
   - **Parse JSON**: 有効にする
   - **Expected Response Type**: JSON

3. **変数アクセス方法**:
   ```
   処理時間: {{response.processing_time_seconds}}
   結果配列: {{response.results}}
   最初のURL: {{response.results[0].url}}
   H1タグ: {{response.results[0].headings.h1}}
   H2セクション: {{response.results[0].headings.h2_sections}}
   ```

4. **デバッグ手順**:
   - Difyのログでレスポンス内容を確認
   - HTTPツールノードの「Test」機能を使用
   - レスポンスが正しく受信されているか確認

## 🧪 動作確認テスト

### 基本テスト
```bash
# ヘルスチェック
curl https://seo-fastapi-449500499475.asia-northeast1.run.app/health

# 単一URL抽出
curl -X POST "https://seo-fastapi-449500499475.asia-northeast1.run.app/extract-headings" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com/"]}'

# 複数URL抽出
curl -X POST "https://seo-fastapi-449500499475.asia-northeast1.run.app/extract-headings" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com/", "https://httpbin.org/html"]}'
```

### PowerShellテスト
```powershell
# 単一URL
$response = Invoke-WebRequest -Uri "https://seo-fastapi-449500499475.asia-northeast1.run.app/extract-headings" -Method POST -Headers @{"Content-Type" = "application/json"} -Body '{"urls": ["https://example.com/"]}'; $response.Content

# 複数URL
$body = '{"urls": ["https://example.com/", "https://httpbin.org/html"]}'; Invoke-WebRequest -Uri "https://seo-fastapi-449500499475.asia-northeast1.run.app/extract-headings" -Method POST -Headers @{"Content-Type" = "application/json"} -Body $body
```

## 📝 Dify統合手順

1. **HTTPツールノードを追加**
2. **設定を入力**:
   - URL: `https://seo-fastapi-449500499475.asia-northeast1.run.app/extract-headings`
   - Method: `POST`
   - Headers: `Content-Type: application/json`
   - Body: `{"urls": ["{{user_input_url}}"]}`
3. **レスポンス変数を設定**: `response`
4. **JSON解析を有効化**
5. **テスト実行**で動作確認
6. **ワークフローに統合**

## 🔗 関連リンク

- **API Documentation**: https://seo-fastapi-449500499475.asia-northeast1.run.app/docs
- **Health Check**: https://seo-fastapi-449500499475.asia-northeast1.run.app/health
- **GitHub Repository**: https://github.com/ytp-adm/API (feature/seo-fastapi-cleanup branch)

## 📈 API仕様

### エンドポイント
- `GET /` - API情報
- `GET /health` - ヘルスチェック
- `POST /extract-headings` - 見出し抽出（メイン機能）

### リクエスト制限
- タイムアウト: 10秒/URL
- 同時処理: 複数URL対応
- レート制限: なし（現在）

### セキュリティ
- HTTPS通信
- CORS対応
- オプションAPIキー認証
- 入力検証（Pydantic）