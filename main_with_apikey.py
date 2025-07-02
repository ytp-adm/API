from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, HttpUrl
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Union, Optional
import logging
import time
import os

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# APIキーの設定（環境変数から取得、デフォルトは簡単なキー）
API_KEY = os.environ.get("API_KEY", "dify-seo-api-key-2025")

app = FastAPI(
    title="HTML見出し抽出API",
    description="指定されたURLリストから<h1>、<h2>、<h3>タグを階層構造で一括抽出するAPI（APIキー認証付き）",
    version="1.0.0"
)

security = HTTPBearer()

class URLListRequest(BaseModel):
    urls: List[HttpUrl]

class H2Section(BaseModel):
    h2_title: str
    h3_tags: List[str]

class HeadingData(BaseModel):
    h1_tags: List[str]
    sections: List[H2Section]
    orphan_h3_tags: List[str]  # h2の前に出現するh3タグ
    total_h1: int
    total_h2: int
    total_h3: int

class ErrorData(BaseModel):
    error: str

class HeadingResponse(BaseModel):
    results: Dict[str, Union[HeadingData, ErrorData]]
    total_processed: int
    total_success: int
    total_errors: int

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """
    APIキーを検証する関数
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return x_api_key

@app.get("/")
async def root():
    """
    APIのルートエンドポイント（認証不要）
    """
    return {
        "message": "HTML見出し抽出API",
        "description": "POST /extract-headings で複数URLから<h1>、<h2>、<h3>タグを階層構造で一括抽出できます",
        "authentication": "X-API-Key ヘッダーが必要です",
        "docs": "/docs"
    }

@app.post("/extract-headings", response_model=HeadingResponse)
async def extract_headings(
    request: URLListRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    指定されたURLリストから<h1>、<h2>、<h3>タグを階層構造で一括抽出する
    
    Args:
        request: URLリストを含むリクエストボディ
        api_key: APIキー（X-API-Keyヘッダーで指定）
        
    Returns:
        HeadingResponse: 各URLの抽出結果とサマリー情報
    """
    results = {}
    success_count = 0
    error_count = 0
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }
    
    for url in request.urls:
        url_str = str(url)
        try:
            logger.info(f"URLからHTMLを取得中: {url_str}")
            
            # キャッシュバスティングパラメータを追加
            cache_buster = int(time.time() * 1000)  # ミリ秒のタイムスタンプ
            separator = '&' if '?' in url_str else '?'
            cache_busted_url = f"{url_str}{separator}_cb={cache_buster}"
            
            response = requests.get(cache_busted_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # HTMLをパース
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # h1タグを抽出
            h1_tags = [tag.get_text(strip=True) for tag in soup.find_all('h1')]
            
            # 階層構造を構築するため、すべての見出しタグを順序通りに取得
            all_headings = soup.find_all(['h2', 'h3'])
            
            sections = []
            orphan_h3_tags = []
            current_h2 = None
            current_h3_list = []
            total_h2 = 0
            total_h3 = 0
            
            for heading in all_headings:
                heading_text = heading.get_text(strip=True)
                
                if heading.name == 'h2':
                    # 前のh2セクションを保存
                    if current_h2 is not None:
                        sections.append(H2Section(
                            h2_title=current_h2,
                            h3_tags=current_h3_list
                        ))
                    
                    # 新しいh2セクションを開始
                    current_h2 = heading_text
                    current_h3_list = []
                    total_h2 += 1
                    
                elif heading.name == 'h3':
                    total_h3 += 1
                    if current_h2 is not None:
                        # 現在のh2セクションにh3を追加
                        current_h3_list.append(heading_text)
                    else:
                        # h2の前に出現するh3（孤立したh3）
                        orphan_h3_tags.append(heading_text)
            
            # 最後のh2セクションを保存
            if current_h2 is not None:
                sections.append(H2Section(
                    h2_title=current_h2,
                    h3_tags=current_h3_list
                ))
            
            logger.info(f"抽出完了 - {url_str}: H1: {len(h1_tags)}個, H2: {total_h2}個, H3: {total_h3}個")
            
            results[url_str] = HeadingData(
                h1_tags=h1_tags,
                sections=sections,
                orphan_h3_tags=orphan_h3_tags,
                total_h1=len(h1_tags),
                total_h2=total_h2,
                total_h3=total_h3
            )
            success_count += 1
            
        except requests.exceptions.RequestException as e:
            error_msg = f"HTTPリクエストエラー: {str(e)}"
            logger.error(f"{url_str} - {error_msg}")
            results[url_str] = ErrorData(error=error_msg)
            error_count += 1
            
        except Exception as e:
            error_msg = f"処理中にエラーが発生しました: {str(e)}"
            logger.error(f"{url_str} - {error_msg}")
            results[url_str] = ErrorData(error=error_msg)
            error_count += 1
    
    return HeadingResponse(
        results=results,
        total_processed=len(request.urls),
        total_success=success_count,
        total_errors=error_count
    )

@app.get("/health")
async def health_check():
    """
    ヘルスチェックエンドポイント（認証不要）
    """
    return {"status": "healthy", "message": "APIは正常に動作しています"}

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Cloud Runの場合はPORT環境変数を使用、ローカルの場合は8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)