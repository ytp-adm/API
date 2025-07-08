from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from typing import List, Dict, Union, Optional
import logging
import time
import os
import tempfile
import shutil

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# APIキーの設定（環境変数から取得、デフォルトは簡単なキー）
API_KEY = os.environ.get("API_KEY", "dify-seo-api-key-2025")

app = FastAPI(
    title="HTML見出し抽出API (Selenium版)",
    description="指定されたURLリストから<h1>、<h2>、<h3>タグを階層構造で一括抽出するAPI（Selenium + headless Chrome使用、JavaScript動的レンダリング対応、画像altタグフォールバック機能付き）",
    version="2.1.0"
)

# CORS設定を追加（Difyからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なドメインに制限
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLListRequest(BaseModel):
    urls: List[HttpUrl]

class H2Section(BaseModel):
    h2_text: str
    h3_tags: List[str]

class HeadingData(BaseModel):
    h1: List[str]
    h2_sections: List[H2Section]

class URLResult(BaseModel):
    url: str
    status: str  # "success" or "error"
    headings: Optional[HeadingData] = None
    error: Optional[str] = None

class HeadingResponse(BaseModel):
    processing_time_seconds: float
    results: List[URLResult]

def create_webdriver():
    """
    Seleniumのheadless Chrome WebDriverを作成する
    """
    chrome_options = Options()
    
    # Cloud Run環境での設定
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-javascript-harmony-shipping")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-field-trial-config")
    chrome_options.add_argument("--disable-back-forward-cache")
    chrome_options.add_argument("--disable-ipc-flooding-protection")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    
    # User-Agentを設定してBot検出を回避
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # メモリ使用量を制限
    chrome_options.add_argument("--memory-pressure-off")
    chrome_options.add_argument("--max_old_space_size=4096")
    
    try:
        # Chrome バイナリの場所を設定
        if os.path.exists("/usr/bin/google-chrome"):
            chrome_options.binary_location = "/usr/bin/google-chrome"
        
        # WebDriverManager を使用して適切なChromeDriverを自動取得
        # Cloud Run環境でも動作するように設定
        service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        
        return driver
        
    except Exception as e:
        logger.error(f"WebDriver作成エラー: {str(e)}")
        raise

def extract_text_with_alt_fallback(tag):
    """
    見出しタグからテキストを抽出し、空の場合は画像のaltタグから取得する
    
    Args:
        tag: BeautifulSoupの見出しタグ要素
        
    Returns:
        str: 抽出されたテキスト（空の場合はNone）
    """
    # まずは通常のテキストを取得
    text = tag.get_text(strip=True)
    
    if text:
        return text
    
    # テキストが空の場合、画像のaltタグを確認
    images = tag.find_all('img')
    alt_texts = []
    
    for img in images:
        alt = img.get('alt', '').strip()
        if alt:
            alt_texts.append(alt)
    
    # altタグが見つかった場合は結合して返す
    if alt_texts:
        combined_alt = ' '.join(alt_texts)
        logger.info(f"見出しタグのテキストが空のため、altタグから取得: {combined_alt}")
        return combined_alt
    
    return None

