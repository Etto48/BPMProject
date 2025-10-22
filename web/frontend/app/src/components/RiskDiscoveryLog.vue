<script setup lang="ts">
import type { Risk } from '@/types';

defineProps<{
    threats: Array<Risk>,
    opportunities: Array<Risk>
}>();
</script>

<template>
    <div class="risk-log">
        <div class="card opportunity-log">
            <h2 class="capsule">Opportunities</h2>
            <div class="risk-list-container">
                <div v-for="([i, opportunity]) in opportunities.entries()" :key="i" class="risk-entry opportunity capsule">
                    <h3 class="risk-title">{{ opportunity.title }}</h3>
                </div>
            </div>
        </div>
        <div class="card threat-log">
            <h2 class="capsule">Threats</h2>
            <div class="risk-list-container">
                <div v-for="([i, threat]) in threats.entries()" :key="i" class="risk-entry threat capsule">
                    <h3 class="risk-title">{{ threat.title }}</h3>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.risk-log {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin: 0;
    flex: 1;
}
.threat-log, .opportunity-log {
    flex: 1;
    min-width: 300px;
    height: calc(50% - 1.5rem);
}

.risk-list-container {
    min-height: 100px;
    height: calc(100% - 3.5rem);
    overflow-y: auto;
    padding: 0.5rem;
}

.threat-log h2, .opportunity-log h2 {
    color: #fff;
    font-weight: 700;
}

.threat-log h2 {
    background-color: var(--color-threat);
}

.opportunity-log h2 {
    background-color: var(--color-opportunity);
}

.threat-log {
    background-color: var(--color-threat-light);
    border: 4px solid var(--color-threat);
}

.opportunity-log {
    background-color: var(--color-opportunity-light);
    border: 4px solid var(--color-opportunity);
}

h2 {
    margin-bottom: 1rem;
    color: var(--color-text);
    font-size: 1.5rem;
    text-align: center;
}

.risk-entry {
    padding: 0.5rem 1rem;
    margin-bottom: 0.5rem;
    color: var(--color-text-opaque);
}

.risk-entry.threat {
    background-color: var(--color-threat-light);
}

.risk-entry.opportunity {
    background-color: var(--color-opportunity-light);
}

</style>