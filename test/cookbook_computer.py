from utils.take_screenshot import take_screenshot
from cookbook_computer_use import get_qwen3_vl_action
screenshot_path = take_screenshot()

import os
import json
import base64
from openai import OpenAI
from PIL import Image
from IPython.display import display
from qwen_agent.llm.fncall_prompts.nous_fncall_prompt import (
    NousFnCallPrompt,
    Message,
    ContentItem,
)
from transformers.models.qwen2_vl.image_processing_qwen2_vl_fast import smart_resize

from utils.agent_function_call import ComputerUse

from PIL import Image, ImageDraw, ImageColor
def draw_point(image: Image.Image, point: list, color=None):
    if isinstance(color, str):
        try:
            color = ImageColor.getrgb(color)
            color = color + (128,)
        except ValueError:
            color = (255, 0, 0, 128)
    else:
        color = (255, 0, 0, 128)

    overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    radius = min(image.size) * 0.05
    x, y = point

    overlay_draw.ellipse(
        [(x - radius, y - radius), (x + radius, y + radius)],
        fill=color
    )

    center_radius = radius * 0.1
    overlay_draw.ellipse(
        [(x - center_radius, y - center_radius),
         (x + center_radius, y + center_radius)],
        fill=(0, 255, 0, 255)
    )

    image = image.convert('RGBA')
    combined = Image.alpha_composite(image, overlay)

    return combined.convert('RGB')


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def perform_gui_grounding_with_api(screenshot_path, user_query, model_id, min_pixels=3136, max_pixels=12845056):
    """
    Perform GUI grounding using Qwen model to interpret user query on a screenshot.

    Args:
        screenshot_path (str): Path to the screenshot image
        user_query (str): User's query/instruction
        model: Preloaded Qwen model
        min_pixels: Minimum pixels for the image
        max_pixels: Maximum pixels for the image

    Returns:
        tuple: (output_text, display_image) - Model's output text and annotated image
    """

    # Open and process image
    input_image = Image.open(screenshot_path)
    base64_image = encode_image(screenshot_path)
    client = OpenAI(
        # If the environment variable is not configured, please replace the following line with the Dashscope API Key: api_key="sk-xxx". Access via https://bailian.console.alibabacloud.com/?apiKey=1 "
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    resized_height, resized_width = smart_resize(
        input_image.height,
        input_image.width,
        factor=32,
        min_pixels=min_pixels,
        max_pixels=max_pixels,
    )

    # Initialize computer use function
    computer_use = ComputerUse(
        cfg={"display_width_px": 1000, "display_height_px": 1000}
    )

    # Build messages
    system_message = NousFnCallPrompt().preprocess_fncall_messages(
        messages=[
            Message(role="system", content=[ContentItem(text="You are a helpful assistant.")]),
        ],
        functions=[computer_use.function],
        lang=None,
    )
    system_message = system_message[0].model_dump()
    messages = [
        {
            "role": "system",
            "content": [
                {"type": "text", "text": msg["text"]} for msg in system_message["content"]
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    # "min_pixels": 1024,
                    # "max_pixels": max_pixels,
                    # Pass in BASE64 image data. Note that the image format (i.e., image/{format}) must match the Content Type in the list of supported images. "f" is the method for string formatting.
                    # PNG image:  f"data:image/png;base64,{base64_image}"
                    # JPEG image: f"data:image/jpeg;base64,{base64_image}"
                    # WEBP image: f"data:image/webp;base64,{base64_image}"
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
                {"type": "text", "text": user_query},
            ],
        }
    ]
    print(json.dumps(messages, indent=4))
    completion = client.chat.completions.create(
        model=model_id,
        messages=messages,

    )

    output_text = completion.choices[0].message.content

    # Parse action and visualize
    action = json.loads(output_text.split('<tool_call>\n')[1].split('\n</tool_call>')[0])
    coordinate_relative = action['arguments']['coordinate']
    coordinate_absolute = [coordinate_relative[0] / 1000 * resized_width,
                           coordinate_relative[1] / 1000 * resized_height]

    display_image = input_image.resize((resized_width, resized_height))
    display_image = draw_point(display_image, coordinate_absolute, color='green')

    return output_text, display_image


# Example usage
user_query = '点击谷歌浏览器'
model_id = "qwen3-vl-235b-a22b-instruct"
output_text, display_image = perform_gui_grounding_with_api(screenshot_path, user_query, model_id)

# Display results
print(output_text)
image1 = display(display_image)
display_image.save('output_image.png', "PNG")




