#include <Windows.h>
#include <iostream>
#include <thread>
#include <atomic>
#include <string>
#include <locale>
#include <codecvt>

using namespace std;

atomic<bool> running(false);
HHOOK keyboardHook = nullptr;

// 设置控制台编码为UTF-8
void SetConsoleToUTF8() {
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    setlocale(LC_ALL, "zh_CN.UTF-8");
    locale utf8_locale(locale(), new codecvt_utf8<wchar_t>);
    wcout.imbue(utf8_locale);
    cout.imbue(utf8_locale);
}

// 鼠标按键枚举
enum MouseButton {
    LEFT,
    MIDDLE,
    RIGHT
};

// 键盘钩子回调函数
LRESULT CALLBACK KeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode == HC_ACTION) {
        KBDLLHOOKSTRUCT* pKeyInfo = (KBDLLHOOKSTRUCT*)lParam;
        
        if (wParam == WM_KEYDOWN || wParam == WM_SYSKEYDOWN) {
            if (pKeyInfo->vkCode == VK_F8) {
                running = !running;
                cout << (running ? "连点器已启动" : "连点器已停止") << endl;
                return 1; // 阻止热键传递
            }
        }
    }
    return CallNextHookEx(keyboardHook, nCode, wParam, lParam);
}

// 模拟鼠标点击
void SimulateClick(MouseButton button) {
    DWORD downEvent = 0;
    DWORD upEvent = 0;
    
    switch (button) {
        case LEFT:
            downEvent = MOUSEEVENTF_LEFTDOWN;
            upEvent = MOUSEEVENTF_LEFTUP;
            break;
        case MIDDLE:
            downEvent = MOUSEEVENTF_MIDDLEDOWN;
            upEvent = MOUSEEVENTF_MIDDLEUP;
            break;
        case RIGHT:
            downEvent = MOUSEEVENTF_RIGHTDOWN;
            upEvent = MOUSEEVENTF_RIGHTUP;
            break;
    }
    
    mouse_event(downEvent, 0, 0, 0, 0);
    mouse_event(upEvent, 0, 0, 0, 0);
}

// 连点器线程
void ClickerThread(int delayMs, MouseButton button) {
    while (true) {
        if (running) {
            SimulateClick(button);
            this_thread::sleep_for(chrono::milliseconds(delayMs));
        } else {
            this_thread::sleep_for(chrono::milliseconds(10));
        }
    }
}

int main(int argc, char* argv[]) {
    SetConsoleToUTF8();
    
    if (argc != 3) {
        cout << "用法: " << argv[0] << " <点击间隔(毫秒)> <鼠标按键(left/middle/right)>" << endl;
        cout << "默认热键: F8 (开始/停止连点)" << endl;
        return 1;
    }
    
    try {
        int delayMs = stoi(argv[1]);
        if (delayMs <= 0) {
            cout << "错误: 点击间隔必须大于0毫秒" << endl;
            return 1;
        }
        
        string buttonStr = argv[2];
        MouseButton button;
        
        if (buttonStr == "left") {
            button = LEFT;
        } else if (buttonStr == "middle") {
            button = MIDDLE;
        } else if (buttonStr == "right") {
            button = RIGHT;
        } else {
            cout << "错误: 无效的鼠标按键，必须是left、middle或right" << endl;
            return 1;
        }
        
        // 设置键盘钩子
        keyboardHook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyboardProc, GetModuleHandle(NULL), 0);
        if (!keyboardHook) {
            cout << "错误: 无法设置键盘钩子" << endl;
            return 1;
        }
        
        cout << "连点器已初始化" << endl;
        cout << "点击间隔: " << delayMs << " 毫秒" << endl;
        cout << "鼠标按键: " << buttonStr << endl;
        cout << "热键: F8 (按此键开始/停止连点)" << endl;
        cout << "按F8键开始连点..." << endl;
        
        // 启动连点线程
        thread clickerThread(ClickerThread, delayMs, button);
        
        // 消息循环
        MSG msg;
        while (GetMessage(&msg, NULL, 0, 0)) {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
        
        // 清理
        UnhookWindowsHookEx(keyboardHook);
        clickerThread.detach();
        
    } catch (const exception& e) {
        cout << "错误: " << e.what() << endl;
        return 1;
    }
    
    return 0;
}