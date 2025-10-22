<template>
    <div class="graph-wrapper">
        <h3 :class="type === 'opportunities' ? 'opportunity-title' : 'threat-title'">
            {{ type === 'opportunities' ? 'Opportunities' : 'Threats' }}
        </h3>
        <svg
            :ref="type === 'opportunities' ? 'opportunitiesGraph' : 'threatsGraph'"
            class="risk-graph"
            :viewBox="type === 'opportunities' ? '0 30 370 370' : '30 30 370 370'"
            @mousemove="handleMouseMove"
            @mouseup="handleMouseUp"
            @mouseleave="handleMouseUp"
        >
            <!-- Gradient Background -->
            <defs>
                <radialGradient 
                    :id="`${type}Gradient`" 
                    :cx="type === 'opportunities' ? '0%' : '100%'" 
                    cy="0%" 
                    r="141%"
                >
                    <stop offset="0%" :class="type === 'opportunities' ? 'opportunity-gradient-start' : 'threat-gradient-start'" />
                    <stop offset="100%" :class="type === 'opportunities' ? 'opportunity-gradient-end' : 'threat-gradient-end'" />
                </radialGradient>
            </defs>
            <rect x="50" y="50" width="300" height="300" :fill="`url(#${type}Gradient)`" />
            
            <!-- Grid -->
            <g class="grid">
                <line x1="50" y1="50" x2="50" y2="350" class="grid-axis" stroke-width="2" />
                <line x1="50" y1="350" x2="350" y2="350" class="grid-axis" stroke-width="2" />
                <!-- Grid lines -->
                <line v-for="i in 9" :key="`h-${i}`" x1="50" :y1="50 + i * 33.33" x2="350" :y2="50 + i * 33.33" class="grid-line" stroke-width="1" />
                <line v-for="i in 9" :key="`v-${i}`" :x1="50 + i * 33.33" y1="50" :x2="50 + i * 33.33" y2="350" class="grid-line" stroke-width="1" />
            </g>
            
            <!-- Axis labels -->
            <text x="200" y="390" text-anchor="middle" class="axis-label">Impact</text>
            <text 
                :x="type === 'opportunities' ? 20 : 380" 
                y="200" 
                text-anchor="middle" 
                class="axis-label" 
                :transform="type === 'opportunities' ? 'rotate(-90, 20, 200)' : 'rotate(90, 380, 200)'"
            >
                Probability
            </text>
            
            <!-- Scale markers -->
            <template v-if="type === 'opportunities'">
                <text v-for="i in 10" :key="`x-${i}`" :x="50 + (i - 1) * 33.33" y="370" text-anchor="middle" class="scale-label">{{ 11 - i }}</text>
                <text v-for="i in 10" :key="`y-${i}`" x="30" :y="355 - (i - 1) * 33.33" text-anchor="middle" class="scale-label">{{ i }}</text>
            </template>
            <template v-else>
                <text v-for="i in 10" :key="`x-${i}`" :x="50 + (i - 1) * 33.33" y="370" text-anchor="middle" class="scale-label">{{ i }}</text>
                <text v-for="i in 10" :key="`y-${i}`" x="370" :y="355 - (i - 1) * 33.33" text-anchor="middle" class="scale-label">{{ i }}</text>
            </template>
            
            <!-- Risk level curves (x*y=k) -->
            <g class="risk-curves">
                <path :d="hyperbolaFillPath" class="risk-curve-fill" />
                <path :d="hyperbolaPath" class="risk-curve" />
            </g>
            
            <!-- Risk points -->
            <g v-for="(point, index) in points" :key="`${type}-${index}`">
                <circle
                    :cx="getPointX(point, index)"
                    :cy="getPointY(point, index)"
                    r="8"
                    class="risk-point"
                    :class="[
                        type === 'opportunities' ? 'opportunity-point' : 'threat-point',
                        { dragging: isDragging(index) }
                    ]"
                    @mousedown="handleMouseDown($event, index)"
                    @mouseenter="handleMouseEnter($event, point, index)"
                    @mouseleave="emit('hideTooltip')"
                />
            </g>
        </svg>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { RiskPoint } from '../composables/useRiskCalculations'
import { 
    getX, 
    getXInverted, 
    getY,
    getImpactFromX,
    getImpactFromXInverted,
    getProbabilityFromY,
    generateHyperbola,
    generateHyperbolaFill
} from '../composables/useRiskCalculations'

interface DragState {
    index: number
    tempImpact: number
    tempProbability: number
}

const props = defineProps<{
    type: 'threats' | 'opportunities'
    points: RiskPoint[]
    riskThreshold: number
    draggedPoint: DragState | null
}>()

