<template>
  <main class="pt-20 flex min-h-screen fade-in">
    <!-- SideNavBar -->
    <aside class="hidden md:flex flex-col p-4 space-y-2 h-[calc(100vh-80px)] w-64 bg-[#f6f3ee] dark:bg-stone-800 text-primary dark:text-stone-100 font-body text-sm font-medium sticky top-20">
      <div class="flex items-center space-x-3 px-2 py-4 mb-4">
        <div class="w-10 h-10 rounded-full bg-app-surface-container-highest overflow-hidden">
          <div class="w-full h-full bg-primary flex items-center justify-center text-white font-bold">A</div>
        </div>
        <div>
          <p class="text-lg font-bold text-primary dark:text-app-text">{{ user.full_name || 'Valued Customer' }}</p>
          <p class="text-xs text-stone-500">Botanical Member</p>
        </div>
      </div>
      
      <a v-for="link in navLinks" :key="link.name" 
         href="#" 
         :class="['flex items-center gap-3 p-3 transition-all duration-200 rounded-lg', link.active ? 'bg-white dark:bg-stone-700 text-primary shadow-sm font-bold' : 'text-stone-600 dark:text-stone-400 hover:bg-stone-200/50 hover:pl-2']"
      >
        <span class="material-symbols-outlined" :style="link.active ? 'font-variation-settings: \'FILL\' 1;' : ''">{{ link.icon }}</span>
        <span>{{ link.label }}</span>
      </a>

      <div class="mt-auto pt-6 px-2">
        <RouterLink to="/" class="w-full py-3 bg-primary text-on-primary rounded-xl font-bold flex items-center justify-center gap-2 shadow-sm hover:bg-primary-container transition-all">
          <span>View Storefront</span>
        </RouterLink>
      </div>
    </aside>

    <!-- Main Content Area -->
    <section class="flex-1 bg-app-surface p-8 md:p-12 overflow-y-auto">
      <div class="max-w-5xl mx-auto space-y-16">
        <!-- Header Section -->
        <header class="space-y-2">
          <h1 class="text-4xl md:text-5xl font-bold italic text-primary">Your Botanical Journey</h1>
          <p class="text-secondary text-lg">Manage your orders and preferences from your verdant sanctuary.</p>
        </header>

        <!-- Order History Section -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
          <div class="lg:col-span-2 space-y-8">
            <div class="flex items-center justify-between">
              <h2 class="text-2xl font-bold text-primary">Order History</h2>
              <button class="text-sm font-semibold underline underline-offset-4 text-primary">Download Statements</button>
            </div>
            
            <div class="bg-app-surface-container-low rounded-xl overflow-hidden shadow-sm">
              <div v-if="orders.length === 0" class="p-12 text-center text-stone-500 italic">
                No orders discovered yet. Let's start your journey!
              </div>
              <table v-else class="w-full text-left border-collapse">
                <thead class="bg-app-surface-container-high text-primary/70 uppercase text-[10px] tracking-widest font-bold">
                  <tr>
                    <th class="px-6 py-4">Order ID</th>
                    <th class="px-6 py-4">Date</th>
                    <th class="px-6 py-4">Status</th>
                    <th class="px-6 py-4">Total</th>
                    <th class="px-6 py-4">Action</th>
                  </tr>
                </thead>
                <tbody class="text-app-text">
                  <tr v-for="order in orders" :key="order.id" class="hover:bg-app-surface-container transition-colors">
                    <td class="px-6 py-5 font-medium">#VM-{{ order.id }}</td>
                    <td class="px-6 py-5 text-stone-500">{{ formatDate(order.created_at) }}</td>
                    <td class="px-6 py-5">
                      <span class="px-3 py-1 bg-secondary-container text-on-secondary-container text-xs rounded-full font-bold">
                        {{ order.status || 'Processing' }}
                      </span>
                    </td>
                    <td class="px-6 py-5 font-semibold text-primary">{{ formatPrice(order.total_price) }}đ</td>
                    <td class="px-6 py-5">
                      <button class="text-primary hover:opacity-70 transition-opacity font-bold text-sm">View Order</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Sidebar Promo Card -->
          <div class="lg:col-span-1 space-y-6">
            <div class="relative bg-primary p-8 rounded-xl text-on-primary overflow-hidden group">
              <div class="relative z-10 space-y-4">
                <h3 class="text-2xl font-serif">The Green Thumb Club</h3>
                <p class="text-sm opacity-80 leading-relaxed">You've reached 'Bloom' status. Enjoy exclusive early access to our seasonal harvests.</p>
                <button class="mt-4 px-6 py-3 bg-app-surface text-primary rounded-xl text-sm font-bold hover:bg-app-surface-container-low transition-all">Redeem Rewards</button>
              </div>
              <div class="absolute -right-12 -bottom-12 opacity-20 transform group-hover:scale-110 transition-transform duration-500">
                <span class="material-symbols-outlined text-[120px]">psychology_alt</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Addresses Section -->
        <div class="space-y-8 pt-8">
          <div class="flex items-center justify-between">
            <h2 class="text-2xl font-bold text-primary">Saved Addresses</h2>
            <button class="flex items-center gap-2 px-6 py-3 border-2 border-outline-variant/30 text-primary rounded-xl font-bold hover:bg-app-surface-container-low transition-all">
              <span class="material-symbols-outlined text-sm">add</span>
              <span>Add New Address</span>
            </button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-app-surface-container-low p-8 rounded-xl space-y-4 flex flex-col border-2 border-primary/10">
              <div class="flex justify-between items-start">
                <span class="bg-primary text-on-primary px-3 py-1 text-[10px] uppercase font-extrabold tracking-widest rounded-full">Default</span>
                <div class="flex gap-2">
                  <button class="p-2 hover:bg-app-surface-container-highest rounded-full transition-colors"><span class="material-symbols-outlined text-sm">edit</span></button>
                </div>
              </div>
              <div>
                <p class="font-bold text-lg text-primary">Home Sanctuary</p>
                <p class="text-app-text-variant leading-relaxed">
                  {{ user.address || 'Hồ Chí Minh, Việt Nam' }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const user = ref({})
const orders = ref([])

const navLinks = [
  { name: 'profile', label: 'My Profile', icon: 'person', active: true },
  { name: 'orders', label: 'Order History', icon: 'local_shipping', active: false },
  { name: 'addresses', label: 'Saved Addresses', icon: 'home', active: false },
]

const formatPrice = (price) => {
  return new Intl.NumberFormat('vi-VN').format(price)
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const fetchData = async () => {
  try {
    if (!authStore.user) return
    
    // Use fallback ID 8 if session is old and lacks ID
    const userId = authStore.user.id || 8 
    
    try {
      const userResponse = await api.get(`/users/${userId}`)
      user.value = userResponse.data
    } catch {
      user.value = authStore.user
    }
    
    try {
      const ordersResponse = await api.get('/orders/my-orders')
      orders.value = ordersResponse.data
    } catch (e) {
      console.warn('Orders endpoint empty or failed.', e)
    }
  } catch (error) {
    console.error('Lỗi khi tải thông tin tài khoản:', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>
