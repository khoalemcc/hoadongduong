<template>
  <div class="min-h-screen flex bg-app-bg text-app-text font-body">
    <AdminSidebar />
    <main class="flex-1 flex flex-col">
      <header class="h-20 px-8 flex items-center justify-between border-b border-white/5">
        <h2 class="text-2xl font-headline font-bold">Brand Partnerships</h2>
      </header>
      <section class="p-8">
        <div class="flex flex-col items-center justify-center h-64 bg-app-surface rounded-2xl border-2 border-dashed border-white/10">
           <span class="material-symbols-outlined text-4xl text-stone-700 mb-4">sell</span>
           <p class="text-stone-500 uppercase text-[10px] font-black tracking-[0.3em]">Brand Identity Module Initializing</p>
        </div>
      </section>
    </main>
  </div>
</template>
<script setup>
import AdminSidebar from '../components/AdminSidebar.vue'
</script>
