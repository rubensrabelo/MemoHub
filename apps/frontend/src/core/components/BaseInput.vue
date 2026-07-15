<script setup lang="ts">
defineProps({
  modelValue: [String, Number],
  label: String,
  type: { type: String, default: 'text' },
  placeholder: String,
  error: String
})
defineEmits(['update:modelValue'])
</script>

<template>
  <div class="flex flex-col gap-1.5 w-full">
    <label v-if="label" class="text-[13px] font-medium text-slate-400 dark:text-slate-300">
      {{ label }}
    </label>
    <input
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      :placeholder="placeholder"
      class="w-full h-12 px-4 bg-(--bg-surface) border rounded-xl text-base text-(--text-main) placeholder-slate-400 outline-none transition-all duration-200 focus:ring-2"
      :class="error 
        ? 'border-danger focus:ring-danger/20' 
        : 'border-(--border-color) focus:border-primary focus:ring-primary/20'"
    />
    <span v-if="error" class="text-xs text-danger font-medium mt-0.5">{{ error }}</span>
  </div>
</template>
