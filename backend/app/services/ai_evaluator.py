# backend/app/services/ai_evaluator.py

import json
import asyncio
from typing import List

import openai
from ..core.config import settings
from ..models.evaluation_models import LLMResponse

# Configure the OpenAI client
# In a real app, you might use different clients based on settings
if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "mock-api-key-for-local-dev":
    client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
else:
    client = None # Mock client behavior later

def build_evaluation_prompt(transcript: str, summary: str, parameters: List[str]) -> str:
    """
    Constructs a detailed prompt for the LLM to evaluate the summary.
    This is a critical step for getting reliable, structured output.
    """
    params_str = ", ".join(parameters)
    json_schema = f'{{"scores": {{ "{parameters[0]}": <score_1_to_10>, ... }}, "explanation": "<detailed_explanation>"}}'

    prompt = f"""
    You are an expert teaching assistant. Your task is to evaluate a student's summary of a given lecture transcript.

    Please evaluate the summary based on the following criteria: {params_str}.
    For each criterion, provide a score from 1 to 10, where 1 is poor and 10 is excellent.
    Also, provide a detailed, constructive explanation for your scores, highlighting strengths and areas for improvement.

    **Lecture Transcript:**
    ---BEGIN TRANSCRIPT---
    {transcript}
    ---END TRANSCRIPT---

    **Student's Summary:**
    ---BEGIN SUMMARY---
    {summary}
    ---END SUMMARY---

    **Instructions:**
    1. Read the transcript and summary carefully.
    2. Evaluate the summary against each of the requested criteria: {params_str}.
    3. Return your evaluation ONLY as a single, valid JSON object, without any markdown formatting or other text outside the JSON.
    4. The JSON object must have two keys: "scores" and "explanation".
    5. The "scores" key should map to an object where each key is a criterion string and the value is an integer score from 1 to 10.
    6. The "explanation" key should map to a string containing your detailed feedback.

    **Required JSON Format:**
    {json_schema}

    Begin your response now with the JSON object.
    """
    return prompt

async def evaluate_summary(transcript: str, summary: str, parameters: List[str]) -> LLMResponse:
    """
    Calls the LLM API to get an evaluation and parses the structured JSON response.
    Includes a mock response for development when no API key is provided.
    """
    if not client:
        # Mocked response for development without an API key
        await asyncio.sleep(1) # Simulate network latency
        mock_scores = {param: 8 for param in parameters}
        mock_explanation = "This is a mocked response. The summary effectively covers the main points from the transcript (Coverage: 8/10) and is written with good clarity (Clarity: 8/10). It could be slightly more concise (Conciseness: 8/10) by removing some redundant phrasing, but overall, it's a strong effort."
        return LLMResponse(scores=mock_scores, explanation=mock_explanation)

    prompt = build_evaluation_prompt(transcript, summary, parameters)

    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview", # A model that's good with JSON mode
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        response_content = response.choices[0].message.content
        if not response_content:
            raise ValueError("LLM returned an empty response.")

        # The model is instructed to return JSON, so we parse it directly.
        llm_json = json.loads(response_content)
        return LLMResponse(**llm_json)

    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode LLM response as JSON: {e}")
    except Exception as e:
        # Catch-all for API errors, etc.
        raise RuntimeError(f"Error calling OpenAI API: {e}")
