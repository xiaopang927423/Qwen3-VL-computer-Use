from typing import Union, Tuple, List
from qwen_agent.tools.base import BaseTool, register_tool
from pynput import mouse, keyboard
from pynput.mouse import Button
import time


@register_tool("computer_use")
class ComputerUse(BaseTool):
    @property
    def description(self):
        return f"""
Use a mouse and keyboard to interact with a computer, and take screenshots.
* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.
* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.
* The screen's resolution is {self.display_width_px}x{self.display_height_px}.
* Whenever you intend to move the cursor to click on an element like an icon, you should consult a screenshot to determine the coordinates of the element before moving the cursor.
* If you tried clicking on a program or link but it failed to load, even after waiting, try adjusting your cursor position so that the tip of the cursor visually falls on the element that you want to click.
* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges.
""".strip()

    parameters = {
        "properties": {
            "action": {
                "description": """
The action to perform. The available actions are:
* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.
* `type`: Type a string of text on the keyboard.
* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.
* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.
* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.
* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.
* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.
* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.
* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).
* `scroll`: Performs a scroll of the mouse scroll wheel.
* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).
* `wait`: Wait specified seconds for the change to happen.
* `terminate`: Terminate the current task and report its completion status.
* `answer`: Answer a question.
""".strip(),
                "enum": [
                    "key",
                    "type",
                    "mouse_move",
                    "left_click",
                    "left_click_drag",
                    "right_click",
                    "middle_click",
                    "double_click",
                    "triple_click",
                    "scroll",
                    "wait",
                    "terminate",
                    "answer",
                ],
                "type": "string",
            },
            "keys": {
                "description": "Required only by `action=key`.",
                "type": "array",
            },
            "text": {
                "description": "Required only by `action=type` and `action=answer`.",
                "type": "string",
            },
            "coordinate": {
                "description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to.",
                "type": "array",
            },
            "pixels": {
                "description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.",
                "type": "number",
            },
            "time": {
                "description": "The seconds to wait. Required only by `action=wait`.",
                "type": "number",
            },
            "status": {
                "description": "The status of the task. Required only by `action=terminate`.",
                "type": "string",
                "enum": ["success", "failure"],
            },
        },
        "required": ["action"],
        "type": "object",
    }

    def __init__(self, cfg=None):
        self.display_width_px = cfg["display_width_px"]
        self.display_height_px = cfg["display_height_px"]
        try:
            self.mouse_controller = mouse.Controller()
            self.keyboard_controller = keyboard.Controller()
            print("成功初始化鼠标和键盘控制器")
        except Exception as e:
            print(f"初始化鼠标和键盘控制器失败: {e}")
            raise
        super().__init__(cfg)

    def call(self, params: Union[str, dict], **kwargs):
        params = self._verify_json_format_args(params)
        action = params["action"]
        print(f"执行操作: {action}")  # 添加调试信息
        print(f"参数: {params}")  # 添加调试信息

        if action in ["left_click", "right_click", "middle_click", "double_click", "triple_click"]:
            return self._mouse_click(action, params.get("coordinate"))
        elif action == "key":
            return self._key(params["keys"])
        elif action == "type":
            return self._type(params["text"])
        elif action == "mouse_move":
            return self._mouse_move(params["coordinate"])
        elif action == "left_click_drag":
            return self._left_click_drag(params["coordinate"])
        elif action == "scroll":
            return self._scroll(params["pixels"])
        elif action == "hscroll":
            return self._hscroll(params["pixels"])
        elif action == "answer":
            return self._answer(params["text"])
        elif action == "wait":
            return self._wait(params["time"])
        elif action == "terminate":
            return self._terminate(params["status"])
        else:
            raise ValueError(f"Invalid action: {action}")

    def _mouse_click(self, button: str, coordinate: Tuple[int, int] = None):
        # button: 'left', 'right', 'middle', 'double_click', 'triple_click'
        # 如果提供了坐标，则先移动鼠标到该位置
        if coordinate is not None:
            x, y = coordinate
            print(f"尝试移动鼠标到 ({x}, {y})")
            try:
                self.mouse_controller.position = (x, y)
                current_pos = self.mouse_controller.position
                print(f"鼠标当前位置: {current_pos}")
            except Exception as e:
                print(f"移动鼠标失败: {e}")
                return f"Failed to move mouse: {e}"

        button_map = {
            'left_click': Button.left,
            'right_click': Button.right,
            'middle_click': Button.middle,
            'double_click': Button.left,
            'triple_click': Button.left
        }

        try:
            if button in ['left_click', 'right_click', 'middle_click']:
                print(f"尝试执行 {button} 操作")
                self.mouse_controller.click(button_map[button])
                print(f"成功执行 {button} 操作")
            elif button == 'double_click':
                print(f"尝试执行 {button} 操作")
                self.mouse_controller.click(button_map[button])
                self.mouse_controller.click(button_map[button])
                print(f"成功执行 {button} 操作")
            elif button == 'triple_click':
                # Triple click simulated with three clicks
                print(f"尝试执行 {button} 操作")
                self.mouse_controller.click(button_map[button])
                self.mouse_controller.click(button_map[button])
                self.mouse_controller.click(button_map[button])
                print(f"成功执行 {button} 操作")
        except Exception as e:
            print(f"执行鼠标点击失败: {e}")
            return f"Failed to click mouse: {e}"

        return f"Performed {button} action"

    def _key(self, keys: List[str]):
        # 按下并释放一系列按键
        try:
            # 处理特殊按键
            processed_keys = []
            for key in keys:
                # 尝试将字符串转换为对应的特殊按键
                if hasattr(keyboard.Key, key):
                    processed_keys.append(getattr(keyboard.Key, key))
                else:
                    processed_keys.append(key)

            print(f"按下按键: {processed_keys}")

            # 按下所有按键
            for key in processed_keys:
                self.keyboard_controller.press(key)

            # 逆序释放所有按键
            for key in reversed(processed_keys):
                self.keyboard_controller.release(key)

            print(f"释放按键: {processed_keys}")
            time.sleep(5)
            return f"Pressed keys: {keys}"
        except Exception as e:
            print(f"按键操作失败: {e}")
            return f"Error pressing keys {keys}: {str(e)}"


    def _type(self, text: str):
        print(f"输入文本: {text}")
        try:
            self.keyboard_controller.type(text)
            print(f"成功输入文本: {text}")
            time.sleep(5)
            return f"Typed text: {text}"
        except Exception as e:
            print(f"文本输入失败: {e}")
            return f"Error typing text: {e}"

    def _mouse_move(self, coordinate: Tuple[int, int]):
        x, y = coordinate
        print(f"尝试移动鼠标到 ({x}, {y})")
        try:
            self.mouse_controller.position = (x, y)
            current_pos = self.mouse_controller.position
            print(f"鼠标当前位置: {current_pos}")
            return f"Moved mouse to ({x}, {y})"
        except Exception as e:
            print(f"移动鼠标失败: {e}")
            return f"Failed to move mouse: {e}"

    def _left_click_drag(self, coordinate: Tuple[int, int]):
        x, y = coordinate
        print(f"尝试拖拽鼠标到 ({x}, {y})")
        try:
            self.mouse_controller.press(Button.left)
            self.mouse_controller.move(x, y)
            self.mouse_controller.release(Button.left)
            print(f"成功拖拽鼠标到 ({x}, {y})")
            return f"Dropped mouse from current position to ({x}, {y})"
        except Exception as e:
            print(f"拖拽鼠标失败: {e}")
            return f"Failed to drag mouse: {e}"

    def _scroll(self, pixels: int):
        # 正数向上滚动，负数向下滚动
        print(f"尝试滚动 {pixels} 像素")
        try:
            self.mouse_controller.scroll(0, pixels)
            print(f"成功滚动 {pixels} 像素")
            return f"Scrolled {pixels} pixels"
        except Exception as e:
            print(f"滚动失败: {e}")
            return f"Failed to scroll: {e}"

    def _hscroll(self, pixels: int):
        # 水平滚动
        print(f"尝试水平滚动 {pixels} 像素")
        try:
            self.mouse_controller.scroll(pixels, 0)
            print(f"成功水平滚动 {pixels} 像素")
            return f"Horizontally scrolled {pixels} pixels"
        except Exception as e:
            print(f"水平滚动失败: {e}")
            return f"Failed to scroll horizontally: {e}"

    def _wait(self, wait_time: int):
        if wait_time is None:
            wait_time = 1  # 默认等待1秒
        print(f"等待 {wait_time} 秒")
        time.sleep(wait_time)
        return f"Waited {wait_time} seconds"

    def _answer(self, text: str):
        print(f"Answer: {text}")
        return text

    def _terminate(self, status: str):
        print(f"Terminating with status: {status}")
        return f"Terminated with status: {status}"