def extract_headings_with_selenium(url: str) -> tuple:
    """
    SeleniumでURLからヘッダータグを抽出する（画像altタグ対応）
    
    Args:
        url: 抽出対象のURL
        
    Returns:
        tuple: (h1_tags, h2_sections, error_message)
    """
    driver = None
    try:
        driver = create_webdriver()
        
        logger.info(f"Seleniumでページを読み込み中: {url}")
        driver.get(url)
        
        # JavaScriptの実行完了を待機
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        # 追加の待機時間（動的コンテンツの読み込み）
        time.sleep(3)
        
        # ページソースを取得してBeautifulSoupでパース
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # h1タグを抽出（テキストまたはaltタグから）
        h1_tags = []
        for tag in soup.find_all('h1'):
            text = extract_text_with_alt_fallback(tag)
            if text:  # テキストまたはaltタグが存在する場合
                h1_tags.append(text)
        
        # 階層構造を構築するため、すべての見出しタグを順序通りに取得
        all_headings = soup.find_all(['h2', 'h3'])
        
        h2_sections = []
        current_h2 = None
        current_h3_list = []
        
        for heading in all_headings:
            heading_text = extract_text_with_alt_fallback(heading)
            
            # テキストもaltタグも空の場合はスキップ
            if not heading_text:
                continue
                
            if heading.name == 'h2':
                # 前のh2セクションを保存
                if current_h2 is not None:
                    h2_sections.append(H2Section(
                        h2_text=current_h2,
                        h3_tags=current_h3_list
                    ))
                
                # 新しいh2セクションを開始
                current_h2 = heading_text
                current_h3_list = []
                
            elif heading.name == 'h3':
                if current_h2 is not None:
                    # 現在のh2セクションにh3を追加
                    current_h3_list.append(heading_text)
        
        # 最後のh2セクションを保存
        if current_h2 is not None:
            h2_sections.append(H2Section(
                h2_text=current_h2,
                h3_tags=current_h3_list
            ))
        
        logger.info(f"抽出完了 - {url}: H1: {len(h1_tags)}個, H2セクション: {len(h2_sections)}個")
        
        return h1_tags, h2_sections, None
        
    except TimeoutException:
        error_msg = "ページの読み込みがタイムアウトしました"
        logger.error(f"{url} - {error_msg}")
        return [], [], error_msg
        
    except WebDriverException as e:
        error_msg = f"WebDriverエラー: {str(e)}"
        logger.error(f"{url} - {error_msg}")
        return [], [], error_msg
        
    except Exception as e:
        error_msg = f"処理エラー: {str(e)}"
        logger.error(f"{url} - {error_msg}")
        return [], [], error_msg
        
    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                logger.warning(f"WebDriver終了時のエラー: {str(e)}")

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """
    APIキーを検証する関数（オプション）
    """
    if x_api_key and x_api_key != API_KEY:
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
        "message": "HTML見出し抽出API (Selenium版)",
        "description": "POST /extract-headings で複数URLから<h1>、<h2>、<h3>タグを階層構造で一括抽出できます（JavaScript動的レンダリング対応）",
        "features": [
            "Selenium + headless Chrome使用",
            "JavaScript動的レンダリング対応",
            "Bot対策サイト対応",
            "空タグ・非標準マークアップ対応"
        ],
        "authentication": "X-API-Key ヘッダー推奨（オプション）",
        "docs": "/docs",
        "version": "2.0.0"
    }

@app.get("/health")
async def health_check():
    """
    ヘルスチェックエンドポイント（認証不要）
    """
    return {"status": "healthy", "message": "APIは正常に動作しています"}

@app.post("/extract-headings", response_model=HeadingResponse)
async def extract_headings(
    request: URLListRequest,
    x_api_key: Optional[str] = Header(None)
):
    """
    指定されたURLリストから<h1>、<h2>、<h3>タグを階層構造で一括抽出する（Selenium使用）
    
    Args:
        request: URLリストを含むリクエストボディ
        x_api_key: APIキー（X-API-Keyヘッダーで指定、オプション）
        
    Returns:
        HeadingResponse: 各URLの抽出結果とサマリー情報
    """
    # APIキーの検証（提供された場合のみ）
    if x_api_key and x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    start_time = time.time()
    results = []
    
    for url in request.urls:
        url_str = str(url)
        try:
            # Seleniumでヘッダータグを抽出
            h1_tags, h2_sections, error_msg = extract_headings_with_selenium(url_str)
            
            if error_msg:
                results.append(URLResult(
                    url=url_str,
                    status="error",
                    error=error_msg
                ))
            else:
                results.append(URLResult(
                    url=url_str,
                    status="success",
                    headings=HeadingData(
                        h1=h1_tags,
                        h2_sections=h2_sections
                    )
                ))
                
        except Exception as e:
            error_msg = f"予期しないエラー: {str(e)}"
            logger.error(f"{url_str} - {error_msg}")
            results.append(URLResult(
                url=url_str,
                status="error",
                error=error_msg
            ))
    
    processing_time = time.time() - start_time
    
    return HeadingResponse(
        processing_time_seconds=round(processing_time, 2),
        results=results
    )

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Cloud Runの場合はPORT環境変数を使用、ローカルの場合は8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)