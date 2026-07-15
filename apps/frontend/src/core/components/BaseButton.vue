<script setup lang="ts">
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value: string) => ['primary', 'secondary', 'danger'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <button
    :disabled="disabled || loading"
    class="h-48 px-6 rounded-xl font-medium text-sm flex items-center justify-center gap-2 transition-all duration-200 cursor-pointer select-none active:scale-[0.98] disabled:opacity-50 disabled:pointer-events-none"
    :class="{
      'bg-primary text-white hover:bg-primary-dark shadow-sm shadow-blue-500/10': variant === 'primary',
      'border-2 border-primary text-primary bg-transparent hover:bg-primary/5': variant === 'secondary',
      'bg-danger text-white hover:bg-red-600': variant === 'danger'
    }"
  >
    <span v-if="loading" class="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
    <slot v-else />
  </button>
</template>
