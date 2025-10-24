<script setup lang="ts">
import { ref, toRaw } from 'vue';
import ProgressNav from './ProgressNav.vue';
import RiskPreview from './RiskPreview.vue';
import { RiskKind, type Risk, type RiskSuggestion } from '@/types';
import RiskSuggestionProgress from './RiskSuggestionProgress.vue';
import RiskDiscoveryLog from './RiskDiscoveryLog.vue';
import { useRoute, useRouter } from 'vue-router';
import { ChevronDown } from 'lucide-vue-next';

const route = useRoute();
const router = useRouter();
const projectId = Number(route.params.id);

const suggestedRisks = ref<Array<RiskSuggestion>>([]);
const currentSuggestionIndex = ref(0);
const acceptedThreats = ref<Array<RiskSuggestion>>([]);
const acceptedOpportunities = ref<Array<RiskSuggestion>>([]);
const showDescription = ref(false);
const projectTitle = ref('');
const projectDescription = ref('');
const isLoadingRisks = ref(true);

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
            console.log('Failed to fetch project data');
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
            console.error('Failed to fetch suggested risks');
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
        body: JSON.stringify({ risks: risksToUpload }),
    }).then(async (response) => {
        if (response.ok) {
            console.log('Successfully uploaded risks');
            router.push(`/projects/${projectId}/qualitative-analysis`);
        } else {
            console.error('Failed to upload risks');
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
        <div class="flex-column log-wrapper">
            <div class="card gradient-border hoverable project-info" @click="showDescription = !showDescription">
                <h3 class="gradient-background capsule project-title" :class="{ 'open': showDescription }">
                    <span>{{ projectTitle }}</span>
                    <ChevronDown class="arrow" :class="{ 'open': showDescription }" :size="20" />
                </h3>
                <Transition name="description">
                    <div v-if="showDescription" class="gradient-background-light project-description">
                        <p>{{ projectDescription }}</p>
                    </div>
                </Transition>
            </div>
            <RiskDiscoveryLog :threats="acceptedThreats" :opportunities="acceptedOpportunities" @remove-risk="remove_risk"/>
        </div>
        <div class="flex-column preview-wrapper">
            <RiskSuggestionProgress :index="currentSuggestionIndex" :suggestions="suggestedRisks" :isLoading="isLoadingRisks" />
            <RiskPreview :index="currentSuggestionIndex" :suggestions="suggestedRisks" @accept="actionOnCurrent(true)" @reject="actionOnCurrent(false)"/>
        </div>
    </div>
    <ProgressNav :total="3" :completed="1" :previousEnabled="false" :nextEnabled="true" @navigate-next="uploadRisks"/>
</template>

<style scoped>
.project-info {
    cursor: pointer;
    transition: background-color 0.2s ease, border-color 0.2s ease;
}

.project-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2px 1rem;
    font-weight: 600;
    color: #fff;
    margin-bottom: 0;
    transition: filter 0.3s ease, background-color 0.2s ease, margin-bottom 0.3s ease;
}

.project-title .arrow {
    transition: transform 0.3s ease;
    display: inline-flex;
    flex-shrink: 0;
}

.project-title .arrow.open {
    transform: rotate(180deg);
}

.project-title.open {
    margin-bottom: 1rem;
}

.project-description {
    border-radius: 8px;
    padding: 1rem;
    transition: filter 0.3s ease, background-color 0.2s ease;
}

.project-description p {
    margin: 0;
    display: block;
    overflow-y: auto;
    max-height: 100px;
}

.description-enter-active {
    transition: all 0.3s ease;
    overflow: hidden;
}

.description-leave-active {
    transition: all 0.3s ease;
    overflow: hidden;
}

.description-enter-from,
.description-leave-to {
    opacity: 0;
    max-height: 0;
    padding-top: 0;
    padding-bottom: 0;
    min-height: 0;
    margin: 0;
}

.description-enter-to,
.description-leave-from {
    opacity: 1;
    max-height: 200px;
}

.preview-wrapper {
    flex: 1;
    min-width: 300px;
}

.log-wrapper {
    flex: 1;
    max-width: 400px;
}

.risk-discovery-container {
    display: flex;
    width: 100%;
    max-width: 1200px;
    padding: 0 2rem;
    flex-direction: row;
    gap: 2rem;
    justify-content: center;
    height: calc(100vh - 13rem);
}

@media (max-width: 768px) {
    .log-wrapper {
        max-width: unset;
    }

    .risk-discovery-container {
        flex-direction: column-reverse;
        align-items: stretch;
        height: auto;
    }
}

</style>