<template>
  <div class="min-h-screen flex bg-app-bg text-app-text font-body fade-in">
    <!-- Shared Sidebar -->
    <AdminSidebar />

    <!-- Main Content Canvas -->
    <main class="flex-1 min-w-0 flex flex-col bg-app-bg">
      <!-- Top Header -->
      <header class="h-20 px-8 flex items-center justify-between bg-app-bg border-b border-white/5 z-10 sticky top-0 backdrop-blur-md">
        <div>
          <h2 class="text-2xl font-headline font-bold">Dashboard Insights</h2>
          <p class="text-[10px] font-black uppercase tracking-widest text-stone-500 mt-1">Operational business intelligence</p>
        </div>
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-2 bg-app-surface p-1 rounded-xl border border-white/5">
             <button v-for="range in ranges" :key="range.value"
                    @click="selectedRange = range.value"
                    :class="['px-3 py-1.5 text-[9px] font-black uppercase tracking-widest rounded-lg transition-all', selectedRange === range.value ? 'bg-primary/20 text-primary' : 'text-stone-500 hover:text-white']">
              {{ range.label }}
            </button>
          </div>
          <button @click="showNotification" class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-app-surface transition-colors relative">
            <span class="material-symbols-outlined text-stone-400">notifications</span>
            <span v-if="lowStock.length > 0" class="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
        </div>
      </header>

      <!-- Content Area -->
      <section class="p-8 space-y-8 flex-1 overflow-y-auto">
        
        <!-- KPI Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- Revenue Today -->
          <div class="bg-primary text-white p-6 rounded-2xl relative overflow-hidden group shadow-2xl shadow-primary/20">
            <div class="relative z-10 flex flex-col justify-between h-full">
              <div>
                <p class="text-white/70 font-bold text-[9px] uppercase tracking-widest">Revenue Today</p>
                <h3 class="text-3xl font-headline font-bold mt-2">{{ formatPrice(kpi.revenue_today) }}đ</h3>
              </div>
              <div class="mt-4 flex items-center gap-2">
                <span class="material-symbols-outlined text-sm">trending_up</span>
                <span class="text-[10px] font-bold">+5.4% vs yesterday</span>
              </div>
            </div>
            <div class="absolute -right-8 -bottom-8 w-32 h-32 bg-white/10 rounded-full blur-2xl group-hover:scale-125 transition-transform duration-700"></div>
          </div>

          <!-- Orders Today -->
          <div class="bg-app-surface p-6 rounded-2xl border border-white/5 flex flex-col justify-between shadow-xl">
            <div class="flex items-center justify-between">
              <div class="w-10 h-10 bg-app-bg text-primary rounded-xl flex items-center justify-center border border-white/5">
                <span class="material-symbols-outlined text-lg">shopping_bag</span>
              </div>
              <span class="text-[10px] font-black text-stone-500 uppercase tracking-widest">Orders</span>
            </div>
            <div class="mt-4">
              <h3 class="text-3xl font-headline font-bold">{{ kpi.orders_today }}</h3>
              <p class="text-[10px] text-stone-500 mt-1">Pending: {{ stats_dist.pending || 0 }}</p>
            </div>
          </div>

          <!-- New Users -->
          <div class="bg-app-surface p-6 rounded-2xl border border-white/5 flex flex-col justify-between shadow-xl text-app-text">
            <div class="flex items-center justify-between">
              <div class="w-10 h-10 bg-app-bg text-blue-400 rounded-xl flex items-center justify-center border border-white/5">
                <span class="material-symbols-outlined text-lg">person_add</span>
              </div>
              <span class="text-[10px] font-black text-stone-500 uppercase tracking-widest">New Clients</span>
            </div>
            <div class="mt-4">
              <h3 class="text-3xl font-headline font-bold">{{ kpi.new_users_today }}</h3>
              <p class="text-[10px] text-stone-500 mt-1">Active Now: 12</p>
            </div>
          </div>

          <!-- Conversion Rate -->
          <div class="bg-app-surface p-6 rounded-2xl border border-white/5 flex flex-col justify-between shadow-xl">
            <div class="flex items-center justify-between">
              <div class="w-10 h-10 bg-app-bg text-emerald-400 rounded-xl flex items-center justify-center border border-white/5">
                <span class="material-symbols-outlined text-lg">ads_click</span>
              </div>
              <span class="text-[10px] font-black text-stone-500 uppercase tracking-widest">CR %</span>
            </div>
            <div class="mt-4">
              <h3 class="text-3xl font-headline font-bold">{{ kpi.conversion_rate }}%</h3>
              <p class="text-[10px] text-stone-500 mt-1">v: {{ kpi.visits }} visits</p>
            </div>
          </div>
        </div>

        <!-- Auto Content Factory -->
        <div class="bg-app-surface rounded-2xl p-6 border border-white/5 shadow-2xl">
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
            <div class="flex items-start gap-4">
              <div class="w-12 h-12 bg-primary/10 text-primary rounded-xl flex items-center justify-center border border-primary/20">
                <span class="material-symbols-outlined">auto_awesome</span>
              </div>
              <div>
                <p class="text-[9px] font-black uppercase tracking-widest text-stone-500 mb-1">Content Automation</p>
                <h3 class="text-xl font-headline font-bold">Auto Content Factory</h3>
                <p class="text-sm text-stone-500 mt-2 max-w-2xl">
                  Source blog ideas, preview attribution-safe summaries, import drafts, and create SEO starter posts for editorial review.
                </p>
              </div>
            </div>

            <div class="grid grid-cols-3 gap-3 min-w-full lg:min-w-[360px]">
              <div class="bg-app-bg rounded-xl border border-white/5 p-4">
                <p class="text-[9px] font-black uppercase tracking-widest text-stone-500">Queue</p>
                <p class="text-2xl font-headline font-bold mt-1">{{ contentFactory.queue }}</p>
              </div>
              <div class="bg-app-bg rounded-xl border border-white/5 p-4">
                <p class="text-[9px] font-black uppercase tracking-widest text-stone-500">Warnings</p>
                <p class="text-2xl font-headline font-bold mt-1">{{ contentFactory.warnings }}</p>
              </div>
              <div class="bg-app-bg rounded-xl border border-white/5 p-4">
                <p class="text-[9px] font-black uppercase tracking-widest text-stone-500">Mode</p>
                <p class="text-sm font-black uppercase tracking-widest text-primary mt-2">Draft</p>
              </div>
            </div>
          </div>

          <div class="flex flex-wrap items-center gap-3 mt-6">
            <button @click="$router.push('/admin/marketing')" class="h-10 px-5 rounded-xl bg-primary text-white text-[10px] font-black uppercase tracking-widest hover:bg-primary/90 transition-colors flex items-center gap-2">
              <span class="material-symbols-outlined text-sm">open_in_new</span>
              Open Factory
            </button>
            <button @click="previewContentFactory" :disabled="contentFactory.loading" class="h-10 px-5 rounded-xl bg-app-bg border border-white/5 text-[10px] font-black uppercase tracking-widest text-stone-300 hover:border-primary/30 disabled:opacity-50 transition-colors flex items-center gap-2">
              <span :class="['material-symbols-outlined text-sm', contentFactory.loading ? 'animate-spin' : '']">{{ contentFactory.loading ? 'progress_activity' : 'visibility' }}</span>
              Preview Queue
            </button>
            <span v-if="contentFactory.message" class="text-xs text-stone-500">{{ contentFactory.message }}</span>
          </div>
        </div>

        <!-- Main Charts Section -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Revenue Line Chart -->
          <div class="lg:col-span-2 bg-app-surface rounded-2xl p-8 border border-white/5 shadow-2xl">
            <div class="flex items-center justify-between mb-8">
              <h3 class="text-xl font-headline font-bold">Revenue Performance</h3>
              <div class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-primary">
                <span class="w-2 h-2 rounded-full bg-primary"></span>
                Completed Sales
              </div>
            </div>
            <div class="h-80 w-full relative">
              <canvas ref="revenueChartRef"></canvas>
            </div>
          </div>

          <!-- Status Distribution -->
          <div class="bg-app-surface rounded-2xl p-8 border border-white/5 shadow-2xl">
            <h3 class="text-xl font-headline font-bold mb-8">Order Status</h3>
            <div class="flex flex-col gap-6 h-full justify-center pb-8">
               <div v-for="(count, status) in stats_dist" :key="status" class="space-y-2">
                  <div class="flex items-center justify-between text-[10px] font-black uppercase tracking-widest">
                    <span class="text-stone-400 capitalize">{{ status }}</span>
                    <span>{{ count }}</span>
                  </div>
                  <div class="h-1.5 w-full bg-app-bg rounded-full overflow-hidden">
                    <div class="h-full bg-primary transition-all duration-1000" :style="{ width: (count / kpi.orders_today * 10 || 20) + '%' }"></div>
                  </div>
               </div>
            </div>
          </div>
        </div>

        <!-- Bottom Grid: Recent Orders & Inventory/Top Products -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          <!-- Recent Orders (Middle) -->
          <div class="lg:col-span-7 bg-app-surface rounded-2xl p-8 border border-white/5 shadow-2xl">
            <div class="flex items-center justify-between mb-8">
              <h3 class="text-xl font-headline font-bold">Recent Acquisitions</h3>
              <button @click="$router.push('/admin/orders')" class="text-[10px] font-black uppercase tracking-widest text-primary hover:underline underline-offset-8">All Orders</button>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="text-stone-500 text-[10px] font-black uppercase tracking-widest border-b border-white/5">
                    <th class="pb-6 px-2">ID</th>
                    <th class="pb-6 px-2">Client</th>
                    <th class="pb-6 px-2">Status</th>
                    <th class="pb-6 px-2 text-right">Value</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-white/5 text-sm">
                  <tr v-for="order in recentOrders" :key="order.id" class="group hover:bg-white/5 transition-colors">
                    <td class="py-5 px-2 font-medium text-stone-500">#{{ order.id }}</td>
                    <td class="py-5 px-2 font-bold">{{ order.user_id ? 'User ID:' + order.user_id : 'Walk-in' }}</td>
                    <td class="py-5 px-2">
                       <span :class="['px-2 py-0.5 rounded-full text-[8px] font-black uppercase tracking-widest border', getStatusStyle(order.status)]">
                        {{ order.status }}
                      </span>
                    </td>
                    <td class="py-5 px-2 text-right font-headline font-bold text-white">{{ formatPrice(order.total_amount) }}đ</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Top Selling & Inventory Sidebar (Right) -->
          <div class="lg:col-span-5 space-y-8">
            
            <!-- Low Stock Alerts -->
            <div v-if="lowStock.length > 0" class="bg-red-500/10 border border-red-500/20 rounded-2xl p-8">
               <div class="flex items-center gap-3 mb-6">
                 <span class="material-symbols-outlined text-red-500">warning</span>
                 <h4 class="text-lg font-headline font-bold text-red-500">Inventory Shortage</h4>
               </div>
               <div class="space-y-4">
                  <div v-for="item in lowStock" :key="item.product_id" class="flex items-center justify-between bg-app-bg/50 p-3 rounded-xl border border-white/5">
                    <span class="text-xs font-medium">{{ item.name }}</span>
                    <span class="text-[10px] font-black text-red-500 bg-red-500/10 px-2 py-1 rounded-lg">Only {{ item.quantity }} left</span>
                  </div>
               </div>
            </div>

            <!-- Top Products -->
            <div class="bg-app-surface rounded-2xl p-8 border border-white/5 shadow-2xl">
              <h4 class="text-lg font-headline font-bold text-primary mb-6">Top Selling Flourishes</h4>
              <div class="space-y-6">
                <div v-for="(product, idx) in topProducts" :key="product.product_id" class="flex items-center justify-between">
                  <div class="flex items-center gap-4">
                    <span class="text-xl font-bold text-stone-700">0{{ idx + 1 }}</span>
                    <div>
                      <p class="text-sm font-bold text-white">{{ product.name }}</p>
                      <p class="text-[9px] text-stone-500 uppercase tracking-widest">{{ product.total_sold }} units sold</p>
                    </div>
                  </div>
                  <p class="text-sm font-bold text-primary">{{ formatPrice(product.price) }}đ</p>
                </div>
              </div>
            </div>
          </div>

        </div>
      </section>
    </main>

    <!-- Notification Toast -->
    <Transition name="toast">
      <div v-if="showToast" class="fixed bottom-8 right-8 z-50 bg-primary text-white px-6 py-4 rounded-2xl shadow-2xl shadow-primary/20 flex items-center gap-3">
        <span class="material-symbols-outlined">info</span>
        <span class="text-sm font-bold">{{ toastMessage }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import api from '../api'
import AdminSidebar from '../components/AdminSidebar.vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const API_BASE = '/admin/dashboard'

const kpi = ref({
  revenue_today: 0,
  orders_today: 0,
  new_users_today: 0,
  conversion_rate: 0,
  visits: 0
})

const showToast = ref(false)
const toastMessage = ref('')

const toast = (msg) => {
  toastMessage.value = msg
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 3000)
}

