<script setup lang="ts">
import { ref } from 'vue'
import RiskGraph from './RiskGraph.vue'
import RiskThresholdSlider from './RiskThresholdSlider.vue'
import RiskTooltip from './RiskTooltip.vue'
import ProjectAndRisksSidePanel from './ProjectAndRisksSidePanel.vue'
import type { TrackedScoredRisk } from '@/types'
import { useRoute, useRouter } from 'vue-router'

interface DragState {
    index: number
    tempImpact: number
    tempProbability: number
}

const route = useRoute()
const router = useRouter()
const projectId = Number(route.params.id)

// Risk threshold curve constant (impact * probability = k)
const riskThreshold = ref(0.1)

const threats = ref<Array<TrackedScoredRisk>>([])
const opportunities = ref<Array<TrackedScoredRisk>>([])
const projectTitle = ref('')
const projectDescription = ref('')

const draggedThreatPoint = ref<DragState | null>(null)
const draggedOpportunityPoint = ref<DragState | null>(null)

const tooltips = ref<Array<{
    x: number
    y: number
    title: string
    description: string
}>>([])

const hoveredPoints = ref<Set<string>>(new Set())

const handleContinue = () => {
    // TODO: Navigate to contingency and fallback planning when implemented
    // router.push(`/project/${projectId}/contingency-planning`)
    alert('Contingency and fallback planning is not yet implemented. Coming soon!')
}

// Opportunity handlers
const handleOpportunityMouseDown = (index: number) => {
    const point = opportunities.value[index]
    if (!point) return
    draggedOpportunityPoint.value = { 
        index,
        tempImpact: point.impact,
        tempProbability: point.probability
    }
    tooltips.value = []
    hoveredPoints.value.clear()
}

const handleOpportunityMouseMove = (impact: number, probability: number) => {
    if (!draggedOpportunityPoint.value) return
    draggedOpportunityPoint.value.tempImpact = impact
    draggedOpportunityPoint.value.tempProbability = probability
}

// Threat handlers
const handleThreatMouseDown = (index: number) => {
    const point = threats.value[index]
    if (!point) return
    draggedThreatPoint.value = { 
        index,
        tempImpact: point.impact,
        tempProbability: point.probability
    }
    tooltips.value = []
    hoveredPoints.value.clear()
}

const handleThreatMouseMove = (impact: number, probability: number) => {
    if (!draggedThreatPoint.value) return
    draggedThreatPoint.value.tempImpact = impact
    draggedThreatPoint.value.tempProbability = probability
}

const handleMouseUp = () => {
    if (draggedOpportunityPoint.value) {
        const point = opportunities.value[draggedOpportunityPoint.value.index]
        if (point) {
            point.impact = Math.round(draggedOpportunityPoint.value.tempImpact)
            point.probability = Math.round(draggedOpportunityPoint.value.tempProbability)
        }
        draggedOpportunityPoint.value = null
    }
    
    if (draggedThreatPoint.value) {
        const point = threats.value[draggedThreatPoint.value.index]
        if (point) {
            point.impact = Math.round(draggedThreatPoint.value.tempImpact)
            point.probability = Math.round(draggedThreatPoint.value.tempProbability)
        }
        draggedThreatPoint.value = null
    }
}

const findOverlappingPoints = (targetPoint: TrackedScoredRisk, type: 'threats' | 'opportunities'): TrackedScoredRisk[] => {
    const overlapping: TrackedScoredRisk[] = [targetPoint]
    
    // Only check within the same graph type
    const pointsToCheck = type === 'threats' ? threats.value : opportunities.value
    
    pointsToCheck.forEach(point => {
        if (point.id !== targetPoint.id && point.impact === targetPoint.impact && point.probability === targetPoint.probability) {
            overlapping.push(point)
        }
    })
    
    return overlapping
}

const showTooltip = (event: MouseEvent, point: TrackedScoredRisk, pointId: string) => {
    if (draggedOpportunityPoint.value || draggedThreatPoint.value) return
    
    // Clear existing tooltips
    tooltips.value = []
    hoveredPoints.value.clear()
    
    // Find all overlapping points
    const overlapping = findOverlappingPoints(point, pointId.startsWith('opp') ? 'opportunities' : 'threats')
    
    // Determine if mouse is closer to the right side of the screen
    const isRightSide = event.clientX > window.innerWidth / 2
    
    // Tooltip width estimate (max-width: 300px + padding + border)
    const tooltipWidth = 320
    
    // Create tooltips for all overlapping points
    overlapping.forEach((p, index) => {
        const xOffset = isRightSide ? -(tooltipWidth + 10) : 10
        
        tooltips.value.push({
            x: event.clientX + xOffset,
            y: event.clientY + 10 + (index * 80), // Offset each tooltip
            title: p.title,
            description: p.description
        })
    })
}

const hideTooltip = () => {
    tooltips.value = []
    hoveredPoints.value.clear()
}

