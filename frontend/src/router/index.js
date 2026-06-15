import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import HomeView from '../views/HomeView.vue'
import ProductDetailView from '../views/ProductDetailView.vue'
import ProductListingView from '../views/ProductListingView.vue'
import CheckoutView from '../views/CheckoutView.vue'
import AccountView from '../views/AccountView.vue'
import BlogView from '../views/BlogView.vue'
import BlogPostDetailView from '../views/BlogPostDetailView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ContactView from '../views/ContactView.vue'
import AdminDashboardView from '../views/AdminDashboardView.vue'
import AdminOrdersView from '../views/AdminOrdersView.vue'
import AdminBlogView from '../views/AdminBlogView.vue'
import AdminAnalyticsView from '../views/AdminAnalyticsView.vue'
import AdminProductsView from '../views/AdminProductsView.vue'
import AdminStaffView from '../views/AdminStaffView.vue'
import AdminRolesView from '../views/AdminRolesView.vue'
import CategoryView from '../views/CategoryView.vue'
import AdminInventoryView from '../views/AdminInventoryView.vue'
import AdminCustomersView from '../views/AdminCustomersView.vue'
import AdminSettingsView from '../views/AdminSettingsView.vue'
import AdminBrandsView from '../views/AdminBrandsView.vue'
import AdminMarketingView from '../views/AdminMarketingView.vue'
import AdminInventoryLogsView from '../views/AdminInventoryLogsView.vue'
import AdminAuditLogsView from '../views/AdminAuditLogsView.vue'
import OrderSuccessView from '../views/OrderSuccessView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/shop',
      name: 'shop',
      component: ProductListingView
    },
    {
      path: '/category',
      name: 'category',
      component: CategoryView
    },
    {
      path: '/product/:id',
      name: 'product-detail',
      component: ProductDetailView
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: CheckoutView
    },
    {
      path: '/account',
      name: 'account',
      component: AccountView
    },
    {
      path: '/profile',
      redirect: '/account'
    },
    {
      path: '/orders',
      redirect: '/account'
    },
    {
      path: '/blog',

      name: 'blog',
      component: BlogView
    },
    {
      path: '/blog/:id',
      name: 'blog-detail',
      component: BlogPostDetailView
    },
    {
      path: '/contact',
      name: 'contact',
      component: ContactView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/admin',
      name: 'admin-dashboard',
      component: AdminDashboardView
    },
    {
      path: '/admin/orders',
      name: 'admin-orders',
      component: AdminOrdersView
    },
    {
      path: '/admin/blog',
      name: 'admin-blog',
      component: AdminBlogView
    },
    {
      path: '/admin/analytics',
      name: 'admin-analytics',
      component: AdminAnalyticsView
    },
    {
      path: '/admin/products',
      name: 'admin-products',
      component: AdminProductsView
    },
    {
      path: '/admin/inventory',
      name: 'admin-inventory',
      component: AdminInventoryView
    },
    {
      path: '/admin/customers',
      name: 'admin-customers',
      component: AdminCustomersView
    },
    {
      path: '/admin/settings',
      name: 'admin-settings',
      component: AdminSettingsView
    },
    {
      path: '/admin/staff',
      name: 'admin-staff',
      component: AdminStaffView
    },
    {
      path: '/admin/roles',
      name: 'admin-roles',
      component: AdminRolesView
    },
    {
      path: '/admin/brands',
      name: 'admin-brands',
      component: AdminBrandsView
    },
    {
      path: '/admin/marketing',
      name: 'admin-marketing',
      component: AdminMarketingView
    },
    {
      path: '/admin/inventory-logs',
      name: 'admin-inventory-logs',
      component: AdminInventoryLogsView
    },
    {
      path: '/admin/audit',
      name: 'admin-audit',
      component: AdminAuditLogsView
    },
    {
      path: '/order-success',
      name: 'order-success',
      component: OrderSuccessView
    }
  ],
  scrollBehavior() {
    return { top: 0 }
  }
})

router.beforeEach((to) => {
  const authStore = useAuthStore()
  
  // Protect routes requiring authentication
  const protectedRoutes = ['/account', '/checkout']
  const isProtected = protectedRoutes.some(p => to.path.startsWith(p))
  
  if (isProtected && !authStore.isLoggedIn) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }

  // Protect admin operations
  if (to.path.startsWith('/admin')) {
    if (!authStore.isLoggedIn) {
      return { path: '/login', query: { redirect: to.fullPath } }
    }
    if (!authStore.isAdmin) {
      return { path: '/' }
    }
  }
  return true
})

export default router
