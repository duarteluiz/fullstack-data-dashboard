from pydantic import BaseModel


class UserRow(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    image: str
    role: str
    state: str


class UsersAnalytics(BaseModel):
    by_state: dict[str, int]
    by_university: dict[str, int]


class UsersResponse(BaseModel):
    table_data: list[UserRow]
    analytics: UsersAnalytics


class ProductStockRow(BaseModel):
    title: str
    stock: int


class ProductsAnalyticsResponse(BaseModel):
    top_brands: dict[str, float]
    products_by_category: dict[str, int]
    price_range_by_category: dict[str, float]
    product_stock: list[ProductStockRow]
