import os
import json
import logging
from pydantic import BaseModel, Field
from typing import List, Optional

class ComparableProperty(BaseModel):
    address: str = Field(description="Full street address of the comparable sold property")
    sale_price: float = Field(description="Final recorded sale price in USD")
    sale_date: str = Field(description="Approximate sale date or timeframe (e.g., 'Jan 2026' or '2 months ago')")
    beds: int = Field(description="Number of bedrooms")
    baths: float = Field(description="Number of bathrooms")
    sqft: int = Field(description="Living square footage")
    distance_miles: float = Field(description="Estimated distance from subject property in miles")
    price_per_sqft: float = Field(description="Sale price divided by square footage")
    selection_rationale: str = Field(
        description="Detailed explanation of WHY this property was selected as a comp."
    )

class CompAnalysisResult(BaseModel):
    subject_address: str
    estimated_arv: float = Field(description="Calculated After Repair Value (ARV) based on comp analysis")
    arv_price_per_sqft: float = Field(description="Average or adjusted price per square foot across selected comps")
    comps: List[ComparableProperty] = Field(description="List of selected comparable sales with rationales")
    valuation_summary: str = Field(description="Brief summary of how the final ARV was determined")

def get_llm_response(prompt: str, system_prompt: str, config) -> Optional[dict]:
    """
    Universal LLM provider adapter. Automatically routes requests through Anthropic SDK, 
    OpenRouter, or OpenAI-compatible endpoints depending on the active agent environment.
    """
    anthropic_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_TOKEN") or getattr(config, "ANTHROPIC_API_KEY", None)
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY") or getattr(config, "OPENAI_API_KEY", None)
    base_url = os.getenv("OPENAI_BASE_URL") or getattr(config, "OPENAI_BASE_URL", None)
    
    provider = getattr(config, "PROVIDER", "auto").lower()

    # Path A: Native Anthropic API SDK (Claude Haiku direct)
    if provider == "anthropic" or (provider == "auto" and anthropic_key and not openai_key):
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=anthropic_key)
            model = getattr(config, "MODEL_NAME", "claude-3-5-haiku-20241022")
            
            # Use Tool Choice schema for structured output extraction
            tools = [{
                "name": "record_comp_analysis",
                "description": "Records structured comparable market analysis results.",
                "input_schema": CompAnalysisResult.model_json_schema()
            }]

            response = client.messages.create(
                model=model,
                max_tokens=2500,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}],
                tools=tools,
                tool_choice={"type": "tool", "name": "record_comp_analysis"}
            )
            
            for content in response.content:
                if content.type == "tool_use" and content.name == "record_comp_analysis":
                    return content.input

        except Exception as e:
            logging.error(f"Anthropic SDK execution error: {e}")

    # Path B: OpenAI-Compatible Endpoint (OpenRouter, Hermes Gateway API, or OpenAI)
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=openai_key or anthropic_key or "agent-stack-key",
            base_url=base_url
        )
        model = getattr(config, "MODEL_NAME", "claude-3-5-haiku-20241022")

        # Try structured Pydantic parsing first
        try:
            response = client.beta.chat.completions.parse(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                response_format=CompAnalysisResult
            )
            return response.choices[0].message.parsed.model_dump()
        except Exception:
            # Fallback to standard JSON completion parsing
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt + "\nReturn ONLY a valid raw JSON object matching the requested schema."},
                    {"role": "user", "content": prompt}
                ]
            )
            raw_content = response.choices[0].message.content
            # Clean JSON codeblock wrappers if present
            if "```json" in raw_content:
                raw_content = raw_content.split("```json")[1].split("```")[0].strip()
            return json.loads(raw_content)

    except Exception as e:
        logging.error(f"OpenAI-compatible endpoint execution error: {e}")

    return None

def find_comps_with_ai(subject_property: dict, config) -> Optional[CompAnalysisResult]:
    address = subject_property.get("address", "Unknown Address")
    zip_code = subject_property.get("zip_code", "")
    beds = subject_property.get("beds", "N/A")
    baths = subject_property.get("baths", "N/A")
    sqft = subject_property.get("sqft", "N/A")
    property_type = subject_property.get("property_type", "Single Family")
    year_built = subject_property.get("year_built", "N/A")

    system_prompt = "You are an expert real estate appraisal agent using real-time market data to identify comparable sold properties."
    
    prompt = f"""
    Find 3 to 4 recently sold comparable properties ("comps") for the following subject property:

    - Address: {address}, {zip_code}
    - Property Type: {property_type}
    - Beds: {beds} | Baths: {baths} | SqFt: {sqft} | Year Built: {year_built}

    Requirements:
    1. Look for properties sold within the last {config.MAX_SALE_AGE_MONTHS} months within roughly {config.MAX_SEARCH_RADIUS_MILES} mile(s).
    2. Prioritize properties with similar bed/bath counts, square footage (within +/- 20%), and property type.
    3. For EACH comp, explain explicitly WHY it was selected (selection_rationale), detailing physical similarities, distance, and time of sale.
    4. Calculate a realistic After Repair Value (ARV) based on the comps' price per square foot applied to the subject property's square footage ({sqft} sqft).
    """

    data_dict = get_llm_response(prompt, system_prompt, config)
    if data_dict:
        try:
            return CompAnalysisResult(**data_dict)
        except Exception as e:
            logging.error(f"Error instantiating CompAnalysisResult from payload: {e}")
            return None
    return None
