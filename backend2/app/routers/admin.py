from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from app.database import get_db
from app.models import Order, OrderItem, Product, User, OrderStatus
from app import auth
from datetime import datetime, date, timedelta
from typing import List, Optional

router = APIRouter(
    prefix="/admin/dashboard", 
    tags=["Admin Dashboard"],
    dependencies=[Depends(auth.check_admin)]
)

@router.get("/kpi")
def get_kpi(db: Session = Depends(get_db)):
    today = date.today()
    
    # Doanh thu hôm nay (Chỉ tính DELIVERED/COMPLETED)
    # BA nói status = 'DELIVERED', trong model OrderStatus có 'completed'.
    # Tôi sẽ coi 'completed' tương đương 'DELIVERED'.
    revenue_today = db.query(func.sum(Order.total_price))\
        .filter(and_(
            Order.status == OrderStatus.completed,
            func.date(Order.created_at) == today
        )).scalar() or 0
    
    # Số đơn hàng hôm nay
    orders_today = db.query(func.count(Order.id))\
        .filter(func.date(Order.created_at) == today).scalar() or 0
    
    # Số user mới hôm nay
    new_users_today = db.query(func.count(User.id))\
        .filter(func.date(User.created_at) == today).scalar() or 0
    
    # Conversion Rate (Mock visits vì chưa có GA)
    # Visits thường lấy từ tracking, ở đây tôi mock số ngẫu nhiên hoặc từ logic nào đó
    mock_visits = 1000 # Giả định 1000 visits
    conversion_rate = (orders_today / mock_visits * 100) if mock_visits > 0 else 0
    
    return {
        "revenue_today": float(revenue_today),
        "orders_today": orders_today,
        "new_users_today": new_users_today,
        "conversion_rate": round(conversion_rate, 2),
        "visits": mock_visits
    }

@router.get("/revenue")
def get_revenue_chart(
    range: str = Query("7days", enum=["today", "7days", "30days", "month", "year"]),
    db: Session = Depends(get_db)
):
    # Logic theo BA: Xem theo ngày / tuần / tháng
    today = date.today()
    if range == "today":
        start_date = today
    elif range == "7days":
        start_date = today - timedelta(days=7)
    elif range == "30days":
        start_date = today - timedelta(days=30)
    else:
        start_date = today - timedelta(days=30) # Default
        
    revenue_data = db.query(
        func.date(Order.created_at).label("date"),
        func.sum(Order.total_price).label("revenue")
    ).filter(and_(
        Order.status == OrderStatus.completed,
        Order.created_at >= start_date
    )).group_by(func.date(Order.created_at))\
    .order_by(func.date(Order.created_at)).all()
    
    return [{"date": str(d.date), "revenue": float(d.revenue)} for d in revenue_data]

@router.get("/orders/recent")
def get_recent_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).order_by(desc(Order.created_at)).limit(10).all()
    return [{
        "id": o.id,
        "user_id": o.user_id,
        "total_amount": float(o.total_price),
        "status": o.status.value,
        "created_at": o.created_at
    } for o in orders]

@router.get("/products/top")
def get_top_products(db: Session = Depends(get_db)):
    # Senior fix: Sử dụng JOIN để lấy toàn bộ dữ liệu trong 1 query duy nhất, tránh lỗi N+1
    top_selling = db.query(
        Product,
        func.sum(OrderItem.quantity).label("total_sold")
    ).join(OrderItem, Product.id == OrderItem.product_id)\
    .join(Order, OrderItem.order_id == Order.id)\
    .filter(Order.status == OrderStatus.completed)\
    .group_by(Product.id)\
    .order_by(desc("total_sold"))\
    .limit(10).all()
    
    return [{
        "product_id": p.id,
        "name": p.name,
        "total_sold": int(total_sold),
        "price": float(p.price)
    } for p, total_sold in top_selling]

@router.get("/inventory/low-stock")
def get_low_stock(db: Session = Depends(get_db)):
    # BA rule: quantity < 10
    low_stock_products = db.query(Product).filter(Product.stock < 10).all()
    return [{
        "product_id": p.id,
        "name": p.name,
        "quantity": p.stock
    } for p in low_stock_products]

@router.get("/orders/status")
def get_order_status_distribution(db: Session = Depends(get_db)):
    status_counts = db.query(
        Order.status,
        func.count(Order.id).label("total")
    ).group_by(Order.status).all()
    
    return {
        (s.status.value if s.status else "unknown"): s.total 
        for s in status_counts
    }

