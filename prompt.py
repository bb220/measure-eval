import base64
import typing
from urllib.request import urlopen


# Type definitions for improved code readability
class Vars(typing.TypedDict):
    image_url: str


class Provider(typing.TypedDict):
    id: str
    label: typing.Optional[str]


class PromptFunctionContext(typing.TypedDict):
    vars: Vars
    provider: Provider


def get_image_base64(image_url: str) -> tuple[str, str]:
    """
    Fetch an image from a URL and convert it to a base64-encoded string.

    Args:
        image_url (str): The URL of the image to fetch.

    Returns:
        tuple[str, str]: The base64-encoded image data and media type.
    """
    with urlopen(image_url) as response:
        media_type = response.headers.get("Content-Type", "image/png").split(";")[0]
        return base64.b64encode(response.read()).decode("utf-8"), media_type


# User prompt for task
user_prompt = """
Measure the length of the red rectangle in this drawing. Think step by step.

This PNG is 1344 x 896 pixels.

## Measurement Process
1. Locate the red rectangle
2. Identify the point coordinates of the starting edge of rectangle and the point coordinates of the ending edge of the rectangle
3. Measure its pixel length
4. Multipy the pixel length values by (36 inches / 1344 pixels)
5. Multiply by 8 (1/8 inches = 1 foot) for the feet value
6. Express results in feet and inches (round to nearest inch)

Show your work for each step.

Include a JSON object in the response that contains:
   - "pixel_length": the length in pixels
   - "start_coordinates": the [x, y] coordinates of the starting edge
   - "end_coordinates": the [x, y] coordinates of the ending edge
   - "feet": the feet portion of the measurement
   - "inches": the inches portion of the measurement (rounded to nearest inch)
"""


def format_image_prompt(context: PromptFunctionContext) -> list[dict[str, typing.Any]]:
    """
    Format the prompt for image analysis based on the AI provider.

    This function generates a formatted prompt for different AI providers,
    tailoring the structure based on the provider's requirements.

    Args:
        context (PromptFunctionContext): A dictionary containing provider information and variables.

    Returns:
        list[dict[str, typing.Any]]: A list of dictionaries representing the formatted prompt.

    Raises:
        ValueError: If an unsupported provider is specified.
    """
    provider_id = context["provider"]["id"]
    if (
        provider_id.startswith("bedrock:anthropic")
        or provider_id.startswith("bedrock:us.anthropic")
        or provider_id.startswith("anthropic:")
    ):
        image_data, media_type = get_image_base64(context["vars"]["image_url"])
        return [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    }
                ],
            },
        ]
    if (
        provider_id.startswith("google:gemini")
    ):
        image_data, media_type = get_image_base64(context["vars"]["image_url"])
        return [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": media_type,
                            "data": image_data,
                        }
                    },
                    {"text": user_prompt},
                ]
            }
        ]
    # TODO Update to use user prompt object instead of system
    if (
        provider_id.startswith("openai:")
        or context["provider"].get("label") == "custom label for gpt-4.1"
    ):
        return [
            {
                "role": "system",
                "content": [{"type": "text", "text": user_prompt}],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": context["vars"]["image_url"],
                        },
                    }
                ],
            },
        ]

    raise ValueError(f"Unsupported provider: {context['provider']}")
