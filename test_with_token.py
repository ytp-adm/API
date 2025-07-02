#!/usr/bin/env python3
"""
IDトークンを使用したAPIテスト
"""

import requests
import json

# IDトークン（gcloudコマンドで取得）
ID_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg4MjUwM2E1ZmQ1NmU5ZjczNGRmYmE1YzUwZDdiZjQ4ZGIyODRhZTkiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJodHRwczovL3Nlby1mYXN0YXBpLTQ0OTUwMDQ5OTQ3NS5hc2lhLW5vcnRoZWFzdDEucnVuLmFwcCIsImF6cCI6IjQ0OTUwMDQ5OTQ3NS1jb21wdXRlQGRldmVsb3Blci5nc2VydmljZWFjY291bnQuY29tIiwiZW1haWwiOiI0NDk1MDA0OTk0NzUtY29tcHV0ZUBkZXZlbG9wZXIuZ3NlcnZpY2VhY2NvdW50LmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJleHAiOjE3NTE0ODE4MzcsImlhdCI6MTc1MTQ3ODIzNywiaXNzIjoiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tIiwic3ViIjoiMTAzNDI4MDAwNTMwMzY5MTgyNTIxIn0.HfqvpleRtLUqfi6uN-4jfwyK2Jw28XLU6lSgH-RXXs9nWhT0yuafhCOPxVJpGN-RvPA15HL9OwNEK9H-RfqpycqcJQy3dUK7knwW7SaLabpze0C4ntpEFJ-Tk8iaclxAmPgmxXYtlmGoL9NEHOjO2_zAV0o1nTprZ90qc1XNHBpMl0bJVTsMo6UTmWoLJEtEC02svVdPaGcJFk0UR59tYj-YeX8tP_ski9OTE5PNex6kL4HSx_9SB4xAee6-7CmQWtbbnbGlE1B1et8pY3F75FTwuV18GBgqdxcT5gtZDn-OIyN7-p9vq1kJiGA3PEdG4gc0oVy_fdVkiXpSRudRkg"

# Cloud Run サービスURL
BASE_URL = "https://seo-fastapi-449500499475.asia-northeast1.run.app"

def test_api():
    """IDトークンを使用してAPIをテスト"""
    
    # 認証ヘッダーを設定
    headers = {
        "Authorization": f"Bearer {ID_TOKEN}",
        "Content-Type": "application/json",
        "X-API-Key": "dify-seo-api-key-2025"
    }
    
    print("=== ルートエンドポイントをテスト ===")
    try:
        response = requests.get(f"{BASE_URL}/", headers=headers, timeout=30)
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            print(f"レスポンス: {response.json()}")
        else:
            print(f"エラー: {response.text[:300]}...")
    except Exception as e:
        print(f"リクエストエラー: {e}")
    
    print("\n=== /healthエンドポイントをテスト ===")
    try:
        response = requests.get(f"{BASE_URL}/health", headers=headers, timeout=30)
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            print(f"レスポンス: {response.json()}")
        else:
            print(f"エラー: {response.text[:300]}...")
    except Exception as e:
        print(f"リクエストエラー: {e}")
    
    print("\n=== /extract-headingsエンドポイントをテスト ===")
    try:
        test_data = {
            "urls": [
                "https://example.com"
            ]
        }
        
        response = requests.post(
            f"{BASE_URL}/extract-headings",
            headers=headers,
            json=test_data,
            timeout=30
        )
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"成功: {len(result.get('results', []))}件のURLを処理")
            for url_result in result.get('results', []):
                print(f"  URL: {url_result.get('url')}")
                print(f"    ステータス: {url_result.get('status')}")
                if url_result.get('status') == 'success':
                    headings = url_result.get('headings', {})
                    print(f"    H1: {len(headings.get('h1', []))}個")
                    print(f"    H2セクション: {len(headings.get('h2_sections', []))}個")
                    # 最初のH2セクションの詳細を表示
                    if headings.get('h2_sections'):
                        first_h2 = headings['h2_sections'][0]
                        print(f"      最初のH2: {first_h2.get('h2_text', 'N/A')}")
                        print(f"      配下のH3: {len(first_h2.get('h3_tags', []))}個")
        else:
            print(f"エラー: {response.text[:300]}...")
    except Exception as e:
        print(f"リクエストエラー: {e}")

if __name__ == "__main__":
    print("IDトークンを使用したAPIテストを開始...")
    test_api()