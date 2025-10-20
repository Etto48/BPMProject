<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import NewProjectButton from './NewProjectButton.vue';
import ProjectCard from './ProjectCard.vue';
</script>

<template>
    <main>
        <h2>Dashboard</h2>
        <div class="project-list">
            <ProjectCard risk_kind="threat" title="Project 1" description="This is a description of Project 1." />
            <ProjectCard risk_kind="opportunity" title="Project 2" description="This is a description of Project 2." />
            <NewProjectButton />
        </div>
    </main>
</template>

<style scoped>
    .project-list {
        display: flex;
        width: 100%;
        flex-direction: row;
        flex-wrap: wrap;
        align-content: flex-start;
        justify-content: flex-start;
        gap: 1rem;
    }
</style>