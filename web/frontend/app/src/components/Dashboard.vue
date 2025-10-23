<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import { ref } from 'vue';
import type { ProjectInDB } from '@/types';
import NewProjectButton from './NewProjectButton.vue';
import ProjectCard from './ProjectCard.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const projects = ref<Array<ProjectInDB>>([]);

function fetchProjects() {
    fetch('/api/projects', {
        method: 'GET',
        credentials: 'include',
    }).then(async (response) => {
        if (response.ok) {
            projects.value = await response.json();
        } else {
            console.error('Failed to fetch projects');
        }
    }).catch((error) => {
        console.error('Error fetching projects:', error);
    });
}

function createNewProject() {
    router.push('/project/create');
}

fetchProjects();
</script>

<template>
    <main>
        <h2>Dashboard</h2>
        <div class="project-list">
            <ProjectCard
                v-for="project in projects"
                :key="project.id"
                :title="project.name"
                :description="project.description"
            />
            <NewProjectButton @click="createNewProject"/>
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