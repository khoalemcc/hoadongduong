import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

# 1. Cấu hình Cloudinary trực tiếp (Inline Configuration)
cloudinary.config(
    cloud_name=os.environ["CLOUDINARY_CLOUD_NAME"],
    api_key=os.environ["CLOUDINARY_API_KEY"],
    api_secret=os.environ["CLOUDINARY_API_SECRET"],
    secure=True
)

def run_cloudinary_demo():
    print("--- STEP 2: Uploading image to Cloudinary ---")
    # Tải lên một ảnh mẫu từ demo domain của Cloudinary
    sample_image_url = "https://res.cloudinary.com/demo/image/upload/cld-sample.jpg"
    
    upload_result = cloudinary.uploader.upload(
        sample_image_url,
        public_id="hoadongduong_demo_product"
    )
    
    secure_url = upload_result.get("secure_url")
    public_id = upload_result.get("public_id")
    print(f"Secure URL: {secure_url}")
    print(f"Public ID: {public_id}")
    
    print("\n--- STEP 3: Getting image details ---")
    # Lấy thông tin metadata của ảnh vừa upload
    image_details = cloudinary.api.resource(public_id)
    width = image_details.get("width")
    height = image_details.get("height")
    format_type = image_details.get("format")
    bytes_size = image_details.get("bytes")
    
    print(f"Width: {width}px")
    print(f"Height: {height}px")
    print(f"Format: {format_type}")
    print(f"File Size: {bytes_size} bytes")
    
    print("\n--- STEP 4: Transforming the image ---")
    # Biến đổi ảnh để tự động tối ưu hóa định dạng và chất lượng
    # f_auto: Tự động chọn định dạng ảnh tối ưu nhất cho trình duyệt (VD: WebP, AVIF)
    # q_auto: Tự động nén dung lượng ảnh mà không làm suy giảm chất lượng hiển thị trực quan
    transformed_url = cloudinary.CloudinaryImage(public_id).build_url(
        fetch_format="auto",
        quality="auto"
    )
    
    print("Done! Click link below to see optimized version of the image. Check the size and the format.")
    print(f"Transformed URL: {transformed_url}")

if __name__ == "__main__":
    run_cloudinary_demo()
