#!/usr/bin/env python3
"""
Cloud Run APIをサービスアカウントキーを使用してテストするスクリプト
"""

import json
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

def get_access_token():
    """サービスアカウントキーからアクセストークンを取得"""
    credentials = service_account.Credentials.from_service_account_file(
        'dify-service-account-key.json',
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    
    # トークンをリフレッシュ
    credentials.refresh(Request())
    return credentials.token

def test_api():
    """APIをテスト"""
    try:
        # アクセストークンを取得
        token = get_access_token()
        print(f"アクセストークンを取得しました: {token[:20]}...")
        
        # APIエンドポイント
        api_url = "https://seo-fastapi-449500499475.asia-northeast1.run.app"
        
        # ヘッダーを設定
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # まずルートエンドポイントをテスト
        print("\n=== ルートエンドポイントをテスト ===")
        response = requests.get(f"{api_url}/", headers=headers)
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.text}")
        
        # docsエンドポイントをテスト
        print("\n=== /docsエンドポイントをテスト ===")
        response = requests.get(f"{api_url}/docs", headers=headers)
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            print("Swagger UIにアクセス可能です")
        
        # APIエンドポイントをテスト
        print("\n=== /extract-headingsエンドポイントをテスト ===")
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
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    test_api()