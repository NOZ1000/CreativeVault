import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import SignIn from './pages/SignIn.vue'
import SignUp from './pages/SignUp.vue'
import ErrorPage from './pages/ErrorPage.vue'
import MyCreatures from './pages/MyCreatures.vue'
import MyCreature from './pages/MyCreature.vue'

const routerHistory = createWebHistory()

const router = createRouter({
  scrollBehavior(to) {
    if (to.hash) {
      window.scroll({ top: 0 })
    } else {
      document.querySelector('html').style.scrollBehavior = 'auto'
      window.scroll({ top: 0 })
      document.querySelector('html').style.scrollBehavior = ''
    }
  },  
  history: routerHistory,
  routes: [
    {
      path: '/',
      component: Home
    },
    {
      path: '/signin',
      component: SignIn
    },
    {
      path: '/signup',
      component: SignUp
    },
    {
      path: '/file',
      component: MyCreature
    },
    {
      path: '/my_creatures',
      component: MyCreatures
    },
    {
      path: '/:pathMatch(.*)*',
      component: ErrorPage
    }    
  ]
})

export default router
