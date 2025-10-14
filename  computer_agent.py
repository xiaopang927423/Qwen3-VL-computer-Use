import os
import json
import dotenv
from openai import OpenAI
from utils.agent_function_call import ComputerUse
from utils.take_screenshot import take_screenshot
from utils.chat_history import Messages
dotenv.load_dotenv("/Users/zjlz/Qwen3-VL-cookbook/pythonProject6/.env")

# 图片编码

def get_qwen3_vl_action(messages, model_id, min_pixels=3136, max_pixels=12845056):
    """
    使用 Qwen 模型执行 GUI 接地，以解释用户在屏幕截图上的查询。
    :param messages:
    :param model_id:
    :param min_pixels:
    :param max_pixels:
    :return:
    tuple(action)
    """
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=os.getenv("DASHSCOPE_URL")
    )

    # 初始化显示屏对象
    computerUse = ComputerUse(
        cfg={"display_width_px": 1000, "display_height_px": 1000}
    )

    completion = client.chat.completions.create(
        model=model_id,
        messages=messages,
    )
    output_text = completion.choices[0].message.content
    print(output_text)
    action = json.loads(output_text.split('<tool_call>\n')[1].split('\n</tool_call>')[0])
    return output_text, action, computerUse


user_query = input("请输入你的需求")
message = Messages(user_query)
action_num = 1
while True:
    image_path = take_screenshot()
    message.add_image_message(image_path=image_path)

    print(message.messages)
    output_text, action, computer_use = get_qwen3_vl_action(message.messages, "qwen3-vl-235b-a22b-instruct")
    message.add_qwen_response(output_text)
    if action["arguments"]["action"] == "terminate":
        if action["arguments"]["status"] == "success":
            print(f"{user_query}成功🎆")
        else:
            print(f"{user_query}失败💔")
        break
    print(f"Qwen3 将要采取第{action_num}步行动:{action["arguments"]["action"]}")
    if action["arguments"]["action"] in ["left_click", "right_click", "middle_click", "double_click", "triple_click","mouse_move","left_click_drag"]:
        coordinate_relative = action['arguments']['coordinate']
        coordinate_absolute = [coordinate_relative[0] / 1000 * 1728, coordinate_relative[1] / 1000 * 1117]
        action['arguments']['coordinate'] = coordinate_absolute
    print(action)
    computer_use.call(action['arguments'])
    action_num += 1


















