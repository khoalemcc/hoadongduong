<template>
  <div class="min-h-screen bg-stone-950 text-stone-100 font-body flex fade-in">
    <!-- SideNavBar -->
    <aside class="h-screen w-64 fixed left-0 top-0 border-r border-stone-800 bg-stone-950 flex flex-col p-4 overflow-y-auto z-50">
      <div class="mb-10 px-4">
        <h1 class="text-emerald-400 font-serif italic text-2xl">Botanical Admin</h1>
        <p class="font-headline text-xs tracking-wide text-stone-500 uppercase mt-1">Management Portal</p>
      </div>
      <nav class="flex-1 space-y-2">
        <RouterLink v-for="link in navLinks" :key="link.name" 
                    :to="link.to" 
                    :class="['flex items-center gap-3 px-4 py-3 transition-colors duration-200 rounded-lg group', $route.path === link.to ? 'text-emerald-400 bg-stone-900 font-bold' : 'text-stone-400 hover:bg-stone-900/50 hover:text-emerald-300']">
          <span class="material-symbols-outlined text-xl">{{ link.icon }}</span>
          <span class="font-headline text-sm tracking-wide">{{ link.label }}</span>
        </RouterLink>
      </nav>
      <div class="mt-auto pt-6 border-t border-stone-800">
        <button class="w-full bg-emerald-500 text-stone-950 font-bold py-3 px-4 rounded-xl flex items-center justify-center gap-2 scale-95 active:duration-100 transition-transform">
          <span class="material-symbols-outlined">add</span>
          New Product
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="ml-64 pt-24 px-8 pb-12 flex-1 flex flex-col min-h-screen bg-stone-950">
      <!-- TopAppBar -->
      <header class="fixed top-0 right-0 left-64 h-16 bg-stone-950/80 backdrop-blur-md z-40 border-b border-stone-800/50 flex items-center px-8 shadow-xl">
        <div class="flex items-center flex-1 max-w-xl">
          <div class="relative w-full group">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-stone-500 group-focus-within:text-emerald-500">search</span>
            <input class="w-full bg-stone-900/5 border-stone-800 border rounded-full py-2 pl-10 pr-4 text-sm text-stone-200 focus:ring-1 focus:ring-emerald-900 placeholder-stone-600 transition-all bg-stone-900/50" placeholder="Search product directory..." type="text"/>
          </div>
        </div>
        <div class="flex items-center gap-6 ml-6">
          <button class="text-stone-400 hover:text-emerald-300 transition-opacity"><span class="material-symbols-outlined">notifications</span></button>
          <div class="h-8 w-8 rounded-full overflow-hidden border border-stone-800 bg-stone-900 flex items-center justify-center">
             <span class="text-[10px] font-bold text-emerald-400">AM</span>
          </div>
        </div>
      </header>

      <div class="flex justify-between items-end mb-10 w-full">
        <div>
          <h2 class="font-headline text-4xl font-bold text-stone-100">Product Inventory</h2>
          <p class="text-stone-500 mt-2 font-body">Manage your botanical collections and stock levels.</p>
        </div>
        <div class="flex gap-3">
          <button class="bg-stone-900 text-stone-300 px-4 py-2.5 rounded-lg text-sm font-medium flex items-center gap-2 hover:bg-stone-800 transition-colors">
            <span class="material-symbols-outlined text-sm">filter_list</span> Filters
          </button>
          <button class="bg-stone-900 text-stone-300 px-4 py-2.5 rounded-lg text-sm font-medium flex items-center gap-2 hover:bg-stone-800 transition-colors">
            <span class="material-symbols-outlined text-sm">file_download</span> Export CSV
          </button>
        </div>
      </div>

      <!-- Data Table -->
      <div class="bg-stone-900/30 rounded-xl overflow-hidden border border-stone-800/50 backdrop-blur-sm shadow-2xl w-full">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-stone-900/50">
              <th class="px-6 py-4 text-xs font-semibold text-stone-500 uppercase tracking-wider">Product</th>
              <th class="px-6 py-4 text-xs font-semibold text-stone-500 uppercase tracking-wider">Category</th>
              <th class="px-6 py-4 text-xs font-semibold text-stone-500 uppercase tracking-wider">Stock Level</th>
              <th class="px-6 py-4 text-xs font-semibold text-stone-500 uppercase tracking-wider">Price</th>
              <th class="px-6 py-4 text-xs font-semibold text-stone-500 uppercase tracking-wider">Status</th>
              <th class="px-6 py-4 text-xs font-semibold text-stone-500 uppercase tracking-wider text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-stone-800">
            <tr v-for="product in products" :key="product.id" class="hover:bg-stone-800/20 transition-colors">
              <td class="px-6 py-5">
                <div class="flex items-center gap-4">
                  <div class="w-12 h-12 rounded-lg overflow-hidden bg-stone-800 shrink-0 flex items-center justify-center">
                    <img v-if="product.image_url" :src="product.image_url" class="h-full w-full object-cover" alt="prod"/>
                    <span v-else class="material-symbols-outlined text-stone-600">image</span>
                  </div>
                  <div>
                    <p class="font-headline text-stone-100 text-base">{{ product.name }}</p>
                    <p class="text-stone-500 text-xs text-left">SKU: BOT-{{ product.id }}-H</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-5">
                <span class="px-3 py-1 bg-emerald-950/30 text-emerald-400 text-xs font-medium rounded-full border border-emerald-900/30">{{ product.category || 'Herbals' }}</span>
              </td>
              <td class="px-6 py-5">
                <div class="flex flex-col gap-1">
                  <div class="flex items-center gap-2">
                    <div class="w-24 h-1.5 bg-stone-800 rounded-full overflow-hidden">
                      <div :class="['h-full transition-all', (product.stock || 20) < 15 ? 'bg-amber-500' : 'bg-emerald-500']" :style="{ width: (product.stock || 20) + '%' }"></div>
                    </div>
                    <span :class="['text-xs font-bold', (product.stock || 20) < 15 ? 'text-amber-500' : 'text-stone-300']">
                      {{ product.stock || 20 }} Units
                    </span>
                  </div>
                  <span v-if="(product.stock || 20) < 15" class="text-[10px] text-amber-600/80 uppercase font-bold tracking-tighter text-left">Low Stock Warning</span>
                </div>
              </td>
              <td class="px-6 py-5 font-medium text-stone-200">{{ formatPrice(product.price) }}đ</td>
              <td class="px-6 py-5">
                <div class="flex items-center gap-2 text-emerald-400 text-xs">
                  <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Published
                </div>
              </td>
              <td class="px-6 py-5 text-right">
                <button class="text-stone-500 hover:text-stone-200 transition-colors">
                  <span class="material-symbols-outlined">more_horiz</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <!-- Pagination Footer -->
        <div class="px-6 py-4 bg-stone-900/50 flex justify-between items-center border-t border-stone-800">
          <p class="text-xs text-stone-500">Showing {{ products.length }} items</p>
          <div class="flex gap-2">
            <button class="p-2 text-stone-500 hover:text-stone-200 bg-stone-800/50 rounded-lg" disabled>
              <span class="material-symbols-outlined text-sm">chevron_left</span>
            </button>
            <button class="px-3 py-1 text-xs font-medium text-emerald-400 bg-emerald-950/40 rounded-lg border border-emerald-900/50">1</button>
            <button class="p-2 text-stone-400 hover:text-stone-200 bg-stone-800/50 rounded-lg">
              <span class="material-symbols-outlined text-sm">chevron_right</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Analytics Widgets -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12 w-full">
        <div v-for="widget in widgets" :key="widget.label" class="bg-stone-900/40 p-6 rounded-xl border border-stone-800/50 shadow-lg">
          <div class="flex justify-between items-start mb-4 text-left">
            <span :class="['material-symbols-outlined p-2 rounded-lg', widget.colorClass]">{{ widget.icon }}</span>
            <span v-if="widget.trend" :class="['text-xs font-bold px-2 py-0.5 rounded', widget.trendClass]">{{ widget.trend }}</span>
          </div>
          <p class="text-stone-500 text-sm font-medium uppercase tracking-wider text-left">{{ widget.label }}</p>
          <h3 class="font-headline text-3xl font-bold text-stone-100 mt-1 text-left">{{ widget.value }}</h3>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const products = ref([])

