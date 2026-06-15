# frontend/dashboard/app.py
"""Streamlit dashboard for Hoa Dong Duong.
Shows KPI metrics from the database: daily revenue, top products, order count, etc.
"""
import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

# Database URL from .env (same as FastAPI)
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://hh_app:password@db:3306/hh")
engine = create_engine(DATABASE_URL)

st.set_page_config(page_title="Hoa Dong Duong Dashboard", layout="wide")
st.title("📊 Dashboard - Hoa Dong Duong")

def query(sql, params=None):
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params)

# 1️⃣ Doanh thu hằng ngày (last 30 days)
rev_df = query(
    """
    SELECT DATE(created_at) AS day, SUM(total_price) AS revenue
    FROM orders
    WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    GROUP BY day
    ORDER BY day DESC;
    """
)
st.subheader("Doanh thu 30 ngày gần nhất")
st.line_chart(rev_df.set_index('day'))

# 2️⃣ Top 5 sản phẩm bán chạy
top_products = query(
    """
    SELECT p.name, COUNT(oi.id) AS sold_qty
    FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    GROUP BY p.id
    ORDER BY sold_qty DESC
    LIMIT 5;
    """
)
st.subheader("Top 5 sản phẩm bán chạy")
st.table(top_products)

# 3️⃣ Tổng số đơn hàng & trung bình đơn hàng
summary = query(
    """
    SELECT COUNT(*) AS total_orders,
           AVG(total_price) AS avg_order_value
    FROM orders;
    """
)
col1, col2 = st.columns(2)
col1.metric("Tổng số đơn hàng", int(summary['total_orders'][0]))
col2.metric("Giá trị trung bình", f"{summary['avg_order_value'][0]:.2f} USD")

st.caption("* Dữ liệu được lấy trực tiếp từ cơ sở dữ liệu PostgreSQL/MySQL. Để cập nhật, chạy ETL script ./backend2/scripts/etl.py.")
