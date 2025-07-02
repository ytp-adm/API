#!/usr/bin/env python3
"""
APIキー認証を使用してCloud Run APIをテストするスクリプト
"""

import json
import requests

def test_api_with_apikey():
    """APIキー認証でAPIをテスト"""
    try:
        # APIエンドポイント
        api_url = "https://seo-fastapi-449500499475.asia-northeast1.run.app"
        
        # APIキー
        api_key = "dify-seo-api-key-2025"
        
        # ヘッダーを設定
        headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
        
        # まずルートエンドポイントをテスト（認証不要）
        print("=== ルートエンドポイントをテスト（認証不要） ===")
        response = requests.get(f"{api_url}/")
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"エラー: {response.text}")
        
        # ヘルスチェックエンドポイントをテスト（認証不要）
        print("\n=== /healthエンドポイントをテスト（認証不要） ===")
        response = requests.get(f"{api_url}/health")
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # APIエンドポイントをテスト（APIキー認証）
        print("\n=== /extract-headingsエンドポイントをテスト（APIキー認証） ===")
        test_data = {
            "urls": ["https://example.com"]
        }
        
        response = requests.post(
            f"{api_url}/extract-headings",
            headers=headers,
            json=test_data
        )
        
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("APIレスポンス:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"エラー: {response.text}")
        
        # 間違ったAPIキーでテスト
        print("\n=== 間違ったAPIキーでテスト ===")
        wrong_headers = {
            "X-API-Key": "wrong-api-key",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{api_url}/extract-headings",
            headers=wrong_headers,
            json=test_data
        )
        
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.text}")
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    test_api_with_apikey()