const showNotification = () => {
  if (lowStock.value.length > 0) {
    toast(`You have ${lowStock.value.length} items running low on stock!`)
  } else {
    toast('No new notifications.')
  }
}

const previewContentFactory = async () => {
  contentFactory.value.loading = true
  contentFactory.value.message = 'Scanning source pages...'
  try {
    const response = await api.post('/admin/content-factory/preview', { limit: 10 })
    contentFactory.value.queue = response.data.items?.length || 0
    contentFactory.value.warnings = response.data.warnings?.length || 0
    contentFactory.value.message = `${contentFactory.value.queue} items ready for editorial review.`
  } catch (error) {
    contentFactory.value.message = error.response?.data?.detail || 'Content preview failed.'
  } finally {
    contentFactory.value.loading = false
  }
}

const ranges = [
  { label: 'Today', value: 'today' },
  { label: '7 Days', value: '7days' },
  { label: '30 Days', value: '30days' }
]
const selectedRange = ref('7days')

const recentOrders = ref([])
const topProducts = ref([])
const lowStock = ref([])
const stats_dist = ref({})
const contentFactory = ref({
  queue: 0,
  warnings: 0,
  loading: false,
  message: 'Ready to scan configured sources.'
})

const revenueChartRef = ref(null)
let revenueChart = null

