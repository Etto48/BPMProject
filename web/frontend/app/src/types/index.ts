/**
 * Represents the kind/category of a risk in the project.
 */
export enum RiskKind {
  /** A potential threat or negative risk */
  Threat = 'threat',
  /** A potential opportunity or positive risk */
  Opportunity = 'opportunity'
}

export type Risk = {
  title: string
  kind: RiskKind
  description: string
}

export type RiskSuggestion = Risk & {
  accepted: boolean
}

export type UserData = {
  username: string
  password: string
}

export type UserResponse = {
  id: number
  username: string
}

export type Project = {
  title: string
  description: string
}

export type ProjectInDB = Project & {
  id: number
  riskScoreThreshold: number
  currentStep: number
}

export type TrackedScoredRisk = Risk & {
    id: number
    impact: number // 1-10
    probability: number // 1-10
}

/**
 * A unified type for displaying risks in side panels
 * Works with both RiskSuggestion (from risk discovery) and TrackedScoredRisk (from qualitative analysis)
 */
export type DisplayableRisk = {
  title: string
  kind: RiskKind
  description: string
}