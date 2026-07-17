<script setup lang="ts">
import { ref, watch } from 'vue'
import { Star } from '@lucide/vue'
import type { KnowledgeResponseDTO, KnowledgeCreateDTO, KnowledgeUpdateDTO } from '../types'

const props = defineProps<{
  isOpen: boolean
  knowledge?: KnowledgeResponseDTO | null
}>()

const emit = defineEmits(['close', 'save'])

const form = ref<KnowledgeCreateDTO | KnowledgeUpdateDTO>({
  category: '',
  question: '',
  answer: '',
  favorite: false
})

const isSubmitting = ref(false)

watch(
  () => props.knowledge,
  (newVal) => {
    if (newVal) {
      form.value = {
        category: newVal.category,
        question: newVal.question,
        answer: newVal.answer,
        favorite: newVal.favorite
      }
    } else {
      form.value = { category: '', question: '', answer: '', favorite: false }
    }
  },
  { immediate: true }
)

const handleClose = () => {
  form.value = { category: '', question: '', answer: '', favorite: false }
  emit('close')
}

const handleSubmit = async () => {
  if (!form.value.category.trim() || !form.value.question.trim() || !form.value.answer.trim()) {
    return
  }
  
  try {
    isSubmitting.value = true
    emit('save', { ...form.value })
    handleClose()
  } catch (error) {
    console.error(error)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div 
    v-if="isOpen" 
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs transition-opacity"
    @click.self="handleClose"
  >
    <div class="bg-white dark:bg-[#1e293b] w-full max-w-xl rounded-2xl shadow-xl border border-slate-200 dark:border-[#475569] overflow-hidden flex flex-col max-h-[90vh]">
      
      <div class="p-6 overflow-y-auto flex flex-col gap-5">
        
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-semibold text-slate-700 dark:text-slate-300">Categoria</label>
          <input 
            v-model="form.category"
            type="text" 
            placeholder="Ex: JavaScript, CSS, TypeScript..." 
            class="w-full h-11 px-4 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-[#475569] rounded-xl text-sm text-slate-800 dark:text-white outline-none focus:border-primary/50 transition-colors"
          />
        </div>

        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-semibold text-slate-700 dark:text-slate-300">Pergunta</label>
          <textarea 
            v-model="form.question"
            rows="3"
            placeholder="O que você quer lembrar? Ex: O que é um closure em JavaScript?" 
            class="w-full p-4 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-[#475569] rounded-xl text-sm text-slate-800 dark:text-white outline-none focus:border-primary/50 transition-colors resize-none leading-relaxed"
          ></textarea>
        </div>

        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-semibold text-slate-700 dark:text-slate-300">Resposta</label>
          <textarea 
            v-model="form.answer"
            rows="5"
            placeholder="Escreva a resposta completa aqui..." 
            class="w-full p-4 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-[#475569] rounded-xl text-sm text-slate-800 dark:text-white outline-none focus:border-primary/50 transition-colors resize-none leading-relaxed"
          ></textarea>
        </div>

        <div 
          @click="form.favorite = !form.favorite"
          class="flex items-center gap-4 p-4 border rounded-xl cursor-pointer select-none transition-all"
          :class="form.favorite 
            ? 'bg-amber-500/10 border-amber-500/40 dark:border-amber-500/50 shadow-xs' 
            : 'bg-slate-50 dark:bg-slate-800/40 border-slate-200 dark:border-[#475569] hover:bg-slate-100/70 dark:hover:bg-slate-800/80'"
        >
          <div 
            class="w-10 h-10 rounded-xl border flex items-center justify-center transition-colors shrink-0"
            :class="form.favorite 
              ? 'bg-amber-500 text-white border-amber-600' 
              : 'text-slate-400 dark:text-slate-400 bg-white dark:bg-[#1e293b] border-slate-200 dark:border-[#475569]'"
          >
            <Star class="w-4 h-4" :class="{ 'fill-current': form.favorite }" />
          </div>
          <div class="flex flex-col min-w-0">
            <span class="text-sm font-semibold text-slate-800 dark:text-slate-200">Marcar como favorito</span>
            <span class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Destaca este conhecimento na lista de favoritos</span>
          </div>
        </div>

      </div>

      <div class="p-4 bg-slate-50 dark:bg-slate-800/40 border-t border-slate-100 dark:border-slate-800 flex items-center justify-end gap-3">
        <button 
          @click="handleClose"
          class="h-10 px-4 text-sm font-semibold text-slate-600 dark:text-slate-300 bg-transparent border border-slate-300 dark:border-[#475569] hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl cursor-pointer transition-colors shadow-2xs"
        >
          Cancelar
        </button>
        <button 
          @click="handleSubmit"
          :disabled="isSubmitting || !form.category.trim() || !form.question.trim() || !form.answer.trim()"
          class="h-10 px-4 text-sm font-semibold bg-primary hover:bg-primary-dark text-white rounded-xl cursor-pointer disabled:opacity-50 disabled:pointer-events-none transition-colors shadow-xs flex items-center justify-center"
        >
          <span v-if="isSubmitting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span v-else>{{ props.knowledge ? "Salvar alterações" : "Adicionar conhecimento" }}</span>
        </button>
      </div>

    </div>
  </div>
</template>
