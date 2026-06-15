<template>
  <div class="min-h-screen flex bg-app-bg text-app-text font-body fade-in">
    <!-- Shared Sidebar -->
    <AdminSidebar />

    <main class="flex-1 min-w-0 flex flex-col bg-app-bg">
      <header class="h-20 px-8 flex items-center justify-between bg-app-bg border-b border-white/5">
        <div>
          <h2 class="text-2xl font-headline font-bold text-white">Acquisitions & Orders</h2>
          <p class="text-[10px] font-black uppercase tracking-widest text-stone-500 mt-1">Manage society transactions and fulfillments</p>
        </div>
        <div class="flex items-center gap-6">
          <div class="flex bg-app-surface p-1 rounded-xl border border-white/5">
            <button @click="activeTab = 'orders'" 
                    :class="['px-4 py-2 text-[10px] font-black uppercase tracking-widest rounded-lg transition-all', activeTab === 'orders' ? 'bg-primary/20 text-primary' : 'text-stone-500 hover:text-white']">
              Manifested Orders
            </button>
            <button @click="activeTab = 'carts'" 
                    :class="['px-4 py-2 text-[10px] font-black uppercase tracking-widest rounded-lg transition-all', activeTab === 'carts' ? 'bg-primary/20 text-primary' : 'text-stone-500 hover:text-white']">
              Live Carts
            </button>
          </div>
          <button @click="openAddOrderModal()" class="px-6 py-2.5 bg-primary text-black text-[10px] font-black uppercase tracking-widest rounded-xl hover:bg-primary/90 transition-all shadow-lg shadow-primary/20">
            Manual Entry
          </button>
        </div>
      </header>

      <section class="p-8">
        <div v-if="activeTab === 'orders'" class="bg-app-surface rounded-2xl border border-white/5 overflow-hidden shadow-2xl">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="text-stone-500 text-[10px] font-black uppercase tracking-widest border-b border-white/5 bg-app-surface/50">
                <th class="py-6 px-8">Acquisition ID</th>
                <th class="py-6 px-6">Timestamp</th>
                <th class="py-6 px-6">Client Identity</th>
                <th class="py-6 px-6 text-center">Lifecycle Status</th>
                <th class="py-6 px-6 text-right">Total Valuation</th>
                <th class="py-6 px-8 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
              <tr v-for="order in orders" :key="order.id" class="hover:bg-app-surface transition-colors group">
                <td class="py-5 px-8">
                  <span class="text-[10px] font-mono font-bold text-stone-500 uppercase">VM-ORD-{{ order.id }}</span>
                </td>
                <td class="py-5 px-6 text-xs text-stone-400">
                  {{ formatDate(order.created_at) }}
                </td>
                <td class="py-5 px-6 font-bold text-sm">
                   Client #{{ order.user_id }}
                </td>
                <td class="py-5 px-6 text-center">
                  <select 
                    v-model="order.status" 
                    @change="updateStatus(order)"
                    :class="['text-[9px] font-black uppercase tracking-widest px-3 py-1.5 rounded-full border border-white/5 bg-app-surface outline-none transition-all', getStatusClass(order.status)]"
                  >
                    <option value="pending">Pending</option>
                    <option value="processing">Processing</option>
                    <option value="shipped">Shipped</option>
                    <option value="delivered">Delivered</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                </td>
                <td class="py-5 px-6 text-right font-headline font-bold text-base">
                  {{ formatPrice(order.total_price) }}đ
                </td>
                <td class="py-5 px-8 text-right">
                  <div class="flex items-center justify-end gap-3 opacity-30 group-hover:opacity-100 transition-opacity">
                    <button @click="viewDetails(order)" class="p-2 text-stone-500 hover:text-primary transition-colors">
                      <span class="material-symbols-outlined text-lg">visibility</span>
                    </button>
                    <button @click="deleteOrder(order)" class="p-2 text-stone-500 hover:text-red-500 transition-colors">
                      <span class="material-symbols-outlined text-lg">delete</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="bg-app-surface rounded-2xl border border-white/5 overflow-hidden shadow-2xl">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="text-stone-500 text-[10px] font-black uppercase tracking-widest border-b border-white/5 bg-app-surface/50">
                <th class="py-6 px-8">Patron</th>
                <th class="py-6 px-6">Cart Items</th>
                <th class="py-6 px-6 text-right">Potential Value</th>
                <th class="py-6 px-8 text-right">Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
              <tr v-for="cart in activeCarts" :key="cart.cart_id" class="hover:bg-app-surface transition-colors group">
                <td class="py-5 px-8">
                  <div class="flex flex-col">
                    <span class="font-bold text-sm text-white">{{ cart.user.full_name }}</span>
                    <span class="text-[10px] text-stone-500">{{ cart.user.email }}</span>
                  </div>
                </td>
                <td class="py-5 px-6">
                   <div class="flex flex-col gap-1">
                      <div v-for="item in cart.items" :key="item.product_name" class="text-xs text-stone-400">
                         {{ item.quantity }}x {{ item.product_name }}
                      </div>
                   </div>
                </td>
                <td class="py-5 px-6 text-right font-headline font-bold text-base text-primary">
                  {{ formatPrice(cart.total_value) }}đ
                </td>
                <td class="py-5 px-8 text-right">
                  <button class="p-2 text-stone-500 hover:text-primary transition-colors">
                    <span class="material-symbols-outlined text-lg">mail</span>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>

    <!-- Order Details Modal -->
    <div v-if="selectedOrder" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm transition-opacity">
      <div class="bg-app-surface w-full max-w-2xl rounded-3xl border border-white/5 p-8 shadow-2xl relative">
        <button @click="selectedOrder = null" class="absolute top-6 right-6 text-stone-500 hover:text-white transition-colors">
          <span class="material-symbols-outlined">close</span>
        </button>
        
        <h3 class="text-2xl font-headline font-bold mb-2">Acquisition Manifest</h3>
        <p class="text-xs text-stone-500 font-mono mb-8 uppercase">VM-ORD-{{ selectedOrder.id }}</p>
        
        <div class="grid grid-cols-2 gap-8 mb-8">
          <div>
            <p class="text-[9px] font-black uppercase tracking-widest text-stone-500 mb-2">Client Details</p>
            <p class="font-bold text-white text-sm">Client #{{ selectedOrder.user_id }}</p>
            <p class="text-stone-400 text-xs mt-1">Acquired on {{ formatDate(selectedOrder.created_at) }}</p>
          </div>
          <div>
            <p class="text-[9px] font-black uppercase tracking-widest text-stone-500 mb-2">Lifecycle Stage</p>
            <span :class="['px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-widest border', getStatusClass(selectedOrder.status)]">
              {{ selectedOrder.status }}
            </span>
          </div>
        </div>

        <div class="border-t border-white/5 pt-6">
          <p class="text-[9px] font-black uppercase tracking-widest text-stone-500 mb-4">Financial Ledger</p>
          <div class="flex justify-between items-center bg-app-bg p-4 rounded-xl border border-white/5">
             <span class="text-sm font-bold text-stone-400">Total Valuation</span>
             <span class="text-2xl font-headline font-bold text-primary">{{ formatPrice(selectedOrder.total_price) }}đ</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Notification Toast -->
    <Transition name="toast">
      <div v-if="showToast" class="fixed bottom-8 right-8 z-50 bg-primary text-black px-6 py-4 rounded-2xl shadow-2xl shadow-primary/20 flex items-center gap-3 border border-white/10">
        <span class="material-symbols-outlined">info</span>
        <span class="text-sm font-black uppercase tracking-widest">{{ toastMessage }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import AdminSidebar from '../components/AdminSidebar.vue'

const orders = ref([])
const activeCarts = ref([])
const activeTab = ref('orders')
const showToast = ref(false)
const toastMessage = ref('')

const toast = (msg) => {
  toastMessage.value = msg
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 3000)
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('vi-VN').format(price)
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  return new Date(dateStr).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusClass = (status) => {
  switch (status?.toLowerCase()) {
    case 'delivered': return 'text-primary border-primary/20 bg-primary/10'
    case 'processing': return 'text-amber-500 border-amber-500/20 bg-amber-500/10'
    case 'shipped': return 'text-blue-500 border-blue-500/20 bg-blue-500/10'
    case 'cancelled': return 'text-error border-error/20 bg-error/10'
    default: return 'text-stone-400 border-white/5 bg-white/5'
  }
}

const fetchOrders = async () => {
  try {
    const response = await api.get('/orders/')
    orders.value = response.data
  } catch (error) {
    console.error('Lỗi khi lấy danh sách đơn hàng:', error)
  }
}

const fetchActiveCarts = async () => {
  try {
    const response = await api.get('/admin/dashboard/active-carts')
    activeCarts.value = response.data
  } catch (error) {
    console.error('Lỗi khi lấy giỏ hàng đang chờ:', error)
  }
}

const updateStatus = async (order) => {
  try {
    await api.patch(`/orders/${order.id}/status?status=${order.status}`)
    toast('Order status updated.')
  } catch (err) {
    toast('Failed to update status.')
  }
}

const deleteOrder = async (order) => {
  if (confirm(`Are you sure you want to strike VM-ORD-${order.id} from the records?`)) {
    try {
      await api.delete(`/orders/${order.id}`)
      toast('Order successfully expunged.')
      fetchOrders()
    } catch (err) {
      toast('Failed to delete order.')
    }
  }
}

const openAddOrderModal = () => {
  toast('Manual entry system initializing... (Feature coming in next update)')
}

const selectedOrder = ref(null)

const viewDetails = (order) => {
  selectedOrder.value = order
}

onMounted(() => {
  fetchOrders()
  fetchActiveCarts()
})
</script>
