GENERATE_RISKS = """\
Given the title and description of a project, generate an exhaustive list of potential risks
associated with the project.
A risk is defined as any uncertain event or condition that, if it occurs, could have a positive
or negative effect on the project's objectives.
Each risk should have a kind: either 'threat' for risks that could negatively impact the
project, or 'opportunity' for risks that could positively impact the project.
For each risk, provide a concise title (maximum 4-5 words) and a description explaining what
the risk entails and the context that causes it.
Try to find around 10 risks but no more than 15.
Respond in JSON format as a list of risks.
"""

GENERATE_RISK_SCORES = """\
Given the title and description of a project, along with a list of identified risks, generate an
impact and probability score for each risk.
The impact score should be a number between 1 and 10 indicating the potential monetary impact of
the risk on the project.
The probability score should be a number between 1 and 10 indicating the likelihood of the risk
occurring.
Respond in JSON format with each risk's impact and probability scores.
"""

GENERATE_RISK_MITIGATION_PLAN_OPPORTUNITY = """\
Given the title and description of a project, along with a specific opportunity including its title,
description, impact score (1 means negligible, 10 means very profitable), and probability score
(1 means very unlikely, 10 means very likely), generate a contingency plan and/or a fallback plan
to manage the opportunity.
The contingency plan should outline the steps to be taken before the opportunity occurs.
The fallback plan should outline the steps to be taken if the opportunity materializes.
The contingency or fallback plans should follow one of these 5 strategies:
1. Exploit: Take actions to ensure the opportunity is realized.
2. Escalate: If the opportunity is beyond the project scope/control, escalate it to higher management.
3. Share: Collaborate with a third party to increase the chance of the opportunity occurring.
4. Enhance: Increase the probability and/or impact of the opportunity.
5. Accept: Acknowledge the opportunity but take no proactive action (leave the plan empty).

If you don't use "Accept", make sure to provide at least one of the plans.
A plan should be explained with one or more plain text conversational sentences.
Avoid titles, markdown formatting, html, or bullet points.
Do not mention directly what strategy you are using.
Respond in JSON format with the contingency and/or fallback plan.
"""

GENERATE_RISK_MITIGATION_PLAN_THREAT = """\
Given the title and description of a project, along with a specific threat including its title,
description, impact score (1 means negligible, 10 means catastrophic), and probability score
(1 means very unlikely, 10 means very likely), generate a contingency plan and/or a fallback plan
to manage the threat.
The contingency plan should outline the steps to be taken before the threat occurs.
The fallback plan should outline the steps to be taken if the threat materializes.
The contingency or fallback plans should follow one of these 5 strategies:
1. Avoid: Change the project plan to eliminate the threat or protect the project objectives from its impact.
2. Escalate: If the threat is beyond the project scope/control, escalate it to higher management.
3. Transfer: Shift the impact of the threat to a third party (e.g., through insurance or outsourcing).
4. Mitigate: Reduce the probability and/or impact of the threat.
5. Accept: Acknowledge the threat but take no proactive action (leave the plan empty).

If you don't use "Accept", make sure to provide at least one of the plans.
A plan should be explained with one or more plain text conversational sentences.
Avoid titles, markdown formatting, html, or bullet points.
Do not mention directly what strategy you are using.
Respond in JSON format with the contingency and/or fallback plan.
"""
