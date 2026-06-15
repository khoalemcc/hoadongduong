<template>
  <div class="min-h-screen bg-[#1c1c19] text-surface font-body flex fade-in">
    <!-- Sidebar Navigation -->
    <aside class="h-screen w-64 fixed left-0 top-0 flex flex-col bg-[#1c1c19] border-r border-[#2d2d2a] z-50 overflow-y-auto">
      <div class="p-8">
        <h1 class="font-headline text-xl font-bold text-app-text">The Conservatory</h1>
        <p class="font-body text-xs text-[#c2c8c1] tracking-widest uppercase mt-1">Staff Management</p>
      </div>
      <nav class="flex-1 px-3 space-y-1">
        <RouterLink v-for="link in navLinks" :key="link.name" 
                    :to="link.to" 
                    :class="['flex items-center gap-3 pl-5 py-3 transition-all rounded-lg group', $route.path === link.to ? 'text-app-text border-l-4 border-[#fcf9f4] bg-[#2d2d2a]' : 'text-[#c2c8c1] hover:bg-[#2d2d2a] hover:text-app-text']">
          <span class="material-symbols-outlined text-lg">{{ link.icon }}</span>
          <span class="font-body text-sm" :class="[$route.path === link.to ? 'font-semibold' : 'font-medium']">{{ link.label }}</span>
        </RouterLink>
      </nav>
      <div class="px-6 py-6 mt-auto">
        <button class="w-full py-4 bg-gradient-to-br from-primary to-primary-container text-white rounded-xl font-body text-sm font-semibold flex items-center justify-center gap-2 transition-transform active:scale-95 shadow-lg">
          <span class="material-symbols-outlined">add_circle</span>
          Add New Staff
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="ml-64 flex-1 min-h-screen bg-[#1c1c19] flex flex-col">
      <!-- Top Header -->
      <header class="sticky top-0 z-40 glass-header flex justify-between items-center w-full px-12 py-6 border-b border-[#2d2d2a]/50">
        <div class="flex items-center gap-4 text-left">
          <h2 class="font-headline text-3xl font-bold text-app-text italic">Role Management</h2>
        </div>
        <div class="flex items-center gap-6">
          <div class="relative group">
            <span class="material-symbols-outlined text-[#c2c8c1] cursor-pointer hover:text-white transition-colors">notifications</span>
            <span class="absolute top-0 right-0 w-2 h-2 bg-error rounded-full"></span>
          </div>
          <span class="material-symbols-outlined text-[#c2c8c1] cursor-pointer hover:text-white transition-colors">settings</span>
          <div class="w-10 h-10 rounded-full overflow-hidden border-2 border-[#2d2d2a] bg-stone-800 flex items-center justify-center font-bold text-emerald-400">
            AU
          </div>
        </div>
      </header>

      <!-- Content Canvas -->
      <section class="flex-1 px-12 pb-12 w-full">
        <!-- Hero Stat Area -->
        <div class="flex justify-between items-end mb-12 mt-8 text-left w-full">
          <div>
            <p class="text-stone-500 font-body text-sm tracking-widest uppercase mb-2">Security & Permissions</p>
            <h3 class="font-headline text-xl text-app-text">Manage access control levels for your staff and garden curators.</h3>
          </div>
          <button class="px-8 py-4 bg-app-surface text-primary rounded-xl font-body text-sm font-bold flex items-center gap-2 hover:bg-stone-200 transition-all shadow-xl">
            <span class="material-symbols-outlined">shield_person</span>
            Create New Role
          </button>
        </div>

        <!-- Roles Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full">
          <div v-for="role in roles" :key="role.title" class="bg-[#2d2d2a] p-8 rounded-xl flex flex-col justify-between shadow-2xl group hover:translate-y-[-4px] transition-all duration-300 text-left border border-[#2d2d2a] hover:border-[#163423]">
            <div>
              <div class="flex justify-between items-start mb-6">
                <span :class="['p-3 rounded-lg', role.iconBg, role.iconColor]">
                  <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">{{ role.icon }}</span>
                </span>
                <span v-if="role.isDefault" class="text-xs font-body bg-[#1c1c19] px-3 py-1 rounded-full text-[#c2c8c1]">System Default</span>
              </div>
              <h4 class="font-headline text-2xl font-bold text-app-text mb-2">{{ role.title }}</h4>
              <p class="text-[#c2c8c1] text-sm leading-relaxed mb-6 font-body">{{ role.description }}</p>
              <div class="space-y-3 mb-8">
                <div v-for="perm in role.permissions" :key="perm.label" :class="['flex items-center gap-2', perm.allowed ? 'text-[#99baa2]' : 'text-[#c2c8c1]/50']">
                  <span class="material-symbols-outlined text-sm">{{ perm.allowed ? 'check_circle' : 'lock' }}</span>
                  <span :class="['text-xs font-body', !perm.allowed && 'line-through']">{{ perm.label }}</span>
                </div>
              </div>
            </div>
            <div class="pt-6 border-t border-[#1c1c19] flex justify-between items-center">
              <div class="flex -space-x-2">
                <div v-for="i in 3" :key="i" class="w-8 h-8 rounded-full border-2 border-[#2d2d2a] bg-stone-700 flex items-center justify-center text-[10px] font-bold">
                  {{ role.users[i-1] || '+' }}
                </div>
              </div>
              <span class="text-[#c2c8c1] text-sm font-body">{{ role.userCount }} Users</span>
            </div>
          </div>

          <!-- New Role Placeholder -->
          <div class="border-2 border-dashed border-[#2d2d2a] p-8 rounded-xl flex flex-col items-center justify-center text-center group cursor-pointer hover:bg-[#2d2d2a] transition-all min-h-[400px]">
            <span class="material-symbols-outlined text-4xl text-[#c2c8c1] group-hover:text-white mb-4">add_moderator</span>
            <h4 class="font-headline text-xl font-bold text-[#c2c8c1] group-hover:text-white mb-2">Define Custom Role</h4>
            <p class="text-stone-600 text-sm font-body">Create specific access levels for seasonal staff or specialized consultants.</p>
          </div>
        </div>

        <!-- Recent Access Logs -->
        <div class="mt-16 bg-[#2d2d2a]/50 p-10 rounded-xl overflow-hidden relative shadow-inner text-left">
          <h3 class="font-headline text-2xl text-app-text mb-6 italic">Recent Access Logs</h3>
          <div class="space-y-4">
            <div v-for="log in logs" :key="log.id" class="flex items-center justify-between py-4 border-b border-[#1c1c19]/50 font-body text-sm">
              <div class="flex items-center gap-4">
                <div :class="['w-8 h-8 rounded-full flex items-center justify-center', log.iconBg, log.iconColor]">
                  <span class="material-symbols-outlined text-xs">{{ log.icon }}</span>
                </div>
                <span class="text-app-text font-semibold">{{ log.user }}</span>
                <span class="text-[#c2c8c1]">{{ log.action }}</span>
              </div>
              <span :class="['font-semibold', log.timeColor || 'text-stone-600']">{{ log.time }}</span>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const navLinks = [
  { name: 'dashboard', label: 'Dashboard', icon: 'dashboard', to: '/admin' },
  { name: 'products', label: 'Products', icon: 'inventory_2', to: '/admin/products' },
  { name: 'orders', label: 'Orders', icon: 'shopping_cart', to: '/admin/orders' },
  { name: 'blog', label: 'Blog', icon: 'edit_note', to: '/admin/blog' },
  { name: 'staff', label: 'Staff', icon: 'badge', to: '/admin/staff' },
  { name: 'roles', label: 'Roles', icon: 'verified_user', to: '/admin/roles' }
]

