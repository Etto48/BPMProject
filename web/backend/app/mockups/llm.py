from models import Project, Risk, Risks, TrackedManagedRisk, TrackedRisk, TrackedScoredRisk, generate_risk_score_model
from prompts import GENERATE_RISK_SCORES, GENERATE_RISKS
import random

class LLM:
    def __init__(self, url: str, model: str, api_key: str = ""):
        pass

    async def load_model(self):
        pass

    async def generate_risks(self, company_description: str, project: Project):
        return [
            Risk(
                title="Technological Advancement",
                kind="opportunity",
                description="Adopting cutting-edge technology may improve efficiency and provide a competitive edge.",
            ),
            Risk(
                title="Data Breach",
                kind="threat",
                description="Unauthorized access to sensitive data could lead to significant financial and reputational damage.",
            ),
            Risk(
                title="Project Delay",
                kind="threat",
                description="Delays in project timeline due to resource unavailability or unforeseen technical challenges.",
            ),
            Risk(
                title="Regulatory Compliance",
                kind="threat",
                description="Failure to comply with industry regulations may result in legal penalties and operational restrictions.",
            ),
            Risk(
                title="Market Opportunity",
                kind="opportunity",
                description="Entering a new market segment could lead to increased revenue and brand recognition.",
            )
        ]

    async def generate_risk_scores(self, company_description: str, project: Project, risks: list[TrackedRisk]):
        return [
            TrackedScoredRisk(
                id=risk.id,
                title=risk.title,
                kind=risk.kind,
                description=risk.description,
                impact=random.randint(1, 10),
                probability=random.randint(1, 10)
            ) for risk in risks
        ]
    
    async def generate_risk_mitigation_plan(self, company_description: str, project: Project, risks: list[TrackedScoredRisk]):
        risks_with_plans: list[TrackedManagedRisk] = []
        for risk in risks:
            risks_with_plans.append(
                TrackedManagedRisk(
                    **risk.model_dump(),
                    contingency=f"Contingency plan for {risk.title}: Allocate additional resources and adjust timelines, if necessary.",
                    fallback=f"Fallback plan for {risk.title}: Reassess project scope and seek expert consultation."
                )
            )
        return risks_with_plans