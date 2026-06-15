<template>
  <div class="min-h-screen flex bg-app-bg text-app-text font-body fade-in">
    <AdminSidebar />
    <main class="flex-1 min-w-0 flex flex-col bg-app-bg">
      <header class="h-20 px-8 flex items-center justify-between bg-app-bg border-b border-white/5">
        <h2 class="text-2xl font-headline font-bold">System Configuration</h2>
      </header>
      <section class="p-8">
        <div class="max-w-2xl bg-app-surface p-10 rounded-2xl border border-white/5 shadow-2xl">
          <div class="space-y-8">
            <div class="pb-8 border-b border-white/5">
              <h3 class="text-lg font-bold text-primary mb-2">Store Profile</h3>
              <p class="text-xs text-stone-500 mb-6">Manage how your botanical brand appears to patrons.</p>
              <div class="space-y-4">
                <div v-for="field in ['Brand Name', 'Service Email', 'Inventory Location']" :key="field" class="space-y-2">
                  <label class="text-[9px] font-black uppercase tracking-widest text-stone-500">{{ field }}</label>
                  <input class="w-full bg-app-surface border-white/5 rounded-xl px-4 py-3 text-sm text-white" :placeholder="'Enter ' + field" />
                </div>
              </div>
            </div>
            <div class="pb-8 border-b border-white/5">
              <h3 class="text-lg font-bold text-primary mb-2">Visual Palette</h3>
              <p class="text-xs text-stone-500 mb-6">Customize the interface ambiance to match your current season.</p>
              <div class="grid grid-cols-2 gap-4">
                <button v-for="theme in themes" :key="theme.id" 
                        @click="setTheme(theme.id)"
                        :class="['p-4 rounded-xl border transition-all text-left flex items-center gap-3', currentTheme === theme.id ? 'border-primary bg-primary/10' : 'border-white/5 bg-app-surface hover:bg-white/5']">
                  <div :class="['w-4 h-4 rounded-full', theme.colorClass]"></div>
                  <div>
                    <p class="text-xs font-bold text-white">{{ theme.name }}</p>
                    <p class="text-[8px] text-stone-500 uppercase tracking-widest mt-0.5">{{ theme.desc }}</p>
                  </div>
                </button>
              </div>
            </div>
            <button @click="saveSettings" class="w-full py-4 bg-primary text-white rounded-2xl font-black uppercase tracking-[0.2em] text-[10px] hover:bg-primary/90 transition-all shadow-xl shadow-primary/10 relative overflow-hidden group">
              <span class="relative z-10 flexItemsCenter justify-center gap-2">
                 <span v-if="saving" class="material-symbols-outlined text-sm animate-spin">progress_activity</span>
                 {{ saving ? 'Saving Parameters...' : 'Save All Parameters' }}
              </span>
            </button>
          </div>
        </div>
      </section>
    </main>

    <!-- Notification Toast -->
    <Transition name="toast">
      <div v-if="showToast" class="fixed bottom-8 right-8 z-50 bg-primary text-white px-6 py-4 rounded-2xl shadow-2xl shadow-primary/20 flex items-center gap-3">
        <span class="material-symbols-outlined">check_circle</span>
        <span class="text-sm font-bold">Parameters synchronized successfully!</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminSidebar from '../components/AdminSidebar.vue'

const saving = ref(false)
const showToast = ref(false)

const currentTheme = ref('botanical')

const themes = [
  { id: 'botanical', name: 'Botanical Green', desc: 'Default Flora', colorClass: 'bg-[#163423]' },
  { id: 'deepsea', name: 'Deep Sea Blue', desc: 'Oceanic Essence', colorClass: 'bg-[#1e3a8a]' },
  { id: 'midnight', name: 'Midnight Bloom', desc: 'Dark Ethereal', colorClass: 'bg-[#8b5cf6]' },
  { id: 'earth', name: 'Terra Cotta', desc: 'Earthy Warmth', colorClass: 'bg-[#78350f]' }
]

const setTheme = (id) => {
  currentTheme.value = id
  localStorage.setItem('verdant-theme', id)
  
  // Apply to document without wiping other classes
  const root = document.documentElement
  themes.forEach(t => root.classList.remove(`theme-${t.id}`))
  root.classList.add(`theme-${id}`)
  
  // Force a small reflow or just ensure variables are updated
  console.log(`Theme set to ${id}`)
}

const saveSettings = () => {
  saving.value = true
  setTimeout(() => {
    saving.value = false
    showToast.value = true
    setTimeout(() => { showToast.value = false }, 3000)
  }, 800)
}

onMounted(() => {
  const saved = localStorage.getItem('verdant-theme') || 'botanical'
  currentTheme.value = saved
  document.documentElement.classList.add(`theme-${saved}`)
})
</script>

<style scoped>
.toast-enter-active { animation: slideUp 0.4s ease; }
.toast-leave-active { animation: slideUp 0.3s ease reverse; }
@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
