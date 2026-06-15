<template>
  <div class="bg-app-surface text-app-text antialiased font-body">
    <main class="pt-32 pb-24">
      <!-- Hero Section -->
      <header class="max-w-screen-2xl mx-auto px-12 mb-24 text-center md:text-left fade-in">
        <div class="max-w-3xl">
          <span class="text-secondary font-medium tracking-[0.2em] uppercase text-xs mb-4 block">Connect With The Source</span>
          <h1 class="text-6xl md:text-8xl font-headline text-primary leading-tight mb-8">Get in Touch</h1>
          <p class="text-lg text-app-text-variant leading-relaxed max-w-xl">
            Whether you are seeking advice on the perfect ritual for your hair or looking to partner with us, our collective is here to guide you.
          </p>
        </div>
      </header>

      <!-- Main Content Grid -->
      <section class="max-w-screen-2xl mx-auto px-12 grid grid-cols-1 lg:grid-cols-12 gap-16 lg:gap-24 w-full">
        <!-- Contact Form Area -->
        <div class="lg:col-span-7 bg-app-surface-container-low rounded-xl p-8 md:p-12 shadow-sm">
          <form @submit.prevent="handleSubmit" class="space-y-8">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 text-left">
              <div class="space-y-2">
                <label class="text-xs uppercase tracking-widest text-secondary font-semibold" for="name">Name</label>
                <input v-model="form.name" class="w-full bg-app-surface-container-highest border-none rounded-lg px-4 py-4 focus:ring-1 focus:ring-primary/20 transition-all placeholder:text-app-text-variant/40" id="name" placeholder="Evelyn Thorne" type="text" required/>
              </div>
              <div class="space-y-2">
                <label class="text-xs uppercase tracking-widest text-secondary font-semibold" for="email">Email</label>
                <input v-model="form.email" class="w-full bg-app-surface-container-highest border-none rounded-lg px-4 py-4 focus:ring-1 focus:ring-primary/20 transition-all placeholder:text-app-text-variant/40" id="email" placeholder="evelyn@botanical.com" type="email" required/>
              </div>
            </div>
            <div class="space-y-2 text-left">
              <label class="text-xs uppercase tracking-widest text-secondary font-semibold" for="topic">Topic</label>
              <select v-model="form.topic" class="w-full bg-app-surface-container-highest border-none rounded-lg px-4 py-4 focus:ring-1 focus:ring-primary/20 transition-all appearance-none" id="topic">
                <option>General Inquiry</option>
                <option>Order Support</option>
                <option>Press & Media</option>
                <option>Wholesale Partnerships</option>
              </select>
            </div>
            <div class="space-y-2 text-left">
              <label class="text-xs uppercase tracking-widest text-secondary font-semibold" for="message">Message</label>
              <textarea v-model="form.message" class="w-full bg-app-surface-container-highest border-none rounded-lg px-4 py-4 focus:ring-1 focus:ring-primary/20 transition-all placeholder:text-app-text-variant/40 resize-none" id="message" placeholder="How can we assist your journey today?" rows="6" required></textarea>
            </div>
            <button :disabled="loading" class="w-full md:w-auto px-12 py-5 bg-primary text-on-primary rounded-xl font-semibold tracking-wide hover:bg-primary-container transition-all duration-300 flex items-center justify-center gap-2" type="submit">
              <span v-if="loading" class="animate-spin material-symbols-outlined">progress_activity</span>
              <span v-else>Send Message</span>
              <span class="material-symbols-outlined text-sm">arrow_forward</span>
            </button>
          </form>
        </div>

        <!-- Sidebar Info -->
        <div class="lg:col-span-5 space-y-16 text-left">
          <!-- Customer Care -->
          <div>
            <h3 class="text-2xl font-headline text-primary mb-8">Customer Care</h3>
            <div class="space-y-8">
              <div v-for="contact in contactInfo" :key="contact.label" class="flex flex-col">
                <span class="text-xs uppercase tracking-widest text-secondary font-bold mb-1">{{ contact.label }}</span>
                <a :href="'mailto:' + contact.email" class="text-lg hover:text-primary transition-colors">{{ contact.email }}</a>
              </div>
            </div>
          </div>

          <!-- Visit Our Sanctuary -->
          <div class="relative overflow-hidden rounded-xl bg-app-surface-container shadow-sm p-8">
            <h3 class="text-2xl font-headline text-primary mb-4">Visit our Sanctuary</h3>
            <p class="text-app-text-variant mb-6 leading-relaxed">
              128 Botanical Way, Greenhouse District<br/>
              Portland, Oregon 97201
            </p>
            <div class="w-full h-48 bg-stone-200 rounded-lg relative overflow-hidden group">
              <img class="w-full h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-700" src="/assets/images/hero.png" alt="Map"/>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="bg-primary text-on-primary px-4 py-2 rounded-full text-xs font-bold tracking-widest uppercase shadow-lg">View Map</span>
              </div>
            </div>
          </div>

          <!-- Brand Quote -->
          <div class="border-t border-outline-variant/30 pt-8 flex gap-6 items-start">
            <div class="w-24 h-32 rounded-lg overflow-hidden shrink-0 shadow-md">
                <img src="/assets/images/shampoo.png" class="w-full h-full object-cover grayscale" alt="Fern"/>
            </div>
            <div class="flex-1">
              <blockquote class="italic font-headline text-app-text-variant leading-relaxed mb-4">
                "True beauty is not manufactured; it is cultivated through patience, purity, and the wisdom of the earth."
              </blockquote>
              <cite class="not-italic text-xs uppercase tracking-[0.2em] font-bold text-secondary">— The Verdant Ethos</cite>
            </div>
          </div>
        </div>
      </section>

      <!-- Global Reach -->
      <section class="max-w-screen-2xl mx-auto px-12 mt-32 text-center">
        <div class="py-16 border-y border-outline-variant/20 flex flex-wrap justify-center items-center gap-12 md:gap-24 opacity-50 grayscale transition-all hover:grayscale-0 hover:opacity-100">
          <span v-for="press in pressLogos" :key="press" class="font-headline text-2xl tracking-tighter">{{ press }}</span>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const loading = ref(false)
const form = reactive({
  name: '',
  email: '',
  topic: 'General Inquiry',
  message: ''
})

const contactInfo = [
  { label: 'Support Rituals', email: 'care@verdantmane.com' },
  { label: 'Press & Media', email: 'journal@verdantmane.com' },
  { label: 'Wholesale & Trade', email: 'stockists@verdantmane.com' }
]

const pressLogos = ['VOGUE', "Harper's BAZAAR", 'ELLE', 'Architectural Digest']

const handleSubmit = async () => {
  loading.value = true
  try {
    // Giả lập gửi tin nhắn liên hệ
    setTimeout(() => {
      console.log('Sending message:', form)
      alert('Tin nhắn của bạn đã được gửi thành công! Chúng tôi sẽ liên hệ lại sớm nhất.')
      form.name = ''
      form.email = ''
      form.message = ''
      loading.value = false
    }, 1500)
  } catch (error) {
    console.error('Contact error:', error)
    loading.value = false
  }
}
</script>
