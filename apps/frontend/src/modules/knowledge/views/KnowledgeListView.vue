<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { Search } from "@lucide/vue";
import { knowledgeService } from "../services/knowledgeService";
import Sidebar from "../../../core/components/Sidebar.vue";
import KnowledgeCard from "../components/KnowledgeCard.vue";
import KnowledgeFormModal from "../components/KnowledgeFormModal.vue";
import type {
  KnowledgeResponseDTO,
  KnowledgeCreateDTO,
  KnowledgeUpdateDTO,
} from "../types";

const knowledges = ref<KnowledgeResponseDTO[]>([]);
const isLoading = ref(true);
const searchQuery = ref("");
const isModalOpen = ref(false);
const selectedKnowledge = ref<KnowledgeResponseDTO | null>(null);

const processedKnowledges = computed(() => {
  return [...knowledges.value].sort(
    (a, b) =>
      new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
  );
});

const fetchKnowledges = async () => {
  try {
    isLoading.value = true;
    const filters: any = {};

    if (searchQuery.value.trim() !== "") {
      filters.search = searchQuery.value;
    }

    knowledges.value = await knowledgeService.getAll(filters);
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};

const handleToggleFavorite = async (id: number) => {
  try {
    const updated = await knowledgeService.toggleFavorite(id);
    knowledges.value = knowledges.value.map((item) =>
      item.id === id ? { ...item, favorite: updated.favorite } : item,
    );
  } catch (error) {
    console.error(error);
  }
};

const handleOpenCreateModal = () => {
  selectedKnowledge.value = null;
  isModalOpen.value = true;
};

const handleOpenEditModal = (id: number) => {
  const item = knowledges.value.find((k) => k.id === id);
  if (item) {
    selectedKnowledge.value = item;
    isModalOpen.value = true;
  }
};

const handleSaveKnowledge = async (
  payload: KnowledgeCreateDTO | KnowledgeUpdateDTO,
) => {
  try {
    if (selectedKnowledge.value?.id) {
      await knowledgeService.update(
        selectedKnowledge.value.id,
        payload as KnowledgeUpdateDTO,
      );
    } else {
      await knowledgeService.create(
        payload as KnowledgeCreateDTO,
      );
    }
    isModalOpen.value = false;
    selectedKnowledge.value = null;
    await fetchKnowledges();
  } catch (error) {
    console.error(error);
  }
};

const handleDeleteKnowledge = async (id: number) => {
  if (!confirm("Tem certeza que deseja excluir este item?")) return;
  try {
    await knowledgeService.delete(id);
    await fetchKnowledges();
  } catch (error) {
    console.error(error);
  }
};

const handleCloseModal = () => {
  isModalOpen.value = false;
  selectedKnowledge.value = null;
};

watch(searchQuery, () => {
  fetchKnowledges();
});

onMounted(() => {
  fetchKnowledges();
});
</script>

<template>
  <div
    class="flex min-h-screen bg-[#f8fafc] text-slate-900 font-sans antialiased"
  >
    <Sidebar currentRoute="knowledge" @new-knowledge="handleOpenCreateModal" />

    <div class="flex-1 flex flex-col min-w-0">
      <main class="flex-1 p-8 overflow-y-auto">
        <div class="max-w-6xl mx-auto">
          <div class="mb-8">
            <h1 class="text-2xl font-bold text-slate-900">Conhecimentos</h1>
          </div>

          <div class="w-full relative mb-8">
            <Search
              class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2"
            />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Pesquisar por título, pergunta ou resposta..."
              class="w-full h-10 bg-white border border-slate-200 rounded-xl pl-10 pr-4 text-sm text-slate-800 outline-none focus:border-primary/50 transition-colors shadow-2xs"
            />
          </div>

          <div
            v-if="isLoading"
            class="grid grid-cols-1 md:grid-cols-2 gap-6 animate-pulse"
          >
            <div
              v-for="i in 4"
              :key="i"
              class="h-44 bg-slate-200 rounded-2xl"
            ></div>
          </div>

          <div
            v-else-if="processedKnowledges.length === 0"
            class="text-center py-16 bg-white rounded-2xl border border-slate-200 shadow-2xs"
          >
            <p class="text-slate-400 font-medium text-sm">
              Nenhum conhecimento cadastrado no backend.
            </p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
            <KnowledgeCard
              v-for="item in processedKnowledges"
              :key="item.id"
              :knowledge="item"
              @toggle-favorite="handleToggleFavorite"
              @edit="handleOpenEditModal"
              @delete="handleDeleteKnowledge"
            />
          </div>
        </div>
      </main>
    </div>

    <KnowledgeFormModal
      :isOpen="isModalOpen"
      :knowledge="selectedKnowledge"
      @close="handleCloseModal"
      @save="handleSaveKnowledge"
    />
  </div>
</template>
