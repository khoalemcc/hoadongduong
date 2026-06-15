# backend2/scripts/scrape_products_from_cocayhoala.py
"""Scrape product data from https://cocayhoala.vn
Creates CSV file `products_from_cocayhoala.csv` in the data root.
The data root is taken from env var DATA_ROOT (defaults to backend2/data).
"""

import os
import csv
import time
import random
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_URL = "https://cocayhoala.vn"
PRODUCTS_PER_PAGE = 30  # cocayhoala pagination size (adjust if needed)

# Determine data directory (may be on D: drive)
DATA_ROOT = os.getenv("DATA_ROOT", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data")))
os.makedirs(DATA_ROOT, exist_ok=True)
OUTPUT_CSV = os.path.join(DATA_ROOT, "products_from_cocayhoala.csv")

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def slug_from_url(url: str) -> str:
    return url.rstrip("/").split("/")[-1]

def fetch_product_detail(product_url: str) -> dict:
    soup = get_soup(product_url)
    # Title
    title_tag = soup.select_one('h1') or soup.select_one('.product-title')
    title = title_tag.get_text(strip=True) if title_tag else ""
    # Description (first paragraph)
    desc_tag = soup.select_one('.description') or soup.select_one('.product-description p')
    description = desc_tag.get_text(strip=True) if desc_tag else ""
    # Price – look for element with class containing price
    price_tag = soup.select_one('.price') or soup.select_one('.product-price')
    price_text = price_tag.get_text(strip=True) if price_tag else "0"
    # Extract numeric part (remove currency symbols, commas)
    price = "".join(ch for ch in price_text if (ch.isdigit() or ch == "."))
    price = float(price) if price else 0.0
    # Image – first img inside gallery or main image container
    img_tag = soup.select_one('.product-gallery img') or soup.select_one('.product-image img')
    img_url = ""
    if img_tag and img_tag.get('src'):
        src = img_tag['src']
        img_url = src if src.startswith('http') else urljoin(BASE_URL, src)
    # Build record
    return {
        "sku": f"COCAY-{random.randint(10000, 99999)}",
        "name": title,
        "slug": slug_from_url(product_url),
        "description": description,
        "price": price,
        "image_url": img_url,
    }

# ---------------------------------------------------------------------------
# Main scraping logic
# ---------------------------------------------------------------------------

def main():
    all_records = []
    page = 1
    while True:
        list_url = f"{BASE_URL}/collections/all?page={page}"
        try:
            soup = get_soup(list_url)
        except Exception as e:
            print(f"[WARN] Could not fetch page {page}: {e}")
            break
        product_links = [a['href'] for a in soup.select('a.product-card-link') if a.get('href')]
        if not product_links:
            # No more products
            break
        print(f"[INFO] Scraping page {page} – found {len(product_links)} products")
        for rel in product_links:
            prod_url = urljoin(BASE_URL, rel)
            try:
                rec = fetch_product_detail(prod_url)
                all_records.append(rec)
                # Be gentle on the server
                time.sleep(random.uniform(0.5, 1.2))
            except Exception as exc:
                print(f"[WARN] Failed to scrape {prod_url}: {exc}")
        page += 1
        # Optional stop after a reasonable number of pages to avoid endless loops
        if page > 20:
            break
    # Write CSV
    if not all_records:
        print("[WARN] No records scraped – exiting")
        return
    fieldnames = ["sku", "name", "slug", "description", "price", "image_url"]
    with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_records)
    print(f"[DONE] Scraped {len(all_records)} products → {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
