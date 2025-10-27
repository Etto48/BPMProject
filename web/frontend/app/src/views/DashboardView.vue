<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import { ref } from 'vue';
import type { ProjectInDB } from '@/types';
import { stepNames } from '@/constants';
import NewProjectButton from '@/components/NewProjectButton.vue';
import ProjectCard from '@/components/ProjectCard.vue';
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
            console.error('Failed to fetch projects:', await response.text());
            router.push('/oops');
        }
    }).catch((error) => {
        console.error('Error fetching projects:', error);
        router.push('/oops');
    }).finally(() => {
        loading.value = false;
    });
}

function removeProject(id: number) {
    projects.value = projects.value.filter((project) => project.id !== id);
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
                :projectId="project.id"
                :title="project.title"
                :description="project.description"

                @click="router.push(`/project/${project.id}/${stepNames[project.currentStep]}`)"
                @deleted="removeProject"
            />
            <NewProjectButton @click="createNewProject"/>
        </div>
    </main>
</template>

<style scoped>
    main {
        margin-top: 2rem;
        width: 100%;
        padding-left: 80px;
        padding-right: 80px;
        box-sizing: border-box;
        margin-bottom: auto;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    main h2 {
        font-size: 32px;
        margin-bottom: 1rem;
        display: inline-block;
    }

    .project-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
        width: 100%;
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

    @media (max-width: 768px) {
        main {
            margin-top: 0;
            width: 100%;
            padding-left: 16px;
            padding-right: 16px;
            box-sizing: border-box;
        }

        .project-list {
            grid-template-columns: 1fr;
        }
    }
</style>