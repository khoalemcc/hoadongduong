<template>
  <main class="pt-32 pb-24 px-4 sm:px-8 max-w-7xl mx-auto fade-in">
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
      <!-- Main Content Area: Steps -->
      <div class="lg:col-span-8 space-y-12">
        <!-- Progress Indicator -->
        <nav aria-label="Progress" class="mb-12">
          <ol class="flex items-center space-x-4" role="list">
            <li class="flex items-center">
              <span class="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-white font-bold text-sm">1</span>
              <span class="ml-3 text-sm font-bold text-primary">Shipping Info</span>
            </li>
            <li class="flex items-center">
              <span class="h-px w-8 bg-outline-variant mx-2"></span>
              <span class="flex h-8 w-8 items-center justify-center rounded-full border-2 border-outline-variant text-stone-400 font-bold text-sm">2</span>
              <span class="ml-3 text-sm font-medium text-stone-400">Confirmation</span>
            </li>
          </ol>
        </nav>

        <!-- Step 1: Shipping Address -->
        <section class="space-y-8">
          <div class="border-b border-surface-container-highest pb-4">
            <h1 class="font-headline text-3xl font-bold text-primary tracking-tight">Shipping Details</h1>
            <p class="text-app-text-variant mt-2">Where should we deliver your botanical collection?</p>
          </div>
          <form @submit.prevent class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="md:col-span-2">
              <label class="block text-xs font-bold text-secondary uppercase tracking-widest mb-2">Full Name</label>
              <input v-model="form.fullName" class="w-full h-14 px-5 rounded-xl border-none bg-app-surface-container-low text-app-text focus:ring-1 focus:ring-primary transition-all placeholder:text-stone-400" placeholder="Enter your full name" type="text"/>
            </div>
            <div class="md:col-span-2">
              <label class="block text-xs font-bold text-secondary uppercase tracking-widest mb-2">Street Address</label>
              <input v-model="form.address" class="w-full h-14 px-5 rounded-xl border-none bg-app-surface-container-low text-app-text focus:ring-1 focus:ring-primary transition-all placeholder:text-stone-400" placeholder="Street name and house number" type="text"/>
            </div>
            <div>
              <label class="block text-xs font-bold text-secondary uppercase tracking-widest mb-2">City</label>
              <input v-model="form.city" class="w-full h-14 px-5 rounded-xl border-none bg-app-surface-container-low text-app-text focus:ring-1 focus:ring-primary transition-all placeholder:text-stone-400" placeholder="City" type="text"/>
            </div>
            <div>
              <label class="block text-xs font-bold text-secondary uppercase tracking-widest mb-2">Phone Number</label>
              <input v-model="form.phone" class="w-full h-14 px-5 rounded-xl border-none bg-app-surface-container-low text-app-text focus:ring-1 focus:ring-primary transition-all placeholder:text-stone-400" placeholder="+84 ..." type="tel"/>
            </div>
          </form>
        </section>

        <!-- Step 2: Payment -->
        <section class="space-y-8">
          <div class="border-b border-surface-container-highest pb-4">
            <h2 class="font-headline text-2xl font-bold text-primary tracking-tight">Payment Method</h2>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div 
              v-for="method in paymentMethods" 
              :key="method.id"
              @click="selectedPayment = method.id"
              :class="['group relative flex flex-col items-center justify-center p-6 rounded-2xl bg-app-surface-container-low border-2 transition-all cursor-pointer', selectedPayment === method.id ? 'border-primary ring-4 ring-primary/5' : 'border-transparent hover:border-primary/20']"
            >
              <div class="h-10 w-24 mb-3 rounded-lg flex items-center justify-center overflow-hidden" :class="method.bgColor || 'bg-[#fcf9f4]'">
                 <span v-if="method.icon" class="material-symbols-outlined text-primary">{{ method.icon }}</span>
                 <span v-if="method.text" :class="method.textColor" class="font-black text-xs">{{ method.text }}</span>
              </div>
              <span class="text-xs font-bold uppercase tracking-widest">{{ method.label }}</span>
              <div v-if="selectedPayment === method.id" class="absolute top-2 right-2">
                <span class="material-symbols-outlined text-primary text-sm">check_circle</span>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Sidebar: Order Summary -->
      <div class="lg:col-span-4">
        <div class="sticky top-28 space-y-6">
          <div class="bg-app-surface-container-low rounded-[32px] p-8 shadow-2xl border border-white/5">
            <h2 class="font-headline text-xl font-bold text-primary mb-8">Order Summary</h2>
            
            <!-- Item List -->
            <div class="space-y-6 mb-8 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
              <div v-for="item in cartStore.items" :key="item.id" class="flex gap-4">
                <div class="h-20 w-16 bg-white rounded-xl overflow-hidden flex-shrink-0 shadow-sm border border-stone-100">
                  <img :src="item.image" class="w-full h-full object-cover" :alt="item.name"/>
                </div>
                <div class="flex-1">
                  <h4 class="text-sm font-bold text-primary leading-snug line-clamp-1">{{ item.name }}</h4>
                  <p class="text-[10px] text-stone-500 mt-1 uppercase tracking-widest">Qty: {{ item.quantity }}</p>
                  <p class="text-sm font-bold text-primary mt-1">{{ formatPrice(item.price * item.quantity) }}đ</p>
                </div>
              </div>

              <div v-if="cartStore.items.length === 0" class="text-center py-12">
                <span class="material-symbols-outlined text-stone-300 text-5xl mb-4">shopping_bag</span>
                <p class="text-stone-500 italic text-sm">Your bag is currently empty.</p>
                <RouterLink to="/shop" class="text-primary font-bold text-xs uppercase tracking-widest mt-4 block hover:underline">Back to Shop</RouterLink>
              </div>
            </div>

            <!-- Financials -->
            <div class="space-y-4 border-t border-outline-variant/20 pt-8 text-sm">
              <div class="flex justify-between items-center">
                <span class="text-stone-500 font-medium">Subtotal</span>
                <span class="font-bold text-primary">{{ formatPrice(subtotal) }}đ</span>
              </div>
              <div class="flex justify-between items-center text-xs">
                <span class="text-stone-500">Shipping</span>
                <span class="font-medium text-primary">{{ formatPrice(shippingFee) }}đ</span>
              </div>
              <div class="flex justify-between pt-6 text-xl font-bold text-primary border-t border-outline-variant/20 mt-2">
                <span class="font-headline">Total</span>
                <span class="font-headline">{{ formatPrice(total) }}đ</span>
              </div>
            </div>

            <!-- Action Button -->
            <button 
              @click="handlePlaceOrder"
              :disabled="loading || cartStore.items.length === 0"
              class="w-full mt-10 h-16 bg-primary text-white rounded-2xl font-bold flex items-center justify-center gap-3 hover:opacity-90 transition-all active:scale-[0.98] disabled:opacity-30 shadow-xl shadow-primary/10"
            >
              <span v-if="loading" class="animate-spin material-symbols-outlined">progress_activity</span>
              <span v-else>{{ 'Complete Order' }}</span>
              <span v-if="!loading" class="material-symbols-outlined text-sm">arrow_forward</span>
            </button>
            
            <p class="text-[10px] text-center text-stone-400 mt-6 px-4 leading-relaxed">
              Transparent & Ethical. All orders are processed with Carbon Neutral shipping.
            </p>
          </div>

          <div class="p-8 border border-outline-variant/10 rounded-3xl bg-app-surface-container-low/50 italic text-sm text-stone-500 text-center leading-relaxed font-serif">
            "We do not inherit the earth from our ancestors, we borrow it from our children."
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed } from 'vue'
import api from '../api'
import { useRouter, RouterLink } from 'vue-router'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

