<template>
  <div class="min-h-screen flex bg-app-bg text-app-text font-body fade-in">
    <AdminSidebar />

    <main class="flex-1 min-w-0 flex flex-col bg-app-bg">
      <header class="h-20 px-8 flex items-center justify-between bg-app-bg border-b border-white/5">
        <div>
          <h2 class="text-2xl font-headline font-bold">Analytics & Revenue</h2>
          <p class="text-[10px] font-black uppercase tracking-widest text-stone-500 mt-1">Real-time botanical business intelligence</p>
        </div>
        <div class="flex items-center gap-3 bg-app-surface p-1 rounded-xl border border-white/5">
          <button v-for="range in ['7 Days', '30 Days', '90 Days', 'All']" :key="range"
                  @click="selectedRange = range"
                  :class="['px-4 py-2 text-[10px] font-black uppercase tracking-widest rounded-lg transition-all', selectedRange === range ? 'bg-primary/20 text-primary' : 'text-stone-500 hover:text-white']">
            {{ range }}
          </button>
        </div>
      </header>

      <!-- KPI Cards -->
      <section class="px-8 pt-8 pb-4">
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
          <div v-for="kpi in kpis" :key="kpi.label" class="bg-app-surface rounded-2xl border border-white/5 p-6 relative overflow-hidden group hover:border-primary/10 transition-all">
            <div class="absolute -right-6 -top-6 w-24 h-24 rounded-full bg-primary/5 blur-2xl group-hover:bg-primary/10 transition-all"></div>
            <div class="flex items-center gap-3 mb-4">
              <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                <span class="material-symbols-outlined text-primary text-lg">{{ kpi.icon }}</span>
              </div>
              <span class="text-[9px] font-black uppercase tracking-widest text-stone-500">{{ kpi.label }}</span>
            </div>
            <div class="flex items-baseline gap-3">
              <h3 class="text-3xl font-black text-white">{{ kpi.value }}</h3>
              <span v-if="kpi.trend" :class="['text-xs font-bold flex items-center gap-1', kpi.trend > 0 ? 'text-primary' : 'text-red-400']">
                <span class="material-symbols-outlined text-xs">{{ kpi.trend > 0 ? 'trending_up' : 'trending_down' }}</span>
                {{ Math.abs(kpi.trend) }}%
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Charts Grid -->
      <section class="px-8 py-4">
        <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
          <!-- Revenue Line Chart (spanning 2 cols) -->
          <div class="xl:col-span-2 bg-app-surface rounded-2xl border border-white/5 p-8 relative overflow-hidden">
            <div class="flex items-center justify-between mb-8">
              <div>
                <h4 class="text-lg font-headline font-bold text-white mb-1">Revenue Over Time</h4>
                <p class="text-[10px] font-black uppercase tracking-widest text-stone-500">Monthly botanical sales performance</p>
              </div>
              <div class="text-right">
                <p class="text-2xl font-black text-primary">{{ formatPrice(stats.total_revenue) }}đ</p>
                <p class="text-[9px] text-stone-600 uppercase tracking-widest">Total net revenue</p>
              </div>
            </div>
            <div class="relative h-72">
              <canvas ref="revenueChartRef"></canvas>
            </div>
          </div>

          <!-- Order Status Doughnut -->
          <div class="bg-app-surface rounded-2xl border border-white/5 p-8">
            <h4 class="text-lg font-headline font-bold text-white mb-1">Order Lifecycle</h4>
            <p class="text-[10px] font-black uppercase tracking-widest text-stone-500 mb-8">Status distribution</p>
            <div class="relative h-56 flex items-center justify-center">
              <canvas ref="statusChartRef"></canvas>
            </div>
            <div class="mt-6 space-y-3">
              <div v-for="(count, status) in stats.status_breakdown" :key="status" class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <span :class="['w-3 h-3 rounded-full', getStatusColor(status)]"></span>
                  <span class="text-xs text-stone-400 capitalize">{{ status }}</span>
                </div>
                <span class="text-xs font-bold text-white">{{ count }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Bottom Section: Predictive Insights -->
      <section class="px-8 py-4 pb-8">
        <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
          <!-- Inventory Forecasting -->
          <div class="bg-app-surface rounded-2xl border border-white/5 p-8 relative overflow-hidden">
            <div class="absolute top-0 right-0 p-8">
              <span class="material-symbols-outlined text-primary/20 text-6xl">timeline</span>
            </div>
            <h4 class="text-lg font-headline font-bold text-white mb-1">Inventory Forecasting</h4>
            <p class="text-[10px] font-black uppercase tracking-widest text-stone-500 mb-8">Lead-time & stock-out predictions</p>
            
            <div class="space-y-4 relative z-10">
              <div v-for="item in inventoryForecast" :key="item.product_id" 
                   class="flex items-center justify-between p-4 bg-app-bg/50 rounded-xl border border-white/5 hover:border-primary/20 transition-all group">
                <div class="flex flex-col">
                  <span class="text-sm font-bold text-white">{{ item.name }}</span>
                  <span class="text-[10px] text-stone-500 uppercase tracking-widest">Velocity: {{ item.daily_velocity }} units/day</span>
                </div>
                <div class="text-right">
                  <div :class="['text-xs font-black uppercase tracking-widest px-2 py-1 rounded-md mb-1 inline-block', 
                                item.status === 'Critical' ? 'bg-red-500/10 text-red-400' : 'bg-amber-500/10 text-amber-400']">
                    {{ item.days_left }} Days Left
                  </div>
                  <p class="text-[9px] text-stone-600 uppercase tracking-widest">Est. Stockout</p>
                </div>
              </div>
              <div v-if="inventoryForecast.length === 0" class="text-center py-8 text-stone-500 text-xs italic">
                All botanical stocks are currently stable.
              </div>
            </div>
          </div>

          <!-- Basket Analysis / Combo Suggestions -->
          <div class="bg-app-surface rounded-2xl border border-white/5 p-8">
            <h4 class="text-lg font-headline font-bold text-white mb-1">Market Basket Analysis</h4>
            <p class="text-[10px] font-black uppercase tracking-widest text-stone-500 mb-8">Affinity & co-purchase patterns</p>
            
            <div class="grid grid-cols-1 gap-4">
              <div v-for="pair in basketAnalysis" :key="pair.pair.join('')" 
                   class="p-4 bg-primary/5 border border-primary/10 rounded-xl flex items-start gap-4 hover:bg-primary/10 transition-all">
                <div class="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
                  <span class="material-symbols-outlined text-primary text-xl">Auto_Awesome</span>
                </div>
                <div>
                  <div class="flex items-center gap-2 mb-1">
                    <span class="text-xs font-bold text-white">{{ pair.pair[0] }}</span>
                    <span class="text-stone-600 text-[10px]">&</span>
                    <span class="text-xs font-bold text-white">{{ pair.pair[1] }}</span>
                  </div>
                  <p class="text-[11px] text-stone-400 leading-relaxed mb-2">{{ pair.suggestion }}</p>
                  <div class="inline-flex items-center gap-2 px-2 py-1 bg-primary/10 text-primary rounded-md text-[9px] font-black uppercase tracking-widest">
                    Frequency: {{ pair.frequency }}
                  </div>
                </div>
              </div>
              <div v-if="basketAnalysis.length === 0" class="text-center py-8 text-stone-500 text-xs italic">
                Accumulating more order data for affinity analysis...
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed, watch } from 'vue'
import api from '../api'
import AdminSidebar from '../components/AdminSidebar.vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const selectedRange = ref('All')
const revenueChartRef = ref(null)
const statusChartRef = ref(null)
const ordersBarChartRef = ref(null)

