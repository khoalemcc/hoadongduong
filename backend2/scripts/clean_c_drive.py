import os
import shutil
import pathlib

# Paths configuration
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]  # backend2 directory
DATA_DIR = PROJECT_ROOT / "data"
TARGET_DATA_DIR = pathlib.Path(r"D:\hoadongduong\data")

def remove_pycache(path: pathlib.Path):
    for pyc in path.rglob('__pycache__'):
        try:
            shutil.rmtree(pyc)
            print(f"[CLEAN] Removed __pycache__: {pyc}")
        except Exception as e:
            print(f"[WARN] Could not remove {pyc}: {e}")

def remove_logs_and_sqlite(path: pathlib.Path):
    for ext in ('*.log', '*.sqlite', '*.db'):
        for file in path.rglob(ext):
            try:
                file.unlink()
                print(f"[CLEAN] Deleted {file}")
            except Exception as e:
                print(f"[WARN] Could not delete {file}: {e}")

def move_data():
    if not DATA_DIR.exists():
        print(f"[INFO] No data directory at {DATA_DIR}, nothing to move.")
        return
    TARGET_DATA_DIR.parent.mkdir(parents=True, exist_ok=True)
    try:
        if TARGET_DATA_DIR.exists():
            # Merge contents if target already exists
            for item in DATA_DIR.iterdir():
                dest = TARGET_DATA_DIR / item.name
                if dest.exists():
                    if item.is_file():
                        dest.unlink()
                    else:
                        shutil.rmtree(dest)
                shutil.move(str(item), str(dest))
        else:
            shutil.move(str(DATA_DIR), str(TARGET_DATA_DIR))
        print(f"[MOVE] Data moved to {TARGET_DATA_DIR}")
    except Exception as e:
        print(f"[ERROR] Failed to move data: {e}")

def main():
    print("[START] Cleaning C: drive temporary files...")
    remove_pycache(PROJECT_ROOT)
    remove_logs_and_sqlite(PROJECT_ROOT)
    print("[START] Moving data directory to D: drive...")
    move_data()
    print("[DONE] Cleanup complete.")

if __name__ == "__main__":
    main()
