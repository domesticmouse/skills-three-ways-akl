<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

const props = withDefaults(
  defineProps<{
    label: string
    text: string
    way?: string | number
    kind?: 'prompt' | 'command'
  }>(),
  {
    way: 0,
    kind: 'prompt',
  }
)

const state = ref<'idle' | 'copied' | 'failed'>('idle')
const statusMessage = ref('')
let resetTimer: ReturnType<typeof setTimeout> | undefined
let lastMessage = ''

const accentStyles = computed(() => {
  const str = String(props.way).toLowerCase()
  if (str.includes('1')) {
    return {
      border: 'border-cyan-500/40',
      badge: 'text-cyan-300 bg-cyan-500/10 border-cyan-500/35',
    }
  }
  if (str.includes('2')) {
    return {
      border: 'border-amber-500/40',
      badge: 'text-amber-300 bg-amber-500/10 border-amber-500/35',
    }
  }
  if (str.includes('3')) {
    return {
      border: 'border-emerald-500/40',
      badge: 'text-emerald-300 bg-emerald-500/10 border-emerald-500/35',
    }
  }
  if (str.includes('4') || str.includes('mashup')) {
    return {
      border: 'border-purple-500/40',
      badge: 'text-purple-300 bg-purple-500/10 border-purple-500/35',
    }
  }
  return {
    border: 'border-gray-700',
    badge: 'text-gray-300 bg-gray-800/80 border-gray-700',
  }
})

const badgeLabel = computed(() => (props.kind === 'command' ? 'Shell' : 'Prompt'))

async function handleCopy() {
  clearTimeout(resetTimer)
  let ok = false
  try {
    await navigator.clipboard.writeText(props.text)
    ok = true
  } catch {
    ok = false
  }

  let msg = ok ? 'Copied' : 'Copy failed'
  if (msg === lastMessage) {
    msg += '\u00A0'
  }
  lastMessage = msg

  state.value = ok ? 'copied' : 'failed'
  statusMessage.value = msg

  resetTimer = setTimeout(() => {
    state.value = 'idle'
    statusMessage.value = ''
  }, 2000)
}

onBeforeUnmount(() => {
  clearTimeout(resetTimer)
})
</script>

<template>
  <div class="rounded-xl bg-[#0d1117] border overflow-hidden" :class="accentStyles.border">
    <div class="flex items-center gap-2.5 px-3.5 py-2 bg-[#161922] border-b border-gray-800">
      <span
        class="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider border shrink-0"
        :class="accentStyles.badge"
      >
        {{ badgeLabel }}
      </span>
      <span class="text-xs font-semibold text-gray-200 mr-auto truncate">
        {{ label }}
      </span>
      <span class="relative inline-flex items-center shrink-0">
        <button
          type="button"
          class="inline-flex items-center justify-center gap-1.5 min-w-[4.5rem] min-h-[1.75rem] px-2.5 py-1 rounded-md border text-xs font-semibold cursor-pointer transition-colors"
          :class="
            state === 'copied'
              ? 'border-emerald-500/60 bg-emerald-500/15 text-emerald-200'
              : state === 'failed'
                ? 'border-red-500/60 bg-red-500/15 text-red-200'
                : 'border-gray-700 bg-[#21232d] text-gray-200 hover:border-gray-500 hover:bg-[#2a2d3a]'
          "
          :aria-label="'Copy ' + label"
          @click="handleCopy"
        >
          <svg
            v-if="state !== 'copied'"
            aria-hidden="true"
            viewBox="0 0 24 24"
            class="w-3.5 h-3.5"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect width="14" height="14" x="8" y="8" rx="2" ry="2" />
            <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" />
          </svg>
          <svg
            v-else
            aria-hidden="true"
            viewBox="0 0 24 24"
            class="w-3.5 h-3.5 text-emerald-300"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <polyline points="20 6 9 17 4 12" />
          </svg>
          <span>Copy</span>
        </button>
        <span
          role="status"
          class="pointer-events-none absolute bottom-full right-0 mb-1.5 px-2 py-0.5 rounded bg-[#0b0d12] border text-[11px] font-semibold whitespace-nowrap transition-opacity duration-150"
          :class="[
            state === 'idle' ? 'opacity-0 border-gray-700 text-gray-200' : 'opacity-100',
            state === 'copied' ? 'border-emerald-500/50 text-emerald-300' : '',
            state === 'failed' ? 'border-red-500/50 text-red-300' : '',
          ]"
        >
          {{ statusMessage }}
        </span>
      </span>
    </div>
    <pre
      tabindex="0"
      class="m-0 px-3.5 py-2.5 overflow-x-auto leading-relaxed"
      :class="
        kind === 'command'
          ? 'font-mono text-xs text-cyan-200 whitespace-pre'
          : 'font-sans text-[13px] text-gray-100 whitespace-pre-wrap break-words'
      "
    ><code>{{ text }}</code></pre>
  </div>
</template>
