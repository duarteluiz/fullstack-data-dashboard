# JTA

Small dashboard over DummyJSON. The Vue app only talks to the Python API.

## What it does

**Users** — table (name, age, gender, photo, role, state) with filter and sort.
Charts for users by state and by university.

**Products** — top brands by review rating, how many products are in stock per
category, price spread (max − min) per category, and the 20 products
closest to running out.

## Run locally

```bash
# backend
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# frontend (another terminal)
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

Checks for the aggregations (no network):

```bash
cd backend && python -m unittest test_services.py
```

## Assumptions

- DummyJSON user records include `password` / `ssn` / bank data. The backend
  asks only for the fields it needs.
- "Available products" means `stock > 0`. A category with nothing left still
  appears, with a count of zero.
- Top brands is the mean of individual review ratings, top 5. Equal averages
  are broken by how many reviews the brand has.
- Price range is `max(price) - min(price)` inside each category.
- Stock chart shows the 20 products with the fewest units, not the fullest.
- Users filter/sort runs in the browser. ~200 rows is small enough and the
  backend already did the grouping for the charts.
- Charts show the 12 busiest states/universities so the bars stay readable.
- DummyJSON responses are cached in memory for 5 minutes so we don't hit their
  public API on every click.
