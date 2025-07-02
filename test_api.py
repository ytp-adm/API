import requests
import json

def test_api():
    """APIの動作をテストする"""
    
    base_url = "http://localhost:8000"
    
    print("=== HTML見出し抽出API テスト ===\n")
    
    # 1. ヘルスチェック
    print("1. ヘルスチェックテスト")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"ステータス: {response.status_code}")
        print(f"レスポンス: {response.json()}")
        print("✅ ヘルスチェック成功\n")
    except Exception as e:
        print(f"❌ ヘルスチェック失敗: {e}\n")
        return
    
    # 2. 単一URL テスト
    print("2. 単一URLテスト")
    test_data = {
        "urls": ["https://example.com/"]
    }
    
    try:
        response = requests.post(
            f"{base_url}/extract-headings",
            headers={"Content-Type": "application/json"},
            json=test_data
        )
        
        print(f"ステータス: {response.status_code}")
        result = response.json()
        
        print(f"処理済みURL数: {result['total_processed']}")
        print(f"成功数: {result['total_success']}")
        print(f"エラー数: {result['total_errors']}")
        
        for url, data in result['results'].items():
            print(f"\nURL: {url}")
            if 'error' in data:
                print(f"  エラー: {data['error']}")
            else:
                print(f"  H1タグ数: {data['total_h1']}")
                print(f"  H2タグ数: {data['total_h2']}")
                print(f"  H3タグ数: {data['total_h3']}")
                
                if data['h1_tags']:
                    print(f"  H1タグ: {data['h1_tags']}")
                
                if data['sections']:
                    print("  階層構造:")
                    for i, section in enumerate(data['sections'], 1):
                        print(f"    {i}. H2: {section['h2_title']}")
                        if section['h3_tags']:
                            for j, h3 in enumerate(section['h3_tags'], 1):
                                print(f"       {i}-{j}. H3: {h3}")
                        else:
                            print(f"       (H3タグなし)")
                
                if data['orphan_h3_tags']:
                    print(f"  孤立したH3タグ: {data['orphan_h3_tags']}")
        
        print("✅ 単一URLテスト成功\n")
        
    except Exception as e:
        print(f"❌ 単一URLテスト失敗: {e}\n")
    
    # 3. 複数URL テスト（成功とエラーの混在）
    print("3. 複数URLテスト（成功とエラーの混在）")
    test_data = {
        "urls": [
            "https://example.com/",
            "https://invalid-domain-12345.com/"
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/extract-headings",
            headers={"Content-Type": "application/json"},
            json=test_data
        )
        
        print(f"ステータス: {response.status_code}")
        result = response.json()
        
        print(f"処理済みURL数: {result['total_processed']}")
        print(f"成功数: {result['total_success']}")
        print(f"エラー数: {result['total_errors']}")
        
        for url, data in result['results'].items():
            print(f"\nURL: {url}")
            if 'error' in data:
                print(f"  ❌ エラー: {data['error']}")
            else:
                print(f"  ✅ 成功 - H1:{data['total_h1']}, H2:{data['total_h2']}, H3:{data['total_h3']}")
        
        print("✅ 複数URLテスト成功\n")
        
    except Exception as e:
        print(f"❌ 複数URLテスト失敗: {e}\n")
    
    # 4. 無効なリクエスト テスト
    print("4. 無効なリクエストテスト")
    invalid_data = {
        "urls": ["invalid-url"]
    }
    
    try:
        response = requests.post(
            f"{base_url}/extract-headings",
            headers={"Content-Type": "application/json"},
            json=invalid_data
        )
        
        print(f"ステータス: {response.status_code}")
        if response.status_code == 422:
            print("✅ バリデーションエラーが正しく返されました")
        else:
            print("❌ 予期しないレスポンス")
        
    except Exception as e:
        print(f"❌ 無効なリクエストテスト失敗: {e}")
    
    print("\n=== テスト完了 ===")

if __name__ == "__main__":
    test_api()