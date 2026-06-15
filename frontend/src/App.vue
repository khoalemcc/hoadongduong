<template>
  <div class="bg-app-bg text-app-text font-body selection:bg-primary/20 selection:text-primary min-h-screen">
    <!-- TopNavBar -->
    <nav v-if="!isAdminRoute" class="fixed top-0 w-full z-50 bg-[#fcf9f4]/80 dark:bg-stone-900/80 backdrop-blur-md shadow-sm dark:shadow-none flex justify-between items-center px-8 h-20 max-w-full mx-auto font-headline text-base tracking-tight">
      <div class="flex items-center gap-12">
        <RouterLink to="/" class="text-2xl font-bold italic text-primary dark:text-[#fcf9f4]">Verdant Mane</RouterLink>
        <div class="hidden md:flex gap-8 items-center">
          <RouterLink to="/shop" class="text-stone-500 hover:text-primary transition-colors hover:opacity-80 transition-all duration-300">Shop</RouterLink>
          <RouterLink to="/category" class="text-stone-500 hover:text-primary transition-colors hover:opacity-80 transition-all duration-300">Category</RouterLink>
          <RouterLink to="/blog" class="text-stone-500 hover:text-primary transition-colors hover:opacity-80 transition-all duration-300">Blog</RouterLink>
        </div>
      </div>
      <div class="flex items-center gap-6">
        <div class="hidden lg:block relative">
          <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-stone-400 font-variation-settings-none">search</span>
          <input class="bg-surface-container-low border-none rounded-full py-2 pl-10 pr-4 text-sm focus:ring-1 focus:ring-primary/20 w-64" placeholder="Search..." type="text"/>
        </div>
        
        <RouterLink to="/checkout" class="relative group">
          <span class="material-symbols-outlined text-primary dark:text-[#fcf9f4] hover:opacity-80 transition-all duration-300">shopping_bag</span>
          <span v-if="cartStore.items.length > 0" class="absolute -top-1 -right-1 bg-primary text-white text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center border-2 border-[#fcf9f4]">
            {{ cartStore.totalItems }}
          </span>
        </RouterLink>

        <div v-if="authStore.user" class="relative group">
          <div class="cursor-pointer flex items-center gap-2">
            <div class="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white text-xs font-bold shadow-lg transition-transform group-hover:scale-105">
              {{ authStore.user.full_name?.[0] || authStore.user.email?.[0].toUpperCase() }}
            </div>
          </div>
          <!-- Dropdown Menu -->
          <div class="absolute right-0 top-full mt-2 w-56 bg-surface dark:bg-stone-900 rounded-2xl shadow-xl border border-outline-variant/30 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50 transform origin-top-right group-hover:translate-y-0 translate-y-2 flex flex-col py-2">
            <div class="px-4 py-3 border-b border-outline-variant/30 mb-2 bg-surface-container-low/50 rounded-t-2xl -mt-2">
              <p class="text-[10px] font-bold text-secondary uppercase tracking-widest mb-1">{{ authStore.user.role || 'Member' }}</p>
              <p class="text-sm font-bold text-primary truncate">{{ authStore.user.email }}</p>
            </div>
            
            <RouterLink v-if="authStore.isAdmin" to="/admin" class="px-4 py-2.5 text-sm font-medium hover:bg-surface-container-high flex items-center gap-3 transition-colors">
              <span class="material-symbols-outlined text-[20px] text-primary">admin_panel_settings</span>
              Admin Dashboard
            </RouterLink>
            
            <RouterLink to="/profile" class="px-4 py-2.5 text-sm font-medium hover:bg-surface-container-high flex items-center gap-3 transition-colors">
              <span class="material-symbols-outlined text-[20px] text-stone-500">person</span>
              My Profile
            </RouterLink>
            
            <RouterLink to="/orders" class="px-4 py-2.5 text-sm font-medium hover:bg-surface-container-high flex items-center gap-3 transition-colors">
              <span class="material-symbols-outlined text-[20px] text-stone-500">local_shipping</span>
              My Orders
            </RouterLink>
            
            <button @click="handleLogout" class="w-full text-left px-4 py-3 text-sm font-bold text-error hover:bg-error/5 flex items-center gap-3 mt-2 border-t border-outline-variant/30 transition-colors">
              <span class="material-symbols-outlined text-[20px]">logout</span>
              Sign Out
            </button>
          </div>
        </div>
        <RouterLink v-else to="/login" class="material-symbols-outlined text-primary dark:text-[#fcf9f4] hover:opacity-80 transition-all duration-300">person</RouterLink>
      </div>
    </nav>

    <!-- Content Area (RouterView) -->
    <RouterView />

    <!-- Chat Bubble -->
    <ChatBubble />

    <!-- Footer -->
    <footer v-if="!isAdminRoute" class="bg-[#ebe8e3] dark:bg-stone-950 w-full pt-16 pb-8 transition-all">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-12 px-12 max-w-7xl mx-auto font-body text-sm leading-relaxed text-primary dark:text-[#fcf9f4]">
        <div class="space-y-6">
          <h2 class="text-xl font-headline text-primary dark:text-[#fcf9f4]">Verdant Mane</h2>
          <p class="text-stone-600 dark:text-stone-400">Our philosophy is simple: hair care should be a ritual of connection with the earth. Consciously grown, ethically bottled.</p>
        </div>
        <div class="space-y-4">
          <h4 class="font-bold uppercase tracking-widest text-xs">Shop</h4>
          <ul class="space-y-2">
            <li><RouterLink to="/shop" class="text-stone-600 dark:text-stone-400 hover:text-primary transition-colors">New Arrivals</RouterLink></li>
            <li><RouterLink to="/shop" class="text-stone-600 dark:text-stone-400 hover:text-primary transition-colors">Hair Care Sets</RouterLink></li>
          </ul>
        </div>
        <div class="space-y-4">
          <h4 class="font-bold uppercase tracking-widest text-xs">Resources</h4>
          <ul class="space-y-2">
            <li><RouterLink to="/contact" class="text-stone-600 dark:text-stone-400 hover:text-primary transition-colors">FAQ</RouterLink></li>
            <li><RouterLink to="/contact" class="text-stone-600 dark:text-stone-400 hover:text-primary transition-colors">Shipping</RouterLink></li>
          </ul>
        </div>
        <div class="space-y-4">
          <h4 class="font-bold uppercase tracking-widest text-xs">Newsletter</h4>
          <form @submit.prevent="handleSubscribe" class="flex gap-2">
            <input v-model="email" class="bg-white/50 border-none rounded-lg px-4 py-2 w-full focus:ring-1 focus:ring-primary" placeholder="Email address" type="email" required/>
            <button type="submit" class="bg-primary text-white p-2 rounded-lg hover:opacity-90 transition-all">
              <span class="material-symbols-outlined">send</span>
            </button>
          </form>
        </div>
      </div>
      <div class="mt-16 pt-8 border-t border-stone-200/30 text-center text-stone-500 text-xs">
        © 2024 Verdant Mane. Consciously grown.
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import { useCartStore } from './stores/cart'
import ChatBubble from './components/ChatBubble.vue'

const authStore = useAuthStore()
const cartStore = useCartStore()
const route = useRoute()
const router = useRouter()

const isAdminRoute = computed(() => route.path.startsWith('/admin'))

// Senior Pattern: Tự động đổi theme dựa trên Route (Admin = Blue)
watch(isAdminRoute, (isAdmin) => {
  const allThemes = ['theme-botanical', 'theme-deepsea', 'theme-midnight', 'theme-earth']
  document.documentElement.classList.remove(...allThemes)
  
  if (isAdmin) {
    document.documentElement.classList.add('theme-deepsea')
  } else {
    const saved = localStorage.getItem('verdant-theme') || 'botanical'
    document.documentElement.classList.add(`theme-${saved}`)
  }
}, { immediate: true })

const email = ref('')

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const handleSubscribe = () => {
  if (email.value) {
    alert(`Thank you for subscribing, ${email.value}! Check your inbox for 15% off.`)
    email.value = ''
  }
}
</script>

<style>
/* Custom transitions and states */
.material-symbols-outlined {
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
.hero-gradient {
    background: linear-gradient(145deg, #0f52ba 0%, #0747a6 100%);
}
.tonal-shift {
    transition: background-color 0.3s ease;
}
</style>
