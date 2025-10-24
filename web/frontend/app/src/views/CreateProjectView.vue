<script setup lang="ts">
import type { Project } from '@/types';
import { useRouter } from 'vue-router';

const router = useRouter();

function createProject() {
    const project: Project = {
        title: (document.getElementById('project-title') as HTMLInputElement).value,
        description: (document.getElementById('project-description') as HTMLTextAreaElement).value,
    }

    fetch('/api/projects', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(project),
    }).then(async (response) => {
        if (response.ok) {
            const id = (await response.json()).id;
            router.push(`/project/${id}/risk-discovery`);
        } else {
            console.error('Failed to create project');
        }
    }).catch((error) => {
        console.error('Error creating project:', error);
    });
}

</script>

<template>
    <div class="card gradient-border">
        <h2 class="gradient-text gradient-border-bottom">Create New Project</h2>
        <div class="input-group">
            <label for="project-title">Project Title</label>
            <div class="input-wrapper input-gradient-border">
                <input id="project-title" type="text" placeholder="Enter your project name" class="styled-input" />
            </div>
        </div>
        <div class="input-group">
            <label for="project-description">Project Description</label>
            <div class="input-wrapper input-gradient-border">
                <textarea id="project-description" placeholder="Describe in detail your project" class="styled-input textarea-input" rows="5"></textarea>
            </div>
        </div>
        <button class="gradient-button" @click="createProject">Create Project</button>
    </div>
</template>

<style scoped>
.card {
    max-width: 600px;
    width: 100%;
    margin: 2rem auto;
    padding: 2rem;
}

h2 {
    border-radius: 8px;
    padding: 0 1.5rem 1.5rem 1.5rem;
    margin-bottom: 2rem;
    color: #fff;
    font-weight: 900;
    font-size: 2rem;
    text-align: center;
}

.textarea-input {
    resize: none;
    min-height: 120px;
    font-family: inherit;
    line-height: 1.5;
}

.gradient-button {
    width: 100%;
    margin-top: 0.5rem;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .card {
        margin: 1rem;
        padding: 1.5rem;
    }

    h1 {
        font-size: 1.25rem;
        padding: 0.625rem 1rem;
        margin-bottom: 1.5rem;
    }

    .textarea-input {
        min-height: 100px;
    }
}
</style>