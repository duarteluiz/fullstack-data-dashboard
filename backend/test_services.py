import unittest

from services import build_products, build_users


class UsersTest(unittest.TestCase):
    def test_flattens_name_and_state_and_counts(self):
        result = build_users(
            [
                {
                    "id": 1,
                    "firstName": "Ada",
                    "lastName": "Lovelace",
                    "age": 36,
                    "gender": "female",
                    "image": "a.png",
                    "role": "admin",
                    "address": {"state": "Texas"},
                    "university": "Alpha",
                    "password": "must-not-leak",
                },
                {
                    "id": 2,
                    "firstName": "Alan",
                    "lastName": "Turing",
                    "age": 41,
                    "gender": "male",
                    "image": "b.png",
                    "role": "user",
                    "address": {"state": "Texas"},
                    "university": "Beta",
                },
                {
                    "id": 3,
                    "firstName": "Grace",
                    "lastName": "Hopper",
                    "age": 50,
                    "address": {},
                    "university": "",
                },
            ]
        )

        ada = result["table_data"][0]
        self.assertEqual(ada["name"], "Ada Lovelace")
        self.assertEqual(ada["state"], "Texas")
        self.assertNotIn("password", ada)
        self.assertEqual(result["analytics"]["by_state"]["Texas"], 2)
        self.assertEqual(result["analytics"]["by_state"]["Unknown"], 1)
        self.assertEqual(result["analytics"]["by_university"]["Alpha"], 1)


class ProductsTest(unittest.TestCase):
    def test_price_spread_is_max_minus_min(self):
        result = build_products(
            [
                {"title": "Cheap", "category": "laptops", "price": 100, "stock": 1, "brand": "A", "reviews": [{"rating": 4}]},
                {"title": "Dear", "category": "laptops", "price": 400, "stock": 1, "brand": "A", "reviews": [{"rating": 4}]},
            ]
        )
        self.assertEqual(result["price_range_by_category"]["laptops"], 300)

    def test_out_of_stock_is_not_available_but_the_category_stays(self):
        result = build_products(
            [
                {"title": "Gone", "category": "beauty", "price": 10, "stock": 0},
                {"title": "Here", "category": "beauty", "price": 12, "stock": 3},
            ]
        )
        self.assertEqual(result["products_by_category"]["beauty"], 1)

    def test_same_average_is_broken_by_review_count(self):
        result = build_products(
            [
                {"title": "One", "category": "c", "price": 1, "stock": 1, "brand": "Thin", "reviews": [{"rating": 5}]},
                {
                    "title": "Many",
                    "category": "c",
                    "price": 1,
                    "stock": 1,
                    "brand": "Proven",
                    "reviews": [{"rating": 5}, {"rating": 5}, {"rating": 5}],
                },
            ]
        )
        self.assertEqual(list(result["top_brands"]), ["Proven", "Thin"])

    def test_stock_list_starts_with_the_lowest(self):
        result = build_products(
            [
                {"title": "Full", "category": "c", "price": 1, "stock": 100},
                {"title": "Empty", "category": "c", "price": 1, "stock": 0},
                {"title": "Low", "category": "c", "price": 1, "stock": 2},
            ]
        )
        titles = [row["title"] for row in result["product_stock"]]
        self.assertEqual(titles, ["Empty", "Low", "Full"])


if __name__ == "__main__":
    unittest.main()
