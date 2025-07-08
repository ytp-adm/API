# Dify統合テスト例

## 🎯 Difyでの設定手順

### 1. HTTPツールノードの追加

Difyワークフローで「HTTP Request」ノードを追加し、以下の設定を行います：

### 2. 基本設定

```
Node Name: SEO見出し抽出
URL: https://seo-fastapi-449500499475.asia-northeast1.run.app/extract-headings
Method: POST
```

### 3. ヘッダー設定

```
Content-Type: application/json
```

### 4. リクエストボディ設定

**固定URL版**:
```json
{
  "urls": ["https://example.com/"]
}
```

**動的URL版**（ユーザー入力を使用）:
```json
{
  "urls": ["{{url_input}}"]
}
```

**複数URL版**:
```json
{
  "urls": ["{{url1}}", "{{url2}}", "{{url3}}"]
}
```

### 5. レスポンス設定

- **Output Variable Name**: `seo_response`
- **Parse Response as JSON**: ✅ 有効
- **Timeout**: 30秒

### 6. 変数アクセス例

レスポンスデータにアクセスする方法：

```
処理時間: {{seo_response.processing_time_seconds}}秒

最初のURLの結果:
- URL: {{seo_response.results[0].url}}
- ステータス: {{seo_response.results[0].status}}
- H1タグ: {{seo_response.results[0].headings.h1[0]}}

H2セクション一覧:
{{#each seo_response.results[0].headings.h2_sections}}
- {{h2_text}}
  {{#each h3_tags}}
  - {{this}}
  {{/each}}
{{/each}}
```

## 🧪 テストケース

### テストケース1: 基本動作確認

**入力**:
```json
{
  "urls": ["https://example.com/"]
}
```

**期待される出力**:
```json
{
  "processing_time_seconds": 0.31,
  "results": [
    {
      "url": "https://example.com/",
      "status": "success",
      "headings": {
        "h1": ["Example Domain"],
        "h2_sections": []
      },
      "error": null
    }
  ]
}
```

### テストケース2: 複数URL処理

**入力**:
```json
{
  "urls": ["https://example.com/", "https://httpbin.org/html"]
}
```

### テストケース3: エラーハンドリング

**入力**:
```json
{
  "urls": ["https://invalid-domain-12345.com/"]
}
```

**期待される出力**:
```json
{
  "processing_time_seconds": 0.15,
  "results": [
    {
      "url": "https://invalid-domain-12345.com/",
      "status": "error",
      "headings": null,
      "error": "HTTPエラー: ..."
    }
  ]
}
```

## 🔧 トラブルシューティング

### 問題1: "Failed to parse JSON"エラー

**原因**: 
- レスポンスが正しく受信されていない
- JSON解析設定が無効

**解決方法**:
1. HTTPツールノードの「Test」機能でレスポンスを確認
2. 「Parse Response as JSON」が有効になっているか確認
3. タイムアウト設定を30秒に延長

### 問題2: 変数にアクセスできない

**原因**: 
- 変数名が間違っている
- JSONパスが正しくない

**解決方法**:
1. レスポンス構造を確認: `{{seo_response}}`
2. 正しいパス使用: `{{seo_response.results[0].headings.h1}}`

### 問題3: タイムアウトエラー

**原因**: 
- 処理時間が長いURL
- ネットワーク遅延

**解決方法**:
1. タイムアウトを60秒に延長
2. URLを分割して複数回実行

## 📋 Difyワークフロー例

### シンプルなSEO分析ワークフロー

```
1. [Start] ユーザーからURL入力
   ↓
2. [HTTP Request] SEO見出し抽出API呼び出し
   ↓
3. [Code] レスポンス処理・整形
   ↓
4. [LLM] 見出し構造の分析・改善提案
   ↓
5. [End] 結果をユーザーに返す
```

### コード例（レスポンス処理）

```python
def process_seo_response(response):
    """SEO APIレスポンスを処理して分析用データを作成"""
    
    results = []
    
    for result in response['results']:
        if result['status'] == 'success':
            headings = result['headings']
            
            # H1分析
            h1_count = len(headings['h1'])
            h1_text = headings['h1'][0] if headings['h1'] else "なし"
            
            # H2構造分析
            h2_count = len(headings['h2_sections'])
            h2_with_h3 = sum(1 for section in headings['h2_sections'] if section['h3_tags'])
            
            analysis = {
                'url': result['url'],
                'h1_count': h1_count,
                'h1_text': h1_text,
                'h2_count': h2_count,
                'h2_with_h3_count': h2_with_h3,
                'structure_score': calculate_structure_score(headings)
            }
            
            results.append(analysis)
    
    return results

def calculate_structure_score(headings):
    """見出し構造のスコアを計算"""
    score = 0
    
    # H1が1つの場合は+10点
    if len(headings['h1']) == 1:
        score += 10
    
    # H2が適切な数（2-8個）の場合は+5点
    h2_count = len(headings['h2_sections'])
    if 2 <= h2_count <= 8:
        score += 5
    
    # H3が適切に使われている場合は+3点
    h3_usage = sum(1 for section in headings['h2_sections'] if section['h3_tags'])
    if h3_usage > 0:
        score += 3
    
    return min(score, 20)  # 最大20点
```

## 🚀 実装のヒント

1. **エラーハンドリング**: 必ずstatus='error'の場合の処理を含める
2. **バッチ処理**: 大量URLの場合は分割して処理
3. **キャッシュ**: 同じURLの重複処理を避ける
4. **ログ**: 処理状況をユーザーに表示
5. **検証**: URL形式の事前チェック

これらの設定でDifyでの統合が成功するはずです！