<script setup lang="ts">
import { Search, Star, FolderKanban } from '@lucide/vue'
</script>

<template>
  <section class="max-w-5xl mx-auto px-6 pb-24">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      
      <div class="bg-[#1e293b] border border-[#475569] rounded-2xl p-6 shadow-sm transition-all duration-300 hover:border-blue-500/50 hover:scale-[1.01] group">
        <div class="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 group-hover:bg-blue-600 group-hover:text-white transition-all duration-200">
          <Search class="w-5 h-5" stroke-width="2.5" />
        </div>
        <h3 class="mt-4 text-base font-semibold text-white tracking-wide">Busca instantânea</h3>
        <p class="mt-2 text-sm text-[#cbd5e1] leading-relaxed">Encontre qualquer conhecimento em segundos</p>
      </div>

      <div class="bg-[#1e293b] border border-[#475569] rounded-2xl p-6 shadow-sm transition-all duration-300 hover:border-amber-500/50 hover:scale-[1.01] group">
        <div class="w-10 h-10 rounded-xl bg-yellow-500/10 border border-yellow-500/20 flex items-center justify-center text-yellow-400 group-hover:bg-yellow-500 group-hover:text-slate-900 transition-all duration-200">
          <Star class="w-5 h-5 fill-current" stroke-width="2.5" />
        </div>
        <h3 class="mt-4 text-base font-semibold text-white tracking-wide">Favoritos</h3>
        <p class="mt-2 text-sm text-[#cbd5e1] leading-relaxed">Destaque os mais importantes</p>
      </div>

      <div class="bg-[#1e293b] border border-[#475569] rounded-2xl p-6 shadow-sm transition-all duration-300 hover:border-emerald-500/50 hover:scale-[1.01] group">
        <div class="w-10 h-10 rounded-xl bg-green-500/10 border border-green-500/20 flex items-center justify-center text-green-400 group-hover:bg-green-500 group-hover:text-white transition-all duration-200">
          <FolderKanban class="w-5 h-5 fill-current" stroke-width="2.5" />
        </div>
        <h3 class="mt-4 text-base font-semibold text-white tracking-wide">Categorias</h3>
        <p class="mt-2 text-sm text-[#cbd5e1] leading-relaxed">Organize por temas e áreas</p>
      </div>

    </div>
  </section>
</template>
