const BASE = 'http://localhost:8000'

async function get<T>(path: string): Promise<T> {
  const response = await fetch(`${BASE}${path}`, {
    headers: { Accept: 'application/json' },
  })
  if (!response.ok) {
    throw new Error(`Request failed (${response.status})`)
  }
  return response.json() as Promise<T>
}

export type UserRow = {
  id: number
  name: string
  age: number
  gender: string
  image: string
  role: string
  state: string
}

export type UsersPayload = {
  table_data: UserRow[]
  analytics: {
    by_state: Record<string, number>
    by_university: Record<string, number>
  }
}

export type ProductsPayload = {
  top_brands: Record<string, number>
  products_by_category: Record<string, number>
  price_range_by_category: Record<string, number>
  product_stock: { title: string; stock: number }[]
}

export const fetchUsers = () => get<UsersPayload>('/api/users')
export const fetchProducts = () => get<ProductsPayload>('/api/products/analytics')
