<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { fetchProducts, type ProductsPayload } from '../api'
import BarChart from '../components/BarChart.vue'

const data = ref<ProductsPayload | null>(null)
const error = ref('')
const loading = ref(true)

onMounted(async () => {
  try {
    data.value = await fetchProducts()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load products'
  } finally {
    loading.value = false
  }
})

function entries(source: Record<string, number>) {
  return Object.entries(source).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
}

// Keep the backend order. Re-sorting by average would undo the review-count tie-break.
const brands = computed(() => (data.value ? Object.entries(data.value.top_brands) : []))
const categories = computed(() => (data.value ? entries(data.value.products_by_category) : []))
const prices = computed(() => (data.value ? entries(data.value.price_range_by_category) : []))
</script>

<template>
  <section>
    <h1>Products</h1>
    <p v-if="loading">Loading…</p>
    <p v-else-if="error" class="error">{{ error }}</p>
    <div v-else-if="data" class="grid">
      <article>
        <h2>Top brands by reviews</h2>
        <p class="muted">Average review rating. Same average: more reviews ranks higher.</p>
        <BarChart
          :labels="brands.map(([label]) => label)"
          :values="brands.map(([, value]) => value)"
          label="Avg. review rating"
        />
      </article>
      <article>
        <h2>Available products by category</h2>
        <BarChart
          :labels="categories.map(([label]) => label)"
          :values="categories.map(([, value]) => value)"
          label="In stock"
        />
      </article>
      <article>
        <h2>Price range by category</h2>
        <p class="muted">Maximum difference (max − min) in each category.</p>
        <BarChart
          :labels="prices.map(([label]) => label)"
          :values="prices.map(([, value]) => value)"
          label="Spread"
        />
      </article>
      <article>
        <h2>Stock</h2>
        <p class="muted">Lowest stock first, including items already at zero.</p>
        <BarChart
          :labels="data.product_stock.map((row) => row.title)"
          :values="data.product_stock.map((row) => row.stock)"
          label="Units"
        />
      </article>
    </div>
  </section>
</template>
