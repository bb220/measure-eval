from typing import Dict, Any, Union
import json
import re


def extract_json_from_markdown(text: str) -> str:
    """
    Extract JSON content from markdown code fences.
    Handles formats like:
    ```json
    {...}
    ```
    or just returns the text if no code fences found.
    """
    # Try to find JSON within markdown code fences
    pattern = r'```(?:json)?\s*\n?(.*?)\n?```'
    match = re.search(pattern, text, re.DOTALL)

    if match:
        return match.group(1).strip()

    # If no code fences found, return original text
    return text.strip()


def get_assert(output: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform measurement output by converting feet+inches to total inches
    and compare against actual value for red rectangle.

    Args:
        output: JSON string with format [{feet: number, inches: number, pixel_length: number, inches_on_drawing: number}]
        context: Promptfoo context with prompt, vars, etc.

    Returns:
        GradingResult dict with pass, score, and reason
    """
    # Actual value in total inches for red rectangle
    actual_value = 211.0  # 17'-7"

    # Extract JSON from markdown code fences if present
    clean_output = extract_json_from_markdown(output)

    # Parse the output JSON (array with single measurement)
    parsed = json.loads(clean_output)

    # Extract the single measurement from the array
    measurement = parsed[0]
    feet = measurement['feet']
    inches = measurement['inches']
    pixel_length = measurement.get('pixel_length', 0)
    inches_on_drawing = measurement.get('inches_on_drawing', 0)

    # Convert to total inches
    total_inches = feet * 12 + inches

    # Calculate difference from actual value
    difference = abs(total_inches - actual_value)

    # Build result object
    result = {
        'measured': total_inches,
        'actual': actual_value,
        'difference': difference,
        'pixel_length': pixel_length,
        'inches_on_drawing': inches_on_drawing
    }

    # Check if difference is within 6-inch tolerance
    passed = difference <= 6

    # Return result with pass/fail and measurement details
    return {
        'pass': passed,
        'score': 1.0 if passed else 0.0,
        'reason': f"Difference: {difference:.2f} inches ({'PASS' if passed else 'FAIL'} - tolerance: ≤24 inches)\n\n{json.dumps(result, indent=2)}"
    }
