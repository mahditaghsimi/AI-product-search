import openai
from backend.ai_clints.API.API import api_key

def run_open_ai_clints(raw_content):
    # Create an OpenAI API client using the provided API key and OpenRouter endpoint
    client = openai.OpenAI(api_key=api_key,base_url="https://openrouter.ai/api/v1")
    # Send a chat completion request to the AI model
    # The system role defines instructions for the model
    # The user role contains the raw input text (product description/query)
    response = client.chat.completions.create(
        model="google/gemini-2.0-flash-exp:free",# Model selection
        messages=[
                {"role": "system", "content": """
                Extract the following product features from the user input: "name", "brand", "company_name", "categories", "description" and "price".
        Return a JSON object with these keys. If any information is missing, use an empty string for that field.
        Only extract what is clearly stated.
        
        Example:
        {
          "name": "",
          "brand": "",
          "company_name": "",
          "categories": "gaming",
          "description": "A good product for gaming under $50."
          "price": ""
        }
        
        """},
                {"role": "user", "content": raw_content},# The actual user-provided input text
            ]
        )
    # Extract and clean the model's response text
    raw_content_x = response.choices[0].message.content.strip()
    # Return the raw JSON-like string output from the model
    return raw_content_x



