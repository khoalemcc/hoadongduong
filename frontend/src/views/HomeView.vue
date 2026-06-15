<template>
  <main>
    <!-- Hero Section -->
    <section class="relative h-[600px] md:h-[800px] flex items-center overflow-hidden bg-app-surface-container-low">
      <div class="absolute inset-0 z-0">
        <img class="w-full h-full object-cover opacity-90 scale-105" src="/assets/images/hero.png" alt="Hero background" />
        <div class="absolute inset-0 bg-gradient-to-r from-surface-container-low/90 via-transparent to-transparent"></div>
      </div>
      <div class="relative z-10 container mx-auto px-8 md:px-16">
        <div class="max-w-xl">
          <span class="text-secondary font-semibold tracking-widest uppercase text-[10px] mb-3 block">Crafted by Nature</span>
          <h1 class="font-headline text-3xl md:text-5xl text-primary leading-tight font-bold mb-6">Naturally Radiant Hair</h1>
          <p class="text-stone-600 text-sm md:text-base mb-8 max-w-md leading-relaxed">
            Experience the profound calm of botanical care. Our formulas are grown, not built, using the purest earth-derived essences.
          </p>
          <div class="flex flex-wrap gap-3">
            <RouterLink to="/shop" class="hero-gradient text-on-primary px-8 py-3.5 rounded-xl font-bold text-sm hover:opacity-95 transition-all transform active:scale-95 shadow-lg shadow-primary/10 flex items-center justify-center">
              Shop Now
            </RouterLink>
            <RouterLink to="/blog" class="border border-stone-200 text-primary px-8 py-3.5 rounded-xl font-bold text-sm hover:bg-white/50 transition-all flex items-center justify-center">
              Our Story
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Brand Benefits -->
    <section class="py-20 bg-app-surface border-t border-stone-100">
      <div class="container mx-auto px-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
          <div v-reveal class="flex flex-col items-center text-center space-y-4">
            <div class="w-16 h-16 bg-secondary-container flex items-center justify-center rounded-full text-primary">
              <span class="material-symbols-outlined text-3xl">eco</span>
            </div>
            <h3 class="font-headline text-xl text-primary font-bold">Eco-Friendly</h3>
            <p class="text-stone-500 text-sm max-w-xs leading-relaxed">Sustainably sourced ingredients from protected botanical gardens.</p>
          </div>
          <div v-reveal class="flex flex-col items-center text-center space-y-4">
            <div class="w-16 h-16 bg-secondary-container flex items-center justify-center rounded-full text-primary">
              <span class="material-symbols-outlined text-3xl">potted_plant</span>
            </div>
            <h3 class="font-headline text-xl text-primary font-bold">100% Organic</h3>
            <p class="text-stone-500 text-sm max-w-xs leading-relaxed">No synthetic chemicals. Just the pure power of living plants.</p>
          </div>
          <div v-reveal class="flex flex-col items-center text-center space-y-4">
            <div class="w-16 h-16 bg-secondary-container flex items-center justify-center rounded-full text-primary">
              <span class="material-symbols-outlined text-3xl">verified</span>
            </div>
            <h3 class="font-headline text-xl text-primary font-bold">Cruelty Free</h3>
            <p class="text-stone-500 text-sm max-w-xs leading-relaxed">Ethical practices that honor every living being on our planet.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Products (Dynamic) -->
    <section class="py-24 bg-app-surface border-t border-stone-100">
      <div class="container mx-auto px-8">
        <div v-reveal class="text-center mb-16">
          <span class="text-secondary font-semibold uppercase tracking-widest text-[10px]">Customer Favorites</span>
          <h2 class="font-headline text-2xl md:text-3xl text-primary font-bold mt-2">Bestsellers</h2>
          <div class="w-8 h-[2px] bg-secondary/35 mx-auto mt-2"></div>
        </div>
        
        <div v-if="products.length" class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="product in displayedProducts" :key="product.id" v-reveal class="group text-left">
            <RouterLink :to="{ name: 'product-detail', params: { id: product.id } }">
              <div class="relative bg-white rounded-xl overflow-hidden mb-4 aspect-[4/5] border border-stone-100 p-2">
                <div class="w-full h-full bg-stone-50 rounded-lg overflow-hidden flex items-center justify-center">
                   <img v-if="product.images && product.images.length" 
                        :src="product.images.find(img => img.is_primary)?.image_url || product.images[0].image_url" 
                        class="w-full h-full object-contain group-hover:scale-102 transition-transform duration-700" 
                        :alt="product.name" />
                   <span v-else class="material-symbols-outlined text-5xl text-stone-300">image</span>
                </div>
                <div v-if="product.stock > 0" class="absolute top-4 left-4 bg-white/95 backdrop-blur-sm px-2 py-0.5 rounded text-[8px] font-bold text-primary tracking-widest">AVAILABLE</div>
                <button @click.prevent="cartStore.addToCart(product)" class="absolute bottom-4 right-4 bg-primary text-white w-10 h-10 rounded-full flex items-center justify-center shadow-md transform translate-y-10 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition-all duration-300 hover:bg-primary-container z-20">
                  <span class="material-symbols-outlined text-lg">add_shopping_cart</span>
                </button>
              </div>
              <h3 class="font-headline text-sm font-bold text-primary mb-1 truncate">{{ product.name }}</h3>
              <p class="text-stone-400 text-[10px] mb-2 uppercase tracking-wider font-semibold">{{ product.brand || 'Botanical Care' }}</p>
              <p class="text-primary font-extrabold text-sm">{{ formatPrice(product.price) }}đ</p>
            </RouterLink>
          </div>
        </div>

        <div v-else class="text-center py-20">
          <p class="text-stone-400 text-xs">Đang tải danh sách sản phẩm từ thiên nhiên...</p>
        </div>
      </div>
    </section>

    <!-- Latest News -->
    <section class="py-24 bg-app-bg border-t border-stone-100">
      <div class="container mx-auto px-8">
        <div v-reveal class="flex flex-col md:flex-row md:items-end md:justify-between gap-6 mb-12">
          <div>
            <span class="text-secondary font-semibold uppercase tracking-widest text-[10px]">Journal Updates</span>
            <h2 class="font-headline text-2xl md:text-3xl text-primary font-bold mt-2">Tin tức mới nhất</h2>
            <p class="text-stone-500 text-sm mt-3 max-w-xl leading-relaxed">
              Cập nhật các bài viết mới về chăm sóc tóc, nguyên liệu tự nhiên và câu chuyện thương hiệu.
            </p>
          </div>
          <RouterLink to="/blog" class="inline-flex items-center gap-2 text-primary text-xs font-black uppercase tracking-widest hover:opacity-70 transition-opacity">
            Xem tất cả
            <span class="material-symbols-outlined text-sm">arrow_forward</span>
          </RouterLink>
        </div>

        <div v-if="latestPosts.length" class="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
          <article v-for="post in latestPosts" :key="post.id" v-reveal class="group bg-app-surface border border-stone-100 rounded-xl overflow-hidden shadow-sm flex flex-col">
            <RouterLink :to="{ name: 'blog-detail', params: { id: post.slug } }" class="block overflow-hidden bg-app-surface-container-low">
              <img :src="getPostImage(post)" class="w-full aspect-[16/11] object-cover group-hover:scale-[1.03] transition-transform duration-700" :alt="post.title" />
            </RouterLink>
            <div class="p-6 flex flex-col flex-1">
              <div class="flex items-center justify-between gap-3 mb-4">
                <span class="text-[10px] font-black text-secondary uppercase tracking-widest">Stories</span>
                <span class="text-[10px] text-stone-400 uppercase tracking-widest font-bold">{{ formatDate(post.created_at) }}</span>
              </div>
              <RouterLink :to="{ name: 'blog-detail', params: { id: post.slug } }">
                <h3 class="font-headline text-lg text-primary mb-3 leading-snug line-clamp-2 hover:text-primary-container transition-colors">{{ post.title }}</h3>
              </RouterLink>
              <p class="text-sm text-stone-500 leading-relaxed line-clamp-3 mb-6">
                {{ getPostExcerpt(post, 130) }}{{ getPostExcerpt(post, 131).length > 130 ? '...' : '' }}
              </p>
              <RouterLink :to="{ name: 'blog-detail', params: { id: post.slug } }" class="mt-auto inline-flex items-center gap-2 text-primary text-xs font-black uppercase tracking-widest hover:opacity-70 transition-opacity">
                Đọc bài
                <span class="material-symbols-outlined text-sm">arrow_forward</span>
              </RouterLink>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- Testimonials -->
    <section v-reveal="'scale'" class="py-20 bg-[#f8fafc] border-t border-stone-100">
      <div class="container mx-auto px-8">
        <div class="max-w-3xl mx-auto text-center space-y-6">
          <div class="flex justify-center mb-2">
            <span class="material-symbols-outlined text-secondary text-4xl opacity-40">format_quote</span>
          </div>
          <h2 class="font-headline text-xl md:text-2xl text-primary italic leading-relaxed">
            "The transition to Verdant Mane was transformative. My hair hasn't just improved in appearance; it feels alive and nourished in a way synthetic products never achieved."
          </h2>
          <div class="flex flex-col items-center">
            <p class="font-bold text-sm text-primary">Elena Richardson</p>
            <p class="text-[11px] text-stone-400">Verified Customer</p>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import api from '../api'