const navLinks = [
  { name: 'dashboard', label: 'Dashboard', icon: 'dashboard', to: '/admin' },
  { name: 'orders', label: 'Orders', icon: 'shopping_bag', to: '/admin/orders' },
  { name: 'blog', label: 'Blog', icon: 'article', to: '/admin/blog' },
  { name: 'analytics', label: 'Reports', icon: 'bar_chart', to: '/admin/analytics' },
  { name: 'inventory', label: 'Products', icon: 'inventory_2', to: '/admin/products' }
]

const widgets = [
  { label: 'Total Sales (Monthly)', value: '42,910kđ', icon: 'trending_up', colorClass: 'text-emerald-500 bg-emerald-500/10', trend: '+12.4%', trendClass: 'text-emerald-500 bg-emerald-500/10' },
  { label: 'Low Stock Items', value: '14', icon: 'inventory', colorClass: 'text-stone-400 bg-stone-800', trend: '3 Alert', trendClass: 'text-amber-500 bg-amber-500/10' },
  { label: 'Active Shipments', value: '86', icon: 'local_shipping', colorClass: 'text-stone-400 bg-stone-800' }
]

const formatPrice = (price) => {
  return new Intl.NumberFormat('vi-VN').format(price)
}

const fetchProducts = async () => {
  try {
    const response = await api.get('/products/')
    products.value = response.data
  } catch (error) {
    console.error('Lỗi khi lấy danh sách sản phẩm:', error)
  }
}

onMounted(() => {
  fetchProducts()
})
</script>
