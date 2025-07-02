#!/usr/bin/env python3
"""
認証されたAPIテスト（修正版）
Google Cloud IDトークンを使用してCloud Run APIにアクセスします
"""

import requests
import json
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.auth import jwt

# サービスアカウントキーファイルのパス
SERVICE_ACCOUNT_KEY_PATH = "dify-service-account-key.json"

# Cloud Run サービスURL
BASE_URL = "https://seo-fastapi-449500499475.asia-northeast1.run.app"

def get_id_token():
    """サービスアカウントからIDトークンを取得"""
    try:
        # サービスアカウント認証情報を読み込み
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_KEY_PATH
        )
        
        # IDトークンを作成
        request = Request()
        id_token = jwt.encode(
            {
                "iss": credentials.service_account_email,
                "sub": credentials.service_account_email,
                "aud": BASE_URL,
                "iat": jwt._helpers.utcnow().timestamp(),
                "exp": (jwt._helpers.utcnow() + jwt._helpers.timedelta(hours=1)).timestamp()
            },
            credentials._private_key,
            algorithm="RS256"
        )
        
        return id_token
    except Exception as e:
        print(f"IDトークン取得エラー: {e}")
        return None

def get_id_token_alternative():
    """代替方法でIDトークンを取得"""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2 import service_account
        import google.auth.transport.requests
        
        # サービスアカウント認証情報を読み込み
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_KEY_PATH
        )
        
        # IDトークン用の認証情報を作成
        id_credentials = service_account.IDTokenCredentials(
            credentials, 
            target_audience=BASE_URL
        )
        
        # トークンを更新
        request = Request()
        id_credentials.refresh(request)
        
        return id_credentials.token
    except Exception as e:
        print(f"代替IDトークン取得エラー: {e}")
        return None

def test_with_gcloud_auth():
    """gcloud auth print-identity-tokenを使用してテスト"""
    import subprocess
    
    try:
        # gcloudコマンドでIDトークンを取得
        result = subprocess.run([
            "gcloud", "auth", "print-identity-token", 
            f"--audiences={BASE_URL}",
            "--project=dify-seo-api-2025"
        ], capture_output=True, text=True, check=True)
        
        id_token = result.stdout.strip()
        
        # 認証ヘッダーを設定
        headers = {
            "Authorization": f"Bearer {id_token}",
            "Content-Type": "application/json",
            "X-API-Key": "dify-seo-api-key-2025"
        }
        
        print("=== gcloud認証でルートエンドポイントをテスト ===")
        response = requests.get(f"{BASE_URL}/", headers=headers, timeout=30)
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            print(f"レスポンス: {response.json()}")
        else:
            print(f"エラー: {response.text[:200]}...")
        
        print("\n=== gcloud認証で/healthエンドポイントをテスト ===")
        response = requests.get(f"{BASE_URL}/health", headers=headers, timeout=30)
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            print(f"レスポンス: {response.json()}")
        else:
            print(f"エラー: {response.text[:200]}...")
        
        print("\n=== gcloud認証で/extract-headingsエンドポイントをテスト ===")
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
        else:
            print(f"エラー: {response.text[:200]}...")
            
    except subprocess.CalledProcessError as e:
        print(f"gcloudコマンドエラー: {e}")
        print(f"stderr: {e.stderr}")
    except Exception as e:
        print(f"テストエラー: {e}")

def test_authenticated_request():
    """認証されたリクエストでAPIをテスト"""
    
    # IDトークンを取得（代替方法）
    id_token = get_id_token_alternative()
    if not id_token:
        print("IDトークンの取得に失敗しました。gcloud認証を試します...")
        test_with_gcloud_auth()
        return
    
    # 認証ヘッダーを設定
    headers = {
        "Authorization": f"Bearer {id_token}",
        "Content-Type": "application/json",
        "X-API-Key": "dify-seo-api-key-2025"
    }
    
    print("=== IDトークン認証でルートエンドポイントをテスト ===")
    try:
        response = requests.get(f"{BASE_URL}/", headers=headers, timeout=30)
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            print(f"レスポンス: {response.json()}")
        else:
            print(f"エラー: {response.text[:200]}...")
    except Exception as e:
        print(f"リクエストエラー: {e}")

if __name__ == "__main__":
    print("Google Cloud IDトークン認証を使用したAPIテストを開始...")
    test_authenticated_request()