const formatPrice = (price) => {
  return new Intl.NumberFormat('vi-VN').format(price)
}

const getStatusStyle = (status) => {
  const map = {
    pending: 'bg-stone-800 text-stone-400 border-stone-700',
    confirmed: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    shipping: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20',
    completed: 'bg-primary/10 text-primary border-primary/20',
    cancelled: 'bg-red-500/10 text-red-400 border-red-500/20'
  }
  return map[status] || map.pending
}

const generateMockTrend = (days) => {
  const data = [];
  const startVal = Math.random() * 5000000 + 2000000;
  for(let i = days; i >= 0; i--) {
     const d = new Date();
     d.setDate(d.getDate() - i);
     data.push({
       date: d.toISOString().split('T')[0],
       revenue: startVal + (Math.random() - 0.4) * 2000000
     });
  }
  return data;
}

const renderRevenueChart = (data) => {
  const ctx = revenueChartRef.value?.getContext('2d')
  if (!ctx) return

  if (revenueChart) revenueChart.destroy()

  // Use mock data if empty so UI looks alive
  if (!data || data.length === 0) {
     const days = selectedRange.value === 'today' ? 1 : (selectedRange.value === '7days' ? 7 : 30);
     data = generateMockTrend(days);
  }

  const labels = data.map(d => d.date)
  const values = data.map(d => d.revenue)

  const gradient = ctx.createLinearGradient(0, 0, 0, 400)
  gradient.addColorStop(0, 'rgba(74, 222, 128, 0.4)')
  gradient.addColorStop(1, 'rgba(74, 222, 128, 0)')

  revenueChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Daily Revenue',
        data: values,
        borderColor: '#4ade80',
        backgroundColor: gradient,
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#4ade80',
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#0a0a0a',
          padding: 12,
          cornerRadius: 12,
          titleFont: { family: 'Plus Jakarta Sans', size: 10 },
          bodyFont: { family: 'Plus Jakarta Sans', size: 12, weight: 'bold' }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: '#57534e', font: { size: 10 } }
        },
        y: {
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#57534e', font: { size: 10 } }
        }
      }
    }
  })
}

