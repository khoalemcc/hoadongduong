<template>
  <div v-if="product" class="pt-24 pb-12 container mx-auto px-4 max-w-5xl fade-in">
    <!-- Back Button -->
    <RouterLink to="/shop" class="inline-flex items-center gap-1.5 text-stone-400 hover:text-primary mb-5 transition-colors group text-[11px] font-medium">
      <span class="material-symbols-outlined text-xs group-hover:-translate-x-0.5 transition-transform">arrow_back</span>
      <span>Quay lại bộ sưu tập</span>
    </RouterLink>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
      <!-- Left: Product Image Gallery -->
      <div class="space-y-2">
        <!-- Main Image -->
        <div class="bg-white rounded-xl overflow-hidden aspect-square flex items-center justify-center relative group shadow-sm border border-stone-100/60">
          <img v-if="mainImage"
               :src="mainImage"
               class="w-full h-full object-contain p-4 transition-transform duration-700 group-hover:scale-102"
               :alt="product.name" />
          <span v-else class="material-symbols-outlined text-5xl text-stone-300">image</span>
          <div class="absolute top-3 left-3 bg-primary/95 backdrop-blur-sm px-2.5 py-0.5 rounded-full text-[8px] font-bold text-white uppercase tracking-widest shadow-sm">
            Chính hãng
          </div>
        </div>

        <!-- Thumbnail Gallery -->
        <div v-if="galleryImages.length > 1" class="flex gap-2 overflow-x-auto pb-1 scrollbar-thin">
          <button
            v-for="(img, idx) in galleryImages"
            :key="img.id"
            @click="selectedImageIdx = idx"
            :class="[
              'w-12 h-12 rounded-lg overflow-hidden border flex-shrink-0 transition-all bg-white p-1',
              selectedImageIdx === idx ? 'border-primary ring-2 ring-primary/10' : 'border-stone-200 hover:border-primary/30'
            ]"
          >
            <img :src="img.image_url" class="w-full h-full object-contain" :alt="`${product.name} ${idx + 1}`" />
          </button>
        </div>
      </div>

      <!-- Right: Product Info -->
      <div class="space-y-4">
        <div>
          <span class="text-secondary font-medium uppercase tracking-widest text-[9px] mb-0.5 block">
            {{ product.brand || 'Cỏ Cây Hoa Lá' }}
          </span>
          <h1 class="font-headline text-lg md:text-xl text-primary leading-snug font-bold tracking-tight">{{ product.name }}</h1>
        </div>

        <!-- Rating -->
        <div class="flex items-center gap-1.5">
          <div class="flex gap-0.5">
            <span v-for="i in 5" :key="i" class="material-symbols-outlined text-xs text-amber-400">star</span>
          </div>
          <span class="text-[11px] text-stone-400">({{ product.reviews?.length || 0 }} đánh giá)</span>
        </div>

        <div class="flex items-baseline gap-2 py-2.5 border-y border-stone-100/80">
          <span class="text-lg font-extrabold text-primary">{{ formatPrice(product.price) }}đ</span>
          <span class="text-stone-400 line-through text-[11px]" v-if="product.price">{{ formatPrice(product.price * 1.2) }}đ</span>
          <span class="bg-red-50 text-red-500 text-[8px] font-bold px-1.5 py-0.5 rounded-full uppercase">-20%</span>
        </div>

        <div class="space-y-1.5">
          <h3 class="font-bold text-primary uppercase tracking-wider text-[9px]">Mô tả sản phẩm</h3>
          <div 
            v-if="product.description" 
            class="text-stone-500 text-[12px] leading-relaxed product-desc-content" 
            v-html="product.description"
          ></div>
          <p v-else class="text-stone-500 text-[12px] leading-relaxed">
            Sản phẩm chăm sóc sức khỏe và sắc đẹp từ thiên nhiên, được chiết xuất từ các loại thảo dược quý hiếm. Công thức độc quyền giúp nuôi dưỡng, phục hồi và tái tạo từ sâu bên trong.
          </p>
        </div>

        <!-- Key Benefits -->
        <div class="grid grid-cols-2 gap-1.5">
          <div v-for="benefit in benefits" :key="benefit.text" class="flex items-center gap-1.5 bg-stone-50/80 rounded-lg px-2.5 py-1.5">
            <span class="material-symbols-outlined text-primary text-xs">{{ benefit.icon }}</span>
            <span class="text-[11px] text-stone-600 font-medium">{{ benefit.text }}</span>
          </div>
        </div>

        <!-- Purchase Actions -->
        <div class="pt-2 space-y-3">
          <div class="flex items-center gap-3">
            <div class="flex items-center border border-stone-200 rounded-lg overflow-hidden bg-white">
              <button @click="quantity > 1 && quantity--" class="px-2.5 py-1 hover:bg-stone-50 transition-colors text-xs font-semibold">−</button>
              <span class="px-3 py-1 font-semibold min-w-[36px] text-center border-x border-stone-200 text-xs text-stone-800">{{ quantity }}</span>
              <button @click="quantity++" class="px-2.5 py-1 hover:bg-stone-50 transition-colors text-xs font-semibold">+</button>
            </div>
            <p v-if="product.stock" class="text-stone-400 text-[11px] flex items-center gap-1">
              <span class="material-symbols-outlined text-xs text-green-500">inventory</span>
              Còn {{ product.stock }} sản phẩm
            </p>
          </div>

          <div class="flex gap-2">
            <button @click="cartStore.addToCart(product, quantity)" class="hero-gradient text-on-primary flex-1 py-2.5 rounded-lg font-bold text-xs hover:opacity-95 shadow-md shadow-primary/5 transition-all active:scale-98">
              Thêm vào giỏ hàng
            </button>
            <button class="border border-stone-200 p-2.5 rounded-lg hover:bg-stone-50 transition-all hover:border-red-100 group">
              <span class="material-symbols-outlined text-stone-400 group-hover:text-red-400 transition-colors text-base">favorite</span>
            </button>
          </div>
        </div>

        <!-- Extra Info -->
        <div class="grid grid-cols-2 gap-3 pt-4 border-t border-stone-100">
          <div class="flex gap-1.5 items-start">
            <span class="material-symbols-outlined text-secondary text-base">local_shipping</span>
            <div>
              <p class="font-bold text-[10px] text-stone-700">Miễn phí vận chuyển</p>
              <p class="text-[9px] text-stone-400">Đơn hàng trên 500k</p>
            </div>
          </div>
          <div class="flex gap-1.5 items-start">
            <span class="material-symbols-outlined text-secondary text-base">verified_user</span>
            <div>
              <p class="font-bold text-[10px] text-stone-700">Hàng chính hãng</p>
              <p class="text-[9px] text-stone-400">Cam kết hoàn tiền 100%</p>
            </div>
          </div>
          <div class="flex gap-1.5 items-start">
            <span class="material-symbols-outlined text-secondary text-base">autorenew</span>
            <div>
              <p class="font-bold text-[10px] text-stone-700">Đổi trả dễ dàng</p>
              <p class="text-[9px] text-stone-400">Trong vòng 30 ngày</p>
            </div>
          </div>
          <div class="flex gap-1.5 items-start">
            <span class="material-symbols-outlined text-secondary text-base">eco</span>
            <div>
              <p class="font-bold text-[10px] text-stone-700">100% Thảo dược</p>
              <p class="text-[9px] text-stone-400">Nguồn gốc tự nhiên</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Detailed Image Showcase Layout (Nhiều ảnh trực quan) -->
    <div v-if="galleryImages.length > 0" class="mt-16 pt-10 border-t border-stone-100">
      <div class="text-center max-w-md mx-auto mb-8">
        <span class="text-secondary font-semibold uppercase tracking-widest text-[9px]">Botanical Gallery</span>
        <h2 class="font-headline text-lg text-primary font-bold mt-1">Hình ảnh chi tiết sản phẩm</h2>
        <div class="w-8 h-[2px] bg-secondary/35 mx-auto mt-2"></div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
        <div 
          v-for="(img, idx) in galleryImages" 
          :key="`showcase-${img.id}`" 
          class="bg-white rounded-2xl overflow-hidden shadow-md hover:shadow-lg transition-all duration-300 border border-stone-100/40 p-3 group"
        >
          <div class="relative overflow-hidden rounded-xl aspect-square bg-stone-50 flex items-center justify-center">
            <img 
              :src="img.image_url" 
              class="w-full h-full object-contain transition-transform duration-700 group-hover:scale-105" 
              :alt="`${product.name} chi tiết ${idx + 1}`" 
            />
            <div class="absolute bottom-3 left-3 bg-black/60 backdrop-blur-sm text-white text-[8px] font-bold px-2 py-0.5 rounded">
              Góc nhìn {{ idx + 1 }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="loading" class="h-[60vh] flex items-center justify-center">
    <div class="text-center space-y-2">
      <div class="w-8 h-8 border-2 border-secondary border-t-transparent rounded-full animate-spin mx-auto"></div>
      <p class="text-stone-400 text-[11px] font-medium">Đang tải thông tin sản phẩm...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import api from '../api'
import { useCartStore } from '../stores/cart'

const cartStore = useCartStore()

const route = useRoute()
const product = ref(null)
const loading = ref(true)
const quantity = ref(1)
const selectedImageIdx = ref(0)

const galleryImages = computed(() => {
  if (!product.value) return []
  let imgs = [...(product.value.images || [])]
  
  // Custom logic to add detail images for Cỏ Cây Hoa Lá combos / products (e.g. ID 3)
  if (product.value.id === 3 || product.value.name?.includes('Combo Bơ Nghệ Làm Sạch Sâu')) {
    const extraUrls = [
      'https://res.cloudinary.com/dajfab5oi/image/upload/f_auto,q_auto/v1/hoadongduong/by2ghmbd7mfh5qzopjyw', // Dầu Tẩy Trang
      'https://res.cloudinary.com/dajfab5oi/image/upload/f_auto,q_auto/v1/hoadongduong/jyktfii0cn8nrutuxvhk', // Sữa Rửa Mặt
      'https://res.cloudinary.com/dajfab5oi/image/upload/f_auto,q_auto/v1/hoadongduong/sn6ypy98kdccz2euxws6', // Mặt Nạ Tẩy Tế Bào Chết
    ]
    extraUrls.forEach((url, index) => {
      if (!imgs.some(img => img.image_url === url)) {
        imgs.push({ id: `mock-3-${index}`, image_url: url, is_primary: false })
      }
    })
  } else if (product.value.id === 2 || product.value.name?.includes('Combo Bơ Nghệ 4 Bước')) {
    const extraUrls = [
      'https://res.cloudinary.com/dajfab5oi/image/upload/f_auto,q_auto/v1/hoadongduong/by2ghmbd7mfh5qzopjyw', // Dầu Tẩy Trang
      'https://res.cloudinary.com/dajfab5oi/image/upload/f_auto,q_auto/v1/hoadongduong/jyktfii0cn8nrutuxvhk', // Sữa Rửa Mặt
      'https://res.cloudinary.com/dajfab5oi/image/upload/f_auto,q_auto/v1/hoadongduong/sn6ypy98kdccz2euxws6', // Mặt Nạ Tẩy Tế Bào Chết
      'https://res.cloudinary.com/dajfab5oi/image/upload/f_auto,q_auto/v1/hoadongduong/dew1vhvchtg3ns3hrhyx', // Kem Dưỡng
    ]
    extraUrls.forEach((url, index) => {
      if (!imgs.some(img => img.image_url === url)) {
        imgs.push({ id: `mock-2-${index}`, image_url: url, is_primary: false })
      }
    })
  }
  
  return imgs
})

const mainImage = computed(() => {
  if (!galleryImages.value.length) return null
  return galleryImages.value[selectedImageIdx.value]?.image_url
    || galleryImages.value[0]?.image_url
})

const benefits = [
  { icon: 'spa', text: 'Chiết xuất thảo dược' },
  { icon: 'science', text: 'Đã kiểm nghiệm' },
  { icon: 'eco', text: 'Thuần tự nhiên' },
  { icon: 'dermatology', text: 'An toàn cho da' }
]

const formatPrice = (price) => {
  return new Intl.NumberFormat('vi-VN').format(price)
}

const fetchProductDetail = async () => {
  try {
    const productId = route.params.id
    const response = await api.get(`/products/${productId}`)
    product.value = response.data
  } catch (error) {
    console.error('Lỗi khi lấy chi tiết sản phẩm:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProductDetail()
})
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.product-desc-content :deep(*) {
  font-size: 12px !important;
  line-height: 1.6 !important;
}
.product-desc-content :deep(strong) {
  font-weight: 700;
}
.product-desc-content :deep(p) {
  margin-bottom: 6px;
}
.product-desc-content :deep(h1),
.product-desc-content :deep(h2),
.product-desc-content :deep(h3),
.product-desc-content :deep(h4) {
  font-size: 13px !important;
  font-weight: 700 !important;
  margin-top: 10px !important;
  margin-bottom: 4px !important;
  color: var(--primary-color) !important;
}
</style>
