import os
import csv
import time
import random
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://cocayhoala.vn"
# Target collection for all products (Vietnamese slug)
COLLECTION_PATH = "/collections/tat-ca-san-pham"
COLLECTION_URL = urljoin(BASE_URL, COLLECTION_PATH)

# Data directory (use DATA_ROOT env var if set, else default)
DATA_ROOT = os.getenv('DATA_ROOT') or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
os.makedirs(DATA_ROOT, exist_ok=True)
OUTPUT_CSV = os.path.join(DATA_ROOT, 'products_from_cocayhoala.csv')

def get_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, 'html.parser')

def slug_from_url(url: str) -> str:
    return url.rstrip('/').split('/')[-1]

def fetch_product_detail(product_url: str) -> dict:
    soup = get_soup(product_url)
    # Title
    title_tag = soup.select_one('h1') or soup.select_one('.product-title')
    title = title_tag.get_text(strip=True) if title_tag else ''
    # Description
    desc_tag = soup.select_one('.description') or soup.select_one('.product-description p')
    description = desc_tag.get_text(strip=True) if desc_tag else ''
    # Price
    price_tag = soup.select_one('.price') or soup.select_one('.product-price')
    price_text = price_tag.get_text(strip=True) if price_tag else '0'
    price_digits = ''.join(ch for ch in price_text if ch.isdigit() or ch == '.')
    price = float(price_digits) if price_digits else 0.0
    # Image URL
    img_tag = soup.select_one('.product-gallery img') or soup.select_one('.product-image img')
    img_url = ''
    if img_tag and img_tag.get('src'):
        src = img_tag['src']
        img_url = src if src.startswith('http') else urljoin(BASE_URL, src)
    return {
        'sku': f"COCAY-{random.randint(10000, 99999)}",
        'name': title,
        'slug': slug_from_url(product_url),
        'description': description,
        'price': price,
        'image_url': img_url,
    }

def main():
    session = requests.Session()
    page = 1
    records = []
    while True:
        list_url = f"{COLLECTION_URL}?page={page}"
        try:
            soup = get_soup(list_url)
        except Exception as e:
            print(f"[WARN] Failed to fetch page {page}: {e}")
            break
        product_links = [a['href'] for a in soup.select('a.product-card-link') if a.get('href')]
        if not product_links:
            print('[INFO] No more product links found, ending.')
            break
        print(f"[INFO] Page {page} – found {len(product_links)} products")
        for rel in product_links:
            prod_url = urljoin(BASE_URL, rel)
            try:
                rec = fetch_product_detail(prod_url)
                records.append(rec)
                time.sleep(random.uniform(0.5, 1.0))
            except Exception as exc:
                print(f"[WARN] Error scraping {prod_url}: {exc}")
        page += 1
        if page > 30:
            print('[INFO] Reached page limit, stopping.')
            break
    if not records:
        print('[WARN] No records scraped.')
        return
    fieldnames = ['sku', 'name', 'slug', 'description', 'price', 'image_url']
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"[DONE] Scraped {len(records)} products → {OUTPUT_CSV}")

if __name__ == '__main__':
    main()
