/**
 * Composable for risk graph coordinate calculations and hyperbola generation
 */

export interface RiskPoint {
    id: string
    title: string
    description: string
    impact: number // 1-10
    probability: number // 1-10
}

/**
 * Convert data values (1-10) to SVG coordinates
 */
export const getX = (impact: number): number => {
    return 50 + ((impact - 1) / 9) * 300
}

/**
 * Convert data values (1-10) to SVG coordinates (inverted for opportunities)
 */
export const getXInverted = (impact: number): number => {
    return 350 - ((impact - 1) / 9) * 300
}

/**
 * Convert probability values (1-10) to SVG Y coordinates
 */
export const getY = (probability: number): number => {
    return 350 - ((probability - 1) / 9) * 300
}

/**
 * Convert SVG X coordinates back to data values (1-10)
 */
export const getImpactFromX = (x: number): number => {
    const value = 1 + ((x - 50) / 300) * 9
    return Math.max(1, Math.min(10, value))
}

/**
 * Convert SVG X coordinates back to data values (1-10) - inverted
 */
export const getImpactFromXInverted = (x: number): number => {
    const value = 1 + ((350 - x) / 300) * 9
    return Math.max(1, Math.min(10, value))
}

/**
 * Convert SVG Y coordinates back to probability values (1-10)
 */
export const getProbabilityFromY = (y: number): number => {
    const value = 1 + ((350 - y) / 300) * 9
    return Math.max(1, Math.min(10, value))
}

/**
 * Generate hyperbola path for risk level curves (impact * probability = k)
 * k is expressed in normalized coordinates where impact and probability go from 0 to 1
 */
export const generateHyperbola = (k: number, inverted: boolean): string => {
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

/**
 * Generate filled area under the hyperbola
 */
export const generateHyperbolaFill = (k: number, inverted: boolean): string => {
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
