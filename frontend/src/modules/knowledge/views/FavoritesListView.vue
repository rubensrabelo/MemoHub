<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { Search } from '@lucide/vue'
import { knowledgeService } from '../services/knowledgeService'
import Sidebar from '../../../core/components/Sidebar.vue'
import KnowledgeCard from '../components/KnowledgeCard.vue'
import type { KnowledgeResponseDTO } from '../types'

const favorites = ref<KnowledgeResponseDTO[]>([])
const isLoading = ref(true)
const searchQuery = ref('')

const processedFavorites = computed(() => {
  return [...favorites.value].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
})

const fetchFavorites = async () => {
  try {
    isLoading.value = true
    const filters: any = { favorite: true }
    
    if (searchQuery.value.trim() !== '') {
      filters.search = searchQuery.value
    }

    favorites.value = await knowledgeService.getAll(filters)
  } catch (error) {
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

const handleToggleFavorite = async (id: number) => {
  try {
    await knowledgeService.toggleFavorite(id)
    favorites.value = favorites.value.filter(item => item.id !== id)
  } catch (error) {
    console.error(error)
  }
}

watch(searchQuery, () => {
  fetchFavorites()
})

onMounted(() => {
  fetchFavorites()
})
</script>

<template>
  <div class="flex min-h-screen bg-[#f8fafc] text-slate-900 font-sans antialiased">
    <Sidebar currentRoute="favorites" />

    <div class="flex-1 flex flex-col min-w-0">
      <main class="flex-1 p-8 overflow-y-auto">
        <div class="max-w-6xl mx-auto">
          
          <div class="mb-8">
            <h1 class="text-2xl font-bold text-slate-900 flex items-center gap-2">
              <span>Favoritos</span>
            </h1>
          </div>

          <div class="w-full relative mb-8">
            <Search class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Buscar nos favoritos..." 
              class="w-full h-10 bg-white border border-slate-200 rounded-xl pl-10 pr-4 text-sm text-slate-800 outline-none focus:border-primary/50 transition-colors shadow-2xs"
            />
          </div>

          <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 gap-6 animate-pulse">
            <div v-for="i in 3" :key="i" class="h-44 bg-slate-200 rounded-2xl"></div>
          </div>

          <div v-else-if="processedFavorites.length === 0" class="text-center py-16 bg-white rounded-2xl border border-slate-200 shadow-2xs">
            <p class="text-slate-400 font-medium text-sm">Nenhum conhecimento favoritado no momento.</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
            <KnowledgeCard 
              v-for="item in processedFavorites" 
              :key="item.id" 
              :knowledge="item"
              @toggle-favorite="handleToggleFavorite"
            />
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
