<script setup lang="ts">
defineProps<{ risk_kind: string, title: string, description: string }>();
</script>

<template>
    <div class="project-card card" :class="risk_kind">
        <h3>{{ title }}</h3>
        <p>{{ description }}</p>
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
        transition: background-color 0.2s ease;
    }

    .project-card p {
        border-radius: 8px;
        padding: 1rem;
        min-height: 80px;
        transition: background-color 0.2s ease;
    }

    .project-card.threat {
        border-color: var(--color-threat);
        background-color: var(--color-threat-light);
    }

    .project-card.threat h3 {
        background-color: var(--color-threat);
    }

    .project-card p {
        background-color: var(--color-threat-light);
    }

    .project-card.opportunity {
        border-color: var(--color-opportunity);
        background-color: var(--color-opportunity-light);
    }

    .project-card.opportunity h3 {
        background-color: var(--color-opportunity);
    }

    .project-card.opportunity p {
        background-color: var(--color-opportunity-light);
    }

    @media (hover: hover) {
        .project-card.threat:hover {
            background-color: var(--color-threat-hover-light);
            border-color: var(--color-threat-hover);
        }

        .project-card.threat:hover h3 {
            background-color: var(--color-threat-hover);
        }

        .project-card.threat:hover p {
            background-color: var(--color-threat-hover-light);
        }

        .project-card.opportunity:hover {
            background-color: var(--color-opportunity-hover-light);
            border-color: var(--color-opportunity-hover);
        }

        .project-card.opportunity:hover h3 {
            background-color: var(--color-opportunity-hover);
        }

        .project-card.opportunity:hover p {
            background-color: var(--color-opportunity-hover-light);
        }
    }
</style>