<script setup lang="ts">
import { Sparkles } from '@lucide/vue'
</script>

<template>
  <section class="max-w-4xl mx-auto text-center pt-24 pb-16 px-6 flex flex-col items-center">
    <div class="inline-flex items-center gap-1.5 bg-blue-500/10 border border-blue-500/30 px-4 py-1.5 rounded-full text-xs font-medium text-blue-400 shadow-sm mb-8">
      <Sparkles class="w-3.5 h-3.5" />
      <span>Sua base pessoal de conhecimento</span>
    </div>

    <h1 class="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight max-w-3xl">
      Organize o que você 
      <span class="block mt-2 bg-linear-to-r from-blue-400 via-blue-500 to-indigo-500 bg-clip-text text-transparent">
        aprende
      </span>
    </h1>

    <p class="mt-8 text-base sm:text-lg text-[#cbd5e1] font-normal max-w-xl leading-relaxed">
      Registre conhecimentos no formato <span class="text-white font-medium">Pergunta → Resposta</span>.
      <span class="block">Pesquise, filtre e encontre qualquer coisa na hora certa.</span>
    </p>
  </section>
</template>
