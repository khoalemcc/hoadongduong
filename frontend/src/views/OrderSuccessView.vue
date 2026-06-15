<template>
  <main class="min-h-screen bg-app-bg flex flex-col items-center justify-center px-4 py-16 fade-in">

    <!-- Hero Banner Image -->
    <div class="w-full max-w-3xl rounded-3xl overflow-hidden shadow-2xl shadow-primary/10 mb-12 relative">
      <img
        src="/order-success-banner.png"
        alt="Order Successful - Botanical Collection"
        class="w-full h-72 object-cover object-center"
      />
      <!-- Overlay gradient for text legibility -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent flex flex-col justify-end p-10">
        <div class="flex items-center gap-4 mb-3">
          <div class="w-12 h-12 rounded-full bg-primary/90 backdrop-blur-sm flex items-center justify-center shadow-xl animate-bounce-once">
            <span class="material-symbols-outlined text-white text-2xl">check_circle</span>
          </div>
          <span class="text-[10px] font-black uppercase tracking-[0.3em] text-primary/80 bg-white/10 backdrop-blur-sm px-4 py-1.5 rounded-full border border-white/20">
            Order Confirmed
          </span>
        </div>
        <h1 class="font-headline text-4xl md:text-5xl font-bold text-white leading-tight drop-shadow-lg">
          Thank You,<br/>Your Botanical Journey Begins.
        </h1>
      </div>
    </div>

    <!-- Order Detail Card -->
    <div class="w-full max-w-3xl bg-app-surface rounded-3xl border border-white/5 shadow-2xl p-10 space-y-8">

      <!-- Order ID & Status -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-8 border-b border-white/5">
        <div>
          <p class="text-[10px] font-black uppercase tracking-widest text-stone-500 mb-1">Order Reference</p>
          <p class="font-mono text-2xl font-bold text-primary">#{{ orderId }}</p>
        </div>
        <div class="inline-flex items-center gap-2 px-5 py-2.5 bg-primary/10 text-primary rounded-full text-[10px] font-black uppercase tracking-widest">
          <div class="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
          Processing
        </div>
      </div>

      <!-- Timeline -->
      <div class="space-y-0">
        <p class="text-[10px] font-black uppercase tracking-widest text-stone-500 mb-6">What Happens Next</p>
        <div class="relative">
          <div class="absolute left-4 top-2 bottom-2 w-px bg-white/5"></div>
          <div
            v-for="(step, i) in steps"
            :key="i"
            class="flex items-start gap-6 pb-8 last:pb-0 relative"
          >
            <div :class="[
              'relative z-10 w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 transition-all',
              i === 0 ? 'bg-primary shadow-lg shadow-primary/30' : 'bg-app-surface border border-white/10'
            ]">
              <span :class="['material-symbols-outlined text-sm', i === 0 ? 'text-white' : 'text-stone-600']">
                {{ step.icon }}
              </span>
            </div>
            <div>
              <p :class="['font-bold text-sm', i === 0 ? 'text-white' : 'text-stone-500']">{{ step.title }}</p>
              <p class="text-stone-500 text-xs mt-1 leading-relaxed">{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Summary quick facts -->
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 pt-8 border-t border-white/5">
        <div v-for="fact in facts" :key="fact.label" class="bg-app-bg/50 rounded-2xl p-5 border border-white/5">
          <span class="material-symbols-outlined text-primary text-xl mb-2 block">{{ fact.icon }}</span>
          <p class="text-[9px] font-black uppercase tracking-widest text-stone-500">{{ fact.label }}</p>
          <p class="text-sm font-bold text-white mt-1">{{ fact.value }}</p>
        </div>
      </div>

      <!-- CTA Buttons -->
      <div class="flex flex-col sm:flex-row gap-4 pt-4">
        <RouterLink
          to="/shop"
          class="flex-1 h-14 bg-primary text-white rounded-2xl font-bold flex items-center justify-center gap-2 hover:opacity-90 transition-all shadow-xl shadow-primary/10 text-sm"
        >
          <span class="material-symbols-outlined text-base">storefront</span>
          Continue Shopping
        </RouterLink>
        <RouterLink
          to="/account"
          class="flex-1 h-14 bg-app-bg text-stone-300 border border-white/10 rounded-2xl font-bold flex items-center justify-center gap-2 hover:border-primary/30 transition-all text-sm"
        >
          <span class="material-symbols-outlined text-base">receipt_long</span>
          View My Orders
        </RouterLink>
      </div>

      <!-- Footer note -->
      <p class="text-center text-[10px] text-stone-600 leading-relaxed pt-2">
        A confirmation email has been sent to your registered address.<br/>
        <span class="text-stone-500">Questions? Contact us at <span class="text-primary">support@hoadongduong.vn</span></span>
      </p>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const orderId = ref(route.query.id || Math.floor(Math.random() * 90000 + 10000))

const steps = [
  {
    icon: 'check_circle',
    title: 'Order Received',
    desc: 'Your order has been confirmed and is being prepared by our botanical team.'
  },
  {
    icon: 'inventory_2',
    title: 'Packaging',
    desc: 'Your items will be carefully packaged with eco-friendly materials within 24 hours.'
  },
  {
    icon: 'local_shipping',
    title: 'Shipping',
    desc: 'You will receive a tracking code via SMS once your order is dispatched.'
  },
  {
    icon: 'where_to_vote',
    title: 'Delivered',
    desc: 'Enjoy your botanical collection. We hope it brings you joy and wellness.'
  }
]

const facts = [
  { icon: 'local_shipping', label: 'Shipping', value: 'Standard 3–5 days' },
  { icon: 'eco', label: 'Packaging', value: '100% Eco-friendly' },
  { icon: 'support_agent', label: 'Support', value: '24/7 Available' }
]
</script>

<style scoped>
@keyframes bounce-once {
  0%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}
.animate-bounce-once {
  animation: bounce-once 0.8s ease 0.3s both;
}
</style>
