<script setup lang="ts">
import { ArrowDownToLine } from 'lucide-vue-next';

const props = defineProps<{ projectId: number }>();

function handleClick(): void {
    const link = `/api/projects/${props.projectId}/download`;
    const anchor = document.createElement('a');
    anchor.href = link;
    anchor.download = 'project_' + props.projectId + '.json';
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
}
</script>

<template>
  <button
    class="download-floating-btn gradient-button"
    @click="handleClick"
    aria-label="Download project as JSON"
    title="Download project as JSON"
  >
    <!-- Simple download SVG icon -->
    <ArrowDownToLine :size="24"/>
  </button>
</template>

<style scoped>
.download-floating-btn {
    padding: 1rem;
    position: fixed;
    right: 1.5rem;
    bottom: 1.5rem;
    border-radius: 50%;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 6px 18px #00000060;
    cursor: pointer;
    z-index: 1000;
    transition: all 0.2s ease;
}

@media (hover: hover) {
    .download-floating-btn:hover {
        filter: brightness(0.8);
    }
}

@media (prefers-color-scheme: dark) {
    @media (hover: hover) {
        .download-floating-btn:hover {
            filter: brightness(1.2);
        }
    }
}
</style>
