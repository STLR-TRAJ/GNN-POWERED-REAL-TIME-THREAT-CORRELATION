<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-red-600 rounded-lg flex items-center justify-center">
                <ShieldAlert class="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 class="text-xl font-bold text-gray-900">RTIP Platform</h1>
                <p class="text-xs text-gray-500">Real-time Threat Intelligence</p>
              </div>
            </router-link>
          </div>
          
          <div class="flex items-center space-x-4">
            <!-- Navigation Links -->
            <router-link
              to="/"
              class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
              :class="$route.path === '/' ? 'bg-red-100 text-red-700' : 'text-gray-600 hover:text-gray-900'"
            >
              Dashboard
            </router-link>
            <router-link
              to="/threats"
              class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
              :class="$route.path === '/threats' ? 'bg-red-100 text-red-700' : 'text-gray-600 hover:text-gray-900'"
            >
              Threats
            </router-link>
            <router-link
              to="/search"
              class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
              :class="$route.path === '/search' ? 'bg-red-100 text-red-700' : 'text-gray-600 hover:text-gray-900'"
            >
              Search
            </router-link>
            <router-link
              to="/alerts"
              class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
              :class="$route.path === '/alerts' ? 'bg-red-100 text-red-700' : 'text-gray-600 hover:text-gray-900'"
            >
              Alerts
            </router-link>
            
            <!-- Status Indicator -->
            <div class="flex items-center space-x-2">
              <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span class="text-xs text-gray-500">Live</span>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 mt-12">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center">
          <div class="text-sm text-gray-500">
            © 2025 RTIP Platform. Democratizing cybersecurity intelligence for SMEs.
          </div>
          <div class="flex space-x-4 text-sm text-gray-500">
            <a href="#" class="hover:text-gray-700">Documentation</a>
            <a href="#" class="hover:text-gray-700">Support</a>
            <a href="#" class="hover:text-gray-700">GitHub</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { ShieldAlert } from 'lucide-vue-next'

export default {
  name: 'App',
  components: {
    ShieldAlert
  }
}
</script>
