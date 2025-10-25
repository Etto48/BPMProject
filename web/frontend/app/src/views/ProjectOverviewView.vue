<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import ProjectAndRisksSidePanel from '@/components/ProjectAndRisksSidePanel.vue';
import RiskDetailView from '@/components/RiskDetails.vue';
import type { ProjectInDB, DisplayableRisk } from '@/types';
import { ref, computed } from 'vue';

const route = useRoute();
const projectId = Number(route.params.id);
const router = useRouter();

const project = ref<ProjectInDB | null>(null);

const threats = ref<Array<DisplayableRisk>>([]);
const opportunities = ref<Array<DisplayableRisk>>([]);
const selectedRisk = ref<{kind: 'threat' | 'opportunity', index: number} | null >(null);

const currentRisk = computed(() => {
    if (!selectedRisk.value) return null;
    const list = selectedRisk.value.kind === 'threat' ? threats.value : opportunities.value;
    return list[selectedRisk.value.index] || null;
});

function selectDefaultRisk() {
    if (opportunities.value.length > 0) {
        selectedRisk.value = { kind: 'opportunity', index: 0 };
    } else if (threats.value.length > 0) {
        selectedRisk.value = { kind: 'threat', index: 0 };
    } else {
        selectedRisk.value = null;
    }
}

function selectRisk(kind: 'threat' | 'opportunity', index: number) {
    selectedRisk.value = { kind, index };
}

function projectUpdated(_project: ProjectInDB) {
    project.value = _project;
}

function fetchRisks() {
    fetch(`/api/projects/${projectId}/risks`, {
        method: 'GET',
        credentials: 'include',
    }).then(async (response) => {
        if (response.ok) {
            const risksData: Array<DisplayableRisk> = await response.json();
            console.log('Fetched risks data:', risksData);
            threats.value = risksData.filter(risk => risk.kind === 'threat');
            opportunities.value = risksData.filter(risk => risk.kind === 'opportunity');
            selectDefaultRisk();
        } else {
            console.error('Failed to fetch risks data:', await response.text());
            router.push('/oops');
        }
    }).catch((error) => {
        console.error('Error fetching risks data:', error);
        router.push('/oops');
    });
}

fetchRisks();
</script>

<template>
    <main>
        <ProjectAndRisksSidePanel 
            :threats="threats"
            :opportunities="opportunities"
            :allow-select="true"
            :show-risk-score-threshold="true"
            :selected-risk="selectedRisk"
            @selectRisk="selectRisk"
            @project-updated="projectUpdated"
        />
        <RiskDetailView :risk="currentRisk" />
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

@media (max-width: 768px) {
    main {
        gap: 0;
        flex-direction: column-reverse;
        align-items: stretch;
        height: auto;
    }
}
</style>