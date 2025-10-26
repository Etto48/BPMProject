<script setup lang="ts">
import type { DisplayableRisk } from '@/types';
import { useProject } from '@/composables/useProject';
import { computed } from 'vue';

const props = defineProps<{
    risk: DisplayableRisk
}>();

const { project } = useProject();

const riskScore = computed(() => {
    if (props.risk.impact === undefined || props.risk.probability === undefined) {
        return null;
    }
    return props.risk.impact * props.risk.probability;
});

const isAboveThreshold = computed(() => {
    if (!project.value || riskScore.value === null) {
        return false;
    }
    return riskScore.value >= project.value.riskScoreThreshold * 100;
});
</script>

<template>
    <div class="risk-info-section">
        <div class="risk-header">
            <h3 class="risk-title">{{ risk.title }}</h3>
            <span class="risk-badge" :class="risk.kind === 'threat' ? 'threat-badge' : 'opportunity-badge'">
                {{ risk.kind === 'threat' ? 'Threat' : 'Opportunity' }}
            </span>
        </div>
        
        <div class="risk-description">
            <p>{{ risk.description }}</p>
        </div>

        <div v-if="risk.impact !== undefined && risk.probability !== undefined" class="risk-scores">
            <div class="score-item">
                <label>Impact</label>
                <span class="score-value">{{ risk.impact }}/10</span>
            </div>
            <div class="score-item">
                <label>Probability</label>
                <span class="score-value">{{ risk.probability }}/10</span>
            </div>
            <div class="score-item">
                <label>Risk Score</label>
                <span class="score-value" :class="{ 'risk-score-active': isAboveThreshold }">{{ riskScore }}%</span>
            </div>
        </div>
    </div>
</template>

<style scoped>
@import '@/assets/risk-shared.css';

.risk-info-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
</style>
