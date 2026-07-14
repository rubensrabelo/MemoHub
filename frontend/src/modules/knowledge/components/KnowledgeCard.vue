<script setup lang="ts">
import { ref, computed } from 'vue'
import { Star, ChevronDown, ChevronUp } from '@lucide/vue'
import type { KnowledgeResponseDTO } from '../types'

const props = defineProps<{
  knowledge: KnowledgeResponseDTO
}>()

const emit = defineEmits(['toggle-favorite'])

const isExpanded = ref(false)

const formattedDate = computed(() => {
  if (!props.knowledge.created_at) return ''
  const date = new Date(props.knowledge.created_at)
  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  }).replace(' de ', ' ').replace('.', '')
})
</script>

<template>
  <div class="bg-white dark:bg-[#1e293b] border border-slate-200 dark:border-[#475569] rounded-2xl p-5 shadow-xs transition-all duration-200 hover:shadow-md hover:border-slate-300 dark:hover:border-slate-500 flex flex-col h-full justify-between">
    <div>
      <div class="flex items-center justify-between gap-4 mb-3">
        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-primary text-white">
          {{ knowledge.category }}
        </span>
        
        <button 
          @click.stop="emit('toggle-favorite', knowledge.id)"
          class="p-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 hover:scale-105 transition-transform cursor-pointer"
          :class="knowledge.favorite ? 'text-favorite' : 'text-slate-400'"
        >
          <Star class="w-4 h-4" :class="{ 'fill-current': knowledge.favorite }" />
        </button>
      </div>

      <h3 class="text-base font-bold text-slate-900 dark:text-white leading-snug">
        {{ knowledge.question }}
      </h3>

      <div 
        class="transition-all duration-300 ease-in-out overflow-hidden mt-3"
        :class="isExpanded ? 'max-h-125 opacity-100' : 'max-h-0 opacity-0'"
      >
        <div class="pt-3 border-t border-slate-100 dark:border-slate-800 text-sm text-slate-600 dark:text-slate-300 whitespace-pre-wrap leading-relaxed">
          {{ knowledge.answer }}
        </div>
      </div>
    </div>

    <div class="flex items-center justify-between mt-5 pt-3 border-t border-slate-50 dark:border-slate-800/50">
      <span class="text-xs text-slate-400">
        {{ formattedDate }}
      </span>

      <button 
        @click="isExpanded = !isExpanded"
        class="text-xs font-semibold text-primary hover:text-primary-dark dark:text-primary-light flex items-center gap-1 cursor-pointer select-none"
      >
        <span>{{ isExpanded ? 'Ocultar resposta' : 'Ver resposta' }}</span>
        <ChevronUp v-if="isExpanded" class="w-3.5 h-3.5" />
        <ChevronDown v-else class="w-3.5 h-3.5" />
      </button>
    </div>
  </div>
</template>
