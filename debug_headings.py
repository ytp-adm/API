import requests
from bs4 import BeautifulSoup
import time

def debug_headings(url):
    """指定されたURLのh1, h2, h3タグを詳細に確認する"""
    
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
    
    # キャッシュバスティングパラメータを追加
    cache_buster = int(time.time() * 1000)
    separator = '&' if '?' in url else '?'
    cache_busted_url = f"{url}{separator}_cb={cache_buster}"
    
    response = requests.get(cache_busted_url, headers=headers, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print(f"URL: {url}")
    print("=" * 80)
    
    # H1タグを確認
    h1_tags = soup.find_all('h1')
    print(f"\nH1タグ ({len(h1_tags)}個):")
    for i, tag in enumerate(h1_tags, 1):
        print(f"  {i}. '{tag.get_text(strip=True)}'")
    
    # H2タグを確認
    h2_tags = soup.find_all('h2')
    print(f"\nH2タグ ({len(h2_tags)}個):")
    for i, tag in enumerate(h2_tags, 1):
        print(f"  {i}. '{tag.get_text(strip=True)}'")
    
    # H3タグを確認
    h3_tags = soup.find_all('h3')
    print(f"\nH3タグ ({len(h3_tags)}個):")
    for i, tag in enumerate(h3_tags, 1):
        print(f"  {i}. '{tag.get_text(strip=True)}'")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    url = "https://www.sharing-tech.co.jp/sentei/momi-sentei/"
    debug_headings(url)