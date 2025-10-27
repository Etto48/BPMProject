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
  companyDescription: string
}

export type UserUpdateData = {
  username: string
  password?: string
  newPassword?: string
  companyDescription: string
}

export type DeleteUserData = {
  password: string
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

export type QualitativeAnalysisData = {
  riskScoreThreshold: number
  risks: Array<TrackedScoredRisk>
}

export type TrackedManagedRisk = TrackedScoredRisk & {
  contingency: string,
  fallback: string
} 

/**
 * A unified type for displaying risks in side panels
 */
export type DisplayableRisk = {
  title: string
  kind: RiskKind
  description: string
  impact?: number
  probability?: number
  contingency?: string
  fallback?: string
}