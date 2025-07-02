#!/usr/bin/env python3
"""
最終APIテスト - レスポンス詳細確認
"""

import requests
import json

# IDトークン（gcloudコマンドで取得）
ID_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg4MjUwM2E1ZmQ1NmU5ZjczNGRmYmE1YzUwZDdiZjQ4ZGIyODRhZTkiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJodHRwczovL3Nlby1mYXN0YXBpLTQ0OTUwMDQ5OTQ3NS5hc2lhLW5vcnRoZWFzdDEucnVuLmFwcCIsImF6cCI6IjQ0OTUwMDQ5OTQ3NS1jb21wdXRlQGRldmVsb3Blci5nc2VydmljZWFjY291bnQuY29tIiwiZW1haWwiOiI0NDk1MDA0OTk0NzUtY29tcHV0ZUBkZXZlbG9wZXIuZ3NlcnZpY2VhY2NvdW50LmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJleHAiOjE3NTE0ODE4MzcsImlhdCI6MTc1MTQ3ODIzNywiaXNzIjoiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tIiwic3ViIjoiMTAzNDI4MDAwNTMwMzY5MTgyNTIxIn0.HfqvpleRtLUqfi6uN-4jfwyK2Jw28XLU6lSgH-RXXs9nWhT0yuafhCOPxVJpGN-RvPA15HL9OwNEK9H-RfqpycqcJQy3dUK7knwW7SaLabpze0C4ntpEFJ-Tk8iaclxAmPgmxXYtlmGoL9NEHOjO2_zAV0o1nTprZ90qc1XNHBpMl0bJVTsMo6UTmWoLJEtEC02svVdPaGcJFk0UR59tYj-YeX8tP_ski9OTE5PNex6kL4HSx_9SB4xAee6-7CmQWtbbnbGlE1B1et8pY3F75FTwuV18GBgqdxcT5gtZDn-OIyN7-p9vq1kJiGA3PEdG4gc0oVy_fdVkiXpSRudRkg"

# Cloud Run サービスURL
BASE_URL = "https://seo-fastapi-449500499475.asia-northeast1.run.app"

def test_extract_headings():
    """見出し抽出APIの詳細テスト"""
    
    # 認証ヘッダーを設定
    headers = {
        "Authorization": f"Bearer {ID_TOKEN}",
        "Content-Type": "application/json",
        "X-API-Key": "dify-seo-api-key-2025"
    }
    
    print("=== /extract-headingsエンドポイントの詳細テスト ===")
    
    test_data = {
        "urls": [
            "https://example.com",
            "https://httpbin.org/html"
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/extract-headings",
            headers=headers,
            json=test_data,
            timeout=30
        )
        
        print(f"ステータスコード: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"レスポンス構造:")
            print(f"  - 処理時間: {result.get('processing_time_seconds', 'N/A')}秒")
            print(f"  - 処理URL数: {len(result.get('results', []))}")
            
            for i, url_result in enumerate(result.get('results', []), 1):
                print(f"\n--- URL {i} ---")
                print(f"URL: {url_result.get('url', 'N/A')}")
                print(f"ステータス: {url_result.get('status', 'N/A')}")
                
                if url_result.get('status') == 'success':
                    headings = url_result.get('headings', {})
                    
                    # H1タグ
                    h1_tags = headings.get('h1', [])
                    print(f"H1タグ: {len(h1_tags)}個")
                    for j, h1 in enumerate(h1_tags[:2], 1):  # 最初の2個のみ表示
                        print(f"  H1-{j}: {h1}")
                    
                    # H2セクション
                    h2_sections = headings.get('h2_sections', [])
                    print(f"H2セクション: {len(h2_sections)}個")
                    for j, section in enumerate(h2_sections[:2], 1):  # 最初の2個のみ表示
                        print(f"  H2-{j}: {section.get('h2_text', 'N/A')}")
                        h3_tags = section.get('h3_tags', [])
                        print(f"    配下のH3: {len(h3_tags)}個")
                        for k, h3 in enumerate(h3_tags[:2], 1):  # 最初の2個のみ表示
                            print(f"      H3-{k}: {h3}")
                
                elif url_result.get('status') == 'error':
                    print(f"エラー: {url_result.get('error', 'N/A')}")
        else:
            print(f"エラーレスポンス: {response.text}")
            
    except Exception as e:
        print(f"リクエストエラー: {e}")

def test_api_key_validation():
    """APIキー認証のテスト"""
    
    print("\n=== APIキー認証テスト ===")
    
    # 正しいIDトークン + 間違ったAPIキー
    headers_wrong_key = {
        "Authorization": f"Bearer {ID_TOKEN}",
        "Content-Type": "application/json",
        "X-API-Key": "wrong-api-key"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/extract-headings",
            headers=headers_wrong_key,
            json={"urls": ["https://example.com"]},
            timeout=30
        )
        
        print(f"間違ったAPIキーでのテスト:")
        print(f"  ステータスコード: {response.status_code}")
        if response.status_code != 200:
            print(f"  エラー: {response.json()}")
        else:
            print("  予期しない成功")
            
    except Exception as e:
        print(f"リクエストエラー: {e}")

if __name__ == "__main__":
    print("最終APIテストを開始...")
    test_extract_headings()
    test_api_key_validation()
    
    print("\n" + "="*50)
    print("🎉 APIデプロイメント完了！")
    print("="*50)
    print(f"API URL: {BASE_URL}")
    print("認証方法: Google Cloud IDトークン + X-API-Key ヘッダー")
    print("APIキー: dify-seo-api-key-2025")
    print("\nDifyでの使用方法:")
    print("1. HTTPリクエストノードを使用")
    print("2. URL: https://seo-fastapi-449500499475.asia-northeast1.run.app/extract-headings")
    print("3. Method: POST")
    print("4. Headers:")
    print("   - Authorization: Bearer [Google Cloud IDトークン]")
    print("   - X-API-Key: dify-seo-api-key-2025")
    print("   - Content-Type: application/json")
    print("5. Body: {\"urls\": [\"https://example.com\"]}")