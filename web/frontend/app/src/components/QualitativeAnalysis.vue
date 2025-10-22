<template>
    <div class="qualitative-analysis">
        <div class="border-wrapper card gradient-border">
            <div class="content-wrapper-wrapper">
                <h2 class="section-title gradient-text gradient-border-bottom">Qualitative Analysis</h2>
                <div class="content-wrapper">
                    <div class="graphs-container">
                        <!-- Opportunities Graph -->
                        <div class="graph-wrapper">
                            <h3 class="opportunity-title">Opportunities</h3>
                            <svg
                            ref="opportunitiesGraph"
                            class="risk-graph"
                            viewBox="0 30 370 370"
                            @mousemove="handleMouseMove($event, 'opportunities')"
                            @mouseup="handleMouseUp"
                            @mouseleave="handleMouseUp"
                            >
                            <!-- Gradient Background -->
                            <defs>
                                <radialGradient id="opportunityGradient" cx="0%" cy="0%" r="141%">
                                    <stop offset="0%" class="opportunity-gradient-start" />
                                    <stop offset="100%" class="opportunity-gradient-end" />
                                </radialGradient>
                            </defs>
                            <rect x="50" y="50" width="300" height="300" fill="url(#opportunityGradient)" />
                            
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
                            <text x="20" y="200" text-anchor="middle" class="axis-label" transform="rotate(-90, 20, 200)">Probability</text>
                            
                            <!-- Scale markers -->
                            <text v-for="i in 10" :key="`x-${i}`" :x="50 + (i - 1) * 33.33" y="370" text-anchor="middle" class="scale-label">{{ 11 - i }}</text>
                            <text v-for="i in 10" :key="`y-${i}`" x="30" :y="355 - (i - 1) * 33.33" text-anchor="middle" class="scale-label">{{ i }}</text>
                            
                            <!-- Risk level curves (x*y=k) -->
                            <g class="risk-curves">
                                <path :d="generateHyperbolaFill(riskThreshold, true)" class="risk-curve-fill" />
                                <path :d="generateHyperbola(riskThreshold, true)" class="risk-curve" />
                            </g>
                            
                            <!-- Opportunity points -->
                            <g v-for="(opportunity, index) in opportunities" :key="`opportunity-${index}`">
                                <circle
                                :cx="draggedPoint?.type === 'opportunities' && draggedPoint?.index === index ? getXInverted(draggedPoint.tempImpact) : getXInverted(opportunity.impact)"
                                :cy="draggedPoint?.type === 'opportunities' && draggedPoint?.index === index ? getY(draggedPoint.tempProbability) : getY(opportunity.probability)"
                                r="8"
                                class="risk-point opportunity-point"
                                :class="{ dragging: draggedPoint?.type === 'opportunities' && draggedPoint?.index === index }"
                                @mousedown="handleMouseDown($event, 'opportunities', index)"
                                @mouseenter="showTooltip($event, opportunity, `opp-${index}`)"
                                @mouseleave="hideTooltip()"
                                />
                            </g>
                        </svg>
                    </div>
                    
                    <!-- Threats Graph -->
                    <div class="graph-wrapper">
                        <h3 class="threat-title">Threats</h3>
                        <svg
                        ref="threatsGraph"
                        class="risk-graph"
                        viewBox="30 30 370 370"
                        @mousemove="handleMouseMove($event, 'threats')"
                        @mouseup="handleMouseUp"
                        @mouseleave="handleMouseUp"
                        >
                        <!-- Gradient Background -->
                        <defs>
                            <radialGradient id="threatGradient" cx="100%" cy="0%" r="141%">
                                <stop offset="0%" class="threat-gradient-start" />
                                <stop offset="100%" class="threat-gradient-end" />
                            </radialGradient>
                        </defs>
                        <rect x="50" y="50" width="300" height="300" fill="url(#threatGradient)" />
                        
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
                        <text x="380" y="200" text-anchor="middle" class="axis-label" transform="rotate(90, 380, 200)">Probability</text>
                        
                        <!-- Scale markers -->
                        <text v-for="i in 10" :key="`x-${i}`" :x="50 + (i - 1) * 33.33" y="370" text-anchor="middle" class="scale-label">{{ i }}</text>
                        <text v-for="i in 10" :key="`y-${i}`" x="370" :y="355 - (i - 1) * 33.33" text-anchor="middle" class="scale-label">{{ i }}</text>
                        
                        <!-- Risk level curves (x*y=k) -->
                        <g class="risk-curves">
                            <path :d="generateHyperbolaFill(riskThreshold, false)" class="risk-curve-fill" />
                            <path :d="generateHyperbola(riskThreshold, false)" class="risk-curve" />
                        </g>
                        
                        <!-- Threat points -->
                        <g v-for="(threat, index) in threats" :key="`threat-${index}`">
                            <circle
                            :cx="draggedPoint?.type === 'threats' && draggedPoint?.index === index ? getX(draggedPoint.tempImpact) : getX(threat.impact)"
                            :cy="draggedPoint?.type === 'threats' && draggedPoint?.index === index ? getY(draggedPoint.tempProbability) : getY(threat.probability)"
                            r="8"
                            class="risk-point threat-point"
                            :class="{ dragging: draggedPoint?.type === 'threats' && draggedPoint?.index === index }"
                            @mousedown="handleMouseDown($event, 'threats', index)"
                            @mouseenter="showTooltip($event, threat, `threat-${index}`)"
                            @mouseleave="hideTooltip()"
                            />
                        </g>
                    </svg>
                </div>
            </div>
            
            
            <!-- Risk Threshold Slider -->
            <div class="threshold-control">
                <label for="risk-threshold">
                    <span class="threshold-label-text">Risk Threshold</span>
                    <span class="threshold-value">{{ (riskThreshold * 100).toFixed(0) }}%</span>
                </label>
                <div class="slider-wrapper">
                    <input 
                    id="risk-threshold"
                    type="range" 
                    v-model.number="riskThreshold" 
                    min="0" 
                    max="1" 
                    step="0.01"
                    class="threshold-slider"
                    />
                    <div class="threshold-labels">
                        <span>100%</span>
                        <span>75%</span>
                        <span>50%</span>
                        <span>25%</span>
                        <span>0%</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Tooltips -->
