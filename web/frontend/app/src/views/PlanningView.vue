<script setup lang="ts">
import { ref, computed } from 'vue';
import ProjectAndRisksSidePanel from '@/components/ProjectAndRisksSidePanel.vue';
import RiskPlanPreview from '@/components/RiskPlanPreview.vue';
import { useRoute, useRouter } from 'vue-router';
import type { TrackedManagedRisk } from '@/types';

const route = useRoute();
const router = useRouter();
const projectId = Number(route.params.id);

const allRisks = ref<Array<TrackedManagedRisk>>([]);
const currentRiskIndex = ref(0);
const isLoadingPlans = ref(true);

// Separate threats and opportunities for the side panel
const acceptedThreats = computed(() => allRisks.value.filter(risk => risk.kind === 'threat'));
const acceptedOpportunities = computed(() => allRisks.value.filter(risk => risk.kind === 'opportunity'));

const allRisksAccepted = computed(() => 
    currentRiskIndex.value >= allRisks.value.length && allRisks.value.length > 0
);

function fetchRiskPlans() {
    isLoadingPlans.value = true;
    fetch(`/api/projects/${projectId}/gen/risks/plans`, {
        method: 'GET',
        credentials: 'include'
    }).then(async (response) => {
        if (response.ok) {
            const data: Array<TrackedManagedRisk> = await response.json();
            // Sort: opportunities first, then threats
            allRisks.value = data.sort((a, b) => {
                if (a.kind === 'opportunity' && b.kind === 'threat') return -1;
                if (a.kind === 'threat' && b.kind === 'opportunity') return 1;
                return 0;
            });
        } else {
            console.error('Failed to fetch risk plans:', await response.text());
            router.push('/oops');
        }
    }).catch((error) => {
        console.error('Error fetching risk plans:', error);
        router.push('/oops');
    }).finally(() => {
        isLoadingPlans.value = false;
    });
}

function acceptCurrentRisk() {
    const currentRisk = allRisks.value[currentRiskIndex.value];
    if (currentRisk) {
        // Move to next risk
        currentRiskIndex.value++;
    }
}

function handleContinue() {
    const risksToUpload: Array<TrackedManagedRisk> = [
        ...acceptedThreats.value,
        ...acceptedOpportunities.value
    ]
    fetch(`/api/projects/${projectId}/risks/plans`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(risksToUpload),
    }).then(async (response) => {
        if (response.ok) {
            router.push(`/project/${projectId}/overview`);
        } else {
            console.error('Failed to submit accepted risk plans:', await response.text());
            router.push('/oops');
        }
    }).catch((error) => {
        console.error('Error submitting accepted risk plans:', error);
        router.push('/oops');
    });
}

fetchRiskPlans();
</script>

<template>
    <main>
        <ProjectAndRisksSidePanel 
            :threats="acceptedThreats"
            :opportunities="acceptedOpportunities"
            :allow-remove="false"
        />
        <RiskPlanPreview
            v-if="!allRisksAccepted"
            :risks="allRisks"
            :index="currentRiskIndex"
            :isLoading="isLoadingPlans"
            @accept="acceptCurrentRisk"
        />
        <div v-else class="flex-column preview-wrapper">
            <div class="completion-card card">
                <h2>All Risk Plans Reviewed!</h2>
                <p>You have successfully reviewed and accepted all risk management plans.</p>
                <p class="summary">
                    Accepted <strong>{{ acceptedThreats.length }}</strong> threat{{ acceptedThreats.length !== 1 ? 's' : '' }}
                    and <strong>{{ acceptedOpportunities.length }}</strong> opportunit{{ acceptedOpportunities.length !== 1 ? 'ies' : 'y' }}.
                </p>
                <button class="gradient-button large-button" @click="handleContinue">
                    Complete Planning
                </button>
            </div>
        </div>
    </main>
</template>

<style scoped>
main {
    display: flex;
    width: 100%;
    padding: 0;
    flex-direction: row;
    gap: 2rem;
    justify-content: stretch;
    flex: 1;
    overflow: hidden;
}

.preview-wrapper {
    flex: 1;
    min-width: 300px;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    min-height: 0;
    padding: 2rem;
    padding-left: 0;
    align-items: center;
    justify-content: start;
    overflow-y: auto;
}

.completion-card {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    width: 100%;
    max-width: 600px;
    padding: 3rem;
    text-align: center;
}

.completion-card h2 {
    margin: 0;
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--color-accent-1), var(--color-accent-2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.completion-card p {
    margin: 0;
    font-size: 1.1rem;
    color: var(--color-text);
    line-height: 1.6;
}

.summary {
    padding: 1rem;
    background-color: var(--color-background-soft);
    border-radius: 8px;
    font-size: 1rem;
}

.summary strong {
    color: var(--color-accent-1);
}

.large-button {
    padding: 0.875rem 2rem;
    font-size: 1.05rem;
    font-weight: 600;
    width: 100%;
    max-width: 300px;
    margin: 0 auto;
}

@media (max-width: 768px) {
    main {
        gap: 0;
        flex-direction: column-reverse;
        align-items: stretch;
        height: auto;
    }

    .preview-wrapper {
        padding: 1rem;
    }

    .completion-card {
        padding: 2rem 1.5rem;
    }

    .completion-card h2 {
        font-size: 1.5rem;
    }
}
</style>