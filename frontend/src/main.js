import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)
const pinia = createPinia()

app.directive('reveal', {
  mounted(el, binding) {
    const direction = binding.value || 'up' // up, left, right, scale
    if (direction === 'left') {
      el.classList.add('reveal-left')
    } else if (direction === 'right') {
      el.classList.add('reveal-right')
    } else if (direction === 'scale') {
      el.classList.add('reveal-scale')
    } else {
      el.classList.add('reveal')
    }
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          el.classList.add('active')
          observer.unobserve(el)
        }
      })
    }, {
      threshold: 0.05,
      rootMargin: '0px 0px -40px 0px'
    })
    observer.observe(el)
  }
})

app.use(pinia)
app.use(router)

app.mount('#app')
