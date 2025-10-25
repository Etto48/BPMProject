import asyncio
import openai

from models import ContingencyAndFallback, Project, Risks, TrackedManagedRisk, TrackedRisk, TrackedScoredRisk, generate_risk_score_model
from prompts import GENERATE_RISK_MITIGATION_PLAN_OPPORTUNITY, GENERATE_RISK_MITIGATION_PLAN_THREAT, GENERATE_RISK_SCORES, GENERATE_RISKS

class LLM:
    def __init__(self, url: str, model: str, api_key: str = ""):
        self.url = url
        self.api_key = api_key
        self.model = model
        self.client = openai.AsyncClient(base_url=self.url, api_key=self.api_key)

    async def load_model(self):
        _response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "user",
                "content": "Load model"
            }],
            max_completion_tokens=0
        )
        return

    async def generate_risks(self, project: Project):
        response = await self.client.chat.completions.parse(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": GENERATE_RISKS
                },
                {
                    "role": "user",
                    "content": f"Project Title: \"{project.title}\"\nProject Description: \"{project.description}\""
                },
            ],
            response_format=Risks
        )

        return response.choices[0].message.parsed.root

    async def generate_risk_scores(self, project: Project, risks: list[TrackedRisk]):
        risk_str = ""
        for risk in risks:
            risk_str += f"- ID: {risk.id}, Title: \"{risk.title}\", Description: \"{risk.description}\"\n"

        response = await self.client.chat.completions.parse(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": GENERATE_RISK_SCORES
                },
                {
                    "role": "user",
                    "content": f"Project Title: \"{project.title}\"\nProject Description: \"{project.description}\"\nRisks: \n{risk_str}"
                },
            ],
            response_format=generate_risk_score_model(risks)
        )

        scores = response.choices[0].message.parsed.model_dump()
        ret = []
        for risk in risks:
            ts_risk = TrackedScoredRisk(
                **risk.model_dump(),
                **scores[f"risk_{risk.id}"]
            )
            ret.append(ts_risk)
        return ret
    
    async def generate_risk_mitigation_plan(self, project: Project, risks: list[TrackedScoredRisk]):
        responses = await asyncio.gather(*[
            self.client.chat.completions.parse(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": GENERATE_RISK_MITIGATION_PLAN_OPPORTUNITY if risk.kind == "opportunity" else GENERATE_RISK_MITIGATION_PLAN_THREAT
                    },
                    {
                        "role": "user",
                        "content": f"Project Title: \"{project.title}\"\nProject Description: \"{project.description}\"\n{risk.kind.capitalize()} Title: \"{risk.title}\"\n{risk.kind.capitalize()} Description: \"{risk.description}\"\nImpact Score: {risk.impact}\nProbability Score: {risk.probability}"
                    }
                ],
                response_format=ContingencyAndFallback
            ) for risk in risks
        ])

        ret = []
        for risk, response in zip(risks, responses):
            plan = response.choices[0].message.parsed
            tm_risk = TrackedManagedRisk(
                **risk.model_dump(),
                **plan.model_dump()
            )
            ret.append(tm_risk)
        return ret