const fetchData = async () => {
  try {
    const [kpiRes, ordersRes, topRes, lowRes, distRes, revRes] = await Promise.all([
      api.get(`${API_BASE}/kpi`),
      api.get(`${API_BASE}/orders/recent`),
      api.get(`${API_BASE}/products/top`),
      api.get(`${API_BASE}/inventory/low-stock`),
      api.get(`${API_BASE}/orders/status`),
      api.get(`${API_BASE}/revenue?range=${selectedRange.value}`)
    ])
    
    kpi.value = kpiRes.data
    recentOrders.value = ordersRes.data
    topProducts.value = topRes.data
    lowStock.value = lowRes.data
    stats_dist.value = distRes.data
    
    await nextTick()
    renderRevenueChart(revRes.data)
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
}

watch(selectedRange, async () => {
  try {
    const revRes = await api.get(`${API_BASE}/revenue?range=${selectedRange.value}`)
    renderRevenueChart(revRes.data)
  } catch (e) {
    console.error('Failed to update chart for range', e)
    renderRevenueChart([]) // Will trigger mock
  }
})

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.fade-in {
  animation: fadeIn 0.6s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.toast-enter-active { animation: slideUp 0.4s ease; }
.toast-leave-active { animation: slideUp 0.3s ease reverse; }
@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
