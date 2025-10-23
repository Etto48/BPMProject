<script setup lang="ts">
defineProps<{ title: string, description: string }>();
</script>

<template>
    <div class="project-card card gradient-border hoverable">
        <h3 class="capsule gradient-background">{{ title }}</h3>
        <div class="gradient-background-light description-wrapper">
            <p>{{ description }}</p>
        </div>
    </div>
</template>

<style scoped>
    .project-card {
        position: relative;
        transition: background-color 0.2s ease, border-color 0.2s ease;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        max-height: 200px;
    }

    .project-card h3 {
        display: block;
        padding: 2px 1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        transition: filter 0.3s ease, background-color 0.2s ease;
        flex-shrink: 0;
    }

    .description-wrapper {
        flex: 1;
        border-radius: 8px;
        padding: 1rem;
        transition: filter 0.3s ease, background-color 0.2s ease;
    }

    .description-wrapper p {
        margin: 0;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        line-clamp: 3;
        -webkit-box-orient: vertical;
        word-wrap: break-word;
    }
</style>