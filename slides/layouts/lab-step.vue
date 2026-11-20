<script setup lang="ts">
import QrBadge from '../components/QrBadge.vue'

function getWayBadgeClass(way: string | number | undefined): string {
  const str = String(way ?? '0').toLowerCase()
  if (str.includes('1')) return 'border-cyan-500/40 bg-cyan-500/10 text-cyan-300'
  if (str.includes('2')) return 'border-amber-500/40 bg-amber-500/10 text-amber-300'
  if (str.includes('3')) return 'border-emerald-500/40 bg-emerald-500/10 text-emerald-300'
  if (str.includes('4') || str.includes('mashup')) return 'border-purple-500/40 bg-purple-500/10 text-purple-300'
  return 'border-gray-600/60 bg-gray-800/80 text-gray-200'
}

function getCardBorderClass(way: string | number | undefined): string {
  const str = String(way ?? '0').toLowerCase()
  if (str.includes('1')) return 'border-cyan-500/30 bg-cyan-950/10'
  if (str.includes('2')) return 'border-amber-500/30 bg-amber-950/10'
  if (str.includes('3')) return 'border-emerald-500/30 bg-emerald-950/10'
  if (str.includes('4') || str.includes('mashup')) return 'border-purple-500/30 bg-purple-950/10'
  return 'border-gray-800 bg-gray-900/40'
}

function getCodelabHref(anchor: string | undefined): string {
  const clean = anchor ? (anchor.startsWith('#') ? anchor : `#${anchor}`) : ''
  return `https://domesticmouse.github.io/skills-three-ways-akl/${clean}`
}
</script>

<template>
  <div class="h-full w-full flex flex-col bg-[#121317] p-6 text-white overflow-hidden">
    <!-- Top Header Bar -->
    <div class="flex items-center justify-between gap-4 pb-3 border-b border-gray-800 shrink-0">
      <div class="flex items-center gap-3 min-w-0">
        <span
          class="px-2.5 py-1 rounded-full text-xs font-mono font-semibold border shrink-0"
          :class="getWayBadgeClass($frontmatter.way)"
        >
          {{ $frontmatter.step || 'Lab' }} &middot; {{ $frontmatter.duration || '~10 min' }}
        </span>
        <h2
          class="text-xl font-bold text-gray-100 m-0 truncate"
          v-html="$frontmatter.title || 'Hands-On Lab Step'"
        />
      </div>
      <a
        :href="getCodelabHref($frontmatter.codelabAnchor)"
        target="_blank"
        rel="noopener"
        class="shrink-0 text-xs font-mono text-cyan-300 underline hover:text-cyan-200"
      >
        Open Codelab {{ $frontmatter.codelabAnchor || '' }} &nearr;
      </a>
    </div>

    <!-- 12-Column Lab Body -->
    <div class="flex-1 min-h-0 grid grid-cols-12 gap-5 mt-4">
      <div class="col-span-8 flex flex-col gap-3 overflow-y-auto pr-1">
        <slot />
      </div>

      <div class="col-span-4 flex flex-col justify-between gap-3 min-h-0">
        <div
          class="rounded-xl border p-4 flex-1 overflow-y-auto space-y-3"
          :class="getCardBorderClass($frontmatter.way)"
        >
          <div class="text-xs font-mono uppercase tracking-wider text-gray-300 font-semibold">
            What to Verify
          </div>
          <div class="text-xs text-gray-200 leading-relaxed space-y-2">
            <slot name="verify">
              <p>Follow the steps in the codelab panel and confirm the expected output in your terminal.</p>
            </slot>
          </div>
          <div
            v-if="$frontmatter.checkpoint"
            class="pt-2 border-t border-gray-800/80 text-[11px] font-mono text-gray-400"
          >
            Checkpoint:
            <code class="text-gray-200">git checkout {{ $frontmatter.checkpoint }}</code>
          </div>
        </div>

        <div class="rounded-xl bg-[#1a1b22] border border-gray-800 p-3 flex items-center justify-center shrink-0">
          <QrBadge
            size="sm"
            :anchor="$frontmatter.codelabAnchor"
            caption="Scan for full step &amp; copy buttons"
          />
        </div>
      </div>
    </div>
  </div>
</template>
