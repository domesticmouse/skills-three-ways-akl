#!/usr/bin/env node
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync, copyFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const REPO_ROOT = resolve(__dirname, '..');
const SLIDES_NODE_MODULES = join(REPO_ROOT, 'slides', 'node_modules');

const require = createRequire(import.meta.url);
const MarkdownIt = require(join(SLIDES_NODE_MODULES, 'markdown-it'));
const matter = require(join(SLIDES_NODE_MODULES, 'gray-matter'));
const { createHighlighter } = await import(join(SLIDES_NODE_MODULES, 'shiki', 'dist', 'index.mjs'));
const { renderSVG } = await import(join(SLIDES_NODE_MODULES, 'uqr', 'dist', 'index.mjs'));

const CODELAB_URL = process.env.CODELAB_URL || 'https://domesticmouse.github.io/skills-three-ways-akl/';
const STEPS_DIR = join(__dirname, 'steps');
const ASSETS_DIR = join(__dirname, 'assets');
const DIST_DIR = join(__dirname, 'dist');
const DIST_ASSETS_DIR = join(DIST_DIR, 'assets');
const SLIDES_QR_PATH = join(REPO_ROOT, 'slides', 'public', 'images', 'codelab-qr.svg');
const DIST_QR_PATH = join(DIST_ASSETS_DIR, 'codelab-qr.svg');

const WAY_META = {
  0: { label: 'Primer & Setup', short: 'Setup', tone: 'neutral' },
  1: { label: 'Way 1 · Plugins', short: 'Way 1', tone: 'way1' },
  2: { label: 'Way 2 · Community', short: 'Way 2', tone: 'way2' },
  3: { label: 'Way 3 · Bespoke', short: 'Way 3', tone: 'way3' },
  mashup: { label: 'Three Ways in Concert', short: 'Payoff', tone: 'mashup' },
};

function escapeHtml(text) {
  return String(text)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function parseFenceInfo(info) {
  const trimmed = (info || '').trim();
  if (!trimmed) {
    return { lang: 'text', label: null };
  }
  const match = trimmed.match(/^([^\s]+)(?:\s+(.*))?$/);
  const lang = match ? match[1] : 'text';
  const rest = match?.[2] || '';
  const labelMatch = rest.match(/label="([^"]+)"/);
  return {
    lang,
    label: labelMatch ? labelMatch[1] : null,
  };
}

function defaultFenceLabel(lang, stepTitle, index) {
  if (lang === 'prompt') return `Prompt ${index} (${stepTitle})`;
  if (lang === 'bash' || lang === 'sh' || lang === 'zsh') return `Terminal command ${index}`;
  return `${lang.toUpperCase()} snippet ${index}`;
}

function renderCopyWidget(codeId, label) {
  const ariaLabel = label.toLowerCase().startsWith('copy') ? label : `Copy ${label}`;
  return `<span class="copy">
  <button type="button" class="copy-button" command="--copy" commandfor="${escapeHtml(codeId)}" aria-label="${escapeHtml(ariaLabel)}">
    <svg class="icon-copy" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
    <svg class="icon-check" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
    <span class="copy-label">Copy</span>
  </button>
  <span class="copy-tip" role="status"></span>
</span>`;
}

