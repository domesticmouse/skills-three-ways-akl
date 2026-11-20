<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    size?: 'sm' | 'md' | 'lg'
    url?: string
    caption?: string
    anchor?: string
  }>(),
  {
    size: 'md',
    url: 'https://domesticmouse.github.io/skills-three-ways-akl/',
    caption: 'Scan to open the codelab',
    anchor: '',
  }
)

const qrSrc = computed(() => {
  const base = (import.meta.env.BASE_URL || '/').replace(/\/$/, '')
  return `${base}/images/codelab-qr.svg`
})

const targetHref = computed(() => {
  const cleanUrl = props.url.replace(/\/$/, '')
  const cleanAnchor = props.anchor ? (props.anchor.startsWith('#') ? props.anchor : `#${props.anchor}`) : ''
  return `${cleanUrl}/${cleanAnchor}`
})

const imgSizeClass = computed(() => {
  if (props.size === 'sm') return 'w-24 h-24'
  if (props.size === 'lg') return 'w-56 h-56'
  return 'w-40 h-40'
})
</script>

<template>
  <div class="flex flex-col items-center text-center gap-2">
    <a
      :href="targetHref"
      target="_blank"
      rel="noopener"
      class="inline-block bg-white p-2.5 rounded-xl shadow-lg border border-white/20 hover:scale-[1.02] transition-transform"
      :aria-label="caption + ' (' + targetHref + ')'"
    >
      <img
        :src="qrSrc"
        alt="QR code to open the Skills Three Ways codelab"
        :class="[imgSizeClass, 'block']"
      />
    </a>
    <div class="text-xs text-gray-300 font-medium leading-snug">
      {{ caption }}
    </div>
    <a
      v-if="size !== 'sm'"
      :href="targetHref"
      target="_blank"
      rel="noopener"
      class="text-[11px] font-mono text-cyan-300 underline break-all max-w-xs"
    >
      {{ targetHref }}
    </a>
  </div>
</template>
