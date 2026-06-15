# Hoa Dong Duong Backend V2

FastAPI backend for Hoa Dong Duong E-commerce platform (Database: `hh`).

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup**:
   - Ensure MySQL is running on `127.0.0.1:3306`.
   - Create a database named `hh`:
     ```sql
     CREATE DATABASE hh;
     ```
   - The app will automatically create tables on first run.

3. **Run the application**:
   ```bash
   $env:PYTHONPATH="D:\github\hoadongduong\backend2"
   python -m uvicorn app.main:app --reload
   ```

## API Documentation
Once running, visit:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
