<template>
  <main class="pt-20 fade-in">
    <!-- Hero Section -->
    <section class="relative h-[480px] flex items-center overflow-hidden bg-app-surface-container-low">
      <div class="absolute inset-0 z-0">
        <img alt="Botanical Banner" class="w-full h-full object-cover" src="/assets/images/hero.png" />
        <div class="absolute inset-0 bg-gradient-to-r from-surface via-surface/40 to-transparent"></div>
      </div>
      <div class="relative z-10 max-w-screen-xl mx-auto px-6 w-full">
        <div class="max-w-xl">
          <span class="uppercase tracking-[0.25em] text-secondary font-bold text-[10px] mb-3 block">The Art of Cleansing</span>
          <h1 class="font-headline text-3xl md:text-5xl text-primary leading-tight mb-5 font-bold">Shampoos & <br/><span class="italic font-normal">Cleansers</span></h1>
          <p class="text-sm md:text-base text-stone-600 leading-relaxed mb-6 max-w-md">
            Elevate your daily ritual with our curated collection of botanical-infused cleansers. From the deep forest roots to the silken petals, each formula is crafted to restore your hair's natural equilibrium.
          </p>
          <div class="flex gap-3">
            <a href="#products-section" class="bg-primary text-on-primary px-8 py-3 rounded-xl font-bold text-xs flex items-center gap-2 hover:bg-primary-container transition-all group">
              Explore Collection
              <span class="material-symbols-outlined text-sm group-hover:translate-x-0.5 transition-transform">arrow_right_alt</span>
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- Category Filter Bar -->
    <section class="sticky top-20 z-40 bg-app-surface/95 backdrop-blur-md border-b border-stone-100">
      <div class="max-w-screen-xl mx-auto px-6 py-4 flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="flex gap-2 overflow-x-auto pb-1 md:pb-0 no-scrollbar w-full md:w-auto">
          <button v-for="cat in subCategories" :key="cat" 
                  @click="currentCategory = cat"
                  :class="['px-4 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all uppercase tracking-wider', 
                           currentCategory === cat ? 'bg-primary text-on-primary' : 'border border-stone-200 text-stone-500 hover:border-primary']">
            {{ cat }}
          </button>
        </div>
        <div class="flex items-center gap-4 w-full md:w-auto justify-between md:justify-end">
          <span class="text-xs text-stone-500 font-medium">Showing {{ filteredProducts.length }} Products</span>
          <div class="relative group">
            <div class="flex items-center gap-1.5 cursor-pointer hover:text-primary transition-colors">
              <span class="text-xs font-bold text-primary">Sort By: {{ currentSortLabel }}</span>
              <span class="material-symbols-outlined text-xs text-primary group-hover:rotate-180 transition-transform">expand_more</span>
            </div>
            
            <div class="absolute right-0 top-full mt-2 w-48 bg-app-surface rounded-xl shadow-xl border border-outline-variant/30 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 py-2">
               <button v-for="option in sortOptions" :key="option.value" @click="currentSort = option.value"
                       class="w-full text-left px-4 py-2 text-xs hover:bg-app-surface-container-high transition-colors text-app-text">
                 {{ option.label }}
               </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Product Grid -->
    <section id="products-section" class="max-w-screen-xl mx-auto px-6 py-12">
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="i in 3" :key="i" class="animate-pulse space-y-3">
          <div class="aspect-[4/5] bg-app-surface-container-high rounded-xl"></div>
          <div class="h-4 bg-app-surface-container-high rounded w-3/4"></div>
          <div class="h-3 bg-app-surface-container-high rounded w-1/2"></div>
        </div>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-16">
        <div v-for="product in filteredProducts" :key="product.id" class="group">
          <RouterLink :to="{ name: 'product-detail', params: { id: product.id } }">
            <div class="aspect-[4/5] bg-app-surface-container-high rounded-xl overflow-hidden mb-4 relative border border-stone-100/60 p-2 bg-white">
              <img v-if="product.images && product.images.length" 
                   :src="product.images[0].image_url" 
                   class="w-full h-full object-contain transition-transform duration-700 group-hover:scale-102" 
                   :alt="product.name" />
              <div v-else class="w-full h-full bg-stone-50 flex items-center justify-center text-stone-300">
                <span class="material-symbols-outlined text-5xl">image</span>
              </div>
              <div class="absolute inset-0 bg-primary/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center z-20">
                <button @click.prevent="cartStore.addToCart(product)" class="bg-app-surface text-primary px-6 py-2.5 rounded-lg font-bold text-xs shadow-md transform translate-y-3 group-hover:translate-y-0 transition-all duration-300 hover:bg-primary hover:text-white">Quick Add</button>
              </div>
            </div>
          </RouterLink>
          <div class="flex justify-between items-start px-1">
            <div class="flex-1 min-w-0 pr-2">
              <p class="text-[9px] uppercase tracking-widest text-stone-400 mb-0.5 font-medium">{{ product.brand || 'Original Formula' }}</p>
              <h3 class="font-headline text-sm text-primary mb-1 font-bold truncate">{{ product.name }}</h3>
              <p class="text-[11px] text-stone-500 mb-2 line-clamp-2 leading-relaxed">{{ product.description }}</p>
              <p class="font-extrabold text-primary text-sm">{{ formatPrice(product.price) }}đ</p>
            </div>
            <button class="p-1.5 rounded-full hover:bg-app-surface-container transition-colors group/fav">
              <span class="material-symbols-outlined text-stone-400 group-hover/fav:text-primary transition-colors text-base">favorite</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Ingredient Spotlight -->
    <section class="bg-app-surface-container-low py-20 overflow-hidden border-t border-stone-100">
      <div class="max-w-screen-xl mx-auto px-6">
        <div class="flex flex-col md:flex-row items-end justify-between mb-12 gap-6 text-on-background">
          <div class="max-w-xl">
            <span class="text-primary font-bold text-xs uppercase tracking-widest mb-2 block">Potent Botanicals</span>
            <h2 class="font-headline text-2xl md:text-3xl text-primary leading-tight font-bold">The <span class="italic font-normal">Essence</span> of Verdant Aura</h2>
          </div>
          <div class="md:text-right">
            <p class="text-stone-500 text-xs max-w-xs leading-relaxed">We harvest our ingredients at peak potency, ensuring every drop contains the raw power of nature's wisdom.</p>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-12 gap-6 h-auto">
          <div class="md:col-span-7 bg-app-surface-container-highest rounded-xl overflow-hidden relative group h-[380px]">
            <img alt="Fermented Rice Water" class="w-full h-full object-cover transition-transform duration-1000 group-hover:scale-103" src="/assets/images/hero.png" />
            <div class="absolute inset-0 bg-gradient-to-t from-primary/80 to-transparent flex flex-col justify-end p-8 text-on-primary">
              <h4 class="text-xl font-headline font-bold mb-2 text-white">Fermented Rice Water</h4>
              <p class="text-stone-200 text-xs max-w-md leading-relaxed">An ancient ritual for modern strength. Rich in inositol, it repairs hair from the inside out, providing unparalleled shine and elasticity.</p>
            </div>
          </div>
          <div class="md:col-span-5 grid grid-rows-2 gap-6">
            <div class="bg-app-surface-container-lowest rounded-xl p-8 flex flex-col justify-center border border-stone-100 shadow-sm text-left">
              <div class="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                <span class="material-symbols-outlined text-primary text-lg">eco</span>
              </div>
              <h4 class="text-lg font-headline font-bold text-primary mb-2">Wild Nettle</h4>
              <p class="text-stone-500 text-xs leading-relaxed">A powerful scalp stimulant that balances oil production and fosters an environment for healthy growth.</p>
            </div>
            <div class="bg-primary rounded-xl p-8 flex flex-col justify-center text-on-primary shadow-lg text-left">
              <div class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center mb-4">
                <span class="material-symbols-outlined text-white text-lg">water_drop</span>
              </div>
              <h4 class="text-lg font-headline font-bold mb-2 text-white">Aloe Barbadensis</h4>
              <p class="text-stone-200 text-xs leading-relaxed">Cold-pressed for maximum enzyme retention, our aloe base provides 24-hour hydration without weight.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonial Section -->
    <section class="max-w-screen-xl mx-auto px-6 py-20">
      <div class="bg-app-surface border border-stone-100 rounded-[24px] p-8 md:p-16 flex flex-col md:flex-row items-center gap-10 relative overflow-hidden shadow-lg bg-white">
        <div class="absolute top-0 left-0 w-48 h-48 bg-primary/5 rounded-full blur-[80px] -translate-x-1/2 -translate-y-1/2"></div>
        <div class="w-full md:w-1/3 relative">
          <div class="aspect-[3/4] rounded-xl overflow-hidden shadow-md relative z-10 bg-stone-50">
            <img alt="Expert Dermatologist" class="w-full h-full object-cover" src="/assets/images/mask.png" />
          </div>
          <div class="absolute -bottom-4 -right-4 w-24 h-24 bg-primary flex items-center justify-center rounded-full text-on-primary z-20 hidden md:flex shadow-md">
            <span class="text-[10px] uppercase tracking-wider text-center font-bold">Expert<br/>Choice</span>
          </div>
        </div>
        <div class="w-full md:w-2/3 text-left">
          <span class="material-symbols-outlined text-primary text-4xl mb-4">format_quote</span>
          <h3 class="font-headline text-xl md:text-2xl text-primary leading-relaxed mb-6 italic">
            "Choosing a cleanser is not just about cleaning; it's about respecting the scalp's microbiome. Verdant Aura uses pH-balanced surfactants that mimic the skin's natural barrier."
          </h3>
          <div>
            <p class="text-base font-bold text-primary">Dr. Elena Thorne</p>
            <p class="text-xs text-stone-500">Director of Trichology, Botanical Institute</p>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import { RouterLink } from 'vue-router'
