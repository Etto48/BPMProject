<script setup lang="ts">
import { ref, toRaw } from 'vue';
import ProgressNav from './ProgressNav.vue';
import RiskPreview from './RiskPreview.vue';
import { RiskKind, type RiskSuggestion } from '@/types';
import RiskSuggestionProgress from './RiskSuggestionProgress.vue';
import RiskDiscoveryLog from './RiskDiscoveryLog.vue';

const suggestedRisks = ref<Array<RiskSuggestion>>([
    {
        kind: RiskKind.Opportunity,
        title: 'Early Completion',
        description: 'Finish project ahead of schedule to gain competitive advantage.',
        accepted: false
    },
    {
        kind: RiskKind.Threat,
        title: 'Resource Shortage',
        description: 'Key personnel may be unavailable during critical phases.',
        accepted: false
    },
    {
        kind: RiskKind.Opportunity,
        title: 'Cost Savings',
        description: 'Reduce expenses through process optimization.',
        accepted: false
    },
    {
        kind: RiskKind.Threat,
        title: 'Scope Creep',
        description: 'Uncontrolled changes may lead to project delays.',
        accepted: false
    },
    {
        kind: RiskKind.Opportunity,
        title: 'Quality Improvement',
        description: 'Exceed quality expectations to enhance customer satisfaction.',
        accepted: false
    },
    {
        kind: RiskKind.Opportunity,
        title: '',
        description: '',
        accepted: false
    }
]);
const currentSuggestionIndex = ref(0);
const acceptedThreats = ref<Array<RiskSuggestion>>([]);
const acceptedOpportunities = ref<Array<RiskSuggestion>>([]);

function actionOnCurrent(accept: boolean) {
    let currentRisk = suggestedRisks.value[currentSuggestionIndex.value];
    if (currentRisk) {
        if (currentRisk.title === '' || currentRisk.description === '') {
            return;
        }
        currentRisk.accepted = accept;
        const clone = structuredClone(toRaw(currentRisk));
        if (accept) {
            if (currentRisk.kind === RiskKind.Threat) {
                acceptedThreats.value.push(clone);
            } else {
                acceptedOpportunities.value.push(clone);
            }
        }
    }
    if (currentSuggestionIndex.value < suggestedRisks.value.length - 1) {
        currentSuggestionIndex.value += 1;
    } else {
        currentRisk = suggestedRisks.value[currentSuggestionIndex.value];
        if (currentRisk) {
            currentRisk.accepted = false;
            currentRisk.title = '';
            currentRisk.description = '';
        }
    }
}
</script>

<template>
    <div class="risk-discovery-container">
        <RiskDiscoveryLog :threats="acceptedThreats" :opportunities="acceptedOpportunities" />
        <div class="flex-column preview-wrapper">
            <RiskSuggestionProgress :index="currentSuggestionIndex" :suggestions="suggestedRisks" />
            <RiskPreview :index="currentSuggestionIndex" :suggestions="suggestedRisks" @accept="actionOnCurrent(true)" @reject="actionOnCurrent(false)"/>
        </div>
    </div>
    <ProgressNav :total="5" :completed="3"/>
</template>

<style scoped>
.preview-wrapper {
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
    height: calc(100vh - 16rem);
}

@media (max-width: 768px) {
    .risk-discovery-container {
        flex-direction: column-reverse;
        align-items: stretch;
        height: auto;
    }
}

</style>