#!/usr/bin/env python3
"""
認証されたAPIテスト
Google Cloud サービスアカウントを使用してCloud Run APIにアクセスします
"""

import requests
import json
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# サービスアカウントキーファイルのパス
SERVICE_ACCOUNT_KEY_PATH = "dify-service-account-key.json"

# Cloud Run サービスURL
BASE_URL = "https://seo-fastapi-449500499475.asia-northeast1.run.app"

def get_access_token():
    """サービスアカウントからアクセストークンを取得"""
    try:
        # サービスアカウント認証情報を読み込み
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_KEY_PATH,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        
        # トークンを更新
        credentials.refresh(Request())
        return credentials.token
    except Exception as e:
        print(f"認証エラー: {e}")
        return None

def test_authenticated_request():
    """認証されたリクエストでAPIをテスト"""
    
    # アクセストークンを取得
    access_token = get_access_token()
    if not access_token:
        print("アクセストークンの取得に失敗しました")
        return
    
    # 認証ヘッダーを設定
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-API-Key": "dify-seo-api-key-2025"  # APIキーも含める
    }
    
    print("=== 認証されたルートエンドポイントをテスト ===")
    try:
        response = requests.get(f"{BASE_URL}/", headers=headers, timeout=30)
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            print(f"レスポンス: {response.json()}")
        else:
            print(f"エラー: {response.text}")
    except Exception as e:
        print(f"リクエストエラー: {e}")
    
    print("\n=== 認証された/healthエンドポイントをテスト ===")
    try:
        response = requests.get(f"{BASE_URL}/health", headers=headers, timeout=30)
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            print(f"レスポンス: {response.json()}")
        else:
            print(f"エラー: {response.text}")
    except Exception as e:
        print(f"リクエストエラー: {e}")
    
    print("\n=== 認証された/extract-headingsエンドポイントをテスト ===")
    try:
        test_data = {
            "urls": [
                "https://example.com",
                "https://httpbin.org/html"
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
            for i, url_result in enumerate(result.get('results', [])[:2]):  # 最初の2件のみ表示
                print(f"  URL {i+1}: {url_result.get('url')}")
                print(f"    ステータス: {url_result.get('status')}")
                if url_result.get('status') == 'success':
                    headings = url_result.get('headings', {})
                    print(f"    H1: {len(headings.get('h1', []))}個")
                    print(f"    H2セクション: {len(headings.get('h2_sections', []))}個")
        else:
            print(f"エラー: {response.text}")
    except Exception as e:
        print(f"リクエストエラー: {e}")

if __name__ == "__main__":
    print("Google Cloud認証を使用したAPIテストを開始...")
    test_authenticated_request()