from flask import Blueprint, request, jsonify
from .db import db
from sqlalchemy import text
from .cache import cache
import time

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Hello, Earthquake App!"

def fetch_random_earthquakes(n):
    print("This should NOT appear if Redis cache hit")
    time.sleep(3)  # Simulate slow fetch
    query = text("SELECT * FROM earthquakes ORDER BY RANDOM() LIMIT :limit")
    results = db.session.execute(query, {"limit": n}).fetchall()
    return [dict(row._mapping) for row in results]

@main.route('/cached-random-queries')
def cached_random_queries():
    try:
        n = int(request.args.get('limit', 10))
        if n <= 0:
            raise ValueError("Limit must be positive.")
    except ValueError:
        return jsonify({"error": "Invalid limit parameter"}), 400

    start = time.time()
    results = cache.memoize(timeout=60)(fetch_random_earthquakes)(n)
    duration_ms = round((time.time() - start) * 1000, 2)

    return jsonify({
        "source": "db_or_cache",
        "count": len(results),
        "limit_requested": n,
        "duration_ms": duration_ms,
        "results": results
    })

@main.route('/filtered')
@cache.cached(timeout=60, query_string=True)
def filtered():
    mag = request.args.get('min_magnitude', 5.0)
    start = time.time()
    results = db.session.execute(f"SELECT * FROM earthquakes WHERE mag >= {mag}").fetchall()
    return jsonify({"time": time.time() - start, "results": [dict(r) for r in results]})
