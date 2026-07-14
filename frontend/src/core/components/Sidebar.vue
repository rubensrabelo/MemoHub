<script setup lang="ts">
import { useRouter } from 'vue-router'
import { BookOpen, Star, Plus } from '@lucide/vue'

defineProps({
  currentRoute: {
    type: String,
    default: 'knowledge'
  }
})

defineEmits(['new-knowledge'])

const router = useRouter()

const navigateTo = (routeName: string) => {
  router.push({ name: routeName })
}
</script>

<template>
  <aside class="w-64 h-screen bg-white dark:bg-[#1e293b] border-r border-slate-200 dark:border-[#475569] flex flex-col justify-between p-4 select-none">
    <div class="flex flex-col gap-6">
      <div class="flex items-center gap-2 px-2 py-1">
        <div class="w-8 h-8 bg-primary rounded-xl flex items-center justify-center shadow-md shadow-blue-500/20">
          <BookOpen class="w-4 h-4 text-white" />
        </div>
        <span class="font-bold text-lg tracking-tight text-slate-900 dark:text-white">MemoHub</span>
      </div>

      <button 
        @click="$emit('new-knowledge')"
        class="w-full h-12 bg-primary hover:bg-primary-dark text-white font-medium rounded-xl flex items-center justify-center gap-2 transition-all active:scale-[0.98] cursor-pointer shadow-xs"
      >
        <Plus class="w-4 h-4" />
        <span>Novo Conhecimento</span>
      </button>

      <nav class="flex flex-col gap-1">
        <button
          @click="navigateTo('knowledge')"
          class="w-full h-11 px-3 rounded-xl flex items-center gap-3 font-medium text-sm transition-colors cursor-pointer"
          :class="currentRoute === 'knowledge' 
            ? 'bg-blue-500/10 text-primary dark:bg-blue-500/20 dark:text-blue-400' 
            : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800'"
        >
          <BookOpen class="w-4 h-4" />
          <span>Conhecimentos</span>
        </button>

        <button
          @click="navigateTo('favorites')"
          class="w-full h-11 px-3 rounded-xl flex items-center gap-3 font-medium text-sm transition-colors cursor-pointer"
          :class="currentRoute === 'favorites' 
            ? 'bg-blue-500/10 text-primary dark:bg-blue-500/20 dark:text-blue-400' 
            : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800'"
        >
          <Star class="w-4 h-4" />
          <span>Favoritos</span>
        </button>
      </nav>
    </div>
  </aside>
</template>
