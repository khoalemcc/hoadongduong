<template>
  <div class="min-h-screen flex bg-app-bg text-app-text font-body">
    <AdminSidebar />
    <main class="flex-1 min-w-0 flex flex-col">
      <header class="h-20 px-8 flex items-center justify-between border-b border-white/5">
        <div>
          <h2 class="text-2xl font-headline font-bold">Auto Content Factory</h2>
          <p class="text-[10px] font-black uppercase tracking-widest text-stone-500 mt-1">Source, review, and draft blog content</p>
        </div>
        <div class="flex items-center gap-3">
          <select v-model="status" class="bg-app-surface border border-white/5 rounded-xl px-4 py-2 text-xs font-bold text-stone-300 outline-none">
            <option value="draft">Draft</option>
            <option value="published">Published</option>
          </select>
          <button @click="previewSources" :disabled="loading" class="h-10 px-5 rounded-xl bg-app-surface border border-white/5 text-xs font-black uppercase tracking-widest hover:border-primary/40 disabled:opacity-50">
            Preview
          </button>
          <button @click="importSources" :disabled="loading || previewItems.length === 0" class="h-10 px-5 rounded-xl bg-primary text-white text-xs font-black uppercase tracking-widest disabled:opacity-50">
            Import
          </button>
        </div>
      </header>

      <section class="p-8 grid grid-cols-1 xl:grid-cols-12 gap-8">
        <div class="xl:col-span-4 space-y-6">
          <div class="bg-app-surface border border-white/5 rounded-2xl p-6 space-y-4">
            <div>
              <h3 class="font-bold text-lg">Source Intake</h3>
              <p class="text-xs text-stone-500 mt-1">One source URL per line. Imported articles are saved with source attribution.</p>
            </div>
            <textarea
              v-model="sourceText"
              class="w-full min-h-48 bg-app-bg border border-white/5 rounded-xl p-4 text-sm text-stone-300 outline-none focus:border-primary/40"
              spellcheck="false"
            />
            <div class="grid grid-cols-2 gap-4">
              <label class="space-y-2">
                <span class="text-[9px] font-black uppercase tracking-widest text-stone-500">Limit</span>
                <input v-model.number="limit" type="number" min="1" max="50" class="w-full bg-app-bg border border-white/5 rounded-xl px-4 py-3 text-sm outline-none" />
              </label>
              <label class="flex items-end gap-3 pb-3 text-xs text-stone-400">
                <input v-model="fullOwnedContent" type="checkbox" class="h-4 w-4 rounded border-white/10 text-primary bg-app-bg" />
                Full owned content
              </label>
              <label class="flex items-end gap-3 pb-3 text-xs text-stone-400">
                <input v-model="allowDuplicates" type="checkbox" class="h-4 w-4 rounded border-white/10 text-primary bg-app-bg" />
                Re-import duplicates
              </label>
            </div>
          </div>

          <div class="bg-app-surface border border-white/5 rounded-2xl p-6 space-y-4">
            <div>
              <h3 class="font-bold text-lg">Lead By Link</h3>
              <p class="text-xs text-stone-500 mt-1">Paste one article URL to pull it directly into the review queue.</p>
            </div>
            <input
              v-model="directLink"
              class="w-full bg-app-bg border border-white/5 rounded-xl px-4 py-3 text-sm outline-none focus:border-primary/40"
              placeholder="https://cocayhoala.vn/blogs/.../article-slug"
            />
            <div class="grid grid-cols-2 gap-3">
              <button @click="previewDirectLink" :disabled="loading || !directLink" class="h-11 rounded-xl bg-app-bg border border-white/5 text-xs font-black uppercase tracking-widest disabled:opacity-50">
                Preview Link
              </button>
              <button @click="importDirectLink" :disabled="loading || !directLink" class="h-11 rounded-xl bg-primary text-white text-xs font-black uppercase tracking-widest disabled:opacity-50">
                Import Link
              </button>
            </div>
          </div>

          <div class="bg-app-surface border border-white/5 rounded-2xl p-6 space-y-4">
            <div>
              <h3 class="font-bold text-lg">Original Draft</h3>
              <p class="text-xs text-stone-500 mt-1">Create a structured SEO draft for editors to refine.</p>
            </div>
            <input v-model="draftForm.topic" class="w-full bg-app-bg border border-white/5 rounded-xl px-4 py-3 text-sm outline-none focus:border-primary/40" placeholder="Topic" />
            <input v-model="draftForm.keyword" class="w-full bg-app-bg border border-white/5 rounded-xl px-4 py-3 text-sm outline-none focus:border-primary/40" placeholder="SEO keyword" />
            <input v-model="draftForm.audience" class="w-full bg-app-bg border border-white/5 rounded-xl px-4 py-3 text-sm outline-none focus:border-primary/40" placeholder="Audience" />
            <button @click="createDraft" :disabled="loading || !draftForm.topic" class="w-full h-11 rounded-xl bg-primary text-white text-xs font-black uppercase tracking-widest disabled:opacity-50">
              Create Draft
            </button>
          </div>
        </div>

        <div class="xl:col-span-8 space-y-6">
          <div v-if="message" class="bg-primary/10 border border-primary/20 text-primary rounded-xl px-5 py-4 text-sm font-bold">
            {{ message }}
          </div>

          <div v-if="warnings.length" class="bg-amber-500/10 border border-amber-500/20 rounded-xl px-5 py-4">
            <p class="text-xs font-black uppercase tracking-widest text-amber-400 mb-2">Warnings</p>
            <ul class="space-y-1 text-xs text-amber-100/80">
              <li v-for="warning in warnings" :key="warning">{{ warning }}</li>
            </ul>
          </div>

          <div class="bg-app-surface border border-white/5 rounded-2xl overflow-hidden">
            <div class="px-6 py-4 border-b border-white/5 flex items-center justify-between">
              <h3 class="font-bold">Preview Queue</h3>
              <span class="text-[10px] font-black uppercase tracking-widest text-stone-500">{{ previewItems.length }} items</span>
            </div>

            <div v-if="loading" class="h-80 flex items-center justify-center text-stone-500">
              <span class="material-symbols-outlined animate-spin mr-2">progress_activity</span>
              Processing
            </div>

            <div v-else-if="previewItems.length === 0" class="h-80 flex flex-col items-center justify-center text-stone-600">
              <span class="material-symbols-outlined text-5xl mb-4">article</span>
              <p class="text-xs font-black uppercase tracking-[0.3em]">No content previewed yet</p>
            </div>

            <div v-else class="divide-y divide-white/5">
              <article v-for="item in previewItems" :key="item.source_url" class="p-6 hover:bg-white/[0.02] transition-colors">
                <div class="flex items-start justify-between gap-6">
                  <div class="flex gap-4 min-w-0">
                    <img v-if="item.image_url" :src="item.image_url" class="h-24 w-32 object-cover rounded-xl border border-white/5 bg-app-bg flex-shrink-0" :alt="item.title" />
                    <div class="min-w-0">
                      <h4 class="font-bold text-lg text-white mb-2">{{ item.title }}</h4>
                      <p class="text-xs text-stone-500 mb-3 truncate">{{ item.source_url }}</p>
                      <p class="text-sm text-stone-400 leading-relaxed line-clamp-3">{{ stripHtml(item.content) }}</p>
                    </div>
                  </div>
                  <span class="shrink-0 text-[9px] font-black uppercase tracking-widest text-primary bg-primary/10 border border-primary/20 px-3 py-1 rounded-full">
                    {{ item.seo_keyword || 'SEO' }}
                  </span>
                </div>
              </article>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AdminSidebar from '../components/AdminSidebar.vue'
