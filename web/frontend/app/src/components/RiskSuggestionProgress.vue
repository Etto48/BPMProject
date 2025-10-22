<script setup lang="ts">
import { type RiskSuggestion } from '@/types';

defineProps<{
    index: number
    suggestions: Array<RiskSuggestion>
}>()
</script>


<template>
    <div class="risk-suggestion-progress">
        <div v-for="([i, suggestion]) in suggestions.entries()" :key="i" class="dot" :class="suggestion.kind + ' ' + (i === index ? 'active' : '') + ' ' + (suggestion.accepted ? 'accepted' : '') + ' ' + (i === suggestions.length - 1 ? 'custom' : '')"></div>
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
</style>