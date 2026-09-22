<script setup lang="ts">
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Tooltip,
} from 'chart.js'
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)

const props = defineProps<{
  labels: string[]
  values: number[]
  label: string
}>()

const data = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      label: props.label,
      data: props.values,
      backgroundColor: '#3d5a80',
    },
  ],
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
}
</script>

<template>
  <div class="chart">
    <Bar :data="data" :options="options" />
  </div>
</template>
