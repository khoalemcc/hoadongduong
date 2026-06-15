<template>
  <div class="fixed bottom-8 right-8 z-50 flex flex-col items-end gap-4 font-body">
    <!-- Chat Window Container -->
    <Transition name="chat-window">
      <div v-if="isOpen" class="w-80 bg-app-surface/90 backdrop-blur-xl border border-white/10 rounded-3xl shadow-2xl overflow-hidden flex flex-col mb-4 ring-1 ring-white/5">
        <!-- Header -->
        <div class="p-6 bg-primary text-white flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center backdrop-blur-md">
              <span class="material-symbols-outlined">support_agent</span>
            </div>
            <div>
              <h4 class="font-headline font-bold text-sm">Hoa Đông Dương Support</h4>
              <p class="text-[10px] text-white/70 uppercase tracking-widest font-black">Online Now</p>
            </div>
          </div>
          <button @click="isOpen = false" class="hover:bg-white/10 p-1 rounded-full transition-colors">
            <span class="material-symbols-outlined text-xl">close</span>
          </button>
        </div>

        <!-- Chat Content -->
        <div class="flex-1 p-6 space-y-4 max-h-[300px] overflow-y-auto">
          <div class="bg-white/5 p-4 rounded-2xl rounded-tl-none border border-white/5">
            <p class="text-xs text-stone-300 leading-relaxed">Chào bạn! Chúng tôi có thể giúp gì cho bạn hôm nay?</p>
          </div>
          
          <!-- Channels -->
          <div class="grid grid-cols-1 gap-3 pt-4">
            <a href="https://zalo.me/0389984272" target="_blank" class="flex items-center justify-between p-4 bg-white/5 border border-white/5 rounded-2xl hover:bg-primary/20 hover:border-primary/30 transition-all group">
              <div class="flex items-center gap-3">
                <img src="https://img.icons8.com/color/48/zalo.png" class="w-6 h-6" alt="Zalo">
                <span class="text-sm font-bold text-white">Chat qua Zalo</span>
              </div>
              <span class="material-symbols-outlined text-stone-600 group-hover:text-primary transition-colors">arrow_forward</span>
            </a>
            
            <a href="https://m.me/yourid" target="_blank" class="flex items-center justify-between p-4 bg-white/5 border border-white/5 rounded-2xl hover:bg-blue-500/20 hover:border-blue-500/30 transition-all group">
              <div class="flex items-center gap-3">
                <img src="https://img.icons8.com/color/48/messenger-new.png" class="w-6 h-6" alt="Messenger">
                <span class="text-sm font-bold text-white">Messenger</span>
              </div>
              <span class="material-symbols-outlined text-stone-600 group-hover:text-blue-400 transition-colors">arrow_forward</span>
            </a>
          </div>
        </div>

        <!-- Footer -->
        <div class="p-4 border-t border-white/5 bg-black/20 flex items-center gap-2">
           <input type="text" placeholder="Gửi tin nhắn..." class="flex-1 bg-white/5 border border-white/10 rounded-full px-4 py-2 text-xs text-white focus:outline-none focus:ring-1 focus:ring-primary/50">
           <button class="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white hover:scale-110 transition-transform">
             <span class="material-symbols-outlined text-sm">send</span>
           </button>
        </div>
      </div>
    </Transition>

    <!-- Floating Trigger Button -->
    <button @click="isOpen = !isOpen" 
      :class="['w-14 h-14 rounded-full flex items-center justify-center shadow-2xl transition-all duration-500 hover:scale-110 relative group', isOpen ? 'bg-stone-800 rotate-90' : 'bg-primary pulse-effect']">
      <span class="material-symbols-outlined text-white text-3xl">
        {{ isOpen ? 'close' : 'chat' }}
      </span>
      
      <!-- Tooltip -->
      <span v-if="!isOpen" class="absolute right-full mr-4 px-3 py-1.5 bg-stone-900 text-white text-[10px] font-black uppercase tracking-widest rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap border border-white/5">
        Chat với chúng tôi
      </span>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isOpen = ref(false)
</script>

<style scoped>
.pulse-effect {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.4); }
  70% { box-shadow: 0 0 0 15px rgba(74, 222, 128, 0); }
  100% { box-shadow: 0 0 0 0 rgba(74, 222, 128, 0); }
}

.chat-window-enter-active {
  animation: slideIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.chat-window-leave-active {
  animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) reverse;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(20px) scale(0.9); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
</style>
