import { createRouter, createWebHistory } from "vue-router"
import DashboardView from "./views/DashboardView.vue"
import ThreatsView from "./views/ThreatsView.vue"
import SearchView from "./views/SearchView.vue"
import AlertsView from "./views/AlertsView.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "dashboard",
      component: DashboardView,
      meta: {
        title: "Dashboard - RTIP Platform",
      },
    },
    {
      path: "/threats",
      name: "threats",
      component: ThreatsView,
      meta: {
        title: "Threats - RTIP Platform",
      },
    },
    {
      path: "/search",
      name: "search",
      component: SearchView,
      meta: {
        title: "Search - RTIP Platform",
      },
    },
    {
      path: "/alerts",
      name: "alerts",
      component: AlertsView,
      meta: {
        title: "Alert Management - RTIP Platform",
      },
    },
  ],
})

// Update page title
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || "RTIP Platform"
  next()
})

export default router
