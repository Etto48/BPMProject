<script setup lang="ts">
import { ref } from 'vue'
import { ChevronDown } from 'lucide-vue-next'
import ExpandableProjectCard from './ExpandableProjectCard.vue'
import type { DisplayableRisk } from '@/types'
import { useRoute, useRouter } from 'vue-router'
import { X } from 'lucide-vue-next'

interface Props {
    threats: Array<DisplayableRisk>
    opportunities: Array<DisplayableRisk>
    allowRemove?: boolean
}

const route = useRoute()
const projectId = Number(route.params.id)
const router = useRouter()
const projectTitle = ref('')
const projectDescription = ref('')

withDefaults(defineProps<Props>(), {
    allowRemove: false
})

const emit = defineEmits<{
    removeRisk: [kind: 'threat' | 'opportunity', index: number]
}>()

const showOpportunities = ref(true)
const showThreats = ref(true)

function fetchProject() {
    fetch(`/api/projects/${projectId}`, {
        method: 'GET',
        credentials: 'include',
    }).then(async (response) => {
        if (response.ok) {
            const projectData = await response.json();
            projectTitle.value = projectData.title;
            projectDescription.value = projectData.description;
        } else {
            console.error('Failed to fetch project data:', await response.text());
            router.push('/oops');
        }
    }).catch((error) => {
        console.error('Error fetching project data:', error);
        router.push('/oops');
    });
}

fetchProject();
</script>

<template>
    <div class="side-panel">
        <ExpandableProjectCard :title="projectTitle" :description="projectDescription" />
    
        <div class="card opportunity-log hoverable" @click="showOpportunities = !showOpportunities">
            <h2 class="capsule" :class="{ 'open': showOpportunities }">
                <span>Opportunities</span>
                <ChevronDown class="arrow" :class="{ 'open': showOpportunities }" :size="20" />
            </h2>
            <Transition name="risk-list">
                <div v-if="showOpportunities" class="risk-list-container">
                    <div v-for="(opportunity, i) in opportunities" :key="i" class="risk-entry opportunity capsule" @click.stop>
                        <h3 class="risk-title">{{ opportunity.title }}</h3>
                        <X v-if="allowRemove" class="remove-button" @click="emit('removeRisk', 'opportunity', i)" title="Remove risk" role="button" />
                    </div>
                </div>
            </Transition>
        </div>
        <div class="card threat-log hoverable" @click="showThreats = !showThreats">
            <h2 class="capsule" :class="{ 'open': showThreats }">
                <span>Threats</span>
                <ChevronDown class="arrow" :class="{ 'open': showThreats }" :size="20" />
            </h2>
            <Transition name="risk-list">
                <div v-if="showThreats" class="risk-list-container">
                    <div v-for="(threat, i) in threats" :key="i" class="risk-entry threat capsule" @click.stop>
                        <h3 class="risk-title">{{ threat.title }}</h3>
                        <X v-if="allowRemove" class="remove-button" @click="emit('removeRisk', 'threat', i)" title="Remove risk" role="button" />
                    </div>
                </div>
            </Transition>
        </div>
        
    </div>
</template>

<style scoped>
.side-panel {
    display: flex;
    flex-direction: column;
    width: 350px;
    min-width: 350px;
    gap: 1.5rem;
    overflow-y: auto;
    padding: 1rem;
    background-color: var(--color-background-soft);
    border-right: 2px solid var(--color-border);
}

.side-panel .card {
    margin: 0;
}

.risk-log {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    flex: 1;
    min-height: 0;
}

.threat-log, .opportunity-log {
    min-width: 100%;
    flex-shrink: 0;
    cursor: pointer;
    transition: background-color 0.2s ease, border-color 0.2s ease;
}

.threat-log h2, .opportunity-log h2 {
    color: #fff;
    font-weight: 600;
    padding: 2px 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0;
    transition: margin-bottom 0.3s ease;
}

.threat-log h2 .arrow, .opportunity-log h2 .arrow {
    transition: transform 0.3s ease;
    display: inline-flex;
    flex-shrink: 0;
}

.threat-log h2 .arrow.open, .opportunity-log h2 .arrow.open {
    transform: rotate(180deg);
}

.threat-log h2.open, .opportunity-log h2.open {
    margin-bottom: 1rem;
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
    margin-bottom: 0;
    color: var(--color-text);
    font-size: 1rem;
    text-align: center;
}

.risk-entry {
    padding: 0.5rem 1rem;
    margin-bottom: 0.5rem;
    color: var(--color-text-opaque);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.risk-entry.threat {
    background-color: var(--color-threat-light);
}

.risk-entry.opportunity {
    background-color: var(--color-opportunity-light);
}

.risk-title {
    font-size: 1rem;
    font-weight: 500;
    margin: 0;
    flex: 1;
}

.remove-button {
    background: none;
    border: none;
    color: var(--color-text-opaque);
    font-size: 1.5rem;
    line-height: 1;
    cursor: pointer;
    padding: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    transition: all 0.2s;
    flex-shrink: 0;
}

.remove-button:hover {
    filter: brightness(1.5);
    background-color: #ffffff30;
}

.risk-list-enter-active {
    transition: all 0.3s ease;
    overflow: hidden;
}

.risk-list-leave-active {
    transition: all 0.3s ease;
    overflow: hidden;
}

.risk-list-enter-from,
.risk-list-leave-to {
    opacity: 0;
    max-height: 0;
    padding-top: 0;
    padding-bottom: 0;
    min-height: 0;
}

.risk-list-enter-to,
.risk-list-leave-from {
    opacity: 1;
    max-height: 500px;
}

@media (max-width: 768px) {
    .side-panel {
        width: 100%;
        min-width: 100%;
        border-right: none;
        border-bottom: 2px solid var(--color-border);
        background-color: unset;
    }
}
</style>