function preprocessContainers(source, stepMeta, renderFragment) {
  const lines = source.split(/\r?\n/);
  const output = [];
  let inFence = false;
  let fenceChar = '';
  let fenceLen = 0;

  let activeBlock = null;
  let blockLines = [];
  let checkCounter = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const fenceMatch = line.match(/^\s*(`{3,}|~{3,})/);
    if (fenceMatch) {
      const marker = fenceMatch[1];
      if (!inFence) {
        inFence = true;
        fenceChar = marker[0];
        fenceLen = marker.length;
      } else if (marker[0] === fenceChar && marker.length >= fenceLen && line.trim() === marker) {
        inFence = false;
      }
      if (activeBlock) {
        blockLines.push(line);
      } else {
        output.push(line);
      }
      continue;
    }

    if (!inFence) {
      if (!activeBlock) {
        const openDetails = line.match(/^:::details\s+(.+?)\s*$/);
        const openCallout = line.match(/^:::callout\s+(info|tip|warn)\s+(.+?)\s*$/);
        const openChecklist = line.match(/^:::checklist\s*$/);

        if (openDetails) {
          activeBlock = { kind: 'details', title: openDetails[1] };
          blockLines = [];
          continue;
        }
        if (openCallout) {
          activeBlock = { kind: 'callout', tone: openCallout[1], title: openCallout[2] };
          blockLines = [];
          continue;
        }
        if (openChecklist) {
          activeBlock = { kind: 'checklist' };
          blockLines = [];
          continue;
        }
      } else if (line.trim() === ':::') {
        const innerMd = blockLines.join('\n');
        let rendered = '';
        if (activeBlock.kind === 'details') {
          const innerHtml = renderFragment(innerMd);
          rendered = `<details class="foldout">\n  <summary><span class="foldout-title">${escapeHtml(activeBlock.title)}</span></summary>\n  <div class="foldout-body">\n${innerHtml}\n  </div>\n</details>`;
        } else if (activeBlock.kind === 'callout') {
          const innerHtml = renderFragment(innerMd);
          rendered = `<aside class="callout callout-${escapeHtml(activeBlock.tone)}">\n  <p class="callout-title">${escapeHtml(activeBlock.title)}</p>\n  <div class="callout-body">\n${innerHtml}\n  </div>\n</aside>`;
        } else if (activeBlock.kind === 'checklist') {
          const items = [];
          for (const itemLine of blockLines) {
            const match = itemLine.match(/^\s*-\s+\[\s*[xX ]?\s*\]\s+(.+)$/);
            if (!match) continue;
            checkCounter += 1;
            const chkId = `chk-${stepMeta.id}-${checkCounter}`;
            const labelHtml = renderFragment(match[1], true);
            items.push(
              `<div class="check-item"><input type="checkbox" id="${escapeHtml(chkId)}" data-step-id="${escapeHtml(stepMeta.id)}" data-check-id="${escapeHtml(chkId)}"><label for="${escapeHtml(chkId)}">${labelHtml}</label></div>`
            );
          }
          rendered = `<div class="checklist" role="group" aria-label="Lab ${escapeHtml(String(stepMeta.step))} completion checklist">\n${items.join('\n')}\n</div>`;
        }
        output.push('');
        output.push(rendered);
        output.push('');
        activeBlock = null;
        blockLines = [];
        continue;
      }
    }

    if (activeBlock) {
      blockLines.push(line);
    } else {
      output.push(line);
    }
  }

  if (activeBlock) {
    throw new Error(`Unclosed :::${activeBlock.kind} container in ${stepMeta.filename}`);
  }

  return output.join('\n');
}

function injectShikiCodeId(shikiHtml, codeId) {
  let updated = shikiHtml.replace('<code>', `<code id="${escapeHtml(codeId)}">`);
  if (!updated.includes('tabindex="0"')) {
    updated = updated.replace('<pre ', '<pre tabindex="0" ');
  }
  return updated;
}

async function build() {
  const checkMode = process.argv.includes('--check');

  if (!existsSync(STEPS_DIR)) {
    throw new Error(`Missing codelab steps directory: ${STEPS_DIR}`);
  }

  const highlighter = await createHighlighter({
    themes: ['github-dark-default'],
    langs: ['bash', 'python', 'markdown', 'yaml', 'json', 'text', 'shellscript', 'diff'],
  });
  const loadedLangs = new Set(highlighter.getLoadedLanguages());

  const md = new MarkdownIt({
    html: true,
    linkify: true,
    typographer: false,
  });

  let currentStepMeta = null;
  let codeCounter = 0;

  md.renderer.rules.fence = (tokens, idx) => {
    const token = tokens[idx];
    const { lang, label } = parseFenceInfo(token.info);
    codeCounter += 1;
    const stepId = currentStepMeta ? currentStepMeta.id : 'global';
    const codeId = `code-${stepId}-${codeCounter}`;
    const rawCode = token.content.replace(/\n$/, '');
    const cardLabel = label || defaultFenceLabel(lang, currentStepMeta?.title || 'Lab', codeCounter);
    const copyWidget = renderCopyWidget(codeId, cardLabel);

    if (lang === 'prompt') {
      return `<div class="code-card code-card-prompt" data-way="${escapeHtml(String(currentStepMeta?.way ?? '0'))}">
  <div class="code-card-header">
    <span class="code-card-badge">Prompt</span>
    <span class="code-card-label">${escapeHtml(cardLabel)}</span>
    ${copyWidget}
  </div>
  <pre class="prompt-pre" tabindex="0"><code id="${escapeHtml(codeId)}">${escapeHtml(rawCode)}</code></pre>
</div>\n`;
    }

    const shikiLang = loadedLangs.has(lang) ? lang : 'text';
    const highlighted = injectShikiCodeId(
      highlighter.codeToHtml(rawCode, {
        lang: shikiLang,
        theme: 'github-dark-default',
      }),
      codeId
    );
    const kindBadge = lang === 'bash' || lang === 'sh' || lang === 'zsh' ? 'Shell' : lang.toUpperCase();
    return `<div class="code-card">
  <div class="code-card-header">
    <span class="code-card-badge">${escapeHtml(kindBadge)}</span>
    <span class="code-card-label">${escapeHtml(cardLabel)}</span>
    ${copyWidget}
  </div>
  ${highlighted}
</div>\n`;
  };

  function renderFragment(fragmentMd, inline = false) {
    return inline ? md.renderInline(fragmentMd) : md.render(fragmentMd);
  }

  const stepFiles = readdirSync(STEPS_DIR)
    .filter((f) => f.endsWith('.md'))
    .sort();

  if (stepFiles.length !== 6) {
    throw new Error(`Expected 6 step files in ${STEPS_DIR}, found ${stepFiles.length}: ${stepFiles.join(', ')}`);
  }

  const requiredFields = ['id', 'step', 'title', 'way', 'duration', 'slide', 'slidePath', 'checkpoint', 'summary'];
  const steps = [];

  for (const filename of stepFiles) {
    const raw = readFileSync(join(STEPS_DIR, filename), 'utf8');
    const parsed = matter(raw);
    const data = parsed.data;
    for (const field of requiredFields) {
      if (data[field] === undefined || data[field] === null || data[field] === '') {
        throw new Error(`Missing required frontmatter field "${field}" in ${filename}`);
      }
    }

    const stepMeta = { ...data, filename };
    currentStepMeta = stepMeta;
    codeCounter = 0;

    const expandedMd = preprocessContainers(parsed.content, stepMeta, renderFragment);
    const bodyHtml = md.render(expandedMd);
    steps.push({
      ...stepMeta,
      wayInfo: WAY_META[String(stepMeta.way)] || WAY_META[0],
      bodyHtml,
    });
  }

  const qrSvg = renderSVG(CODELAB_URL, { border: 2, ecc: 'M' });
  mkdirSync(dirname(SLIDES_QR_PATH), { recursive: true });
  mkdirSync(DIST_ASSETS_DIR, { recursive: true });
  writeFileSync(SLIDES_QR_PATH, qrSvg, 'utf8');
  writeFileSync(DIST_QR_PATH, qrSvg, 'utf8');

  copyFileSync(join(ASSETS_DIR, 'style.css'), join(DIST_ASSETS_DIR, 'style.css'));
  copyFileSync(join(ASSETS_DIR, 'codelab.js'), join(DIST_ASSETS_DIR, 'codelab.js'));

  const navItemsHtml = steps
    .map((step, index) => {
      const currentAttr = index === 0 ? ' aria-current="step"' : '';
      return `      <li class="step-nav-item" data-way="${escapeHtml(String(step.way))}">
        <a href="#${escapeHtml(step.id)}" class="step-nav-link" data-step-target="${escapeHtml(step.id)}"${currentAttr}>
          <span class="step-num" aria-hidden="true">${escapeHtml(String(step.step))}</span>
          <span class="step-nav-text">
            <span class="step-nav-title">${escapeHtml(step.title)}</span>
            <span class="step-nav-meta">${escapeHtml(step.wayInfo.short)} &middot; ${escapeHtml(step.duration)}</span>
          </span>
          <span class="step-done-mark" aria-hidden="true">✓</span>
        </a>
      </li>`;
    })
    .join('\n');

  const panelsHtml = steps
    .map((step, index) => {
      const hiddenAttr = index === 0 ? '' : ' hidden';
      const prevStep = index > 0 ? steps[index - 1] : null;
      const nextStep = index < steps.length - 1 ? steps[index + 1] : null;

      const prevButton = prevStep
        ? `<a class="pager-btn pager-prev" href="#${escapeHtml(prevStep.id)}" data-step-target="${escapeHtml(prevStep.id)}">&larr; Lab ${escapeHtml(String(prevStep.step))}: ${escapeHtml(prevStep.title)}</a>`
        : `<span class="pager-spacer"></span>`;

      const nextButton = nextStep
        ? `<button type="button" class="pager-btn pager-next" data-complete-step="${escapeHtml(step.id)}" data-next-step="${escapeHtml(nextStep.id)}">Mark Lab ${escapeHtml(String(step.step))} Complete &amp; Next &rarr;</button>`
        : `<button type="button" class="pager-btn pager-next pager-finish" data-complete-step="${escapeHtml(step.id)}">Mark Lab ${escapeHtml(String(step.step))} Complete</button>`;

      return `    <article class="step-panel" id="${escapeHtml(step.id)}" data-step-index="${index}" data-step-id="${escapeHtml(step.id)}" data-step-title="${escapeHtml(step.title)}" data-way="${escapeHtml(String(step.way))}"${hiddenAttr}>
      <div class="step-hero">
        <div class="step-meta-row">
          <span class="way-pill" data-way="${escapeHtml(String(step.way))}">Lab ${escapeHtml(String(step.step))} &middot; ${escapeHtml(step.wayInfo.label)}</span>
          <span class="duration-pill">${escapeHtml(step.duration)}</span>
          <a class="slide-ref-pill" href="${escapeHtml(step.slidePath)}" title="Open matching slide ${escapeHtml(step.slide)}">Slide ${escapeHtml(step.slide)} &nearr;</a>
        </div>
        <h1 class="step-heading" tabindex="-1">${escapeHtml(step.title)}</h1>
        <p class="step-summary">${escapeHtml(step.summary)}</p>
        <div class="checkpoint-strip">
          <span class="checkpoint-label">Recovery checkpoint:</span>
          <code>git checkout ${escapeHtml(step.checkpoint)}</code>
        </div>
      </div>

      <div class="step-body">
${step.bodyHtml}
      </div>

      <nav class="step-pager" aria-label="Lab ${escapeHtml(String(step.step))} progression">
        ${prevButton}
        ${nextButton}
      </nav>
    </article>`;
    })
    .join('\n\n');

  const html = `<!doctype html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark">
  <title>Lab 0: ${escapeHtml(steps[0].title)} | Skills Three Ways Codelab</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <a href="#step-content" class="skip-link visually-hidden">Skip to lab content</a>

  <header class="topbar">
    <div class="topbar-inner">
      <div class="brand-group">
        <a class="brand" href="#step-0">Skills Three Ways</a>
        <span class="brand-sub">90-Minute Self-Paced Codelab</span>
      </div>

      <div class="progress-group">
        <label for="lab-progress" class="progress-label">
          <span id="progress-text">0 of ${steps.length} labs complete</span>
        </label>
        <progress id="lab-progress" max="${steps.length}" value="0"></progress>
      </div>

      <div class="topbar-actions">
        <a class="topbar-link" href="./slides/">Presentation Deck &nearr;</a>
        <button type="button" id="reset-progress-btn" class="ghost-btn">Reset progress</button>
      </div>
    </div>
  </header>

  <div class="status-announcer visually-hidden" id="codelab-status" role="status" aria-live="polite"></div>

  <div class="layout-shell">
    <nav class="sidebar" aria-label="Codelab steps">
      <div class="sidebar-header">
        <span class="sidebar-kicker">DevFest Auckland 2026</span>
        <p class="sidebar-lead">Ecosystem, Community &amp; Bespoke Skills</p>
      </div>

      <ol class="step-list">
${navItemsHtml}
      </ol>

      <div class="qr-sidebar-card">
        <div class="qr-frame">
          <img src="assets/codelab-qr.svg" alt="QR code to open the Skills Three Ways codelab" width="132" height="132">
        </div>
        <p class="qr-caption">Share or open on another screen</p>
        <a class="qr-url" href="${escapeHtml(CODELAB_URL)}" target="_blank" rel="noopener">domesticmouse.github.io/skills-three-ways-akl/</a>
      </div>
    </nav>

    <main id="step-content">
${panelsHtml}
    </main>
  </div>

  <footer class="site-footer">
    <div class="footer-inner">
      <span>Companion codelab by Brett Morgan &middot; <a href="https://github.com/domesticmouse/skills-three-ways-akl" target="_blank" rel="noopener">github.com/domesticmouse/skills-three-ways-akl</a></span>
      <span>Apache 2.0 License &middot; Not an official Google product</span>
    </div>
  </footer>

  <script src="assets/codelab.js" defer></script>
</body>
</html>
`;

  writeFileSync(join(DIST_DIR, 'index.html'), html, 'utf8');
  validateBuiltSite(html);

  if (checkMode) {
    console.log('Validated codelab output (--check passed).');
  }

  console.log(`Built codelab (${steps.length} labs) -> codelab/dist/index.html`);
  console.log(`Generated QR SVGs -> codelab/dist/assets/codelab-qr.svg & slides/public/images/codelab-qr.svg`);
}

function validateBuiltSite(html) {
  const errors = [];

  for (const summaryMatch of html.matchAll(/<summary\b[^>]*>([\s\S]*?)<\/summary>/gi)) {
    if (/<h[1-6][\s>]/i.test(summaryMatch[1])) {
      errors.push('Heading tag (<h1..h6>) detected inside <summary>');
    }
  }

  const ids = new Set();
  for (const match of html.matchAll(/\bid="([^"]+)"/g)) {
    ids.add(match[1]);
  }
  for (const match of html.matchAll(/\bcommandfor="([^"]+)"/g)) {
    if (!ids.has(match[1])) {
      errors.push(`commandfor="${match[1]}" does not match any element id in compiled HTML`);
    }
  }

  const copyLabels = new Set();
  for (const match of html.matchAll(/<button[^>]*class="copy-button"[^>]*aria-label="([^"]+)"/g)) {
    const label = match[1];
    if (!label.startsWith('Copy')) {
      errors.push(`Copy button aria-label "${label}" must begin with visible text "Copy"`);
    }
    if (copyLabels.has(label)) {
      errors.push(`Duplicate Copy button aria-label detected: "${label}"`);
    }
    copyLabels.add(label);
  }

  for (const qrPath of [SLIDES_QR_PATH, DIST_QR_PATH]) {
    if (!existsSync(qrPath)) {
      errors.push(`Missing QR SVG at ${qrPath}`);
    } else {
      const content = readFileSync(qrPath, 'utf8');
      if (!content.includes('<svg')) {
        errors.push(`Invalid QR SVG content at ${qrPath}`);
      }
    }
  }

  if (errors.length > 0) {
    throw new Error(`Codelab validation failed:\n- ${errors.join('\n- ')}`);
  }
}

build().catch((err) => {
  console.error(err);
  process.exit(1);
});
