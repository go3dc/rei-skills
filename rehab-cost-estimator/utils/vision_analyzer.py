import json
import logging
from openai import OpenAI

def analyze_property_photos(api_key, model_name, image_urls, max_photos):
    """
    Sends property image URLs to a multimodal vision AI model to identify 
    visual distress, interior condition, and required rehab scope.
    """
    if not image_urls:
        return {"rehab_level": "unknown", "detected_items": [], "confidence": "low"}

    client = OpenAI(api_key=api_key)
    sample_urls = image_urls[:max_photos]
    
    # Construct vision API prompt with structured JSON response instructions
    content_payload = [
        {
            "type": "text",
            "text": (
                "You are an expert real estate general contractor. Inspect these property listing photos "
                "and identify necessary renovation items. Evaluate the overall interior and exterior condition.\n"
                "Return ONLY a valid JSON object matching this exact structure:\n"
                "{\n"
                '  "rehab_level": "light" | "medium" | "heavy" | "full_gut",\n'
                '  "needs_kitchen": true/false,\n'
                '  "needs_bathrooms": true/false,\n'
                '  "needs_flooring": true/false,\n'
                '  "needs_paint": true/false,\n'
                '  "needs_roof": true/false,\n'
                '  "needs_exterior_work": true/false,\n'
                '  "notes": "Brief summary of visual distress observed"\n'
                "}"
            )
        }
    ]
    
    for url in sample_urls:
        content_payload.append({
            "type": "image_url",
            "image_url": {"url": url}
        })

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": content_payload}],
            response_format={"type": "json_object"},
            max_tokens=500
        )
        result_text = response.choices[0].message.content
        return json.loads(result_text)
    except Exception as e:
        logging.error(f"Vision API evaluation error: {e}")
        return {"rehab_level": "medium", "detected_items": [], "notes": "Analysis failed, using baseline."}
