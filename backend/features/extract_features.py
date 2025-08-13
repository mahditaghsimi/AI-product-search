import json
import re

def run_extract_features(raw_content_x):
    """
    Extract product feature queries from the AI model's raw output.

    The AI might return JSON directly, or it might wrap JSON inside ```json ... ``` code fences.
    This function:
      1. Detects if JSON is inside triple backticks.
      2. Removes the backticks and extracts the JSON string.
      3. Parses it into a Python dictionary.
      4. Prints and returns the dictionary.

    :param raw_content_x: (str) Raw text returned by the AI model.
    :return: Dictionary containing extracted product features.
    """
    # Try to find JSON enclosed in triple backticks (```json ... ```)
    matches = re.findall(r'```(?:json)?\s*(.*?)```', raw_content_x, re.DOTALL)

    if matches:
        # If matches found, take the first match as JSON content
        json_str = matches[0].strip()
    else:
        # No code fences — assume the whole string is JSON
        json_str = raw_content_x

    # Convert the JSON string to a Python dictionary
    feat_queries = json.loads(json_str)
    # Print extracted features for debugging
    print(feat_queries)
    # Return the extracted features
    return feat_queries