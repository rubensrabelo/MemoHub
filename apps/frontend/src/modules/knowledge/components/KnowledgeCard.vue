<script setup lang="ts">
import { ref, computed } from "vue";
import { Star, ChevronDown, ChevronUp, Pencil, Trash2 } from "@lucide/vue";
import type { KnowledgeResponseDTO } from "../types";

const props = defineProps<{
  knowledge: KnowledgeResponseDTO;
}>();

const emit = defineEmits(["toggle-favorite", "edit", "delete"]);

const isExpanded = ref(false);

const formattedDate = computed(() => {
  if (!props.knowledge.created_at) return "";
  const date = new Date(props.knowledge.created_at);
  return date
    .toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    })
    .replace(" de ", " ")
    .replace(".", "");
});
</script>

<template>
  <div
    class="group bg-white border border-slate-200 rounded-2xl p-5 shadow-xs transition-all duration-200 hover:shadow-md hover:border-slate-300 flex flex-col h-full justify-between"
  >
    <div>
      <div class="flex items-start justify-between gap-4 mb-3">
        <span
          class="inline-flex items-center px-3 py-1 bg-blue-500/10 text-primary border border-blue-500/20 rounded-full text-xs font-semibold"
        >
          {{ knowledge.category }}
        </span>

        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <button
            @click.stop="emit('toggle-favorite', knowledge.id)"
            class="p-1.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 transition-colors cursor-pointer"
            :class="knowledge.favorite ? 'text-favorite border-favorite/30 bg-favorite/5' : 'text-slate-400'"
            title="Favoritar"
          >
            <Star
              class="w-4 h-4"
              :class="{ 'fill-current': knowledge.favorite }"
            />
          </button>

          <button
            @click.stop="emit('edit', knowledge.id)"
            class="p-1.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-500 hover:text-slate-700 transition-colors cursor-pointer"
            title="Editar"
          >
            <Pencil class="w-4 h-4" />
          </button>

          <button
            @click.stop="emit('delete', knowledge.id)"
            class="p-1.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-red-50 text-slate-500 hover:text-red-600 hover:border-red-200 transition-colors cursor-pointer"
            title="Excluir"
          >
            <Trash2 class="w-4 h-4" />
          </button>
        </div>
      </div>

      <h3 class="text-base font-bold text-slate-900 leading-snug">
        {{ knowledge.question }}
      </h3>

      <div
        class="transition-all duration-300 ease-in-out overflow-hidden mt-3"
        :class="isExpanded ? 'max-h-125 opacity-100' : 'max-h-0 opacity-0'"
      >
        <div
          class="pt-3 border-t border-slate-100 text-sm text-slate-600 whitespace-pre-wrap leading-relaxed"
        >
          {{ knowledge.answer }}
        </div>
      </div>
    </div>

    <div
      class="flex items-center justify-between mt-5 pt-3 border-t border-slate-100"
    >
      <span class="text-xs text-slate-400">
        {{ formattedDate }}
      </span>

      <button
        @click="isExpanded = !isExpanded"
        class="text-xs font-semibold text-primary hover:text-primary-dark flex items-center gap-1 cursor-pointer select-none"
      >
        <span>{{ isExpanded ? "Ocultar resposta" : "Ver resposta" }}</span>
        <ChevronUp v-if="isExpanded" class="w-3.5 h-3.5" />
        <ChevronDown v-else class="w-3.5 h-3.5" />
      </button>
    </div>
  </div>
</template>
