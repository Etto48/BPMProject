GENERATE_RISKS = """\
Given the title and description of a project, generate an exhaustive list of potential risks associated with the project.
Each risk should have a kind: either 'threat' for risks that could negatively impact the project, or 'opportunity' for risks that could positively impact the project.
For each risk, provide a concise title (maximum 4-5 words) and a detailed description explaining what the risk entails and the context that causes it.
Respond in JSON format as a list of risks.
"""