<script setup lang="ts">
import { ref } from 'vue'
import ProgressNav from './ProgressNav.vue'
import RiskGraph from './RiskGraph.vue'
import RiskThresholdSlider from './RiskThresholdSlider.vue'
import RiskTooltip from './RiskTooltip.vue'
import type { RiskPoint } from '../composables/useRiskCalculations'

interface DragState {
    index: number
    tempImpact: number
    tempProbability: number
}

// Risk threshold curve constant (impact * probability = k)
const riskThreshold = ref(0.1)

// Sample data - replace with actual data from props or API
const threats = ref<RiskPoint[]>([
    { id: '1', title: 'Budget Overrun', description: 'Project costs exceed allocated budget', impact: 8, probability: 6 },
    { id: '2', title: 'Schedule Delay', description: 'Timeline extends beyond deadline', impact: 6, probability: 7 },
    { id: '3', title: 'Resource Shortage', description: 'Key personnel unavailable', impact: 9, probability: 4 },
])

const opportunities = ref<RiskPoint[]>([
    { id: '4', title: 'Early Completion', description: 'Finish project ahead of schedule', impact: 6, probability: 4 },
    { id: '5', title: 'Cost Savings', description: 'Reduce expenses through optimization', impact: 8, probability: 6 },
    { id: '6', title: 'Quality Improvement', description: 'Exceed quality expectations', impact: 9, probability: 5 },
])

const draggedThreatPoint = ref<DragState | null>(null)
const draggedOpportunityPoint = ref<DragState | null>(null)

const tooltips = ref<Array<{
    x: number
    y: number
    title: string
    description: string
}>>([])

const hoveredPoints = ref<Set<string>>(new Set())

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

const findOverlappingPoints = (targetPoint: RiskPoint, type: 'threats' | 'opportunities'): RiskPoint[] => {
    const overlapping: RiskPoint[] = [targetPoint]
    
    // Only check within the same graph type
    const pointsToCheck = type === 'threats' ? threats.value : opportunities.value
    
    pointsToCheck.forEach(point => {
        if (point.id !== targetPoint.id && point.impact === targetPoint.impact && point.probability === targetPoint.probability) {
            overlapping.push(point)
        }
    })
    
    return overlapping
}

const showTooltip = (event: MouseEvent, point: RiskPoint, pointId: string) => {
    if (draggedOpportunityPoint.value || draggedThreatPoint.value) return
    
    // Clear existing tooltips
    tooltips.value = []
    hoveredPoints.value.clear()
    
    // Find all overlapping points
    const overlapping = findOverlappingPoints(point, pointId.startsWith('opp') ? 'opportunities' : 'threats')
    
    // Create tooltips for all overlapping points
    overlapping.forEach((p, index) => {
        tooltips.value.push({
            x: event.clientX + 10,
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
</script>

<template>
    <div class="qualitative-analysis">
        <div class="border-wrapper card gradient-border">
            <div class="content-wrapper-wrapper">
                <h2 class="section-title gradient-text gradient-border-bottom">Qualitative Analysis</h2>
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
        
        <ProgressNav :total="3" :completed="2" :previousEnabled="true" :nextEnabled="true"/>
    </div>
</template>

<style scoped>
.qualitative-analysis {
    padding: 1rem 2rem;
    width: 100%;
    max-width: 1200px;
    height: calc(100vh - 16rem);
    margin: 0 auto;
    background-color: var(--color-background);
    color: var(--color-text);
    transition: background-color 0.5s, color 0.5s;
}

.section-title {
    font-size: 2rem;
    font-weight: 700;
    text-align: center;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
}

.border-wrapper {
    height: 100%;
}

.content-wrapper-wrapper {
    display: flex;
    flex-direction: column;
    max-height: 100%;
}

.content-wrapper {
    display: flex;
    gap: 1rem;
    overflow: hidden;
    height: 100%;
}

.graphs-container {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    align-items: center;
    flex: 1;
    overflow: auto;
    align-self: stretch;
}

@media (max-width: 1024px) {
    .qualitative-analysis {
        max-width: 600px;
        height: fit-content;
    }
    
    .content-wrapper {
        flex-direction: column;
    }
    
    .graphs-container {
        flex-direction: column;
    }
}
</style>