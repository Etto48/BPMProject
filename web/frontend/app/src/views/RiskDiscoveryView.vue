<script setup lang="ts">
import { ref, toRaw, computed } from 'vue';
import RiskPreview from '@/components/RiskPreview.vue';
import { RiskKind, type Risk, type RiskSuggestion } from '@/types';
import RiskSuggestionProgress from '@/components/RiskSuggestionProgress.vue';
import ProjectAndRisksSidePanel from '@/components/ProjectAndRisksSidePanel.vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const projectId = Number(route.params.id);

const suggestedRisks = ref<Array<RiskSuggestion>>([]);
const currentSuggestionIndex = ref(0);
const acceptedThreats = ref<Array<RiskSuggestion>>([]);
const acceptedOpportunities = ref<Array<RiskSuggestion>>([]);
const projectTitle = ref('');
const projectDescription = ref('');
const isLoadingRisks = ref(true);

const allRisksProcessed = computed(() => {
    // Check if we're at the last (empty) risk and it hasn't been filled
    const isAtEnd = currentSuggestionIndex.value === suggestedRisks.value.length - 1;
    const lastRisk = suggestedRisks.value[currentSuggestionIndex.value];
    const lastRiskEmpty = lastRisk && lastRisk.title === '' && lastRisk.description === '';
    return isAtEnd && lastRiskEmpty && (acceptedThreats.value.length > 0 || acceptedOpportunities.value.length > 0);
});

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

function remove_risk(kind: 'threat' | 'opportunity', index: number) {
    if (kind === 'threat') {
        acceptedThreats.value.splice(index, 1);
    } else {
        acceptedOpportunities.value.splice(index, 1);
    }
}

function fetchProject() {
    fetch(`/api/projects/${projectId}`, {
        method: 'GET',
        credentials: 'include',
    }).then(async (response) => {
        if (response.ok) {
            const data = await response.json();
            console.log('Fetched project data:', data);
            projectTitle.value = data.title || 'Untitled Project';
            projectDescription.value = data.description || 'No description available';
        } else {
            console.log('Failed to fetch project data:', await response.text());
            router.push('/oops');
        }
    }).catch((error) => {
        console.error('Error fetching project data:', error);
        router.push('/oops');
    })
}

function fetchSuggestedRisks() {
    isLoadingRisks.value = true;
    fetch(`/api/projects/${projectId}/gen/risks`, {
        method: 'GET',
        credentials: 'include'
    }).then(async (response) => {
        if (response.ok) {
            const data: Array<Risk> = await response.json();
            console.log('Fetched suggested risks:', data);
            suggestedRisks.value = data.map((risk) => ({
                kind: risk.kind,
                title: risk.title,
                description: risk.description,
                accepted: false,
            }));
            suggestedRisks.value.push({
                kind: RiskKind.Threat,
                title: '',
                description: '',
                accepted: false,
            });
        } else {
            console.error('Failed to fetch suggested risks:', await response.text());
            router.push('/oops');
        }
    }).catch((error) => {
        console.error('Error fetching suggested risks:', error);
        router.push('/oops');
    }).finally(() => {
        isLoadingRisks.value = false;
    })
}

function uploadRisks() {
    const risksToUpload: Array<Risk> = [
        ...acceptedThreats.value.map((risk) => ({
            kind: RiskKind.Threat,
            title: risk.title,
            description: risk.description,
        })),
        ...acceptedOpportunities.value.map((risk) => ({
            kind: RiskKind.Opportunity,
            title: risk.title,
            description: risk.description,
        })),
    ];
    fetch(`/api/projects/${projectId}/risks`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(risksToUpload),
    }).then(async (response) => {
        if (response.ok) {
            console.log('Successfully uploaded risks');
            router.push(`/project/${projectId}/qualitative-analysis`);
        } else {
            console.error('Failed to upload risks:', await response.text());
            router.push('/oops');
        }
    }).catch((error) => {
        console.error('Error uploading risks:', error);
        router.push('/oops');
    })
}

fetchProject();
fetchSuggestedRisks();
</script>

<template>
    <div class="risk-discovery-container">
        <ProjectAndRisksSidePanel 
            :project-title="projectTitle"
            :project-description="projectDescription"
            :threats="acceptedThreats"
            :opportunities="acceptedOpportunities"
            :allow-remove="true"
            @remove-risk="remove_risk"
        />
        <div class="flex-column preview-wrapper">
            <div class="preview-container">
                <RiskSuggestionProgress :index="currentSuggestionIndex" :suggestions="suggestedRisks" :isLoading="isLoadingRisks" />
                <RiskPreview :index="currentSuggestionIndex" :suggestions="suggestedRisks" @accept="actionOnCurrent(true)" @reject="actionOnCurrent(false)"/>
                <Transition name="fade-slide">
                    <div v-if="allRisksProcessed" class="continue-section">
                        <p class="completion-message">All risks processed! Ready to continue to qualitative analysis.</p>
                        <button class="gradient-button large-button" @click="uploadRisks">
                            Continue to Analysis
                        </button>
                    </div>
                </Transition>
            </div>
        </div>
    </div>
</template>

<style scoped>
.preview-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    width: 100%;
    max-width: 700px;
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
    overflow-y: auto;
}

.preview-container > :first-child {
    flex-shrink: 0;
}

.preview-container > :nth-child(2) {
    flex-shrink: 0;
}

.risk-discovery-container {
    display: flex;
    width: 100%;
    padding: 0;
    flex-direction: row;
    gap: 2rem;
    justify-content: center;
    flex: 1;
    overflow: hidden;
}

@media (max-width: 768px) {
    .risk-discovery-container {
        flex-direction: column-reverse;
        align-items: stretch;
        height: auto;
    }
}

.continue-section {
    padding: 1.5rem;
    margin-bottom: 1rem;
    background: var(--color-background-soft);
    border-radius: 12px;
    border: 2px solid var(--color-border);
    text-align: center;
    flex-shrink: 0;
}

.completion-message {
    margin: 0 0 1rem 0;
    font-size: 1.1rem;
    font-weight: 500;
    color: var(--color-text);
}

.large-button {
    padding: 0.875rem 2rem;
    font-size: 1.05rem;
    font-weight: 600;
    width: 100%;
    max-width: 300px;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
    transition: all 0.4s ease;
}

.fade-slide-enter-from {
    opacity: 0;
    transform: translateY(-20px);
}

.fade-slide-leave-to {
    opacity: 0;
    transform: translateY(20px);
}

@media (max-width: 768px) {
    .preview-wrapper {
        padding: 1rem;
    }

    .preview-container {
        max-width: 100%;
    }
    
    .risk-discovery-container {
        gap: 0;
    }
}

</style>