from utils.take_screenshot import take_screenshot
from computer_agent import get_qwen3_vl_action
screenshot_path = take_screenshot()

action,  computer_use = get_qwen3_vl_action(screenshot_path, "打开vscode","qwen3-vl-235b-a22b-instruct")
print(action)
coordinate_relative = action['arguments']['coordinate']
coordinate_absolute = [coordinate_relative[0] / 1000 * 1728, coordinate_relative[1] / 1000 * 1117]
print(coordinate_relative, coordinate_absolute)
action['arguments']['coordinate'] = coordinate_absolute
computer_use.call(action['arguments'])




