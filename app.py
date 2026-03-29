import streamlit as st
import time
import math

st.set_page_config(page_title="数字合体实验室 V4.0", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    /* 星空暗黑主题深度覆盖 */
    [data-testid="stAppViewContainer"] {
        background-color: #080a14 !important;
        background-image: radial-gradient(circle at 50% 10%, #1a1e36 0%, #080a14 60%);
    }
    [data-testid="stSidebar"] {
        background-color: #0f121e !important;
    }
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    h1, h2, h3, p, span {
        color: #e0e7ff !important;
    }
    
    /* 容器框体边框与荧光 */
    .lab-container {
        border: 2px solid #1e293b;
        background-color: rgba(15, 23, 42, 0.6);
        border-radius: 20px;
        padding: 20px;
        min-height: 400px;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .lab-title {
        font-size: 1.5rem;
        font-weight: 900;
        margin-bottom: 20px;
        text-align: center;
        text-shadow: 0 0 10px rgba(255,255,255,0.3);
    }
    
    /* 个位：十格阵 (Ten-Frame) */
    .ten-frame-wrapper { display: flex; flex-direction: column; gap: 15px; }
    .ten-frame { 
        display: grid; 
        grid-template-columns: repeat(5, 1fr); 
        gap: 8px; 
        background: #111827; 
        padding: 12px; 
        border-radius: 12px; 
        border: 2px solid #3b82f6; 
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.2); 
    }
    .circle { 
        width: 35px; height: 35px; 
        border-radius: 50%; 
        border: 2px solid #1f2937; 
        background: #030712; 
        transition: all 0.3s;
    }
    .circle.active { 
        background: radial-gradient(circle at 30% 30%, #60a5fa, #2563eb); 
        box-shadow: 0 0 15px #3b82f6, inset 0 0 10px #93c5fd; 
        border: none; 
    }
    
    /* 十位：能量棒 */
    .tens-wrapper { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; }
    .energy-rod { 
        display: flex; flex-direction: column; gap: 2px; padding: 4px; 
        background: #111827; 
        border-radius: 8px; 
        border: 2px solid #f59e0b; 
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.2);
    }
    .rod-ball { 
        width: 25px; height: 12px; 
        border-radius: 6px; 
        background: radial-gradient(ellipse at center, #fcd34d, #d97706); 
        box-shadow: 0 0 8px #f59e0b; 
    }
    .rod-empty { border: 2px solid #1f2937; background: transparent; opacity: 0.3; box-shadow: none; width: 37px; height: 140px;}
    
    /* 百位：高能方块 */
    .hundreds-wrapper { display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; }
    .hundred-block { 
        display: grid; grid-template-columns: repeat(10, 1fr); gap: 1px; padding: 4px; 
        background: #6d28d9; 
        border-radius: 8px; 
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.5); 
        border: 2px solid #a78bfa;
    }
    .hundred-dot { width: 8px; height: 8px; background: #ddd6fe; border-radius: 2px; }
    .block-empty { border: 2px solid #333; background: transparent; opacity: 0.3; width: 60px; height: 60px;}
    
    /* 千位：超能星体 */
    .thousands-wrapper { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; align-items: center; height: 100%;}
    .thousand-cube { 
        width: 80px; height: 80px; 
        background: radial-gradient(circle at 30% 30%, #f43f5e, #be123c); 
        border-radius: 20px; 
        box-shadow: 0 0 30px rgba(225, 29, 72, 0.6); 
        display:flex; align-items:center; justify-content:center; 
        color:white; font-size: 2.5rem; font-weight:900; 
        transform: rotate(45deg);
    }
    .cube-inner { transform: rotate(-45deg); text-shadow: 0 0 10px white; }
    
    /* 按钮定制 Override Default Buttons */
    button[kind="secondary"] {
        background-color: transparent !important;
        border: 2px solid #3b82f6 !important;
        color: #60a5fa !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        height: 60px !important;
        font-size: 1.2rem !important;
    }
    button[kind="secondary"]:hover {
        background-color: rgba(59, 130, 246, 0.1) !important;
        box-shadow: 0 0 10px #3b82f6 !important;
        color: white !important;
    }
    
    .final-display {
        text-align: center;
        margin-top: 50px;
        padding: 30px;
        background: rgba(15, 23, 42, 0.8);
        border-top: 2px solid #3b82f6;
        border-bottom: 2px solid #3b82f6;
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.3);
    }
    .final-number {
        font-size: 8rem;
        font-weight: 900;
        color: #60a5fa;
        text-shadow: 0 0 20px #2563eb, 0 0 40px #3b82f6;
        font-family: 'Courier New', monospace;
        letter-spacing: 0.1em;
        margin: 0;
    }
    .final-label {
        font-size: 1.5rem;
        color: #94a3b8;
        letter-spacing: 0.2em;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

if 'units' not in st.session_state: st.session_state.units = 0
if 'tens' not in st.session_state: st.session_state.tens = 0
if 'hundreds' not in st.session_state: st.session_state.hundreds = 0
if 'thousands' not in st.session_state: st.session_state.thousands = 0
if 'trigger_fusion' not in st.session_state: st.session_state.trigger_fusion = None

def render_units(n):
    frames = max(1, math.ceil(n / 10))
    if n == 0: frames = 1
    html = "<div class='ten-frame-wrapper'>"
    drawn = 0
    for _ in range(frames):
        html += "<div class='ten-frame'>"
        for _ in range(10):
            c = "circle active" if drawn < n else "circle"
            html += f"<div class='{c}'></div>"
            drawn += 1
        html += "</div>"
    html += "</div>"
    return html

def render_tens(n):
    html = "<div class='tens-wrapper'>"
    if n == 0:
        html += "<div class='energy-rod rod-empty'></div>"
    else:
        for _ in range(n):
            html += "<div class='energy-rod'>" + ("<div class='rod-ball'></div>"*10) + "</div>"
    html += "</div>"
    return html

def render_hundreds(n):
    html = "<div class='hundreds-wrapper'>"
    if n == 0:
        html += "<div class='block-empty'></div>"
    else:
        for _ in range(n):
            html += "<div class='hundred-block'>" + ("<div class='hundred-dot'></div>"*100) + "</div>"
    html += "</div>"
    return html

def render_thousands(n):
    html = "<div class='thousands-wrapper'>"
    if n == 0:
        html += "<div class='thousand-cube' style='opacity:0.1; background:transparent; border:2px dashed #555; box-shadow:none;'><div class='cube-inner'>0</div></div>"
    else:
        for _ in range(n):
            html += "<div class='thousand-cube'><div class='cube-inner'>1k</div></div>"
    html += "</div>"
    return html

def add_units():
    st.session_state.units += 1
    if st.session_state.units >= 10:
        st.session_state.trigger_fusion = 'units'

def add_tens():
    st.session_state.tens += 1
    if st.session_state.tens >= 10:
        st.session_state.trigger_fusion = 'tens'

def add_hundreds():
    st.session_state.hundreds += 1
    if st.session_state.hundreds >= 10:
        st.session_state.trigger_fusion = 'hundreds'

def break_tens():
    if st.session_state.tens > 0:
        st.session_state.tens -= 1
        st.session_state.units += 10
        st.toast("💥 十位棒断裂散成了10个等离子球！", icon="⚠️")

def break_hundreds():
    if st.session_state.hundreds > 0:
        st.session_state.hundreds -= 1
        st.session_state.tens += 10
        st.toast("💥 百位块瓦解成了10根能量棒！", icon="⚠️")

def break_thousands():
    if st.session_state.thousands > 0:
        st.session_state.thousands -= 1
        st.session_state.hundreds += 10
        st.toast("💥 核心降维成了10块高能方块！", icon="⚠️")

def reset():
    st.session_state.units = 0
    st.session_state.tens = 0
    st.session_state.hundreds = 0
    st.session_state.thousands = 0
    st.session_state.trigger_fusion = None

with st.sidebar:
    st.title("🛰️ 重力控制台")
    st.markdown("---")
    st.button("🧹 重置星空实验室", use_container_width=True, on_click=reset, type="primary")
    st.markdown("<p style='color:#64748b; font-size:1rem; margin-top: 20px; line-height: 1.6;'><b>逆向思维课：</b><br>试着点击 💥拆解 高级能量块，观察低级网格会发生什么！请数一数拆解后留下的光球有几个？</p>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#60a5fa; text-shadow:0 0 15px #2563eb;'>🌌 数字合体实验室 V4.0</h1>", unsafe_allow_html=True)

if st.session_state.trigger_fusion == 'units':
    st.toast("⚡ 检测到十格阵充能100%！执行合体压缩...", icon="🧬")
    time.sleep(0.5)
    st.balloons()
    st.session_state.units -= 10
    st.session_state.tens += 1
    st.session_state.trigger_fusion = None
    st.rerun()
elif st.session_state.trigger_fusion == 'tens':
    st.toast("⚡ 10根能量棒充能完毕！聚合为高能方块...", icon="🧲")
    time.sleep(0.5)
    st.snow()
    st.session_state.tens -= 10
    st.session_state.hundreds += 1
    st.session_state.trigger_fusion = None
    st.rerun()
elif st.session_state.trigger_fusion == 'hundreds':
    st.toast("⚡ 10个高能方块临界质变！演化为千位星体...", icon="☄️")
    time.sleep(0.8)
    st.balloons()
    st.snow()
    st.session_state.hundreds -= 10
    st.session_state.thousands += 1
    st.session_state.trigger_fusion = None
    st.rerun()

col1, col2, col3, col4 = st.columns(4)

with col4:
    st.markdown("<div class='lab-container'>", unsafe_allow_html=True)
    st.markdown("<div class='lab-title' style='color:#60a5fa;'>✨ 个位舱 (Units)</div>", unsafe_allow_html=True)
    st.markdown(render_units(st.session_state.units), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.button("✨ 充能 (+1)", use_container_width=True, on_click=add_units)

with col3:
    st.markdown("<div class='lab-container'>", unsafe_allow_html=True)
    st.markdown("<div class='lab-title' style='color:#fbbf24;'>⚡ 十位舱 (Tens)</div>", unsafe_allow_html=True)
    st.markdown(render_tens(st.session_state.tens), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.button("⚡ 聚合 (+10)", use_container_width=True, on_click=add_tens)
    st.button("💥 拆解一层 (-10)", use_container_width=True, on_click=break_tens)

with col2:
    st.markdown("<div class='lab-container'>", unsafe_allow_html=True)
    st.markdown("<div class='lab-title' style='color:#a78bfa;'>🧲 百位舱 (Hundreds)</div>", unsafe_allow_html=True)
    st.markdown(render_hundreds(st.session_state.hundreds), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.button("🧲 聚合 (+100)", use_container_width=True, on_click=add_hundreds)
    st.button("💥 打碎方块 (-100)", use_container_width=True, on_click=break_hundreds)

with col1:
    st.markdown("<div class='lab-container'>", unsafe_allow_html=True)
    st.markdown("<div class='lab-title' style='color:#fb7185;'>☄️ 千位核心 (Thousands)</div>", unsafe_allow_html=True)
    st.markdown(render_thousands(st.session_state.thousands), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.button("☄️ 聚合 (+1000)", use_container_width=True, on_click=lambda: st.session_state.update(thousands=st.session_state.thousands+1))
    st.button("💥 核心降维 (-1000)", use_container_width=True, on_click=break_thousands)

abstract_number = st.session_state.thousands * 1000 + st.session_state.hundreds * 100 + st.session_state.tens * 10 + st.session_state.units

st.markdown(f"""
<div class='final-display'>
    <div class='final-label'>SUPERNOVA MATRIX RESULT</div>
    <div class='final-number'>{abstract_number}</div>
</div>
""", unsafe_allow_html=True)
