<template>
  <div class="min-h-screen flex bg-app-bg text-app-text font-body">
    <AdminSidebar />
    <main class="flex-1 flex flex-col">
      <header class="h-20 px-8 flex items-center justify-between border-b border-white/5">
        <div>
          <h2 class="text-2xl font-headline font-bold">Stock Movement Logs</h2>
          <p class="text-[10px] font-black uppercase tracking-widest text-stone-500 mt-1">Traceability for every inventory transaction</p>
        </div>
      </header>

      <section class="p-8">
        <div class="bg-app-surface rounded-2xl border border-white/5 overflow-hidden shadow-2xl">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="text-stone-500 text-[10px] font-black uppercase tracking-widest border-b border-white/5 bg-app-surface/50">
                <th class="py-6 px-8">Timestamp</th>
                <th class="py-6 px-6">Product ID</th>
                <th class="py-6 px-6">Action</th>
                <th class="py-6 px-6 text-center">Before</th>
                <th class="py-6 px-6 text-center">After</th>
                <th class="py-6 px-8">Note</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
              <tr v-for="log in logs" :key="log.id" class="hover:bg-white/5 transition-colors">
                <td class="py-5 px-8 text-xs text-stone-400">{{ formatDate(log.created_at) }}</td>
                <td class="py-5 px-6 font-bold text-sm">#{{ log.product_id }}</td>
                <td class="py-5 px-6">
                  <span :class="['px-2 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest border', getActionStyle(log.action)]">
                    {{ log.action }}
                  </span>
                </td>
                <td class="py-5 px-6 text-center font-mono text-stone-500">{{ log.quantity_before }}</td>
                <td class="py-5 px-6 text-center font-mono font-bold" :class="log.quantity_after > log.quantity_before ? 'text-primary' : 'text-red-400'">
                  {{ log.quantity_after }}
                </td>
                <td class="py-5 px-8 text-sm text-stone-400 italic">{{ log.note || '---' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminSidebar from '../components/AdminSidebar.vue'
import api from '../api'

const logs = ref([])

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString()
}

const getActionStyle = (action) => {
  const map = {
    import: 'bg-primary/10 text-primary border-primary/20',
    export: 'bg-amber-500/10 text-amber-500 border-amber-500/20',
    refund: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    lock: 'bg-stone-800 text-stone-400 border-stone-700'
  }
  return map[action] || map.lock
}

const fetchLogs = async () => {
  try {
    const res = await api.get('/admin/inventory/logs')
    logs.value = res.data
  } catch (err) {
    console.error('Failed to fetch logs', err)
  }
}

onMounted(fetchLogs)
</script>