<div
v-for="(tooltip, index) in tooltips"
:key="`tooltip-${index}`"
class="tooltip"
:style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }"
>
<div class="tooltip-title">{{ tooltip.title }}</div>
<div class="tooltip-description">{{ tooltip.description }}</div>
</div>
</div>
<ProgressNav :total="5" :completed="4"/>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ProgressNav from './ProgressNav.vue'

interface RiskPoint {
    id: string
    title: string
    description: string
    impact: number // 1-10
    probability: number // 1-10
}

interface DragState {
    type: 'threats' | 'opportunities'
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

const draggedPoint = ref<DragState | null>(null)

const tooltips = ref<Array<{
    x: number
    y: number
    title: string
    description: string
}>>([])

const hoveredPoints = ref<Set<string>>(new Set())
    
    // Convert data values (1-10) to SVG coordinates
    const getX = (impact: number): number => {
        return 50 + ((impact - 1) / 9) * 300
    }
    
    const getXInverted = (impact: number): number => {
        return 350 - ((impact - 1) / 9) * 300
    }
    
    const getY = (probability: number): number => {
        return 350 - ((probability - 1) / 9) * 300
    }
    
    // Convert SVG coordinates back to data values (1-10)
    const getImpactFromX = (x: number): number => {
        const value = 1 + ((x - 50) / 300) * 9
        return Math.max(1, Math.min(10, value)) // Keep as float during drag
    }
    
    const getImpactFromXInverted = (x: number): number => {
        const value = 1 + ((350 - x) / 300) * 9
        return Math.max(1, Math.min(10, value)) // Keep as float during drag
    }
    
    const getProbabilityFromY = (y: number): number => {
        const value = 1 + ((350 - y) / 300) * 9
        return Math.max(1, Math.min(10, value)) // Keep as float during drag
    }
    
    // Generate hyperbola path for risk level curves (impact * probability = k)
    // k is expressed in normalized coordinates where impact and probability go from 0 to 1
    const generateHyperbola = (k: number, inverted: boolean): string => {
        const pointsMap = new Map<number, number>() // impact -> probability
        
        // Use a fine step size for smoother curves
        const step = 0.002
        
        // Sample from impact axis (fixed impact, calculate probability)
        for (let impactNorm = step; impactNorm <= 1; impactNorm += step) {
            const probabilityNorm = k / impactNorm
            
            // Only add if probability is within valid range
            if (probabilityNorm >= 0 && probabilityNorm <= 1) {
                pointsMap.set(impactNorm, probabilityNorm)
            }
        }
        
        // Sample from probability axis (fixed probability, calculate impact)
        for (let probabilityNorm = step; probabilityNorm <= 1; probabilityNorm += step) {
            const impactNorm = k / probabilityNorm
            
            // Only add if impact is within valid range
            if (impactNorm >= 0 && impactNorm <= 1) {
                pointsMap.set(impactNorm, probabilityNorm)
            }
        }
        
        // Sort points by impact and generate path
        const sortedPoints = Array.from(pointsMap.entries()).sort((a, b) => a[0] - b[0])
        
        const pathSegments: string[] = []
        sortedPoints.forEach(([impactNorm, probabilityNorm], index) => {
            // Convert normalized values (0-1) to actual values (1-10)
            const impact = 1 + impactNorm * 9
            const probability = 1 + probabilityNorm * 9
            
            const x = inverted ? getXInverted(impact) : getX(impact)
            const y = getY(probability)
            
            if (index === 0) {
                pathSegments.push(`M ${x} ${y}`)
            } else {
                pathSegments.push(`L ${x} ${y}`)
            }
        })
        
        return pathSegments.join(' ')
    }
    
