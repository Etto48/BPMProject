<script setup lang="ts">
import { ref } from 'vue';
import { ChevronDown } from 'lucide-vue-next';
import type { ProjectInDB } from '@/types';

withDefaults(defineProps<{
    project: ProjectInDB | null
    showRiskScoreThreshold?: boolean
}>(), {
    showRiskScoreThreshold: false
});

const showDescription = ref(true);
</script>

<template>
    <div class="card gradient-border hoverable project-info" @click="showDescription = !showDescription">
        <h3 class="gradient-background capsule project-title" :class="{ 'open': showDescription }">
            <span>{{ project?.title }}</span>
            <ChevronDown class="arrow" :class="{ 'open': showDescription }" :size="20" />
        </h3>
        <Transition name="description">
            <div v-if="showDescription">
                <div v-if="showRiskScoreThreshold" class="risk-score-panel">
                    <small>Risk Score Threshold</small><strong>{{ ((project?.riskScoreThreshold || 0) * 100).toFixed(0) }}%</strong>
                </div>
                <div class="gradient-background-light project-description">
                    <p>{{ project?.description }}</p>
                </div>
            </div>
        </Transition>
    </div>
</template>

<style scoped>
.risk-score-panel small {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--color-text-mute);
    padding: 0.5rem 2rem;
    border-right: 2px solid var(--color-border);
}

.risk-score-panel strong {
    display: flex;
    align-items: center;
    font-weight: 700;
    padding: 0.5rem 2rem;
}

.risk-score-panel {
    margin-bottom: 1rem;
    border-radius: 8px;
    padding: 0;
    background-color: var(--color-background-mute);
    display: flex;
    flex-direction: row;
    justify-content: end;
    align-items: stretch;
}

.project-info {
    cursor: pointer;
    transition: background-color 0.2s ease, border-color 0.2s ease;
}

.project-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2px 1rem;
    font-weight: 600;
    color: #fff;
    margin-bottom: 0;
    transition: filter 0.3s ease, background-color 0.2s ease, margin-bottom 0.3s ease;
}

.project-title .arrow {
    transition: transform 0.3s ease;
    display: inline-flex;
    flex-shrink: 0;
}

.project-title .arrow.open {
    transform: rotate(180deg);
}

.project-title.open {
    margin-bottom: 1rem;
}

.project-description {
    border-radius: 8px;
    padding: 1rem;
    transition: filter 0.3s ease, background-color 0.2s ease;
}

.project-description p {
    margin: 0;
    display: block;
}

.description-enter-active {
    transition: all 0.3s ease;
    overflow: hidden;
}

.description-leave-active {
    transition: all 0.3s ease;
    overflow: hidden;
}

.description-enter-from,
.description-leave-to {
    opacity: 0;
    max-height: 0;
    padding-top: 0;
    padding-bottom: 0;
    min-height: 0;
    margin: 0;
}

.description-enter-to,
.description-leave-from {
    opacity: 1;
    max-height: 200px;
}
</style>
