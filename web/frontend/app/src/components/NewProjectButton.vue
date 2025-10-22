<script setup lang="ts">
import { Plus } from 'lucide-vue-next';
</script>

<template>
    <button class="new-project-button card">
        <Plus :size="64" />
    </button>
</template>

<style scoped>
.new-project-button {
    background-color: var(--color-background);
    color: var(--color-text);
    min-width: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    flex-grow: 1;
    transition: background-color 0.2s ease;
    color: var(--color-text-opaque);
}

@media (hover: hover) {
    .new-project-button:hover {
        background-color: var(--color-border);
        cursor: pointer;
    }
}
</style>