    // Generate filled area under the hyperbola
    const generateHyperbolaFill = (k: number, inverted: boolean): string => {
        // Special case: if k >= 1, fill the entire graph
        if (k >= 1) {
            const x_1 = inverted ? getXInverted(1) : getX(1)
            const x_10 = inverted ? getXInverted(10) : getX(10)
            const y_1 = getY(1)
            const y_10 = getY(10)
            return `M ${x_1} ${y_1} L ${x_10} ${y_1} L ${x_10} ${y_10} L ${x_1} ${y_10} Z`
        }
        
        const pointsMap = new Map<number, number>() // impact -> probability
        
        // Use a fine step size for smoother curves
        const step = 0.002
        
        // Sample from impact axis (fixed impact, calculate probability)
        for (let impactNorm = step; impactNorm <= 1; impactNorm += step) {
            const probabilityNorm = k / impactNorm
            
            // Only add if probability is within valid range
            if (probabilityNorm >= 0 && probabilityNorm <= 1) {
                pointsMap.set(impactNorm, probabilityNorm)
            }
        }
        
        // Sample from probability axis (fixed probability, calculate impact)
        for (let probabilityNorm = step; probabilityNorm <= 1; probabilityNorm += step) {
            const impactNorm = k / probabilityNorm
            
            // Only add if impact is within valid range
            if (impactNorm >= 0 && impactNorm <= 1) {
                pointsMap.set(impactNorm, probabilityNorm)
            }
        }
        
        // Sort points by impact
        const sortedPoints = Array.from(pointsMap.entries()).sort((a, b) => a[0] - b[0])
        
        if (sortedPoints.length === 0) return ''
        
        const pathSegments: string[] = []
        
        // Define corner coordinates
        const x_1 = inverted ? getXInverted(1) : getX(1)
        const x_10 = inverted ? getXInverted(10) : getX(10)
        const y_1 = getY(1)
        const y_10 = getY(10)
        
        // Start at (1,1)
        pathSegments.push(`M ${x_1} ${y_1}`)
        
        // Get first point on curve
        const firstPoint = sortedPoints[0]
        if (!firstPoint) return ''
        
        // If curve doesn't start at impact=1, draw along bottom to curve start
        pathSegments.push(`L ${x_1} ${y_10}`)
        
        
        // Draw the hyperbola curve
        sortedPoints.forEach(([impactNorm, probabilityNorm]) => {
            const impact = 1 + impactNorm * 9
            const probability = 1 + probabilityNorm * 9
            
            const x = inverted ? getXInverted(impact) : getX(impact)
            const y = getY(probability)
            
            pathSegments.push(`L ${x} ${y}`)
        })
        
        // Get last point on curve
        const lastPoint = sortedPoints[sortedPoints.length - 1]
        if (!lastPoint) return ''
        
        const lastImpact = 1 + lastPoint[0] * 9
        const lastProbability = 1 + lastPoint[1] * 9
        
        // From curve end, complete the polygon with only the corners below/left of the curve
        // Path: curve end → horizontally to edge if needed → down to (?,1) → along bottom to (1,1) → up to (1,?) → close
        
        // If curve doesn't end at impact=10, go horizontally to right/left edge
        if (lastImpact < 9.99) {
            const lastY = getY(lastProbability)
            pathSegments.push(`L ${x_10} ${lastY}`)
        }
        
        // Go down to corner (10,1)
        pathSegments.push(`L ${x_10} ${y_1}`)
        
        // Close path back to (1,1) - SVG will automatically draw the line
        pathSegments.push(`Z`)
        
        return pathSegments.join(' ')
    }
    
    const handleMouseDown = (event: MouseEvent, type: 'threats' | 'opportunities', index: number) => {
        event.preventDefault()
        const dataArray = type === 'threats' ? threats.value : opportunities.value
        const point = dataArray[index]
        if (!point) return
        draggedPoint.value = { 
            type, 
            index,
            tempImpact: point.impact,
            tempProbability: point.probability
        }
        tooltips.value = []
        hoveredPoints.value.clear()
    }
    
