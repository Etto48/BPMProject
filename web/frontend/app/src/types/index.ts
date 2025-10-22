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