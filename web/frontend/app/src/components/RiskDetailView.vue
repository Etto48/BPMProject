<script setup lang="ts">
import type { DisplayableRisk } from '@/types';
import { computed } from 'vue';

const props = defineProps<{
    risk: DisplayableRisk | null
}>();

const hasRisk = computed(() => props.risk !== null);

const riskScore = computed(() => {
    if (!props.risk || props.risk.impact === undefined || props.risk.probability === undefined) {
        return null;
    }
    return props.risk.impact * props.risk.probability;
});
</script>

<template>
    <div class="flex-column detail-wrapper">
        <div v-if="hasRisk && risk" class="detail-container card">
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
                    <span class="score-value">{{ riskScore }}%</span>
                </div>
            </div>

            <div class="plan-section">
                <h4 class="plan-title">Contingency Plan</h4>
                <div class="plan-content" :class="{ 'no-plan': !risk.contingency }">
                    <p>{{ risk.contingency || 'No contingency plan available.' }}</p>
                </div>
            </div>

            <div class="plan-section">
                <h4 class="plan-title">Fallback Plan</h4>
                <div class="plan-content" :class="{ 'no-plan': !risk.fallback }">
                    <p>{{ risk.fallback || 'No fallback plan available.' }}</p>
                </div>
            </div>
        </div>
        
        <div v-else class="empty-state card">
            <p class="empty-text">Select a risk to view its details</p>
        </div>
    </div>
</template>

<style scoped>
.detail-wrapper {
    flex: 1;
    min-width: 300px;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    min-height: 0;
    padding: 2rem;
    padding-left: 0;
    align-items: center;
    overflow-y: auto;
}

.detail-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
    max-width: 700px;
    padding: 1.5rem;
    position: relative;
}

.empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 700px;
    padding: 3rem;
    text-align: center;
}

.empty-text {
    margin: 0;
    font-size: 1.1rem;
    color: var(--color-text-muted, #999);
}

.risk-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
}

.risk-title {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--color-text);
    flex: 1;
}

.risk-badge {
    padding: 0.375rem 0.875rem;
    border-radius: 6px;
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: capitalize;
    flex-shrink: 0;
}

.threat-badge {
    background-color: var(--color-threat);
    color: white;
}

.opportunity-badge {
    background-color: var(--color-opportunity);
    color: white;
}

.risk-description {
    padding: 0.75rem;
    background-color: var(--color-background-soft);
    border-radius: 8px;
    border-left: 4px solid var(--color-border);
}

.risk-description p {
    margin: 0;
    line-height: 1.5;
    color: var(--color-text);
    font-size: 0.95rem;
}

.risk-scores {
    display: flex;
    gap: 1rem;
    padding: 0.75rem;
    background-color: var(--color-background-soft);
    border-radius: 8px;
}

.score-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.125rem;
    text-align: center;
}

.score-item label {
    font-size: 0.8rem;
    color: var(--color-text-muted, #999);
    font-weight: 500;
}

.score-value {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--color-text);
}

.plan-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.plan-title {
    margin: 0;
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--color-text);
}

.plan-content {
    padding: 0.875rem;
    background-color: var(--color-background-soft);
    border-radius: 8px;
    border-left: 4px solid var(--color-accent-1);
}

.plan-content p {
    margin: 0;
    line-height: 1.6;
    color: var(--color-text);
    font-size: 0.95rem;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.plan-content.no-plan {
    border-left-color: var(--color-border);
    opacity: 0.7;
}

.plan-content.no-plan p {
    color: var(--color-text-muted, #999);
    font-style: italic;
}

@media (max-width: 768px) {
    .detail-wrapper {
        padding: 1rem;
    }

    .detail-container {
        max-width: 100%;
        padding: 1.5rem;
    }

    .risk-header {
        flex-direction: column;
    }

    .risk-scores {
        flex-direction: column;
        gap: 0.75rem;
    }

    .empty-state {
        padding: 2rem 1.5rem;
    }
}
</style>
