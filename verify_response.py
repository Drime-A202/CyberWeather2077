"""直接用 Flask test_client 验证 /art 返回的 HTML 是否包含最新的下拉菜单代码"""
import sys
sys.path.insert(0, r"d:\GUI WeatherReporter")
from app import app

client = app.test_client()
resp = client.get("/art")
html = resp.get_data(as_text=True)

print("=== HTTP 状态码 ===")
print(resp.status_code)
print()
print("=== Cache-Control 响应头 ===")
for k, v in resp.headers.items():
    if k.lower() in ("cache-control", "pragma", "expires", "last-modified"):
        print(f"  {k}: {v}")
print()

checks = [
    ("id='city-wrapper'",         "city-wrapper 容器"),
    ('id="city-wrapper"',         "city-wrapper 容器(双引号)"),
    ("z-index: 9999",             "z-index:9999 置顶层级"),
    ("cityPulse",                 "cityPulse 脉冲动画关键帧"),
    ("animation: cityPulse",      "容器绑定脉冲动画"),
    ("bottom: 40px",              "底部 40px 定位"),
    ("left: 50%",                 "水平居中 left:50%"),
    ("translateX(-50%)",          "水平居中 transform"),
    ("id='city-select'",          "city-select 下拉元素"),
    ('id="city-select"',          "city-select 下拉元素(双引号)"),
    ("appearance: none",          "select 原生样式重置"),
    ("北京 BEIJING",              "北京选项"),
    ("香港 HONG KONG",            "香港选项"),
    ("border-radius: 999px",      "胶囊形状"),
    ('rgba(0, 255, 242',          "霓虹青发光色"),
    ('rgba(255, 0, 170',          "霓虹粉发光色"),
    ("meta http-equiv=\"Cache-Control\"", "HTML meta 防缓存标签"),
    ("meta http-equiv=\"Pragma\"",        "HTML meta Pragma 标签"),
    ("forceT = setTimeout",       "JS 6秒硬超时(防 loading 卡死)"),
    ("PARTICLE_COUNT = 420",      "420 粒子数"),
    ("tempToHue",                 "温度-色相映射函数"),
    ("iconToShape",               "天气代码-形态映射函数"),
    ("globalCompositeOperation = 'lighter'", "发光叠加混合模式"),
]

print("=== 页面内容检查（共 %d 项）===" % len(checks))
pass_count = 0
for needle, desc in checks:
    found = needle in html
    mark = "✓" if found else "✗"
    print(f"  {mark} {desc:<32s} -> {'找到' if found else '未找到'}  [{needle[:50]}]")
    if found:
        pass_count += 1

print()
print(f"=== 结果: {pass_count}/{len(checks)} 通过 ===")
if pass_count == len(checks):
    print("结论：服务器返回的 HTML 是**最新版本**，已包含高可见性下拉菜单。")
    print("若你浏览器仍看不到，请按以下步骤强制刷新：")
    print("  1. 关闭所有 Flask 终端窗口，重新运行 python app.py")
    print("  2. 浏览器按 Ctrl+Shift+R (Win) / Cmd+Shift+R (Mac) 强制刷新忽略缓存")
    print("  3. 或打开 DevTools(F12) -> Network 面板，勾选 Disable cache，再刷新")
    print("  4. 下拉菜单位于屏幕**底部正中央**，是一个青粉色发光胶囊，一直在呼吸闪烁")
else:
    print("结论：HTML 缺少关键代码，需要修复 art.html")
