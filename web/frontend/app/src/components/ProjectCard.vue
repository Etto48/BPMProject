<script setup lang="ts">
defineProps<{ title: string, description: string }>();
</script>

<template>
    <div class="project-card card gradient-border hoverable">
        <h3 class="gradient-background">{{ title }}</h3>
        <p class="gradient-background-light">{{ description }}</p>
    </div>
</template>

<style scoped>
    .project-card {
        position: relative;
        flex-grow: 1;
        transition: background-color 0.2s ease, border-color 0.2s ease;
        cursor: pointer;
    }

    .project-card h3 {
        display: block;
        border-radius: 1rem;
        padding: 2px 1rem;
        font-weight: 600;
        color: var(--color-background);
        margin-bottom: 1rem;
        transition: filter 0.3s ease, background-color 0.2s ease;
    }

    .project-card p {
        border-radius: 8px;
        padding: 1rem;
        min-height: 80px;
        transition: filter 0.3s ease, background-color 0.2s ease;
    }

    @media (hover: hover) {
        
    }
</style>