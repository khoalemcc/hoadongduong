<template>
  <aside class="hidden md:flex h-screen w-64 border-r border-white/5 bg-app-surface flex-col p-4 space-y-2 sticky top-0">
    <div class="px-4 py-6 mb-4">
      <h1 class="text-xl font-headline font-bold text-primary">Verdant</h1>
      <p class="text-[10px] text-stone-500 font-bold uppercase tracking-widest mt-1">Management Suite</p>
    </div>
    
    <nav class="flex-1 space-y-1">
      <RouterLink v-for="link in adminLinks" :key="link.name" 
         :to="{ name: 'admin-' + link.name }" 
         :class="['flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group', currentRouteName === 'admin-' + link.name ? 'bg-app-bg text-primary shadow-sm font-bold border border-white/5' : 'text-stone-400 hover:bg-stone-800/50']"
      >
        <span class="material-symbols-outlined text-primary text-xl" :style="currentRouteName === 'admin-' + link.name ? 'font-variation-settings: \'FILL\' 1;' : ''">{{ link.icon }}</span>
        <span class="text-sm font-medium">{{ link.label }}</span>
      </RouterLink>
    </nav>

    <div class="pt-6 mt-6 border-t border-white/5">
      <div v-if="authStore.user" class="flex items-center gap-3 px-4 py-2 mb-6">
        <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white text-[10px] font-bold shadow-lg">
          {{ authStore.user.full_name?.[0] || 'A' }}
        </div>
        <div class="flex flex-col min-w-0">
          <span class="text-xs font-bold text-app-text truncate">{{ authStore.user.full_name || 'Admin' }}</span>
          <span class="text-[9px] text-primary uppercase font-black">{{ authStore.user.role }}</span>
        </div>
      </div>
      
      <RouterLink to="/" class="w-full py-4 bg-app-surface text-stone-300 border border-white/5 rounded-2xl text-[10px] uppercase font-black hover:bg-stone-800 transition-all text-center flex items-center justify-center gap-2 tracking-widest group">
        <span class="material-symbols-outlined text-sm group-hover:-translate-x-1 transition-transform">arrow_back</span>
        View Storefront
      </RouterLink>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const route = useRoute()
const currentRouteName = computed(() => route.name)

const adminLinks = [
  { name: 'dashboard', label: 'Dashboard', icon: 'dashboard' },
  { name: 'inventory', label: 'Inventory', icon: 'inventory_2' },
  { name: 'brands', label: 'Brands', icon: 'sell' },
  { name: 'orders', label: 'Orders', icon: 'local_shipping' },
  { name: 'customers', label: 'Customers', icon: 'group' },
  { name: 'blog', label: 'Blog Content', icon: 'article' },
  { name: 'marketing', label: 'Marketing', icon: 'campaign' },
  { name: 'inventory-logs', label: 'Stock Logs', icon: 'history' },
  { name: 'audit', label: 'Audit Logs', icon: 'security' },
  { name: 'settings', label: 'Settings', icon: 'settings' }
]
</script>
