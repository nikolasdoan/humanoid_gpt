from pydantic import BaseModel
from openai import OpenAI
import os 


client = OpenAI(api_key="k-proj-GKFp7rtvJBXawW416roTT3BlbkFJWkLC3REh4rxpmeQ2pkZj")

class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
        {"role": "user", "content": "how can I solve 8x + 7 = -23"}
    ],
    response_format=MathReasoning,
)

math_reasoning = completion.choices[0].message.parsed