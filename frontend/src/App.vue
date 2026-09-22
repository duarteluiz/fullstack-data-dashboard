<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="layout">
    <header class="top">
      <strong>JTA</strong>
      <nav>
        <RouterLink to="/users">Users</RouterLink>
        <RouterLink to="/products">Products</RouterLink>
      </nav>
    </header>
    <main>
      <RouterView />
    </main>
  </div>
</template>