    const handleMouseMove = (event: MouseEvent, type: 'threats' | 'opportunities') => {
        if (!draggedPoint.value || draggedPoint.value.type !== type) return
        
        const svg = event.currentTarget as SVGSVGElement
        const pt = svg.createSVGPoint()
        pt.x = event.clientX
        pt.y = event.clientY
        const svgP = pt.matrixTransform(svg.getScreenCTM()?.inverse())
        
        const impact = type === 'opportunities' ? getImpactFromXInverted(svgP.x) : getImpactFromX(svgP.x)
        const probability = getProbabilityFromY(svgP.y)
        
        // Update temporary float values for smooth dragging
        draggedPoint.value.tempImpact = impact
        draggedPoint.value.tempProbability = probability
    }
    
    const handleMouseUp = () => {
        if (draggedPoint.value) {
            // Snap to integer values when drag ends
            const dataArray = draggedPoint.value.type === 'threats' ? threats.value : opportunities.value
            const point = dataArray[draggedPoint.value.index]
            if (point) {
                point.impact = Math.round(draggedPoint.value.tempImpact)
                point.probability = Math.round(draggedPoint.value.tempProbability)
            }
        }
        draggedPoint.value = null
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
        if (draggedPoint.value) return
        
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

.tooltip {
    position: fixed;
    background: var(--color-background-mute);
    color: var(--color-text-opaque);
    padding: 0.75rem 1rem;
    border-radius: 6px;
    border: 1px solid var(--color-border);
    pointer-events: none;
    z-index: 1000;
    max-width: 300px;
    box-shadow: 0 4px 12px var(--shadow-color);
}

.tooltip-title {
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.25rem;
    color: var(--color-heading);
}

.tooltip-description {
    font-size: 0.875rem;
    color: var(--color-text-dim-opaque);
}

.threshold-control {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1rem 0 1rem 1rem;
    border-left: 1px solid var(--color-border);
    position: relative;
    align-self: stretch;
    box-sizing: border-box;
}

.slider-wrapper {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
    height: 100%;
}

.threshold-control label {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--color-heading);
    text-align: center;
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    margin-bottom: 1rem;
}

.threshold-label-text {
    white-space: nowrap;
}

.threshold-value {
    font-size: 1.1rem;
    color: var(--color-accent-1);
}

.threshold-slider {
    width: 6px;
    max-height: calc(100vh - 28rem);
    border-radius: 3px;
    background: var(--color-border);
    outline: none;
    -webkit-appearance: slider-vertical;
    appearance: auto;
    writing-mode: vertical-lr;
    direction: rtl;
    cursor: pointer;
}

.threshold-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: var(--color-accent-1);
    cursor: pointer;
    transition: all 0.2s ease;
}

.threshold-slider::-webkit-slider-thumb:hover,
.threshold-slider::-webkit-slider-thumb:active {
    background: var(--color-accent-2);
    transform: scale(1.1);
}

.threshold-slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: var(--color-accent-1);
    cursor: pointer;
    border: none;
    transition: all 0.2s ease;
}

.threshold-slider::-moz-range-thumb:hover,
.threshold-slider::-moz-range-thumb:active {
    background: var(--color-accent-2);
    transform: scale(1.1);
}

.threshold-labels {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    margin-top: 0;
    margin-left: 0;
    font-size: 0.875rem;
    color: var(--color-text-dim-opaque);
}

@media (max-width: 1024px) {
    
    .qualitative-analysis {
        max-width: 600px;
    }
    
    .content-wrapper {
        flex-direction: column;
    }
    
    .graphs-container {
        flex-direction: column;
    }
    
    .graph-wrapper {
        min-width: unset;
        max-width: unset;
        width: 100%;
    }
    
    .threshold-control {
        flex-direction: row;
        border-left: none;
        border-top: 1px solid var(--color-border);
        padding: 1rem 1rem 0 1rem;
        height: fit-content;
        align-items: center;
        justify-content: center;
    }
    
    .threshold-control label {
        writing-mode: horizontal-tb;
        transform: rotate(0deg);
        margin-bottom: 0;
        margin-right: 1rem;
        height: fit-content;
    }
    
    .slider-wrapper {
        flex-direction: column;
        align-items: center;
        width: 100%;
        height: fit-content;
    }
    
    .threshold-labels {
        flex-direction: row;
        justify-content: space-between;
        width: 100%;
        height: fit-content;
    }
    
    .threshold-slider {
        width: 100%;
        height: 6px;
        -webkit-appearance: slider-horizontal;
        appearance: auto;
        writing-mode: horizontal-tb;
        direction: ltr;
        cursor: pointer;
    }
}
</style>