import { useCartStore } from '../stores/cart'

const products = ref([])
const latestPosts = ref([])
const cartStore = useCartStore()
const fallbackBlogImage = 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&q=80&w=1200'

const formatPrice = (price) => {
  return new Intl.NumberFormat('vi-VN').format(price)
}

const stripHtml = (value) => {
  const div = document.createElement('div')
  div.innerHTML = value || ''
  return div.textContent || div.innerText || ''
}

const getPostImage = (post) => {
  if (!post) return fallbackBlogImage
  if (post.image_url) return post.image_url
  const match = String(post.content || '').match(/<img[^>]+src=["']([^"']+)["']/i)
  return match?.[1] || fallbackBlogImage
}

const getPostExcerpt = (post, length) => {
  return stripHtml(post?.content || '').substring(0, length)
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' })
}

const displayedProducts = computed(() => products.value.slice(0, 6))

const fetchProducts = async () => {
  try {
    const response = await api.get('/products/')
    products.value = response.data
  } catch (error) {
    console.error('Lỗi khi lấy danh sách sản phẩm:', error)
  }
}

const fetchLatestPosts = async () => {
  try {
    const response = await api.get('/blog/')
    latestPosts.value = response.data.slice(0, 3)
  } catch (error) {
    console.error('Failed to fetch latest blog posts:', error)
  }
}

onMounted(() => {
  fetchProducts()
  fetchLatestPosts()
})
</script>