let revChartInst = null
let statusChartInst = null
let barChartInst = null

const stats = ref({
  total_revenue: 0,
  total_orders: 0,
  avg_order_value: 0,
  monthly: [],
  status_breakdown: {}
})

const inventoryForecast = ref([])
const basketAnalysis = ref([])
const topProducts = ref([])

const kpis = computed(() => [
  { label: 'Total Revenue', value: formatPrice(stats.value.total_revenue) + 'đ', icon: 'payments', trend: 12.5 },
  { label: 'Total Orders', value: stats.value.total_orders.toString(), icon: 'shopping_cart', trend: 8.3 },
  { label: 'Avg. Order Value', value: formatPrice(stats.value.avg_order_value) + 'đ', icon: 'query_stats', trend: 3.1 },
  { label: 'Inventory Risk', value: inventoryForecast.value.filter(i => i.status === 'Critical').length.toString(), icon: 'warning', trend: null },
])

const formatPrice = (price) => {
  if (!price) return '0'
  return new Intl.NumberFormat('vi-VN').format(Math.round(price))
}

const getStatusHex = (status) => {
  const map = {
    pending: '#f59e0b',
    confirmed: '#3b82f6',
    shipping: '#6366f1',
    completed: '#4ade80',
    cancelled: '#f87171'
  }
  return map[status] || '#78716c'
}

const getStatusColor = (status) => {
  const map = {
    pending: 'bg-amber-500',
    confirmed: 'bg-blue-500',
    shipping: 'bg-indigo-500',
    completed: 'bg-green-500',
    cancelled: 'bg-red-500'
  }
  return map[status] || 'bg-stone-500'
}

const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

const renderRevenueChart = () => {
  const ctx = revenueChartRef.value?.getContext('2d')
  if (!ctx) return

  const monthly = [...stats.value.monthly].sort((a, b) => a.month - b.month)
  const labels = monthly.map(m => monthNames[m.month - 1] || m.month)
  const data = monthly.map(m => m.revenue)

  const gradient = ctx.createLinearGradient(0, 0, 0, 280)
  gradient.addColorStop(0, 'rgba(74, 222, 128, 0.25)')
  gradient.addColorStop(1, 'rgba(74, 222, 128, 0.0)')

  if (revChartInst) revChartInst.destroy()

  revChartInst = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Revenue',
        data,
        borderColor: '#4ade80',
        backgroundColor: gradient,
        borderWidth: 3,
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.03)' } },
        y: { grid: { color: 'rgba(255,255,255,0.03)' } }
      }
    }
  })
}

const renderStatusChart = () => {
  const ctx = statusChartRef.value?.getContext('2d')
  if (!ctx) return

  const breakdown = stats.value.status_breakdown
  const labels = Object.keys(breakdown)
  const data = Object.values(breakdown)
  const colors = labels.map(l => getStatusHex(l))

  if (statusChartInst) statusChartInst.destroy()

  statusChartInst = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{ data, backgroundColor: colors, borderWidth: 0 }]
    },
    options: { responsive: true, maintainAspectRatio: false, cutout: '70%' }
  })
}

onMounted(async () => {
  try {
    const [statsRes, forecastRes, basketRes] = await Promise.all([
      api.get('/admin/dashboard/stats'),
      api.get('/admin/dashboard/inventory/forecast'),
      api.get('/admin/dashboard/basket-analysis')
    ])
    
    stats.value = statsRes.data
    inventoryForecast.value = forecastRes.data
    basketAnalysis.value = basketRes.data

    await nextTick()
    renderRevenueChart()
    renderStatusChart()
  } catch (e) {
    console.error('Fetch error:', e)
  }
})

watch(selectedRange, () => {
  nextTick(() => {
    renderRevenueChart()
    renderStatusChart()
  })
})
</script>
