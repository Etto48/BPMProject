<script setup lang="ts">
import ProgressNav from './ProgressNav.vue';
import RiskPreview from './RiskPreview.vue';
import { RiskKind } from '@/types';
</script>

<template>
    <div class="risk-discovery-container">
        <div class="risk-log">
            <div class="card opportunity-log">
                <h2 class="capsule">Opportunities</h2>
            </div>
            <div class="card threat-log">
                <h2 class="capsule">Threats</h2>
            </div>
        </div>
        <RiskPreview :risk_kind="RiskKind.Opportunity"/>
    </div>
    <ProgressNav :total="5" :completed="3"/>
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
}

.risk-discovery-container {
    display: flex;
    width: 100%;
    padding: 0 2rem;
    flex-direction: row;
    gap: 2rem;
    justify-content: center;
    flex-wrap: wrap;
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
</style>