<script setup lang="ts">
import { type RiskSuggestion } from '@/types';

defineProps<{
    index: number
    suggestions: Array<RiskSuggestion>
    isLoading?: boolean
}>()
</script>


<template>
    <div class="risk-suggestion-progress">
        <template v-if="isLoading">
            <div v-for="i in 5" :key="`loading-${i}`" class="dot loading" :style="{ animationDelay: `${i * 0.15}s` }"></div>
        </template>
        <template v-else>
            <div v-for="([i, suggestion]) in suggestions.entries()" :key="i" class="dot" :class="suggestion.kind + ' ' + (i === index ? 'active' : '') + ' ' + (suggestion.accepted ? 'accepted' : '') + ' ' + (i === suggestions.length - 1 ? 'custom' : '')"></div>
        </template>
    </div>
</template>

<style scoped>
.risk-suggestion-progress {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: row;
    gap: 0.5rem;
    margin: 1rem;
}
.dot {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    transition: all 0.3s ease;
    border: 0 solid transparent;
}

.dot.threat {
    background: var(--color-threat);
}

.dot.opportunity {
    background: var(--color-opportunity);
}

.dot:not(.active) {
    border: 3px solid var(--color-background);
}

.dot.custom {
    background: linear-gradient(135deg, var(--color-accent-1) 0%, var(--color-accent-2) 100%);
}

.dot:not(.accepted):not(.active) {
    opacity: 0.4;
}

.dot.loading {
    background: linear-gradient(135deg, var(--color-accent-1) 0%, var(--color-accent-2) 100%);
    animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
        opacity: 0.4;
    }
    50% {
        transform: scale(1.3);
        opacity: 1;
    }
}
</style>