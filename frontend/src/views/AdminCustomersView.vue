<template>
  <div class="min-h-screen flex bg-app-bg text-app-text font-body fade-in">
    <!-- Shared Sidebar -->
    <AdminSidebar />

    <main class="flex-1 min-w-0 flex flex-col bg-app-bg">
      <header class="h-20 px-8 flex items-center justify-between bg-app-bg border-b border-white/5">
        <div>
          <h2 class="text-2xl font-headline font-bold text-white">Community & Patronage</h2>
          <p class="text-[10px] font-black uppercase tracking-widest text-stone-500 mt-1">Manage your botanical society members</p>
        </div>
        <div class="flex items-center gap-6">
          <button @click="openModal()" class="px-6 py-2.5 bg-primary text-black text-[10px] font-black uppercase tracking-widest rounded-xl hover:bg-primary/90 transition-all shadow-lg shadow-primary/20">
            Enlist New Patron
          </button>
          <div class="px-4 py-2 bg-app-surface border border-white/5 rounded-xl flex items-center gap-3">
             <span class="text-[10px] font-black uppercase tracking-widest text-stone-500">Member Base</span>
             <span class="text-primary font-bold">{{ customers.length }}</span>
          </div>
        </div>
      </header>

      <section class="p-8">
        <div class="bg-app-surface rounded-2xl border border-white/5 overflow-hidden shadow-2xl">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="text-stone-500 text-[10px] font-black uppercase tracking-widest border-b border-white/5 bg-app-surface/50">
                <th class="py-6 px-8">Patron Identity</th>
                <th class="py-6 px-6">Email Address</th>
                <th class="py-6 px-6">Joined Harvest</th>
                <th class="py-6 px-6 text-center">Status</th>
                <th class="py-6 px-8 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
              <tr v-for="user in customers" :key="user.id" class="hover:bg-app-surface transition-colors group">
                <td class="py-5 px-8 flex items-center gap-5">
                  <div class="w-12 h-12 rounded-full bg-primary/20 text-primary flex items-center justify-center font-black text-xs border border-primary/20 shadow-inner">
                    {{ user.full_name?.[0] || user.email?.[0].toUpperCase() }}
                  </div>
                  <div class="flex flex-col">
                    <span class="font-bold text-sm text-white">{{ user.full_name || 'Anonymous Patron' }}</span>
                    <span class="text-[9px] text-stone-500 uppercase tracking-widest mt-1">ID: #{{ user.id }}</span>
                  </div>
                </td>
                <td class="py-5 px-6 text-sm text-stone-400 font-medium">{{ user.email }}</td>
                <td class="py-5 px-6 text-xs text-stone-500">{{ formatDate(user.created_at) }}</td>
                <td class="py-5 px-6 text-center">
                  <span :class="['px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-widest border border-white/5', user.status === 'active' || !user.status ? 'bg-primary/10 text-primary border-primary/20' : 'bg-stone-800 text-stone-500']">
                    {{ user.status || 'Active' }}
                  </span>
                </td>
                <td class="py-5 px-8 text-right">
                  <div class="flex items-center justify-end gap-2 opacity-30 group-hover:opacity-100 transition-opacity">
                    <button @click="openModal(user)" class="p-2 text-stone-500 hover:text-primary transition-colors">
                      <span class="material-symbols-outlined text-[18px]">edit</span>
                    </button>
                    <button @click="viewHistory(user)" class="p-2 text-stone-500 hover:text-white transition-colors">
                      <span class="material-symbols-outlined text-[18px]">history</span>
                    </button>
                    <button @click="deleteCustomer(user)" class="p-2 text-stone-500 hover:text-red-500 transition-colors">
                      <span class="material-symbols-outlined text-[18px]">delete</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Unified Patron Modal (Add/Edit) -->
      <Transition name="modal">
        <div v-if="showEditModal" class="fixed inset-0 z-[70] flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-black/90 backdrop-blur-md" @click="showEditModal = false"></div>
          <div class="bg-app-surface w-full max-w-md rounded-3xl border border-white/10 shadow-2xl overflow-hidden relative z-10">
            <header class="p-8 border-b border-white/5 flex items-center justify-between">
              <h3 class="text-xl font-headline font-bold text-white">{{ editingCustomer ? 'Update Patron' : 'Enlist Patron' }}</h3>
              <button @click="showEditModal = false" class="text-stone-500 hover:text-white transition-colors">
                <span class="material-symbols-outlined">close</span>
              </button>
            </header>
            
            <form @submit.prevent="saveCustomer" class="p-8 space-y-6">
              <div class="space-y-1.5">
                <label class="text-[9px] font-black uppercase tracking-widest text-stone-500 px-1">Patron Identity (Full Name)</label>
                <input v-model="customerForm.full_name" type="text" required class="w-full bg-app-bg border border-white/5 rounded-xl px-5 py-3 text-sm text-white focus:border-primary/50 outline-none transition-all" placeholder="e.g. Alexander Green">
              </div>
              
              <div class="space-y-1.5">
                <label class="text-[9px] font-black uppercase tracking-widest text-stone-500 px-1">Email Address</label>
                <input v-model="customerForm.email" type="email" required :disabled="editingCustomer" class="w-full bg-app-bg border border-white/5 rounded-xl px-5 py-3 text-sm text-white focus:border-primary/50 outline-none transition-all disabled:opacity-50" placeholder="patron@verdantmane.com">
              </div>

              <div v-if="!editingCustomer" class="space-y-1.5">
                <label class="text-[9px] font-black uppercase tracking-widest text-stone-500 px-1">Initial Password</label>
                <input v-model="customerForm.password" type="password" required class="w-full bg-app-bg border border-white/5 rounded-xl px-5 py-3 text-sm text-white focus:border-primary/50 outline-none transition-all">
              </div>

              <div class="space-y-1.5">
                <label class="text-[9px] font-black uppercase tracking-widest text-stone-500 px-1">Lifecycle Status</label>
                <select v-model="customerForm.status" class="w-full bg-app-bg border border-white/5 rounded-xl px-5 py-3 text-sm text-white focus:border-primary/50 outline-none transition-all">
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                  <option value="banned">Banned</option>
                </select>
              </div>

              <button type="submit" class="w-full py-4 bg-primary text-black font-black uppercase tracking-[0.2em] text-[10px] rounded-2xl hover:shadow-lg hover:shadow-primary/20 transition-all mt-4">
                {{ editingCustomer ? 'Commit Changes' : 'Confirm Enlistment' }}
              </button>
            </form>
          </div>
        </div>
      </Transition>
    </main>

    <!-- Purchase History Modal -->
    <Transition name="modal">
      <div v-if="selectedCustomer" class="fixed inset-0 z-[60] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/80 backdrop-blur-md" @click="selectedCustomer = null"></div>
        <div class="bg-app-surface w-full max-w-4xl rounded-3xl border border-white/10 shadow-2xl overflow-hidden relative z-10 flex flex-col max-h-[85vh]">
          <header class="p-8 border-b border-white/5 flex items-center justify-between">
            <div>
              <h3 class="text-xl font-headline font-bold text-white">Purchase Legacy</h3>
              <p class="text-[10px] font-black uppercase tracking-widest text-stone-500 mt-1">
                Records for {{ selectedCustomer.full_name || selectedCustomer.email }}
              </p>
            </div>
            <div class="flex items-center gap-6">
               <div class="text-right">
                  <span class="block text-[9px] font-black uppercase tracking-widest text-stone-600">Total Investment</span>
                  <span class="text-xl font-black text-primary">{{ formatPrice(customerTotalSpent) }}đ</span>
               </div>
               <button @click="selectedCustomer = null" class="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center hover:bg-white/10 transition-colors">
                 <span class="material-symbols-outlined text-sm">close</span>
               </button>
            </div>
          </header>

          <div class="flex-1 overflow-y-auto p-8">
            <div v-if="customerOrders.length === 0" class="flex flex-col items-center justify-center py-20 text-stone-600">
              <span class="material-symbols-outlined text-5xl mb-4">inventory_2</span>
              <p class="font-bold uppercase tracking-widest text-[10px]">No orders found for this patron yet.</p>
            </div>
            <table v-else class="w-full text-left">
              <thead>
                <tr class="text-[9px] font-black uppercase tracking-widest text-stone-500 border-b border-white/5">
                  <th class="pb-4 px-4">Order ID</th>
                  <th class="pb-4 px-4">Harvest Date</th>
                  <th class="pb-4 px-4 text-right">Value</th>
                  <th class="pb-4 px-4 text-center">Status</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/5">
                <tr v-for="order in customerOrders" :key="order.id" class="hover:bg-white/[0.02] transition-colors">
                  <td class="py-4 px-4 text-xs font-bold text-white">#{{ order.id }}</td>
                  <td class="py-4 px-4 text-xs text-stone-400">{{ formatDate(order.created_at) }}</td>
                  <td class="py-4 px-4 text-xs text-right font-bold text-primary">{{ formatPrice(order.total_price) }}đ</td>
                  <td class="py-4 px-4 text-center">
                    <span :class="['px-2 py-0.5 rounded text-[8px] font-black uppercase tracking-widest border', 
                      order.status === 'completed' ? 'bg-primary/10 text-primary border-primary/20' : 'bg-stone-800 text-stone-500 border-white/5']">
                      {{ order.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import AdminSidebar from '../components/AdminSidebar.vue'

const customers = ref([])
const showToast = ref(false)
const toastMessage = ref('')
const selectedCustomer = ref(null)
const customerOrders = ref([])

// CRUD State
const showEditModal = ref(false)
const editingCustomer = ref(null)
const customerForm = ref({
  full_name: '',
  email: '',
  password: '',
  status: 'active'
})

const toast = (msg) => {
  toastMessage.value = msg
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 3000)
}

const openModal = (user = null) => {
  if (user) {
    editingCustomer.value = user
    customerForm.value = { 
      full_name: user.full_name, 
      email: user.email, 
      status: user.status || 'active' 
    }
  } else {
    editingCustomer.value = null
    customerForm.value = { full_name: '', email: '', password: '', status: 'active' }
  }
  showEditModal.value = true
}

const saveCustomer = async () => {
  try {
    if (editingCustomer.value) {
      await api.patch(`/users/${editingCustomer.value.id}`, {
        full_name: customerForm.value.full_name,
        status: customerForm.value.status
      })
      toast('Patron profile updated successfully.')
    } else {
      await api.post('/users/', customerForm.value)
      toast('New patron enlisted into the society.')
    }
    showEditModal.value = false
    fetchCustomers()
  } catch (err) {
    toast(err.response?.data?.detail || 'Operation failed.')
  }
}

const deleteCustomer = async (user) => {
  if (confirm(`Are you sure you want to banish ${user.full_name || user.email} from the community?`)) {
    try {
      await api.delete(`/users/${user.id}`)
      toast('Patron has been removed.')
      fetchCustomers()
    } catch (err) {
      toast('Failed to remove patron.')
    }
  }
}

const formatPrice = (price) => {
  if (!price) return '0'
  return new Intl.NumberFormat('vi-VN').format(price)
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'Genesis'
  return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const customerTotalSpent = computed(() => {
  return customerOrders.value.reduce((sum, order) => sum + parseFloat(order.total_price || 0), 0)
})

const fetchCustomers = async () => {
  try {
    const response = await api.get('/users/')
    customers.value = response.data
  } catch (error) {
    console.error('Lỗi khi lấy khách hàng:', error)
  }
}

const viewHistory = async (user) => {
  try {
    const response = await api.get(`/orders/user/${user.id}`)
    customerOrders.value = response.data
    selectedCustomer.value = user
  } catch (err) {
    toast('Error fetching patron history.')
  }
}

const contactCustomer = (user) => {
  window.location.href = `mailto:${user.email}?subject=Thông báo từ Verdant Mane`
  toast(`Đang chuyển hướng sang ứng dụng gửi Email cho ${user.email}...`)
}

onMounted(() => fetchCustomers())
</script>

<style scoped>
.toast-enter-active { animation: slideUp 0.4s ease; }
.toast-leave-active { animation: slideUp 0.3s ease reverse; }
@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