import { useCartStore } from '../stores/cart'

const cartStore = useCartStore()

const products = ref([])
const loading = ref(true)
const currentCategory = ref('All Cleansers')
const subCategories = ['All Cleansers', 'Volumizing', 'Deep Hydrating', 'Scalp Care', 'Color Protect']

const currentSort = ref('featured')
const sortOptions = [
  { label: 'Featured', value: 'featured' },
  { label: 'Price: Low to High', value: 'price_asc' },
  { label: 'Price: High to Low', value: 'price_desc' }
]

const currentSortLabel = computed(() => {
  return sortOptions.find(o => o.value === currentSort.value)?.label || 'Featured'
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('vi-VN').format(price)
}

const filteredProducts = computed(() => {
  let list = products.value
  
  if (currentCategory.value !== 'All Cleansers') {
     list = products.value.filter(p => p.name.toLowerCase().includes('shampoo') || p.name.toLowerCase().includes('cleanser'))
  }
  
  // Clone to avoid mutating original
  let sorted = [...list]
  
  if (currentSort.value === 'price_asc') {
    sorted.sort((a, b) => Number(a.price) - Number(b.price))
  } else if (currentSort.value === 'price_desc') {
    sorted.sort((a, b) => Number(b.price) - Number(a.price))
  }
  
  return sorted
})

const fetchProducts = async () => {
  try {
    const response = await api.get('/products/')
    products.value = response.data
    // Filter specifically for "cleansing" products for this view
    products.value = products.value.filter(p => 
      p.name.toLowerCase().includes('gội') || 
      p.name.toLowerCase().includes('shampoo') || 
      p.name.toLowerCase().includes('cleaser')
    )
  } catch (error) {
    console.error('Lỗi khi tải sản phẩm danh mục:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