function fetchProject() {
    fetch(`/api/projects/${projectId}`, {
        method: 'GET',
        credentials: 'include',
    }).then(async (response) => {
        if (response.ok) {
            const data = await response.json()
            projectTitle.value = data.title || 'Untitled Project'
            projectDescription.value = data.description || 'No description available'
        } else {
            console.error('Failed to fetch project:', await response.text())
            router.push('/oops')
        }
    }).catch((error) => {
        console.error('Error fetching project:', error)
        router.push('/oops')
    })
}

function fetchRiskScores() {
    fetch(`/api/projects/${projectId}/gen/risks/scores`, {
        method: 'GET',
        credentials: 'include',
    }).then(async (response) => {
        if (response.ok) {
            const data: Array<TrackedScoredRisk> = await response.json()
            threats.value = data.filter(risk => risk.kind === 'threat')
            opportunities.value = data.filter(risk => risk.kind === 'opportunity')
        } else {
            console.error('Failed to fetch risk scores:', await response.text())
            router.push('/oops')
        }
    }).catch((error) => {
        console.error('Error fetching risk scores:', error)
        router.push('/oops')
    })
}

fetchProject()
fetchRiskScores()
</script>

<template>
    <div class="qualitative-analysis">
        <!-- Side Panel -->
        <ProjectAndRisksSidePanel 
            :project-title="projectTitle"
            :project-description="projectDescription"
            :threats="threats"
            :opportunities="opportunities"
        />

        <!-- Main Content -->
        <div class="border-wrapper">
            <div class="content-wrapper-wrapper">
                <!-- <h2 class="section-title gradient-text gradient-border-bottom">Qualitative Analysis</h2> -->
                <div class="content-wrapper">
                    <div class="graphs-container">
                        <!-- Opportunities Graph -->
                        <RiskGraph
                            type="opportunities"
                            :points="opportunities"
                            :risk-threshold="riskThreshold"
                            :dragged-point="draggedOpportunityPoint"
                            @mouse-down="handleOpportunityMouseDown"
                            @mouse-move="handleOpportunityMouseMove"
                            @mouse-up="handleMouseUp"
                            @show-tooltip="showTooltip"
                            @hide-tooltip="hideTooltip"
                        />
                        
                        <!-- Threats Graph -->
                        <RiskGraph
                            type="threats"
                            :points="threats"
                            :risk-threshold="riskThreshold"
                            :dragged-point="draggedThreatPoint"
                            @mouse-down="handleThreatMouseDown"
                            @mouse-move="handleThreatMouseMove"
                            @mouse-up="handleMouseUp"
                            @show-tooltip="showTooltip"
                            @hide-tooltip="hideTooltip"
                        />
                    </div>
                    
                    <!-- Risk Threshold Slider -->
                    <RiskThresholdSlider v-model="riskThreshold" />
                </div>
                
                <!-- Continue Section -->
                <div class="continue-section">
                    <p class="completion-message">Complete your risk assessment and move to the next phase.</p>
                    <button class="gradient-button large-button" @click="handleContinue">
                        Continue to Planning
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Tooltips -->
        <RiskTooltip
            v-for="(tooltip, index) in tooltips"
            :key="`tooltip-${index}`"
            :x="tooltip.x"
            :y="tooltip.y"
            :title="tooltip.title"
            :description="tooltip.description"
        />
    </div>
</template>

<style scoped>
.qualitative-analysis {
    display: flex;
    gap: 2rem;
    padding: 0;
    width: 100%;
    max-width: 100vw;
    height: 100vh;
    max-height: 100vh;
    background-color: var(--color-background);
    color: var(--color-text);
    transition: background-color 0.5s, color 0.5s;
    align-items: stretch;
    box-sizing: border-box;
    overflow: hidden;
}

.section-title {
    font-size: 2rem;
    font-weight: 700;
    text-align: center;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
}

.border-wrapper {
    flex: 1;
    min-width: 0;
    padding: 1rem 2rem 1rem 0;
    align-self: stretch;
    box-sizing: border-box;
}

.content-wrapper-wrapper {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
}

.content-wrapper {
    display: flex;
    gap: 1rem;
    overflow: hidden;
    flex: 1;
    min-height: 0;
}

.graphs-container {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    align-items: center;
    flex: 1;
    overflow: hidden;
    align-self: stretch;
    min-height: 0;
}

.continue-section {
    padding: 1.5rem;
    margin-top: 1rem;
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

@media (max-width: 1024px) {
    .content-wrapper {
        flex-direction: column;
    }
}

@media (max-width: 768px) {
    .qualitative-analysis {
        flex-direction: column-reverse;
        height: auto;
        max-height: none;
        gap: 1rem;
        overflow-y: auto;
    }

    .border-wrapper {
        padding: 1rem;
        padding-right: 1rem;
    }

    .content-wrapper-wrapper {
        height: auto;
        overflow: visible;
    }

    .content-wrapper {
        overflow: visible;
    }
    
    .graphs-container {
        flex-direction: column;
        overflow: visible;
    }
}
</style>