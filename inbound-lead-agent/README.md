# Inbound Lead Agent

A conversion-focused AI sub-agent skill designed to textually pre-qualify inbound property leads. It transforms raw traffic into highly structured property lead data matching a standardized investment intake process.

## Architecture & Assets
* **`soul.md`**: Deep system prompt logic mapping conversation progression loops, empathy check requirements, and tactical value phrasing.
* **`closebot_prompt.txt`**: A flattened, copy-paste format optimized specifically for no-code automated chatbot configurations (CloseBot, Vapi, GoHighLevel, etc.).
* **`lead_sheet_schema.json`**: Structured JSON layout data mapping to turn chat transcripts into clean database arrays.

## Integration Methods
### 1. In a Custom OpenAI GPT or Vapi Engine
Copy the markdown contents of `soul.md` and paste it directly into the "Instructions" text area.

### 2. In CloseBot / GoHighLevel SMS Funnels
Copy the text within `closebot_prompt.txt` and drop it into your primary Main Objective or Base System Character prompt field. Configure your custom fields to bind dynamically to the fields itemized inside `lead_sheet_schema.json`.

##Done for you setup
If you're looking to have this done for you - 3 Degrees Consulting is proud to offer Velocity CRM - it is the single most robust build out of GHL for real estate investors on the market today.  You can use these skills inside of that tool to help handle inbound leads.  
Please head to www.BestREICRM.com


## ⚠️ Disclaimer
This tool is provided "as-is" for educational and personal use only. **No technical support, custom software debugging, API setup help, or individualized platform training is provided.** Users must manage their own third-party chatbot subscription tools and system logic.
