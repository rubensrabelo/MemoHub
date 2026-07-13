<script setup lang="ts">
import { BookOpen } from '@lucide/vue'
import BaseButton from '../../../core/components/BaseButton.vue'
import HeroSection from '../components/HeroSection.vue'
import FeaturesSection from '../components/FeaturesSection.vue'
</script>

<template>
  <div class="dark min-h-screen bg-[#0f172a] text-[#f8fafc] font-sans antialiased relative overflow-hidden">
    
    <div class="absolute inset-0 opacity-5 pointer-events-none select-none">
      <div class="absolute top-10 right-10 w-48 h-48 border border-white rounded-full flex items-center justify-center">
        <div class="w-0 h-0 border-l-30 border-l-transparent border-r-30 border-r-transparent border-b-52 border-b-white"></div>
      </div>
      <div class="absolute bottom-20 left-10 w-0 h-0 border-l-40 border-l-transparent border-r-40 border-r-transparent border-b-69 border-b-white"></div>
    </div>

    <header class="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center border-b border-[#475569]">
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 bg-blue-600 rounded-xl flex items-center justify-center shadow-md shadow-blue-500/20">
          <BookOpen class="w-4 h-4 text-white" />
        </div>
        <span class="font-bold text-lg tracking-tight text-white">MemoHub</span>
      </div>

      <div class="flex items-center gap-4">
        <BaseButton variant="secondary" class="h-9.5! px-4 rounded-lg border-blue-500! text-blue-400! hover:bg-blue-500/10!">
          Entrar
        </BaseButton>
      </div>
    </header>

    <main class="relative z-10">
      <HeroSection />
      <FeaturesSection /> 
    </main>
  </div>
</template>
