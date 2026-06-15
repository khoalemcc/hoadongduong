<template>
  <div class="min-h-screen bg-app-surface text-app-text font-body selection:bg-primary-fixed selection:text-on-primary-fixed">
    <!-- Glass Header -->
    <header class="fixed top-0 left-0 w-full z-50 glass-nav bg-[#fcf9f4]/80 flex justify-between items-center px-8 h-20 border-b border-surface-container/50">
      <RouterLink to="/" class="font-headline text-2xl font-bold italic text-primary">Verdant Haircare</RouterLink>
      <div class="flex items-center gap-6">
        <button class="text-secondary hover:opacity-70 transition-opacity active:scale-95 duration-300">
          <span class="material-symbols-outlined">help_outline</span>
        </button>
      </div>
    </header>

    <main class="min-h-screen flex items-stretch">
      <!-- Left Editorial Section -->
      <section class="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-app-surface-container">
        <img alt="Verdant Botanical Aesthetics" class="absolute inset-0 w-full h-full object-cover zoom-in" src="/assets/images/mask.png"/>
        <div class="absolute inset-0 bg-primary/10 mix-blend-multiply"></div>
        <div class="relative z-10 flex flex-col justify-end p-20 w-full text-surface-container-lowest">
          <h1 class="font-headline text-5xl font-bold leading-tight mb-6">Rooted in <br/><span class="italic">Nature's Wisdom</span></h1>
          <p class="font-body text-lg max-w-md opacity-90 leading-relaxed">Experience the transformative power of botanical science. Our artisanal formulas are crafted for the modern individual.</p>
        </div>
      </section>

      <!-- Right Login Section -->
      <section class="w-full lg:w-1/2 flex items-center justify-center p-8 md:p-16 bg-app-surface mt-20 lg:mt-0">
        <div class="w-full max-w-md fade-in">
          <div class="mb-12">
            <h2 class="font-headline text-4xl font-bold text-primary mb-4">Welcome Back</h2>
            <p class="text-secondary font-body">Sign in to access your personalized haircare sanctuary.</p>
            <p v-if="errorMsg" class="mt-4 text-error text-sm font-bold bg-error-container/20 p-3 rounded-lg flex items-center gap-2">
              <span class="material-symbols-outlined text-lg">error</span>
              {{ errorMsg }}
            </p>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-6">
            <div class="space-y-2">
              <label class="block text-xs font-label uppercase tracking-widest text-secondary font-semibold" for="email">Email Address</label>
              <input v-model="email" class="w-full h-14 px-6 rounded-xl bg-white border border-outline-variant/30 focus:ring-2 focus:ring-primary/20 transition-all duration-300 text-black placeholder:text-stone-400" id="email" placeholder="name@example.com" type="email" required/>
            </div>

            <div class="space-y-2">
              <div class="flex justify-between items-center">
                <label class="block text-xs font-label uppercase tracking-widest text-secondary font-semibold" for="password">Password</label>
                <a class="text-xs font-label uppercase tracking-widest text-primary hover:underline transition-all" href="#">Forgot password?</a>
              </div>
              <input v-model="password" class="w-full h-14 px-6 rounded-xl bg-white border border-outline-variant/30 focus:ring-2 focus:ring-primary/20 transition-all duration-300 text-black placeholder:text-stone-400" id="password" placeholder="••••••••" type="password" required/>
            </div>

            <div class="flex items-center gap-3 py-2">
              <input v-model="remember" class="w-5 h-5 rounded border-outline-variant text-primary focus:ring-primary" id="remember" type="checkbox"/>
              <label class="text-sm text-secondary" for="remember">Keep me signed in for 30 days</label>
            </div>

            <button :disabled="loading" class="w-full h-14 bg-gradient-to-br from-primary to-primary-container text-on-primary rounded-xl font-semibold tracking-wide editorial-shadow hover:opacity-95 transition-all active:scale-95 duration-300 flex items-center justify-center gap-2" type="submit">
              <span v-if="loading" class="animate-spin material-symbols-outlined">progress_activity</span>
              <span v-else>Sign In</span>
              <span class="material-symbols-outlined text-lg">arrow_forward</span>
            </button>
          </form>

          <div class="mt-12 pt-8 border-t border-surface-container flex flex-col items-center gap-6">
            <p class="text-sm text-secondary">New to Verdant Haircare?</p>
            <button class="w-full h-14 border border-outline-variant text-primary rounded-xl font-semibold hover:bg-app-surface-container-low transition-all duration-300">
              Create an Account
            </button>
          </div>
        </div>
      </section>
    </main>

    <footer class="bg-app-surface-container-low text-primary font-body flex flex-col md:flex-row justify-between items-center px-12 py-8 w-full">
      <div class="font-headline text-xl font-semibold mb-4 md:mb-0">Verdant Haircare</div>
      <div class="flex flex-wrap justify-center gap-8 mb-4 md:mb-0">
        <a class="text-xs font-label uppercase tracking-widest text-secondary hover:text-primary transition-colors" href="#">Privacy</a>
        <a class="text-xs font-label uppercase tracking-widest text-secondary hover:text-primary transition-colors" href="#">Terms</a>
        <a class="text-xs font-label uppercase tracking-widest text-secondary hover:text-primary transition-colors" href="#">Accessibility</a>
      </div>
      <div class="text-[10px] font-label uppercase tracking-widest text-secondary opacity-60">
        © 2024 Verdant Botanical Haircare. All rights reserved.
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const email = ref('')
const password = ref('')
const remember = ref(false)
const loading = ref(false)
const errorMsg = ref('')

const handleLogin = async () => {
  loading.value = true
  errorMsg.value = ''
  try {
    const formData = new FormData()
    formData.append('username', email.value)
    formData.append('password', password.value)

    const response = await api.post('/auth/login', formData)
    
    // Extract info from response
    const { access_token, user } = response.data
    
    // Senior Pattern: Store data in Pinia (which handles localStorage)
    authStore.setUser(user, access_token)

    // Redirect based on role
    const redirect = router.currentRoute.value.query.redirect
    if (typeof redirect === 'string' && redirect.startsWith('/')) {
      router.push(redirect)
    } else if (authStore.isAdmin) {
      router.push('/admin')
    } else {
      router.push('/')
    }
  } catch (error) {
    console.error('Login error:', error)
    errorMsg.value = error.response?.data?.detail || 'Invalid email or password'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.glass-nav {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
.editorial-shadow {
  box-shadow: 0px 24px 48px rgba(28, 28, 25, 0.06);
}
.zoom-in {
  animation: zoom 20s infinite alternate;
}
@keyframes zoom {
  from { transform: scale(1); }
  to { transform: scale(1.1); }
}
</style>
