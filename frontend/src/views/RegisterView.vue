<template>
  <div class="min-h-screen bg-app-surface text-app-text font-body selection:bg-primary-fixed selection:text-on-primary-fixed">
    <div class="min-h-screen flex flex-col md:flex-row relative overflow-hidden">
      <!-- Left Side: Editorial Image & Brand Identity -->
      <div class="hidden md:flex md:w-5/12 lg:w-1/2 relative bg-app-surface-container overflow-hidden items-center justify-center p-12">
        <div class="absolute inset-0 z-0">
          <img class="w-full h-full object-cover opacity-90 scale-105" src="/assets/images/wax.png" alt="Botany"/>
          <div class="absolute inset-0 bg-gradient-to-tr from-primary/30 to-transparent"></div>
        </div>
        <div class="relative z-10 text-center max-w-md fade-in">
          <RouterLink to="/" class="font-headline text-5xl lg:text-7xl font-bold italic text-white tracking-tight leading-tight block">
            Verdant Mane
          </RouterLink>
          <p class="mt-6 text-white/90 text-lg font-light leading-relaxed tracking-wide">
            Cultivate your natural radiance through the science of botanical alchemy.
          </p>
          <div class="mt-12 inline-flex items-center space-x-4 px-6 py-3 bg-white/10 backdrop-blur-md rounded-xl border border-white/20">
            <span class="material-symbols-outlined text-white">eco</span>
            <span class="text-white text-sm uppercase tracking-widest font-medium">Eco-Conscious Formulations</span>
          </div>
        </div>
      </div>

      <!-- Right Side: Registration Form -->
      <main class="flex-1 flex items-center justify-center p-6 md:p-12 lg:p-24 relative z-10 bg-app-surface">
        <!-- Mobile Brand Logo -->
        <div class="md:hidden absolute top-8 left-8">
          <RouterLink to="/" class="font-headline text-2xl font-bold italic text-primary">Verdant Mane</RouterLink>
        </div>

        <div class="w-full max-w-md space-y-10 fade-in">
          <header class="space-y-4">
            <h2 class="font-headline text-4xl font-bold text-primary tracking-tight text-left">Create your sanctuary</h2>
            <p class="text-secondary text-base leading-relaxed text-left">Join our circle and experience the purity of curated botanical haircare tailored to your unique essence.</p>
          </header>

          <form @submit.prevent="handleRegister" class="space-y-6">
            <div class="group">
              <label class="block text-xs font-semibold uppercase tracking-widest text-secondary mb-2 ml-1 text-left" for="full_name">Full Name</label>
              <input v-model="form.fullName" class="w-full h-14 px-6 bg-app-surface-container-low border-none rounded-xl text-app-text placeholder:text-outline/50 focus:ring-1 focus:ring-primary/20 focus:bg-app-surface-container-highest transition-all duration-300" id="full_name" placeholder="Evelyn Thorne" type="text" required/>
            </div>

            <div class="group">
              <label class="block text-xs font-semibold uppercase tracking-widest text-secondary mb-2 ml-1 text-left" for="email">Email Address</label>
              <input v-model="form.email" class="w-full h-14 px-6 bg-app-surface-container-low border-none rounded-xl text-app-text placeholder:text-outline/50 focus:ring-1 focus:ring-primary/20 focus:bg-app-surface-container-highest transition-all duration-300" id="email" placeholder="hello@verdantmane.com" type="email" required/>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="group">
                <label class="block text-xs font-semibold uppercase tracking-widest text-secondary mb-2 ml-1 text-left" for="password">Password</label>
                <input v-model="form.password" class="w-full h-14 px-6 bg-app-surface-container-low border-none rounded-xl text-app-text focus:ring-1 focus:ring-primary/20 focus:bg-app-surface-container-highest transition-all duration-300" id="password" placeholder="••••••••" type="password" required/>
              </div>
              <div class="group">
                <label class="block text-xs font-semibold uppercase tracking-widest text-secondary mb-2 ml-1 text-left" for="confirm_password">Confirm Password</label>
                <input v-model="form.confirmPassword" class="w-full h-14 px-6 bg-app-surface-container-low border-none rounded-xl text-app-text focus:ring-1 focus:ring-primary/20 focus:bg-app-surface-container-highest transition-all duration-300" id="confirm_password" placeholder="••••••••" type="password" required/>
              </div>
            </div>

            <div class="flex items-start space-x-3 py-2">
              <div class="flex items-center h-6">
                <input v-model="form.newsletter" class="h-5 w-5 rounded border-outline-variant text-primary focus:ring-primary-container bg-app-surface-container-low transition-colors" id="newsletter" type="checkbox"/>
              </div>
              <div class="text-sm">
                <label class="text-secondary leading-snug cursor-pointer select-none text-left block" for="newsletter">Subscribe to our botanical newsletter for exclusive seasonal rituals and early collection access.</label>
              </div>
            </div>

            <div class="pt-4">
              <button :disabled="loading" class="cta-gradient w-full h-14 rounded-xl text-on-primary font-semibold tracking-wide text-lg shadow-lg active:scale-[0.98] transition-transform duration-200 flex items-center justify-center space-x-2">
                <span v-if="loading" class="animate-spin material-symbols-outlined">progress_activity</span>
                <span v-else>Create Account</span>
                <span class="material-symbols-outlined text-xl">arrow_forward</span>
              </button>
            </div>
          </form>

          <footer class="text-center pt-6">
            <p class="text-sm text-secondary">
              Already have an account? 
              <RouterLink to="/login" class="text-primary font-bold hover:underline underline-offset-4 transition-all">Sign In</RouterLink>
            </p>
            <div class="mt-12 flex items-center justify-center space-x-8 opacity-40 grayscale contrast-125">
              <div class="flex items-center space-x-1">
                <span class="material-symbols-outlined text-sm">verified</span>
                <span class="text-[10px] uppercase tracking-[0.2em] font-bold">Cruelty Free</span>
              </div>
              <div class="flex items-center space-x-1">
                <span class="material-symbols-outlined text-sm">nature</span>
                <span class="text-[10px] uppercase tracking-[0.2em] font-bold">100% Organic</span>
              </div>
            </div>
          </footer>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const form = reactive({
  fullName: '',
  email: '',
  password: '',
  confirmPassword: '',
  newsletter: true
})

const handleRegister = async () => {
  if (form.password !== form.confirmPassword) {
    alert('Mật khẩu xác nhận không khớp!')
    return
  }

  loading.value = true
  try {
    // Giả lập gọi API đăng ký
    setTimeout(() => {
      console.log('Registering user:', form.email)
      alert('Tạo tài khoản thành công! Chào mừng bạn đến với Verdant Mane.')
      router.push('/login')
      loading.value = false
    }, 1500)
  } catch (error) {
    console.error('Registration error:', error)
    loading.value = false
  }
}
</script>

<style scoped>
.cta-gradient {
  background: linear-gradient(145deg, #0f52ba 0%, #0747a6 100%);
}
.zoom-in {
  animation: zoom 20s infinite alternate;
}
@keyframes zoom {
  from { transform: scale(1); }
  to { transform: scale(1.1); }
}
</style>
