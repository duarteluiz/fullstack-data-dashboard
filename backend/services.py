import time
from collections import defaultdict

import httpx

DUMMYJSON = "https://dummyjson.com"
TIMEOUT = 10.0
CACHE_SECONDS = 300

# "Stock on products" is shown as a restock watchlist, not a full inventory dump:
# the items closest to running out are the ones that need action. A table with
# every SKU would bury that signal and isn't actionable in a dashboard widget.
STOCK_WATCHLIST_SIZE = 20

# DummyJSON also ships password, ssn, bank, crypto. Never request those.
USER_FIELDS = "firstName,lastName,age,gender,image,role,address,university"
PRODUCT_FIELDS = "title,brand,category,price,stock,reviews"

_cache: dict = {}


async def _load(resource: str, fields: str) -> list:
    cached = _cache.get(resource)
    if cached and time.monotonic() - cached["at"] < CACHE_SECONDS:
        return cached["items"]

    items: list = []
    skip = 0
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        while True:
            response = await client.get(
                f"{DUMMYJSON}/{resource}",
                params={"limit": 100, "skip": skip, "select": fields},
            )
            response.raise_for_status()
            body = response.json()
            page = body.get(resource) or []
            items.extend(page)
            skip += len(page)
            total = body.get("total", len(items))
            if skip >= total or not page:
                break

    _cache[resource] = {"items": items, "at": time.monotonic()}
    return items


def _avg(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 2)


def build_users(users: list) -> dict:
    table = []
    by_state: dict[str, int] = defaultdict(int)
    by_university: dict[str, int] = defaultdict(int)

    for user in users:
        address = user.get("address") or {}
        state = address.get("state") or "Unknown"
        university = user.get("university") or "Unknown"
        first = user.get("firstName") or ""
        last = user.get("lastName") or ""

        table.append(
            {
                "id": user.get("id"),
                "name": f"{first} {last}".strip(),
                "age": user.get("age") or 0,
                "gender": user.get("gender") or "",
                "image": user.get("image") or "",
                "role": user.get("role") or "",
                "state": state,
            }
        )
        by_state[state] += 1
        by_university[university] += 1

    return {
        "table_data": table,
        "analytics": {
            "by_state": dict(by_state),
            "by_university": dict(by_university),
        },
    }


async def get_users_data() -> dict:
    return build_users(await _load("users", USER_FIELDS))


def build_products(products: list) -> dict:
    brand_ratings: dict[str, list[float]] = defaultdict(list)
    available_by_category: dict[str, int] = defaultdict(int)
    prices_by_category: dict[str, list[float]] = defaultdict(list)
    stock_rows = []

    for product in products:
        category = product.get("category") or "unknown"
        price = float(product.get("price") or 0)
        stock = int(product.get("stock") or 0)
        title = product.get("title") or "Untitled"

        prices_by_category[category].append(price)
        stock_rows.append({"title": title, "stock": stock})

        # "available" = currently sellable. Categories with nothing in stock stay at 0.
        available_by_category[category] += 1 if stock > 0 else 0

        brand = product.get("brand")
        reviews = product.get("reviews") or []
        if brand and reviews:
            for review in reviews:
                try:
                    brand_ratings[brand].append(float(review.get("rating") or 0))
                except (TypeError, ValueError):
                    continue

    price_ranges = {}
    for category, prices in prices_by_category.items():
        price_ranges[category] = round(max(prices) - min(prices), 2) if prices else 0

    # Mean rating first. A single 5-star review must not beat a brand with the
    # same average and many more reviews.
    ranked = sorted(
        brand_ratings.items(),
        key=lambda item: (_avg(item[1]), len(item[1])),
        reverse=True,
    )
    top_brands = {brand: _avg(ratings) for brand, ratings in ranked[:5]}

    # Lowest stock first: the useful view is what is about to run out.
    stock_rows.sort(key=lambda row: (row["stock"], row["title"]))

    return {
        "top_brands": top_brands,
        "products_by_category": dict(available_by_category),
        "price_range_by_category": price_ranges,
        "product_stock": stock_rows[:STOCK_WATCHLIST_SIZE],
    }


async def get_products_analytics() -> dict:
    return build_products(await _load("products", PRODUCT_FIELDS))
