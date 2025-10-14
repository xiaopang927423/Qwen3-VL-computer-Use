#!/usr/bin/env python3
"""
测试 pynput 库的基本功能
此脚本测试鼠标控制和键盘输入功能
"""

import time
from pynput import mouse, keyboard


def test_mouse():
    """测试鼠标功能"""
    print("开始测试鼠标功能...")
    
    # 创建鼠标控制器
    mouse_controller = mouse.Controller()
    
    # 获取当前鼠标位置
    print(f"当前鼠标位置: {mouse_controller.position}")
    
    # 移动鼠标到坐标 (100, 100)
    print("移动鼠标到 (100, 100)")
    mouse_controller.position = (100, 100)
    time.sleep(1)
    
    # 相对移动鼠标
    print("相对移动鼠标 (+50, +50)")
    mouse_controller.move(50, 50)
    time.sleep(1)
    
    # 鼠标左键点击
    print("执行鼠标左键点击")
    mouse_controller.click(mouse.Button.left, 1)
    time.sleep(1)
    
    # 鼠标右键点击
    print("执行鼠标右键点击")
    mouse_controller.click(mouse.Button.right, 1)
    time.sleep(1)
    
    # 按下和释放鼠标按钮
    print("按下鼠标左键")
    mouse_controller.press(mouse.Button.left)
    time.sleep(1)
    print("释放鼠标左键")
    mouse_controller.release(mouse.Button.left)
    time.sleep(1)
    
    # 滚动鼠标滚轮
    print("向上滚动鼠标滚轮")
    mouse_controller.scroll(0, 2)
    time.sleep(1)
    
    print("鼠标功能测试完成\n")


def on_move(x, y):
    """鼠标移动回调函数"""
    print(f'鼠标移动到坐标: ({x}, {y})')


def on_click(x, y, button, pressed):
    """鼠标点击回调函数"""
    if pressed:
        print(f'鼠标在 ({x}, {y}) 点击 {button}')
    else:
        print(f'鼠标在 ({x}, {y}) 释放 {button}')
        # 点击一次后停止监听
        return False


def on_scroll(x, y, dx, dy):
    """鼠标滚动回调函数"""
    print(f'鼠标在 ({x}, {y}) 滚动 ({dx}, {dy})')
    # 滚动一次后停止监听
    return False


def test_mouse_listener():
    """测试鼠标监听器"""
    print("开始测试鼠标监听器...")
    print("请移动鼠标或点击鼠标按钮进行测试，5秒后开始监听...")
    
    time.sleep(5)
    
    # 收集鼠标事件直到点击一次
    print("监听鼠标移动和点击事件（点击任意键结束监听）...")
    with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        listener.join()
    
    print("鼠标监听器测试完成\n")


def test_keyboard():
    """测试键盘功能"""
    print("开始测试键盘功能...")
    
    # 创建键盘控制器
    keyboard_controller = keyboard.Controller()
    
    # 输入文字
    print("输入文字 'Hello World'")
    keyboard_controller.type('Hello World')
    time.sleep(1)
    
    # 按下和释放空格键
    print("按下和释放空格键")
    keyboard_controller.press(keyboard.Key.space)
    keyboard_controller.release(keyboard.Key.space)
    time.sleep(1)
    
    # 组合键 Ctrl+A
    print("按下组合键 Ctrl+A")
    keyboard_controller.press(keyboard.Key.ctrl)
    keyboard_controller.press('a')
    keyboard_controller.release('a')
    keyboard_controller.release(keyboard.Key.ctrl)
    time.sleep(1)
    
    # 按下回车键
    print("按下回车键")
    keyboard_controller.press(keyboard.Key.enter)
    keyboard_controller.release(keyboard.Key.enter)
    time.sleep(1)
    
    print("键盘功能测试完成\n")


def on_press(key):
    """键盘按下回调函数"""
    try:
        print(f'按键 {key.char} 被按下')
    except AttributeError:
        print(f'特殊键 {key} 被按下')


def on_release(key):
    """键盘释放回调函数"""
    print(f'{key} 被释放')
    # 如果按下了 Esc 键则停止监听
    if key == keyboard.Key.esc:
        print("键盘监听器停止")
        return False


def test_keyboard_listener():
    """测试键盘监听器"""
    print("开始测试键盘监听器...")
    print("请按任意键进行测试，按 Esc 键结束监听...")
    
    # 收集键盘事件直到按下 Esc
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
    
    print("键盘监听器测试完成\n")


def main():
    """主函数"""
    print("=" * 50)
    print("pynput 库功能测试")
    print("=" * 50)
    
    try:
        test_mouse()
        test_keyboard()
        
        print("是否要测试监听器功能？(鼠标监听器需要手动操作)")
        print("1. 测试鼠标监听器（需要手动移动/点击鼠标）")
        print("2. 测试键盘监听器（按任意键测试，Esc退出）")
        print("3. 跳过监听器测试")
        
        choice = input("请选择 (1/2/3): ").strip()
        
        if choice == "1":
            test_mouse_listener()
        elif choice == "2":
            test_keyboard_listener()
        elif choice == "3":
            print("跳过监听器测试")
        else:
            print("无效选择，跳过监听器测试")
            
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        print("请确保您已经安装了 pynput 库: pip install pynput")
        print("在某些系统上可能需要额外的权限配置")
    
    print("=" * 50)
    print("测试完成")
    print("=" * 50)


if __name__ == "__main__":
    main()