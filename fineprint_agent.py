# fineprint_agent.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("CLOUDRIFT_API_KEY"),
    base_url="https://inference.cloudrift.ai/v1"
)

def analyze_fine_print(fineprint_text: str) -> str:
    prompt = f"""
You are a policy watchdog. Analyze this fine print and return ONLY this JSON:

{{
  "context": "Brief summary of the fine print in 1-2 sentences.",
  "red_flags": ["Short bullet points of any concerning terms (max 3)."],
  "recommendations": ["Helpful advice for the user based on the red flags (max 3)."]
}}

Rules:
- JSON must be valid and complete.
- Each item must be under 15 words.
- Return ONLY JSON, no commentary or explanation.

Fine print:
\"\"\"
{fineprint_text}
\"\"\"
"""

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content
