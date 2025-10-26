<script setup lang="ts">
import type { DisplayableRisk } from '@/types';
import { computed } from 'vue';
import RiskInfoSection from './RiskInfoSection.vue';

const props = defineProps<{
    risk: DisplayableRisk | null
}>();

const hasRisk = computed(() => props.risk !== null);
</script>

<template>
    <div class="flex-column detail-wrapper">
        <div v-if="hasRisk && risk" class="detail-container card" :class="risk.kind">
            <RiskInfoSection :risk="risk" />

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
@import '@/assets/risk-shared.css';

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
    .empty-state {
        padding: 2rem 1.5rem;
    }
}
</style>