@router.get("/inventory/forecast")
def get_inventory_forecast(db: Session = Depends(get_db)):
    # Senior Logic: Dự báo ngày còn lại dựa trên tốc độ bán 30 ngày gần nhất
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # Tính tổng số lượng bán của mỗi SP trong 30 ngày qua
    sales_velocity = db.query(
        OrderItem.product_id,
        func.sum(OrderItem.quantity).label("total_sold")
    ).join(Order).filter(and_(
        Order.status == OrderStatus.completed,
        Order.created_at >= thirty_days_ago
    )).group_by(OrderItem.product_id).all()
    
    velocity_map = {item.product_id: float(item.total_sold) / 30 for item in sales_velocity}
    
    products = db.query(Product).filter(Product.is_active == True).all()
    forecast = []
    
    for p in products:
        daily_velocity = velocity_map.get(p.id, 0)
        days_left = float('inf') if daily_velocity == 0 else p.stock / daily_velocity
        
        if days_left < 15 or p.stock < 10: # Chỉ hiển thị các SP sắp hết hoặc rủi ro
            forecast.append({
                "product_id": p.id,
                "name": p.name,
                "current_stock": p.stock,
                "daily_velocity": round(daily_velocity, 2),
                "days_left": round(days_left, 1) if days_left != float('inf') else "N/A",
                "status": "Critical" if days_left < 3 else ("Warning" if days_left < 7 else "Stable")
            })
            
    return sorted(forecast, key=lambda x: x['days_left'] if isinstance(x['days_left'], (int, float)) else 999)

@router.get("/basket-analysis")
def get_basket_analysis(db: Session = Depends(get_db)):
    # Senior Logic: Phân tích cộng hưởng (Sản phẩm thường mua cùng nhau)
    # Tương đương thuật toán Market Basket Analysis cơ bản
    from sqlalchemy.orm import aliased
    OI1 = aliased(OrderItem)
    OI2 = aliased(OrderItem)
    
    pairs = db.query(
        OI1.product_id.label("p1"),
        OI2.product_id.label("p2"),
        func.count("*").label("frequency")
    ).join(OI2, and_(
        OI1.order_id == OI2.order_id,
        OI1.product_id < OI2.product_id
    )).group_by("p1", "p2")\
    .order_by(desc("frequency"))\
    .limit(10).all()
    
    result = []
    for p1_id, p2_id, freq in pairs:
        prod1 = db.query(Product).filter(Product.id == p1_id).first()
        prod2 = db.query(Product).filter(Product.id == p2_id).first()
        if prod1 and prod2:
            result.append({
                "pair": [prod1.name, prod2.name],
                "frequency": freq,
                "suggestion": f"Nên tạo Combo {prod1.name} + {prod2.name} để tăng doanh số."
            })
    return result

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Tổng doanh thu & đơn hàng (Toàn thời gian)
    total_stats = db.query(
        func.sum(Order.total_price).label("revenue"),
        func.count(Order.id).label("count")
    ).filter(Order.status == OrderStatus.completed).first()
    
    total_revenue = float(total_stats.revenue or 0)
    total_orders = total_stats.count or 0
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Doanh thu theo tháng (6 tháng gần nhất)
    monthly_stats = db.query(
        func.extract('month', Order.created_at).label("month"),
        func.sum(Order.total_price).label("revenue"),
        func.count(Order.id).label("count")
    ).filter(Order.status == OrderStatus.completed)\
    .group_by("month").all()
    
    # Phân bổ trạng thái
    status_counts = db.query(
        Order.status,
        func.count(Order.id).label("total")
    ).group_by(Order.status).all()
    
    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "avg_order_value": round(avg_order_value, 2),
        "monthly": [{"month": int(m.month), "revenue": float(m.revenue), "count": m.count} for m in monthly_stats],
        "status_breakdown": { (s.status.value if s.status else "unknown"): s.total for s in status_counts }
    }

@router.get("/active-carts")
def get_active_carts(db: Session = Depends(get_db)):
    # Senior Logic: Lấy các giỏ hàng có sản phẩm
    from app.models import Cart, CartItem, User, Product
    
    active_carts = db.query(Cart).join(CartItem).group_by(Cart.id).all()
    
    result = []
    for cart in active_carts:
        user = db.query(User).filter(User.id == cart.user_id).first()
        items = db.query(CartItem, Product).join(Product).filter(CartItem.cart_id == cart.id).all()
        
        cart_data = {
            "cart_id": cart.id,
            "user": {
                "email": user.email if user else "Guest",
                "full_name": user.full_name if user else "Unknown"
            },
            "created_at": cart.created_at,
            "items": [
                {
                    "product_name": p.name,
                    "quantity": ci.quantity,
                    "price": float(ci.price or p.price)
                } for ci, p in items
            ],
            "total_value": sum(float(ci.price or p.price) * ci.quantity for ci, p in items)
        }
        result.append(cart_data)
        
    return result
