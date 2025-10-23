<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import { ref } from 'vue';
import type { ProjectInDB } from '@/types';
import { stepNames } from '@/constants';
import NewProjectButton from './NewProjectButton.vue';
import ProjectCard from './ProjectCard.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const projects = ref<Array<ProjectInDB>>([]);
const loading = ref(true);

function fetchProjects() {
    loading.value = true;
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
    }).finally(() => {
        loading.value = false;
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
        <div v-if="loading" class="loading-container">
            <div class="spinner"></div>
            <p>Loading projects...</p>
        </div>
        <div v-else class="project-list">
            <ProjectCard
                v-for="project in projects"
                :key="project.id"
                :title="project.title"
                :description="project.description"

                @click="router.push(`/project/${project.id}/${stepNames[project.currentStep]}`)"
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

    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 300px;
        gap: 1rem;
    }

    .spinner {
        width: 50px;
        height: 50px;
        position: relative;
        border-radius: 50%;
        border: 4px solid transparent;
        background: linear-gradient(var(--color-background), var(--color-background)) padding-box,
                    linear-gradient(45deg, var(--color-accent-1), var(--color-accent-2)) border-box;
        animation: spin 0.5s linear infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    .loading-container p {
        color: #666;
        font-size: 1rem;
    }
</style>