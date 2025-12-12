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
    Evaluate measurement output by comparing pixel_length against actual value.
    Pass/fail is determined solely by pixel_length difference (< 5 pixels).

    Args:
        output: JSON string with format {pixel_length: number, start_coordinates: [x, y],
                end_coordinates: [x, y], feet: number, inches: number}
        context: Promptfoo context with prompt, vars, etc.

    Returns:
        GradingResult dict with pass, score, and reason
    """
    # Actual value in pixels for red rectangle
    actual_pixel_length = 83  # pixels

    # Extract JSON from markdown code fences if present
    clean_output = extract_json_from_markdown(output)

    # Parse the output JSON (single measurement object)
    parsed = json.loads(clean_output)

    # Extract measurement values
    feet = parsed['feet']
    inches = parsed['inches']
    pixel_length = parsed.get('pixel_length', 0)

    # Extract coordinates
    start_coords = parsed['start_coordinates']
    end_coords = parsed['end_coordinates']

    # Calculate pixel length difference (PRIMARY CRITERION)
    pixel_difference = abs(pixel_length - actual_pixel_length)

    # Calculate y-coordinate differences
    start_y_diff = abs(start_coords[1] - 1051)
    end_y_diff = abs(end_coords[1] - 1134)
    total_y_diff = start_y_diff + end_y_diff

    # Build result object
    result = {
        'measured_feet': feet,
        'measured_inches': inches,
        'measured_pixel_length': pixel_length,
        'actual_pixel_length': actual_pixel_length,
        'pixel_difference': pixel_difference,
        'start_coordinates': {
            'measured': start_coords,
            'actual': [start_coords[0], 1051],
            'y_difference': start_y_diff
        },
        'end_coordinates': {
            'measured': end_coords,
            'actual': [end_coords[0], 1134],
            'y_difference': end_y_diff
        },
        'total_y_difference': total_y_diff
    }

    # Check if pixel difference is within tolerance
    passed = pixel_difference < 5

    # Return result with pass/fail and measurement details
    return {
        'pass': passed,
        'score': 1.0 if passed else 0.0,
        'reason': f"Pixel difference: {pixel_difference:.2f} px ({'PASS' if passed else 'FAIL'} - tolerance: < 5 px)\n\n{json.dumps(result, indent=2)}"
    }
