from flask import Blueprint, request, jsonify
from .db import db
from .cache import cache
import time

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Hello, Earthquake App!"

@main.route('/random-queries')
def random_queries():
    n = int(request.args.get('n', 10))
    start = time.time()
    results = db.session.execute(f"SELECT * FROM earthquakes ORDER BY RANDOM() LIMIT {n}").fetchall()
    return jsonify({"time": time.time() - start, "results": [dict(r) for r in results]})

@main.route('/filtered')
@cache.cached(timeout=60, query_string=True)
def filtered():
    mag = request.args.get('min_magnitude', 5.0)
    start = time.time()
    results = db.session.execute(f"SELECT * FROM earthquakes WHERE mag >= {mag}").fetchall()
    return jsonify({"time": time.time() - start, "results": [dict(r) for r in results]})
