<template>
    <div
        class="tooltip"
        :style="{ left: x + 'px', top: y + 'px' }"
    >
        <div class="tooltip-title">{{ title }}</div>
        <div class="tooltip-description">{{ description }}</div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    x: number
    y: number
    title: string
    description: string
}>()
</script>

<style scoped>
.tooltip {
    position: fixed;
    background: var(--color-background-mute);
    color: var(--color-text-opaque);
    padding: 0.75rem 1rem;
    border-radius: 6px;
    border: 1px solid var(--color-border);
    pointer-events: none;
    z-index: 1000;
    max-width: 300px;
    box-shadow: 0 4px 12px var(--shadow-color);
}

.tooltip-title {
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.25rem;
    color: var(--color-heading);
}

.tooltip-description {
    font-size: 0.875rem;
    color: var(--color-text-dim-opaque);
}
</style>
