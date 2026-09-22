<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { fetchUsers, type UserRow } from '../api'
import BarChart from '../components/BarChart.vue'

type SortKey = 'name' | 'age' | 'gender' | 'role' | 'state'

const users = ref<UserRow[]>([])
const analytics = ref<{ by_state: Record<string, number>; by_university: Record<string, number> } | null>(
  null,
)
const search = ref('')
const sortBy = ref<SortKey>('name')
const sortDir = ref<'asc' | 'desc'>('asc')
const error = ref('')
const loading = ref(true)

onMounted(async () => {
  try {
    const data = await fetchUsers()
    users.value = data.table_data
    analytics.value = data.analytics
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load users'
  } finally {
    loading.value = false
  }
})

const rows = computed(() => {
  const q = search.value.trim().toLowerCase()
  const filtered = users.value.filter((user) => {
    if (!q) return true
    return (
      user.name.toLowerCase().includes(q) ||
      user.role.toLowerCase().includes(q) ||
      user.state.toLowerCase().includes(q) ||
      user.gender.toLowerCase().includes(q)
    )
  })

  const key = sortBy.value
  const dir = sortDir.value === 'asc' ? 1 : -1
  return [...filtered].sort((a, b) => {
    const left = a[key]
    const right = b[key]
    if (left < right) return -1 * dir
    if (left > right) return 1 * dir
    return a.id - b.id
  })
})

function setSort(key: SortKey) {
  if (sortBy.value === key) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
    return
  }
  sortBy.value = key
  sortDir.value = 'asc'
}

function topEntries(source: Record<string, number>, limit = 12) {
  return Object.entries(source)
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, limit)
}
</script>

<template>
  <section>
    <h1>Users</h1>
    <p v-if="loading">Loading…</p>
    <p v-else-if="error" class="error">{{ error }}</p>
    <template v-else>
      <div class="controls">
        <input v-model="search" type="search" placeholder="Filter by name, role, state…" />
        <select v-model="sortBy">
          <option value="name">Name</option>
          <option value="age">Age</option>
          <option value="gender">Gender</option>
          <option value="role">Role</option>
          <option value="state">State</option>
        </select>
      </div>
      <p class="muted">{{ rows.length }} of {{ users.length }} users</p>

      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th></th>
              <th><button type="button" @click="setSort('name')">Name</button></th>
              <th><button type="button" @click="setSort('age')">Age</button></th>
              <th><button type="button" @click="setSort('gender')">Gender</button></th>
              <th><button type="button" @click="setSort('role')">Role</button></th>
              <th><button type="button" @click="setSort('state')">State</button></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in rows" :key="user.id">
              <td>
                <img :src="user.image" :alt="user.name" width="36" height="36" />
              </td>
              <td>{{ user.name }}</td>
              <td>{{ user.age }}</td>
              <td>{{ user.gender }}</td>
              <td>{{ user.role }}</td>
              <td>{{ user.state }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="analytics" class="grid">
        <article>
          <h2>By state</h2>
          <BarChart
            :labels="topEntries(analytics.by_state).map(([label]) => label)"
            :values="topEntries(analytics.by_state).map(([, count]) => count)"
            label="Users"
          />
        </article>
        <article>
          <h2>By university</h2>
          <BarChart
            :labels="topEntries(analytics.by_university).map(([label]) => label)"
            :values="topEntries(analytics.by_university).map(([, count]) => count)"
            label="Users"
          />
        </article>
      </div>
    </template>
  </section>
</template>