import api from '../api'

const defaultSources = [
  'https://cocayhoala.vn/blogs/news-cocayhoala?view=en',
  'https://cocayhoala.vn/blogs/cham-soc-toc',
  'https://cocayhoala.vn/blogs/cham-soc-co-the',
  'https://cocayhoala.vn/blogs/cham-soc-da'
]

const sourceText = ref(defaultSources.join('\n'))
const directLink = ref('')
const limit = ref(10)
const status = ref('draft')
const fullOwnedContent = ref(true)
const allowDuplicates = ref(false)
const loading = ref(false)
const previewItems = ref([])
const warnings = ref([])
const message = ref('')
const draftForm = ref({
  topic: '',
  keyword: '',
  audience: ''
})

const payload = () => ({
  source_urls: sourceText.value.split('\n').map(url => url.trim()).filter(Boolean),
  limit: limit.value || 10,
  full_owned_content: fullOwnedContent.value,
  allow_duplicates: allowDuplicates.value,
  status: status.value
})

const directPayload = () => ({
  source_urls: [directLink.value.trim()],
  limit: 1,
  full_owned_content: fullOwnedContent.value,
  allow_duplicates: allowDuplicates.value,
  status: status.value
})

const stripHtml = (value) => {
  const div = document.createElement('div')
  div.innerHTML = value || ''
  return div.textContent || div.innerText || ''
}

const previewSources = async () => {
  loading.value = true
  message.value = ''
  try {
    const res = await api.post('/admin/content-factory/preview', payload())
    previewItems.value = res.data.items || []
    warnings.value = res.data.warnings || []
  } catch (error) {
    message.value = error.response?.data?.detail || 'Preview failed'
  } finally {
    loading.value = false
  }
}

const importSources = async () => {
  loading.value = true
  message.value = ''
  try {
    const res = await api.post('/admin/content-factory/import', payload())
    warnings.value = res.data.warnings || []
    const duplicateCount = res.data.duplicates?.length || 0
    message.value = `Created ${res.data.created?.length || 0} posts, skipped ${res.data.skipped || 0}${duplicateCount ? ` (${duplicateCount} duplicate links)` : ''}.`
  } catch (error) {
    message.value = error.response?.data?.detail || 'Import failed'
  } finally {
    loading.value = false
  }
}

const previewDirectLink = async () => {
  loading.value = true
  message.value = ''
  try {
    const res = await api.post('/admin/content-factory/preview', directPayload())
    previewItems.value = res.data.items || []
    warnings.value = res.data.warnings || []
    message.value = previewItems.value.length ? 'Direct link is ready for review.' : 'No article was found for that link.'
  } catch (error) {
    message.value = error.response?.data?.detail || 'Direct link preview failed'
  } finally {
    loading.value = false
  }
}

const importDirectLink = async () => {
  loading.value = true
  message.value = ''
  try {
    const res = await api.post('/admin/content-factory/import', directPayload())
    warnings.value = res.data.warnings || []
    const duplicateCount = res.data.duplicates?.length || 0
    message.value = duplicateCount && !res.data.created?.length
      ? 'This link already exists. Enable Re-import duplicates to create another draft.'
      : `Created ${res.data.created?.length || 0} post from link, skipped ${res.data.skipped || 0}.`
  } catch (error) {
    message.value = error.response?.data?.detail || 'Direct link import failed'
  } finally {
    loading.value = false
  }
}

const createDraft = async () => {
  loading.value = true
  message.value = ''
  try {
    const res = await api.post('/admin/content-factory/draft', {
      ...draftForm.value,
      status: status.value
    })
    message.value = `Draft created: ${res.data.title}`
    draftForm.value = { topic: '', keyword: '', audience: '' }
  } catch (error) {
    message.value = error.response?.data?.detail || 'Draft creation failed'
  } finally {
    loading.value = false
  }
}
</script>
