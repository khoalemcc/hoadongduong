<template>
  <main class="pt-32 pb-20 px-8 max-w-7xl mx-auto fade-in">
    <!-- Header & Breadcrumbs -->
    <header class="mb-8">
      <nav class="flex items-center text-secondary text-xs font-medium mb-3 tracking-wide">
        <RouterLink to="/" class="hover:text-primary transition-colors">Trang chủ</RouterLink>
        <span class="mx-2 text-outline">/</span>
        <span class="text-primary font-semibold">Tất cả sản phẩm</span>
      </nav>
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <h1 class="font-headline text-3xl lg:text-4xl text-primary font-bold">Tất cả sản phẩm</h1>
        <p class="text-secondary max-w-md italic font-headline text-sm leading-relaxed">
          Chăm sóc sức khỏe và sắc đẹp với các sản phẩm thảo dược thiên nhiên từ Cỏ Cây Hoa Lá.
        </p>
      </div>
    </header>

    <div class="flex flex-col lg:flex-row gap-12">
      <!-- Sidebar Filter -->
      <aside class="w-full lg:w-64 space-y-10">
        <!-- Hair Type Filter -->
        <section>
          <h3 class="font-bold text-primary mb-6 text-lg tracking-tight border-b border-surface-container-highest pb-2">Hair Type</h3>
          <div class="flex flex-col gap-3">
            <label v-for="type in hairTypes" :key="type" class="flex items-center group cursor-pointer">
              <input class="w-5 h-5 rounded text-primary focus:ring-primary-fixed border-outline-variant bg-app-surface-container-low mr-3 transition-all" type="checkbox"/>
              <span class="text-app-text-variant group-hover:text-primary transition-colors">{{ type }}</span>
            </label>
          </div>
        </section>

        <!-- Price Range -->
        <section>
          <h3 class="font-bold text-primary mb-6 text-lg tracking-tight border-b border-surface-container-highest pb-2">Price Range</h3>
          <div class="px-2">
            <input class="w-full h-1 bg-app-surface-container-highest rounded-lg appearance-none cursor-pointer accent-primary" type="range" min="10000" max="1000000" step="10000"/>
            <div class="flex justify-between text-xs text-secondary mt-3 font-medium">
              <span>10k</span>
              <span>1M+</span>
            </div>
          </div>
        </section>

        <button class="w-full py-3 bg-app-surface-container-high text-primary font-bold rounded-xl hover:bg-app-surface-container-highest transition-colors">
          Clear All Filters
        </button>
      </aside>

      <!-- Product Grid -->
      <div class="flex-1">
        <div v-if="products.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-y-12 gap-x-8">
          <div v-for="product in products" :key="product.id" class="group relative">
            <RouterLink :to="{ name: 'product-detail', params: { id: product.id } }">
              <div class="aspect-[4/5] bg-app-surface-container-low rounded-xl overflow-hidden mb-6 relative">
                <div class="w-full h-full bg-stone-200 flex items-center justify-center">
                   <img v-if="product.images && product.images.length" 
                        :src="product.images.find(img => img.is_primary)?.image_url || product.images[0].image_url" 
                        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" 
                        :alt="product.name" />
                   <span v-else class="material-symbols-outlined text-6xl text-stone-400">image</span>
                </div>
                <div class="absolute bottom-4 left-4 right-4 translate-y-4 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition-all duration-300 z-20">
                  <button @click.prevent="cartStore.addToCart(product)" class="w-full py-4 bg-primary text-on-primary rounded-xl font-bold shadow-xl flex items-center justify-center gap-2 hover:bg-primary-container transition-colors">
                    <span class="material-symbols-outlined text-xl">shopping_basket</span>
                    Add to Cart
                  </button>
                </div>
              </div>
              <div class="space-y-2 px-2">
                <div class="flex justify-between items-start">
                  <h3 class="font-headline text-sm font-bold text-primary leading-tight line-clamp-2">{{ product.name }}</h3>
                  <span class="font-bold text-primary text-sm">{{ formatPrice(product.price) }}đ</span>
                </div>
                <div class="flex items-center text-secondary-container">
                  <div class="flex text-amber-500 mr-2">
                    <span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
                    <span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
                    <span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
                    <span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
                    <span class="material-symbols-outlined text-sm">star</span>
                  </div>
                  <span class="text-xs font-medium text-secondary">(42 reviews)</span>
                </div>
                <p class="text-xs text-app-text-variant line-clamp-1 truncate">{{ product.description || 'Sản phẩm thảo dược thiên nhiên.' }}</p>
              </div>
            </RouterLink>
          </div>
        </div>

        <div v-else class="text-center py-40">
          <p class="text-stone-500 font-headline italic text-xl">Searching for more botanical remedies...</p>
        </div>

        <!-- Pagination -->
        <div class="mt-20 flex justify-center items-center gap-4">
          <button class="w-12 h-12 rounded-full border border-outline-variant flex items-center justify-center text-primary hover:bg-app-surface-container-high transition-colors">
            <span class="material-symbols-outlined">chevron_left</span>
          </button>
          <span class="text-primary font-bold font-headline text-lg px-4">1 of 1</span>
          <button class="w-12 h-12 rounded-full bg-primary text-on-primary flex items-center justify-center hover:bg-primary-container transition-colors shadow-lg">
            <span class="material-symbols-outlined">chevron_right</span>
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { RouterLink } from 'vue-router'

import { useCartStore } from '../stores/cart'

const cartStore = useCartStore()

const products = ref([])
const hairTypes = ['Oily', 'Dry', 'Curly', 'Straight']

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
