import { reactive, watch } from 'vue'

const savedCart = JSON.parse(localStorage.getItem('cart') || '[]')
const savedUser = JSON.parse(localStorage.getItem('user') || 'null')

export const store = reactive({
  user: savedUser,
  cart: savedCart,
  
  // Auth actions
  setUser(userData) {
    this.user = userData
    localStorage.setItem('user', JSON.stringify(userData))
  },
  logout() {
    this.user = null
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  },
  
  // Cart actions
  addToCart(product, quantity = 1) {
    const existing = this.cart.find(item => item.id === product.id)
    if (existing) {
      existing.quantity += quantity
    } else {
      this.cart.push({
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.images?.[0]?.image_url || '/assets/images/shampoo.png',
        quantity
      })
    }
  },
  removeFromCart(productId) {
    this.cart = this.cart.filter(item => item.id !== productId)
  },
  clearCart() {
    this.cart = []
  }
})

// Persistence
watch(() => store.cart, (newCart) => {
  localStorage.setItem('cart', JSON.stringify(newCart))
}, { deep: true })
