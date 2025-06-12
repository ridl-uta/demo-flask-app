import requests
import csv
import io
from datetime import datetime
from .db import db, Earthquake

USGS_CSV_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv"

def import_earthquake_data(limit=100):
    response = requests.get(USGS_CSV_URL)
    if response.status_code != 200:
        raise Exception("Failed to fetch earthquake data.")

    data = csv.DictReader(io.StringIO(response.text))

    count = 0
    for row in data:
        if count >= limit:
            break

        if not row.get("id") or not row.get("time"):
            continue

        try:
            quake = Earthquake(
                id=row["id"],
                time=datetime.strptime(row["time"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
                depth=float(row["depth"]),
                mag=float(row["mag"]) if row["mag"] else None,
                place=row["place"],
                type=row["type"]
            )
            db.session.merge(quake)  # Upsert (skip duplicates)
            count += 1
        except Exception as e:
            print(f"Skipping row due to error: {e}")
            continue

    db.session.commit()
    print(f"Imported {count} earthquake entries.")
