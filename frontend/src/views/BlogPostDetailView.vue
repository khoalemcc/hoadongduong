<template>
  <main v-if="post" class="pt-32 pb-24 fade-in">
    <div class="max-w-4xl mx-auto px-8">
      <!-- Breadcrumbs -->
      <nav class="flex items-center text-secondary text-xs uppercase tracking-widest font-bold mb-12">
        <RouterLink to="/blog" class="hover:text-primary transition-colors">The Journal</RouterLink>
        <span class="mx-4 text-stone-300">/</span>
        <span class="text-primary">{{ post.category || 'Rituals' }}</span>
      </nav>

      <!-- Article Header -->
      <header class="mb-16">
        <h1 class="font-headline text-3xl md:text-5xl text-primary leading-tight mb-8 max-w-4xl">{{ post.title }}</h1>
        <div class="flex items-center justify-between border-y border-stone-100 py-8">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-full bg-primary flex items-center justify-center text-white font-bold">JD</div>
            <div>
              <p class="font-bold text-primary">Julian Thorne</p>
              <p class="text-xs text-stone-500">{{ formatDate(post.created_at) }} • 5 Min Read</p>
            </div>
          </div>
          <div class="flex items-center gap-6 text-secondary">
            <button class="hover:text-primary transition-colors"><span class="material-symbols-outlined">share</span></button>
            <button class="hover:text-primary transition-colors"><span class="material-symbols-outlined">bookmark_add</span></button>
          </div>
        </div>
      </header>

      <!-- Featured Image -->
      <figure class="mb-16 rounded-2xl overflow-hidden shadow-2xl skew-y-0 hover:scale-[1.01] transition-transform duration-1000">
        <img :src="getPostImage(post)" class="w-full aspect-video object-cover" :alt="post.title"/>
      </figure>

      <!-- Article Content -->
      <div class="prose prose-lg max-w-none font-body text-app-text-variant leading-relaxed space-y-8">
        <div class="imported-content text-lg" v-html="post.content"></div>
      </div>

      <!-- Article Footer -->
      <footer class="mt-24 pt-12 border-t border-stone-100 flex flex-col md:flex-row justify-between items-center gap-8">
        <div class="flex items-center gap-4">
           <span class="text-xs font-bold uppercase tracking-widest text-secondary">Tags:</span>
           <div class="flex gap-2">
             <span class="px-3 py-1 bg-app-surface-container-low text-[10px] font-bold uppercase rounded">Botanical</span>
             <span class="px-3 py-1 bg-app-surface-container-low text-[10px] font-bold uppercase rounded">Grooming</span>
           </div>
        </div>
        <div class="flex gap-4">
          <button class="p-4 bg-primary text-white rounded-full hover:bg-primary/90 transition-all shadow-xl"><span class="material-symbols-outlined">favorite</span></button>
          <RouterLink v-if="nextPostSlug" :to="{ name: 'blog-detail', params: { id: nextPostSlug } }" class="p-4 border border-stone-200 rounded-full hover:bg-stone-50 transition-all font-bold text-xs uppercase tracking-widest px-8 flex items-center justify-center">Next Story</RouterLink>
          <RouterLink v-else to="/blog" class="p-4 border border-stone-200 rounded-full hover:bg-stone-50 transition-all font-bold text-xs uppercase tracking-widest px-8 flex items-center justify-center">Back to Journal</RouterLink>
        </div>
      </footer>
    </div>
  </main>
  
  <!-- Loading State -->
  <div v-else class="h-screen flex items-center justify-center">
    <div class="text-center animate-pulse">
      <span class="material-symbols-outlined text-5xl text-primary mb-4 block">compost</span>
      <p class="font-headline italic text-xl text-stone-500">Unveiling botanical insights...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import api from '../api'

const route = useRoute()
const post = ref(null)
const nextPostSlug = ref(null)
const fallbackImage = 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&q=80&w=1200'

const getPostImage = (post) => {
  if (!post) return fallbackImage
  if (post.image_url) return post.image_url
  const match = String(post.content || '').match(/<img[^>]+src=["']([^"']+)["']/i)
  return match?.[1] || fallbackImage
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
}

const fetchPost = async () => {
  post.value = null // reset for loading state
  try {
    const postSlug = route.params.id
    
    // Fetch current post
    const response = await api.get(`/blog/${postSlug}`)
    post.value = response.data
    
    // Fetch all posts to determine next post
    const allResponse = await api.get('/blog/')
    const allPosts = allResponse.data
    
    const currentIndex = allPosts.findIndex(p => p.slug === postSlug)
    if (currentIndex >= 0 && currentIndex < allPosts.length - 1) {
      nextPostSlug.value = allPosts[currentIndex + 1].slug
    } else if (allPosts.length > 1) {
      nextPostSlug.value = allPosts[0].slug // Loop back to the first one
    } else {
      nextPostSlug.value = null
    }
  } catch (error) {
    console.error('Lỗi khi lấy chi tiết bài viết:', error)
  }
}

watch(() => route.params.id, () => {
  if(route.name === 'blog-detail') {
    fetchPost()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
})

onMounted(() => {
  fetchPost()
})
</script>

<style scoped>
.imported-content :deep(figure) {
  margin: 2rem 0;
}

.imported-content :deep(img) {
  width: 100%;
  border-radius: 1rem;
  object-fit: cover;
}

.imported-content :deep(h2) {
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--primary);
}

.imported-content :deep(h3) {
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary);
}

.imported-content :deep(p) {
  margin-bottom: 1rem;
}

.imported-content :deep(a) {
  color: var(--primary);
  text-decoration: underline;
}
</style>
