import os
import requests
import re
from bs4 import BeautifulSoup
import cloudinary
import cloudinary.uploader
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

# 1. Cấu hình Cloudinary
cloudinary.config(
    cloud_name="dajfab5oi",
    api_key="792567117298111",
    api_secret="r84ftdpY9D853t4dheIiZhWZQgA",
    secure=True
)

def scrape_and_sync():
    url = "https://cocayhoala.vn/collections/tat-ca-san-pham"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Connecting to target website: {url} ...")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch website, status: {response.status_code}")
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Phân tích các khối sản phẩm (thông thường trên nền tảng Haravan/Shopify)
    products_scraped = []
    
    # Tìm kiếm các thẻ div chứa sản phẩm hoặc thẻ img của sản phẩm
    # Shopify/Haravan thường dùng các class dạng product-loop-lock, product-block, product-item, vv.
    # Hãy tìm tất cả các thẻ hình ảnh sản phẩm
    img_tags = soup.find_all("img")
    print(f"Found {len(img_tags)} total images on page.")
    
    count = 0
    db = SessionLocal()
    try:
        # Lấy danh sách sản phẩm hiện có trong db để gán ảnh thật cho đẹp
        db_products = db.query(models.Product).filter(models.Product.is_deleted == False).all()
        if not db_products:
            print("No active products in database to link images to!")
            return
            
        print(f"Found {len(db_products)} products in local database to update images.")
        
        for img in img_tags:
            src = img.get("data-src") or img.get("src")
            if not src:
                continue
                
            # Đảm bảo là ảnh sản phẩm từ cdn haravan/shopify
            if "product" in src or "products" in src or "thumb" in src:
                # Chuẩn hóa URL ảnh
                if src.startswith("//"):
                    img_url = "https:" + src
                elif src.startswith("/"):
                    img_url = "https://cocayhoala.vn" + src
                else:
                    img_url = src
                
                # Bỏ bớt tham số resize của haravan để lấy ảnh gốc chất lượng cao
                img_url = re.sub(r'_[0-9]+x[0-9]+', '', img_url)
                img_url = img_url.split("?")[0]
                
                # Bỏ qua các định dạng gif
                if img_url.endswith(".gif") or img_url in [p[1] for p in products_scraped]:
                    continue
                
                alt = img.get("alt", "").strip() or f"Botanical Product {count + 1}"
                products_scraped.append((alt, img_url))
                
                print(f"\nScraped product image ID {count+1} -> URL: {img_url}")
                
                # Upload lên Cloudinary
                print(f"Uploading to Cloudinary...")
                upload_res = cloudinary.uploader.upload(img_url, folder="hoadongduong")
                public_id = upload_res.get("public_id")
                
                # Tạo URL tối ưu tự động
                optimized_url = cloudinary.CloudinaryImage(public_id).build_url(
                    fetch_format="auto",
                    quality="auto"
                )
                print(f"Cloudinary Optimized URL: {optimized_url}")
                
                # Cập nhật vào DB cho các sản phẩm cục bộ
                if count < len(db_products):
                    prod = db_products[count]
                    
                    # Xóa ảnh cũ
                    db.query(models.ProductImage).filter(models.ProductImage.product_id == prod.id).delete()
                    
                    # Thêm ảnh Cloudinary mới
                    new_img = models.ProductImage(
                        product_id=prod.id,
                        image_url=optimized_url,
                        is_primary=True
                    )
                    db.add(new_img)
                    
                    # Cập nhật luôn tên sản phẩm theo ảnh thật cho đẹp
                    # Tách tên sản phẩm sạch
                    clean_name = re.sub(r' - Cỏ Cây Hoa Lá.*', '', alt)
                    clean_name = re.sub(r' chính hãng.*', '', clean_name)
                    if clean_name:
                        prod.name = clean_name
                    
                    print(f"Updated local product ID {prod.id} with Cloudinary image!")
                    count += 1
                else:
                    break
                    
        db.commit()
        print(f"\nSuccessfully synchronized {count} product images from cocayhoala.vn to your Cloudinary account and local database!")
        
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    scrape_and_sync()
