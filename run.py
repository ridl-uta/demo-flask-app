from app import create_app
from app.importer import import_earthquake_data
from sqlalchemy.exc import OperationalError
from app.db import db
import time


app = create_app()

for i in range(10):  # Retry 10 times with 3s delay
    try:
        with app.app_context():
            db.create_all()
            print("Database initialized.")

            # ⬇️ Import USGS earthquake data
            import_earthquake_data(limit=200)
            print("Earthquake data imported.")
            break
    except OperationalError as e:
        print(f"Attempt {i+1}: DB not ready — {e}")
        time.sleep(3)
else:
    raise RuntimeError("Failed to connect to the database after multiple attempts.")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
