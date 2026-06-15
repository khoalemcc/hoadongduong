<template>
  <div class="min-h-screen bg-[#1c1c19] text-surface font-body flex fade-in">
    <!-- Sidebar Navigation -->
    <aside class="h-screen w-64 fixed left-0 top-0 flex flex-col bg-[#1c1c19] border-r border-[#2d2d2a] z-50 overflow-y-auto">
      <div class="px-8 py-10">
        <h1 class="font-headline text-xl font-bold text-app-text">The Conservatory</h1>
        <p class="text-[#c2c8c1] text-xs mt-1 font-medium tracking-wider uppercase">Staff Management</p>
      </div>
      <nav class="flex-1 flex flex-col gap-1">
        <RouterLink v-for="link in navLinks" :key="link.name" 
                    :to="link.to" 
                    :class="['flex items-center gap-3 pl-5 py-3 transition-all', $route.path === link.to ? 'text-app-text border-l-4 border-[#fcf9f4] bg-[#2d2d2a]' : 'text-[#c2c8c1] hover:bg-[#2d2d2a] hover:text-app-text']">
          <span class="material-symbols-outlined text-[20px]">{{ link.icon }}</span>
          <span :class="['text-sm', $route.path === link.to ? 'font-semibold' : 'font-medium']">{{ link.label }}</span>
        </RouterLink>
      </nav>
      <div class="p-6 mt-auto border-t border-[#2d2d2a]">
        <div class="flex flex-col gap-1 mb-6">
          <RouterLink to="/" class="flex items-center gap-3 text-[#c2c8c1] pl-2 py-2 hover:text-app-text transition-colors">
            <span class="material-symbols-outlined text-[20px]">storefront</span>
            <span class="text-xs">View Store</span>
          </RouterLink>
          <button class="flex items-center gap-3 text-[#c2c8c1] pl-2 py-2 hover:text-error transition-colors">
            <span class="material-symbols-outlined text-[20px]">logout</span>
            <span class="text-xs">Logout</span>
          </button>
        </div>
        <button class="w-full bg-[#163423] hover:bg-[#2d4b38] text-white py-3 px-4 rounded-xl text-sm font-semibold transition-all flex items-center justify-center gap-2 shadow-lg">
          <span class="material-symbols-outlined text-[20px]">add</span>
          Add New Staff
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="ml-64 flex-1 min-h-screen bg-[#1c1c19] flex flex-col">
      <!-- Top Header -->
      <header class="sticky top-0 z-40 flex justify-between items-center w-full px-12 py-6 bg-[#1c1c19]/80 backdrop-blur-md border-b border-[#2d2d2a]/50">
        <div class="flex flex-col text-left">
          <h2 class="font-headline text-3xl font-bold text-app-text">Staff Directory</h2>
          <p class="text-[#c2c8c1] text-sm font-medium mt-1">Manage your conservatory specialists and administrators.</p>
        </div>
        <div class="flex items-center gap-6">
          <div class="relative group">
            <input class="bg-[#2d2d2a] border-none text-surface text-sm rounded-xl py-3 pl-12 pr-6 w-72 focus:ring-2 focus:ring-[#163423] transition-all outline-none" placeholder="Search staff members..." type="text"/>
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-[#c2c8c1] group-focus-within:text-app-text">search</span>
          </div>
          <button class="p-2.5 rounded-full hover:bg-[#2d2d2a] text-[#c2c8c1] hover:text-app-text transition-colors">
            <span class="material-symbols-outlined">notifications</span>
          </button>
          <div class="w-10 h-10 rounded-full overflow-hidden border border-[#2d2d2a] shadow-inner flex items-center justify-center bg-stone-800 font-bold text-emerald-400">
            AU
          </div>
        </div>
      </header>

      <!-- Content Canvas -->
      <section class="px-12 pb-12 w-full pt-10">
        <!-- Quick Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
          <div v-for="stat in stats" :key="stat.label" class="bg-[#2d2d2a] p-6 rounded-xl border border-transparent hover:border-[#466551]/30 transition-all text-left">
            <p class="text-[#c2c8c1] text-xs font-semibold uppercase tracking-widest mb-1">{{ stat.label }}</p>
            <div class="flex items-end justify-between">
              <h3 class="text-3xl font-bold text-app-text">{{ stat.value }}</h3>
              <span v-if="stat.badge" :class="['text-xs font-medium flex items-center px-2 py-1 rounded-full', stat.badgeColor]">
                {{ stat.badge }}
              </span>
            </div>
          </div>
        </div>

        <!-- Staff Table -->
        <div class="bg-[#1c1c19] rounded-xl overflow-hidden border border-[#2d2d2a] shadow-2xl">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-[#2d2d2a] border-b border-[#3a3a37]">
                <th class="px-8 py-5 text-xs font-bold text-app-text uppercase tracking-wider">Name</th>
                <th class="px-8 py-5 text-xs font-bold text-app-text uppercase tracking-wider">Email</th>
                <th class="px-8 py-5 text-xs font-bold text-app-text uppercase tracking-wider">Role</th>
                <th class="px-8 py-5 text-xs font-bold text-app-text uppercase tracking-wider">Status</th>
                <th class="px-8 py-5 text-xs font-bold text-app-text uppercase tracking-wider text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-[#2d2d2a]">
              <tr v-for="member in staff" :key="member.id" class="hover:bg-[#2d2d2a]/50 transition-colors group">
                <td class="px-8 py-5">
                  <div class="flex items-center gap-4">
                    <div class="w-10 h-10 rounded-full bg-[#2d2d2a] overflow-hidden flex items-center justify-center">
                      <span class="material-symbols-outlined text-stone-500">person</span>
                    </div>
                    <div>
                      <p class="text-sm font-semibold text-app-text">{{ member.fullName || 'Staff member' }}</p>
                      <p class="text-xs text-[#c2c8c1]">{{ member.role || 'Guest Specialist' }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-8 py-5 text-sm text-[#c2c8c1]">{{ member.email }}</td>
                <td class="px-8 py-5">
                  <span :class="['text-[11px] font-bold px-3 py-1 rounded-full uppercase tracking-tighter', getRoleBadge(member.role)]">
                    {{ member.role || 'Support' }}
                  </span>
                </td>
                <td class="px-8 py-5">
                  <div class="flex items-center gap-2">
                    <span :class="['w-2 h-2 rounded-full', member.isActive ? 'bg-[#99baa2] animate-pulse' : 'bg-stone-600']"></span>
                    <span class="text-sm text-app-text">{{ member.isActive ? 'Active' : 'Inactive' }}</span>
                  </div>
                </td>
                <td class="px-8 py-5 text-right">
                  <div class="flex items-center justify-end gap-3 md:opacity-0 group-hover:opacity-100 transition-opacity">
                    <button class="p-2 rounded-lg hover:bg-[#163423] text-[#c2c8c1] hover:text-white transition-all">
                      <span class="material-symbols-outlined text-[20px]">edit</span>
                    </button>
                    <button class="p-2 rounded-lg hover:bg-error/20 text-[#c2c8c1] hover:text-error transition-all">
                      <span class="material-symbols-outlined text-[20px]">delete</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <!-- Table Footer -->
          <div class="px-8 py-5 bg-[#2d2d2a] border-t border-[#3a3a37] flex items-center justify-between">
            <p class="text-xs text-[#c2c8c1]">Showing <span class="text-app-text font-bold">{{ staff.length }}</span> staff members</p>
            <div class="flex gap-2">
              <button class="p-2 rounded-lg bg-[#1c1c19] text-[#c2c8c1] hover:text-app-text disabled:opacity-30" disabled>
                <span class="material-symbols-outlined text-[18px]">chevron_left</span>
              </button>
              <button class="w-8 h-8 rounded-lg bg-[#163423] text-white text-xs font-bold">1</button>
              <button class="p-2 rounded-lg bg-[#1c1c19] text-[#c2c8c1] hover:text-app-text">
                <span class="material-symbols-outlined text-[18px]">chevron_right</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Editorial Feature -->
        <div class="mt-12 flex items-center gap-10 bg-[#163423] rounded-2xl p-10 relative overflow-hidden text-left shadow-2xl">
          <div class="relative z-10 w-full lg:w-2/3">
            <span class="inline-block text-[#99baa2] text-xs font-bold tracking-[0.2em] uppercase mb-4">Editorial Spotlight</span>
            <h2 class="font-headline text-4xl text-white font-bold leading-tight mb-6 italic">Empowering the <br/> Keepers of the Green</h2>
            <p class="text-[#adcfb6] text-lg max-w-lg font-light leading-relaxed mb-8">
              Our management system is designed to flow like nature. Streamlined permissions and elegant controls ensure your staff can focus on what matters.
            </p>
            <button class="flex items-center gap-2 text-white border-b border-white/30 pb-1 hover:border-white transition-all text-sm font-semibold">
              View Management Guidelines <span class="material-symbols-outlined">arrow_forward</span>
            </button>
          </div>
          <div class="absolute right-0 top-0 w-1/3 h-full opacity-40 mix-blend-overlay hidden lg:block">
            <img class="w-full h-full object-cover" src="https://images.unsplash.com/photo-1545239351-ef3c34650518?auto=format&fit=crop&q=80&w=800" alt="Botany"/>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const staff = ref([])

const stats = [
  { label: 'Total Staff', value: '24', badge: '+2 this month', badgeColor: 'bg-[#163423]/30 text-[#99baa2]' },
  { label: 'Active Now', value: '18', badge: '75% capacity', badgeColor: 'bg-[#163423]/30 text-[#99baa2]' },
  { label: 'Pending Roles', value: '3', badge: 'Onboarding', badgeColor: 'bg-[#382c1f]/30 text-[#c2af9c]' },
  { label: 'Support Tickets', value: '12', badge: 'Managed', badgeColor: 'bg-[#163423]/30 text-[#99baa2]' }
]

const navLinks = [
  { name: 'dashboard', label: 'Dashboard', icon: 'dashboard', to: '/admin' },
  { name: 'staff', label: 'Staff', icon: 'badge', to: '/admin/staff' },
  { name: 'orders', label: 'Orders', icon: 'shopping_cart', to: '/admin/orders' },
  { name: 'blog', label: 'Blog', icon: 'edit_note', to: '/admin/blog' },
  { name: 'analytics', label: 'Reports', icon: 'analytics', to: '/admin/analytics' },
  { name: 'products', label: 'Products', icon: 'inventory_2', to: '/admin/products' }
]

const getRoleBadge = (role) => {
  const r = (role || '').toLowerCase()
  if (r.includes('admin')) return 'bg-[#163423]/30 text-[#99baa2]'
  if (r.includes('editor')) return 'bg-[#2d4b38]/30 text-[#99baa2]'
  return 'bg-[#382c1f]/30 text-[#c2af9c]'
}

const fetchStaff = async () => {
  try {
    // Trong thực tế sẽ gọi API /users/ hoặc một endpoint quản lý nhân sự chuyên biệt
    const response = await api.get('/users/')
    // Giả lập thêm dữ liệu vai trò để hiển thị đẹp hơn
    staff.value = response.data.map((user, idx) => ({
      ...user,
      role: idx === 0 ? 'Lead Botanist' : idx === 1 ? 'System Architect' : 'Guest Specialist',
      isActive: true
    }))
  } catch (error) {
    console.error('Lỗi khi lấy danh sách nhân sự:', error)
  }
}

onMounted(() => {
  fetchStaff()
})
</script>