const loading = ref(false)
const selectedPayment = ref('cod')
const shippingFee = ref(35000)

const form = ref({
  fullName: authStore.user?.full_name || '',
  address: '',
  city: '',
  phone: ''
})

const paymentMethods = [
  { id: 'cod', label: 'Cash on Delivery', icon: 'local_shipping', text: '' },
  { id: 'momo', label: 'MoMo Wallet', text: 'MOMO', bgColor: 'bg-[#a50064]', textColor: 'text-white' },
  { id: 'vnpay', label: 'VNPAY', text: 'VNPAY', bgColor: 'bg-[#005ba1]', textColor: 'text-white' }
]

const subtotal = computed(() => {
  return cartStore.items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
})

const total = computed(() => subtotal.value + shippingFee.value)

const formatPrice = (price) => {
  return new Intl.NumberFormat('vi-VN').format(price)
}

const handlePlaceOrder = async () => {
  if (!authStore.user?.id) {
    alert('Vui lòng đăng nhập trước khi đặt hàng.')
    router.push('/login')
    return
  }

  if (!form.value.fullName || !form.value.phone || !form.value.address) {
    alert('Xin vui lòng điền đầy đủ thông tin giao hàng.')
    return
  }

  loading.value = true
  try {
    const orderData = {
      status: 'pending',
      payment_method: selectedPayment.value,
      shipping_fee: shippingFee.value.toString(),
      shipping_address: `${form.value.fullName} - ${form.value.phone} - ${form.value.address}, ${form.value.city}`,
      items: cartStore.items.map(item => ({
        product_id: item.id,
        quantity: item.quantity
      }))
    }

    const response = await api.post('/orders/', orderData)
    
    // Clear cart on success
    cartStore.clearCart()
    
    router.push({ name: 'order-success', query: { id: response.data.id } })
  } catch (error) {
    console.error('Lỗi khi đặt hàng:', error)
    alert('Có lỗi xảy ra khi đặt hàng. Vui lòng thử lại sau.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #e5e2dd;
  border-radius: 10px;
}
</style>
