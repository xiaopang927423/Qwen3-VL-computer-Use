import base64
from pathlib import Path
from qwen_agent.llm.fncall_prompts.nous_fncall_prompt import (
    NousFnCallPrompt,
    Message,
    ContentItem,
)
from utils.agent_function_call import ComputerUse
computer_use = ComputerUse(cfg={"display_width_px": 1000, "display_height_px": 1000})

class Messages:
    def __init__(self, user_query):
        system_message = NousFnCallPrompt().preprocess_fncall_messages(
            messages=[
                Message(role="system", content=[ContentItem(text='''
You MUST respond using the following format with XML tags:

<tool_call>
{"name": "computer_use", "arguments": {"action": "action_name", ...}}
</tool_call>

NEVER respond with raw JSON. Always use the XML tags. Failure to follow this format will cause errors.
''')]),
            ],
            functions=[computer_use.function],
            lang="zh",
        )
        system_message = system_message[0].model_dump()

        self.messages = [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": msg["text"]} for msg in system_message["content"]
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_query},
                ],
            }
        ]
        print(self.messages)

    def add_image_message(self, image_path):
        ext = Path(image_path).suffix.lower()
        mime_type = {
            '.png': 'png',
            '.jpg': 'jpeg',
            '.jpeg': 'jpeg',
            '.webp': 'webp'
        }.get(ext, 'png')  # 默认为 png

        with open(image_path, "rb") as img_file:
            base64_data = base64.b64encode(img_file.read()).decode('utf-8')

        self.messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/{mime_type};base64,{base64_data}"
                    },
                },
                {"type": "text", "text": "当前完成的操作后的屏幕"},
            ],
        })

    def add_qwen_response(self, qwen_response):
        self.messages.append({
            "role": "assistant",
            "content": [
                {"type": "text", "text": qwen_response},
            ],
        })