const roles = [
  { 
    title: 'Super Admin', 
    description: 'Full access to all systems, billing, staff management, and security configurations.',
    icon: 'security', iconBg: 'bg-primary/20', iconColor: 'text-[#99baa2]', isDefault: true,
    userCount: 4, users: ['MT', 'EV', 'AL'],
    permissions: [
      { label: 'Unrestricted Platform Access', allowed: true },
      { label: 'Manage Security Protocols', allowed: true },
      { label: 'Financial & P&L Reporting', allowed: true }
    ]
  },
  { 
    title: 'Editorial Lead', 
    description: 'Responsible for blog content, product descriptions, and horticultural guides.',
    icon: 'auto_stories', iconBg: 'bg-secondary/20', iconColor: 'text-[#99baa2]',
    userCount: 1, users: ['JV'],
    permissions: [
      { label: 'Publish & Schedule Blogs', allowed: true },
      { label: 'Modify Product Copy', allowed: true },
      { label: 'System Settings', allowed: false }
    ]
  },
  { 
    title: 'Inventory Manager', 
    description: 'Full control over stock levels, nursery shipments, and supplier communications.',
    icon: 'potted_plant', iconBg: 'bg-[#3f4a35]', iconColor: 'text-[#dae7c9]',
    userCount: 2, users: ['FB', 'SM'],
    permissions: [
      { label: 'Manage Inventory Levels', allowed: true },
      { label: 'Process Supply Orders', allowed: true },
      { label: 'Nursery Shipping Logs', allowed: true }
    ]
  }
]

const logs = [
  { id: 1, user: 'Julianna Vane', action: 'updated permissions for "Inventory Manager"', time: '2 hours ago', icon: 'shield', iconBg: 'bg-primary-container', iconColor: 'text-primary' },
  { id: 2, user: 'Marcus Thorne', action: 'was assigned to "Super Admin"', time: '5 hours ago', icon: 'person', iconBg: 'bg-secondary-container', iconColor: 'text-secondary' },
  { id: 3, user: 'System Audit', action: 'Quarterly permission review required', time: 'Action Required', timeColor: 'text-error', icon: 'history', iconBg: 'bg-tertiary-container', iconColor: 'text-tertiary' }
]
</script>

<style scoped>
.glass-header {
  backdrop-filter: blur(12px);
  background-color: rgba(28, 28, 25, 0.8);
}
</style>
