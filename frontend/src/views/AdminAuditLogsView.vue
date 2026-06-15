<template>
  <div class="min-h-screen flex bg-app-bg text-app-text font-body">
    <AdminSidebar />
    <main class="flex-1 flex flex-col">
      <header class="h-20 px-8 flex items-center justify-between border-b border-white/5">
        <div>
          <h2 class="text-2xl font-headline font-bold">System Audit Trail</h2>
          <p class="text-[10px] font-black uppercase tracking-widest text-stone-500 mt-1">Immutable record of administrative operations</p>
        </div>
      </header>

      <section class="p-8">
        <div class="bg-app-surface rounded-2xl border border-white/5 overflow-hidden shadow-2xl">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="text-stone-500 text-[10px] font-black uppercase tracking-widest border-b border-white/5 bg-app-surface/50">
                <th class="py-6 px-8">Timestamp</th>
                <th class="py-6 px-6">Admin</th>
                <th class="py-6 px-6">Module</th>
                <th class="py-6 px-6">Action</th>
                <th class="py-6 px-8">IP Address</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
              <tr v-for="log in logs" :key="log.id" class="hover:bg-white/5 transition-colors">
                <td class="py-5 px-8 text-xs text-stone-400">{{ formatDate(log.created_at) }}</td>
                <td class="py-5 px-6 font-bold text-sm">#{{ log.admin_id }}</td>
                <td class="py-5 px-6 uppercase text-[10px] tracking-widest font-black text-primary">{{ log.module }}</td>
                <td class="py-5 px-6 text-sm">{{ log.action }}</td>
                <td class="py-5 px-8 text-xs font-mono text-stone-500">{{ log.ip_address || 'N/A' }}</td>
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

const fetchLogs = async () => {
  try {
    const res = await api.get('/admin/audit/logs')
    logs.value = res.data
  } catch (err) {
    console.error('Failed to fetch audit logs', err)
  }
}

onMounted(fetchLogs)
</script>
