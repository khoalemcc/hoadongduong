from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas, auth
from app.database import get_db

router = APIRouter(
    prefix="/admin",
    tags=["Admin Operations"],
    dependencies=[Depends(auth.check_admin)]
)

# Brands
@router.post("/brands", response_model=schemas.Brand)
def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
    return crud.create_brand(db, brand)

@router.get("/brands", response_model=List[schemas.Brand])
def list_brands(db: Session = Depends(get_db)):
    return db.query(models.Brand).filter(models.Brand.is_deleted == False).all()

# Banners
@router.post("/banners", response_model=schemas.Banner)
def create_banner(banner: schemas.BannerBase, db: Session = Depends(get_db)):
    return crud.create_banner(db, banner)

@router.get("/banners", response_model=List[schemas.Banner])
def list_banners(db: Session = Depends(get_db)):
    return db.query(models.Banner).filter(models.Banner.is_deleted == False).all()

# Inventory Logs
@router.get("/inventory/logs", response_model=List[schemas.InventoryLog])
def list_inventory_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.InventoryLog).filter(models.InventoryLog.is_deleted == False).order_by(models.InventoryLog.created_at.desc()).offset(skip).limit(limit).all()

# Audit Logs
@router.get("/audit/logs", response_model=List[schemas.AuditLog])
def list_audit_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.AuditLog).filter(models.AuditLog.is_deleted == False).order_by(models.AuditLog.created_at.desc()).offset(skip).limit(limit).all()

# Shipments
@router.post("/shipments", response_model=schemas.Shipment)
def create_shipment(shipment: schemas.ShipmentBase, db: Session = Depends(get_db)):
    db_shipment = models.Shipment(**shipment.model_dump())
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment

@router.get("/shipments", response_model=List[schemas.Shipment])
def list_shipments(db: Session = Depends(get_db)):
    return db.query(models.Shipment).filter(models.Shipment.is_deleted == False).all()
