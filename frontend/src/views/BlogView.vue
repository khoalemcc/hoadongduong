<template>
  <main class="pt-28 pb-20 fade-in bg-app-bg">
    <header class="max-w-7xl mx-auto px-5 sm:px-8 mb-14">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:items-end">
        <div class="lg:col-span-7">
          <span class="text-secondary font-bold tracking-widest uppercase text-[11px] mb-4 block">Archive & Insights</span>
          <h1 class="font-headline text-4xl md:text-6xl font-bold text-primary mb-5 leading-tight">The Journal</h1>
          <p class="font-body text-base md:text-lg text-app-text-variant leading-relaxed max-w-2xl">
            A curated collection of botanical wisdom, product rituals, and ingredient notes for considered daily care.
          </p>
        </div>

        <div class="lg:col-span-5 lg:justify-self-end">
          <div class="flex flex-wrap gap-2 lg:justify-end">
            <button
              v-for="cat in categories"
              :key="cat"
              @click="selectedCategory = cat"
              :class="[
                'h-10 px-4 rounded-full font-bold text-xs transition-all border',
                selectedCategory === cat
                  ? 'bg-primary text-on-primary border-primary'
                  : 'bg-app-surface text-secondary border-outline-variant/20 hover:border-primary/40'
              ]"
            >
              {{ cat }}
            </button>
          </div>
        </div>
      </div>
    </header>

    <section v-if="featuredPost" class="max-w-7xl mx-auto px-5 sm:px-8 mb-16">
      <article class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-10 bg-app-surface border border-outline-variant/15 rounded-xl p-4 md:p-6 shadow-sm">
        <RouterLink :to="{ name: 'blog-detail', params: { id: featuredPost.slug } }" class="lg:col-span-7 block overflow-hidden rounded-lg bg-app-surface-container-low">
          <img class="w-full aspect-[16/10] object-cover hover:scale-[1.025] transition-transform duration-700" :src="getPostImage(featuredPost)" :alt="featuredPost.title" />
        </RouterLink>

        <div class="lg:col-span-5 flex flex-col justify-center py-2 md:py-6">
          <div class="flex items-center gap-3 mb-5">
            <span class="inline-flex h-8 items-center px-3 bg-primary/10 text-primary text-[10px] font-black uppercase tracking-widest rounded-full">Featured</span>
            <span class="text-[11px] text-stone-500 font-bold uppercase tracking-widest">{{ formatDate(featuredPost.created_at) }}</span>
          </div>
          <RouterLink :to="{ name: 'blog-detail', params: { id: featuredPost.slug } }">
            <h2 class="font-headline text-2xl md:text-3xl text-primary mb-5 leading-tight hover:text-primary-container transition-colors line-clamp-3">
              {{ featuredPost.title }}
            </h2>
          </RouterLink>
          <p class="font-body text-app-text-variant mb-7 leading-relaxed line-clamp-4">
            {{ getPostExcerpt(featuredPost, 240) }}{{ getPostExcerpt(featuredPost, 241).length > 240 ? '...' : '' }}
          </p>
          <RouterLink :to="{ name: 'blog-detail', params: { id: featuredPost.slug } }" class="inline-flex w-fit items-center gap-2 h-11 px-5 rounded-full bg-primary text-white text-xs font-black uppercase tracking-widest hover:opacity-90 transition-opacity">
            Read Story
            <span class="material-symbols-outlined text-sm">arrow_forward</span>
          </RouterLink>
        </div>
      </article>
    </section>

    <section class="max-w-7xl mx-auto px-5 sm:px-8">
      <div v-if="regularPosts.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 lg:gap-8">
        <article
          v-for="post in regularPosts"
          :key="post.id"
          class="bg-app-surface border border-outline-variant/15 rounded-xl overflow-hidden shadow-sm flex flex-col min-h-full"
        >
          <RouterLink :to="{ name: 'blog-detail', params: { id: post.slug } }" class="block bg-app-surface-container-low overflow-hidden">
            <img :src="getPostImage(post)" class="w-full aspect-[16/11] object-cover hover:scale-[1.03] transition-transform duration-700" :alt="post.title" />
          </RouterLink>

          <div class="p-6 flex flex-col flex-1">
            <div class="flex items-center justify-between gap-3 mb-4">
              <span class="text-[10px] font-black text-secondary uppercase tracking-widest">{{ post.category || 'Stories' }}</span>
              <span class="text-[10px] text-stone-400 uppercase tracking-widest font-bold">{{ formatDate(post.created_at) }}</span>
            </div>
            <RouterLink :to="{ name: 'blog-detail', params: { id: post.slug } }">
              <h3 class="font-headline text-xl text-primary mb-4 leading-snug line-clamp-2 hover:text-primary-container transition-colors">
                {{ post.title }}
              </h3>
            </RouterLink>
            <p class="font-body text-sm text-app-text-variant mb-6 line-clamp-3 leading-relaxed">
              {{ getPostExcerpt(post, 150) }}{{ getPostExcerpt(post, 151).length > 150 ? '...' : '' }}
            </p>
            <div class="mt-auto pt-5 border-t border-outline-variant/15 flex items-center justify-between">
              <span class="text-[11px] font-bold text-stone-500">5 Min Read</span>
              <RouterLink :to="{ name: 'blog-detail', params: { id: post.slug } }" class="text-xs font-black text-primary uppercase tracking-widest hover:opacity-70 transition-opacity">
                Read
              </RouterLink>
            </div>
          </div>
        </article>
      </div>

      <div v-else-if="!featuredPost" class="min-h-80 flex flex-col items-center justify-center rounded-xl bg-app-surface border border-outline-variant/15 text-center px-6">
        <span class="material-symbols-outlined text-5xl text-stone-400 mb-4">article</span>
        <p class="font-headline text-2xl text-primary mb-2">No journal entries yet</p>
        <p class="text-sm text-stone-500 max-w-md">Published posts will appear here after they are created in the admin content studio.</p>
      </div>
    </section>

    <section class="max-w-7xl mx-auto px-5 sm:px-8 mt-16">
      <div class="rounded-xl bg-primary text-on-primary px-6 py-8 md:px-10 md:py-10 grid grid-cols-1 lg:grid-cols-12 gap-6 lg:items-center shadow-sm">
        <div class="lg:col-span-7">
          <span class="text-[10px] font-black uppercase tracking-widest text-white/60 mb-3 block">Newsletter</span>
          <h3 class="font-headline text-2xl md:text-3xl mb-3 leading-tight">Join the Inner Grove</h3>
          <p class="font-body text-sm text-white/75 leading-relaxed max-w-2xl">
            Receive monthly botanical insights, product notes, and seasonal care rituals.
          </p>
        </div>
        <form @submit.prevent="handleSubscribe" class="lg:col-span-5 flex flex-col sm:flex-row gap-3">
          <input v-model="email" class="h-12 flex-1 bg-white/10 border border-white/15 rounded-lg px-4 text-sm focus:ring-1 focus:ring-white/40 text-white placeholder:text-white/45 outline-none" placeholder="Email address" type="email" required />
          <button type="submit" class="h-12 px-6 bg-white text-primary font-black text-xs rounded-lg hover:bg-app-surface-container-high transition-colors uppercase tracking-widest">Subscribe</button>
        </form>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'

const email = ref('')
const posts = ref([])
const categories = ['All Stories', 'Rituals', 'Ingredients', 'Sustainability']
const selectedCategory = ref('All Stories')
const fallbackImage = 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&q=80&w=1200'

const handleSubscribe = () => {
  if (email.value) {
    alert(`Thank you for subscribing, ${email.value}.`)
    email.value = ''
  }
}

const featuredPost = computed(() => posts.value[0] || null)
const regularPosts = computed(() => posts.value.slice(1))

const stripHtml = (value) => {
  const div = document.createElement('div')
  div.innerHTML = value || ''
  return div.textContent || div.innerText || ''
}

const getPostImage = (post) => {
  if (!post) return fallbackImage
  if (post.image_url) return post.image_url
  const match = String(post.content || '').match(/<img[^>]+src=["']([^"']+)["']/i)
  return match?.[1] || fallbackImage
}

const getPostExcerpt = (post, length) => {
  return stripHtml(post?.content || '').substring(0, length)
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const fetchBlogs = async () => {
  try {
    const response = await api.get('/blog/')
    posts.value = response.data
  } catch (error) {
    console.error('Failed to fetch blog list:', error)
  }
}

onMounted(fetchBlogs)
</script>