const emit = defineEmits<{
    (e: 'mouseDown', index: number): void
    (e: 'mouseMove', impact: number, probability: number): void
    (e: 'mouseUp'): void
    (e: 'showTooltip', event: MouseEvent, point: RiskPoint, pointId: string): void
    (e: 'hideTooltip'): void
}>()

const isInverted = computed(() => props.type === 'opportunities')

const hyperbolaPath = computed(() => 
    generateHyperbola(props.riskThreshold, isInverted.value)
)

const hyperbolaFillPath = computed(() => 
    generateHyperbolaFill(props.riskThreshold, isInverted.value)
)

const getPointX = (point: RiskPoint, index: number): number => {
    if (props.draggedPoint && props.draggedPoint.index === index) {
        return isInverted.value 
            ? getXInverted(props.draggedPoint.tempImpact) 
            : getX(props.draggedPoint.tempImpact)
    }
    return isInverted.value ? getXInverted(point.impact) : getX(point.impact)
}

const getPointY = (point: RiskPoint, index: number): number => {
    if (props.draggedPoint && props.draggedPoint.index === index) {
        return getY(props.draggedPoint.tempProbability)
    }
    return getY(point.probability)
}

const isDragging = (index: number): boolean => {
    return props.draggedPoint !== null && props.draggedPoint.index === index
}

const handleMouseDown = (event: MouseEvent, index: number) => {
    event.preventDefault()
    emit('mouseDown', index)
}

const handleMouseMove = (event: MouseEvent) => {
    if (!props.draggedPoint) return
    
    const svg = event.currentTarget as SVGSVGElement
    const pt = svg.createSVGPoint()
    pt.x = event.clientX
    pt.y = event.clientY
    const svgP = pt.matrixTransform(svg.getScreenCTM()?.inverse())
    
    const impact = isInverted.value ? getImpactFromXInverted(svgP.x) : getImpactFromX(svgP.x)
    const probability = getProbabilityFromY(svgP.y)
    
    emit('mouseMove', impact, probability)
}

const handleMouseUp = () => {
    emit('mouseUp')
}

const handleMouseEnter = (event: MouseEvent, point: RiskPoint, index: number) => {
    emit('showTooltip', event, point, `${props.type.slice(0, 3)}-${index}`)
}
</script>

<style scoped>
.graph-wrapper {
    flex: 1;
    max-width: 50%;
    display: flex;
    flex-direction: column;
    height: fit-content;
    height: 100%;
}

.graph-wrapper h3 {
    text-align: center;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.opportunity-title {
    color: var(--color-opportunity);
}

.threat-title {
    color: var(--color-threat);
}

.risk-graph {
    width: 100%;
    height: 100%;
    max-height: 100%;
    border-radius: 8px;
    cursor: default;
    object-fit: contain;
}

.axis-label {
    font-size: 14px;
    font-weight: 600;
    fill: var(--color-text-opaque);
}

.scale-label {
    font-size: 12px;
    fill: var(--color-text-dim-opaque);
}

.grid-axis {
    stroke: var(--color-border-hover);
}

.grid-line {
    stroke: var(--color-border);
}

.risk-point {
    cursor: move;
    transition: all 0.2s ease;
}

.threat-point {
    fill: var(--color-threat);
    stroke: var(--color-threat-hover);
    stroke-width: 2;
}

.threat-point:hover {
    fill: var(--color-threat-hover);
    r: 10;
}

.opportunity-point {
    fill: var(--color-opportunity);
    stroke: var(--color-opportunity-hover);
    stroke-width: 2;
}

.opportunity-point:hover {
    fill: var(--color-opportunity-hover);
    r: 10;
}

.risk-point.dragging {
    r: 10;
    opacity: 0.7;
}

.opportunity-gradient-start {
    stop-color: var(--color-opportunity);
    stop-opacity: 0.3;
}

.opportunity-gradient-end {
    stop-color: var(--color-background-mute);
    stop-opacity: 0.3;
}

.threat-gradient-start {
    stop-color: var(--color-threat);
    stop-opacity: 0.3;
}

.threat-gradient-end {
    stop-color: var(--color-background-mute);
    stop-opacity: 0.3;
}

.risk-curve {
    fill: none;
    stroke: var(--color-background);
    stroke-width: 1.5;
    opacity: 1;
}

.risk-curve-fill {
    fill: var(--color-background);
    opacity: 0.6;
    stroke: none;
}

@media (max-width: 1024px) {
    .graph-wrapper {
        min-width: unset;
        max-width: unset;
        width: 100%;
    }
}
</style>
