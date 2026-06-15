import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: JSON.parse(localStorage.getItem('cart') || '[]'),
  }),
  
  getters: {
    totalItems: (state) => state.items.reduce((acc, item) => acc + item.quantity, 0),
    totalPrice: (state) => state.items.reduce((acc, item) => acc + (item.price * item.quantity), 0),
  },
  
  actions: {
    addToCart(product, quantity = 1) {
      const existing = this.items.find(item => item.id === product.id)
      if (existing) {
        existing.quantity += quantity
      } else {
        this.items.push({
          id: product.id,
          name: product.name,
          price: product.price,
          image: product.images?.[0]?.image_url || '/assets/images/shampoo.png',
          quantity
        })
      }
      this.saveToLocal()
    },
    
    removeFromCart(productId) {
      this.items = this.items.filter(item => item.id !== productId)
      this.saveToLocal()
    },
    
    clearCart() {
      this.items = []
      this.saveToLocal()
    },
    
    saveToLocal() {
      localStorage.setItem('cart', JSON.stringify(this.items))
    }
  }
})
