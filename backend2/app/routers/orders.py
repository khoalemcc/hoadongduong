from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas, auth
from app.database import get_db

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    order.user_id = current_user.id
    return crud.create_order(db=db, order=order)

@router.get("/", response_model=List[schemas.Order])
def read_all_orders(skip: int = 0, limit: int = 200, db: Session = Depends(get_db), admin: models.User = Depends(auth.check_admin)):
    return db.query(models.Order).filter(models.Order.is_deleted == False).offset(skip).limit(limit).all()

@router.get("/stats")
def get_order_stats(db: Session = Depends(get_db), admin: models.User = Depends(auth.check_admin)):
    from sqlalchemy import func, extract
    orders = db.query(models.Order).filter(models.Order.is_deleted == False).all()
    total_revenue = sum(float(o.total_price or 0) for o in orders)
    total_orders = len(orders)
    
    # Monthly revenue breakdown
    monthly = db.query(
        extract('month', models.Order.created_at).label('month'),
        func.sum(models.Order.total_price).label('revenue'),
        func.count(models.Order.id).label('count')
    ).filter(models.Order.is_deleted == False).group_by(extract('month', models.Order.created_at)).all()
    
    monthly_data = [{"month": int(m.month), "revenue": float(m.revenue or 0), "count": m.count} for m in monthly]
    
    # Status breakdown
    status_counts = db.query(
        models.Order.status,
        func.count(models.Order.id).label('count')
    ).filter(models.Order.is_deleted == False).group_by(models.Order.status).all()
    
    status_data = {str(s.status.value) if hasattr(s.status, 'value') else str(s.status): s.count for s in status_counts}
    
    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "avg_order_value": total_revenue / total_orders if total_orders > 0 else 0,
        "monthly": monthly_data,
        "status_breakdown": status_data
    }

@router.get("/my-orders", response_model=List[schemas.Order])
def read_my_orders(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    orders = db.query(models.Order).filter(models.Order.user_id == current_user.id, models.Order.is_deleted == False).all()
    return orders

@router.get("/user/{user_id}", response_model=List[schemas.Order])
def read_user_orders(user_id: int, db: Session = Depends(get_db), admin: models.User = Depends(auth.check_admin)):
    return db.query(models.Order).filter(models.Order.user_id == user_id, models.Order.is_deleted == False).all()

@router.get("/{order_id}", response_model=schemas.Order)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_order = db.query(models.Order).filter(models.Order.id == order_id, models.Order.is_deleted == False).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    auth.require_self_or_admin(db_order.user_id, current_user)
    return db_order

@router.patch("/{order_id}/status")
def update_order_status(order_id: int, status: models.OrderStatus, db: Session = Depends(get_db), admin: models.User = Depends(auth.check_admin)):
    db_order = crud.update_order(db, order_id=order_id, order_update={"status": status})
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.patch("/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order_update: dict, db: Session = Depends(get_db), admin: models.User = Depends(auth.check_admin)):
    db_order = crud.update_order(db, order_id=order_id, order_update=order_update)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db), admin: models.User = Depends(auth.check_admin)):
    success = crud.delete_order(db, order_id=order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted successfully"}
