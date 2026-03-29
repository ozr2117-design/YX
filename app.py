import streamlit as st
import time

st.set_page_config(page_title="数字爆炸实验室 V2.0", page_icon="💥", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .main-title { text-align: center; color: #ff3366; font-size: 3.5rem; font-weight: 900; margin-bottom: 2rem; text-shadow: 2px 2px 0px #ffe6e6; }
    
    [data-testid="stMetricValue"] {
        font-size: 5.5rem !important;
        font-weight: 900 !important;
        color: #2c3e50 !important;
        text-align: center;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.4rem !important;
        font-weight: bold !important;
        color: #7f8c8d !important;
        text-align: center;
    }
    
    /* 大按钮统一定制 */
    [data-testid="column"] button {
        height: 120px !important;
        font-size: 2rem !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        color: white !important;
        border: none !important;
        transition: transform 0.1s;
    }
    [data-testid="column"] button:active {
        transform: scale(0.95);
    }
    
    /* 按列染色 */
    [data-testid="column"]:nth-child(1) button { background-color: #ff3b30 !important; box-shadow: 0 8px 15px rgba(255,59,48,0.3) !important; }
    [data-testid="column"]:nth-child(2) button { background-color: #007aff !important; box-shadow: 0 8px 15px rgba(0,122,255,0.3) !important; }
    [data-testid="column"]:nth-child(3) button { background-color: #f1c40f !important; color: #856404 !important; box-shadow: 0 8px 15px rgba(241,196,15,0.3) !important; text-shadow: none !important;}
    
    .bottom-status {
        background-color: #f8f9fa;
        border: 4px dashed #ced4da;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin-top: 40px;
    }
    .status-text { font-size: 1.8rem; font-weight: bold; color: #495057; line-height: 1.6; }
    .final-number { font-size: 4.5rem; font-weight: 900; color: #d32f2f; margin-top: 15px; font-family: 'Courier New', monospace; letter-spacing: 0.5rem; }
    
    /* 强光高亮效果提示框 */
    .alert-glow {
        padding: 20px;
        border-radius: 15px;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        animation: breath 1s infinite alternate;
    }
    @keyframes breath {
        from { box-shadow: 0 0 10px #ff9ecd; }
        to { box-shadow: 0 0 30px #ff3366; }
    }
</style>
""", unsafe_allow_html=True)

if 'units' not in st.session_state: st.session_state.units = 0
if 'tens' not in st.session_state: st.session_state.tens = 0
if 'hundreds' not in st.session_state: st.session_state.hundreds = 0
if 'thousands' not in st.session_state: st.session_state.thousands = 0

def add_units(): st.session_state.units += 1
def add_tens(): st.session_state.tens += 1
def add_hundreds(): st.session_state.hundreds += 1
def reset():
    st.session_state.units = 0
    st.session_state.tens = 0
    st.session_state.hundreds = 0
    st.session_state.thousands = 0

with st.sidebar:
    st.title("⚙️ 实验室控制台")
    st.markdown("---")
    st.button("🧹 重置实验室", use_container_width=True, on_click=reset, type="primary")

st.markdown("<p class='main-title'>💥 数字爆炸实验室 V2.0</p>", unsafe_allow_html=True)

alert_placeholder = st.empty()

col1, col2, col3, col4 = st.columns(4)
col1.metric("千位工厂 🏭", st.session_state.thousands)
col2.metric("百位仓库 📦", st.session_state.hundreds)
col3.metric("十位盒子 🥢", st.session_state.tens)
col4.metric("个位盘子 🔮", st.session_state.units)

st.write("---")

c1, c2, c3 = st.columns(3, gap="large")
with c1: st.button("➕ 增加 1 能量", use_container_width=True, on_click=add_units)
with c2: st.button("⏩ 注入 10 能量", use_container_width=True, on_click=add_tens)
with c3: st.button("⚡ 注入 100 能量", use_container_width=True, on_click=add_hundreds)

abstract_number = st.session_state.thousands * 1000 + st.session_state.hundreds * 100 + st.session_state.tens * 10 + st.session_state.units

st.markdown(f"""
<div class='bottom-status'>
    <div class='status-text'>🗣️ 现在你有：<br><span style='color:#e74c3c; font-size:2.2rem;'>{st.session_state.thousands}</span> 个工厂，<span style='color:#e67e22; font-size:2.2rem;'>{st.session_state.hundreds}</span> 个仓库，<span style='color:#2980b9; font-size:2.2rem;'>{st.session_state.tens}</span> 个盒子，<span style='color:#27ae60; font-size:2.2rem;'>{st.session_state.units}</span> 个球。</div>
    <div class='final-number'>💎 {abstract_number}</div>
</div>
""", unsafe_allow_html=True)

# 物理进位机制与连环聚变的降速观察引擎
if st.session_state.units >= 10:
    st.toast("💥 能量聚变！10个小球合体！", icon="💥")
    alert_placeholder.markdown("<div class='alert-glow' style='background-color:#ffe6e6; color:#d32f2f; border:3px solid #ff3b30;'>🚨 个位盘子满了！10个小球正在聚变合体成 1 个盒子...</div>", unsafe_allow_html=True)
    time.sleep(1.2)
    st.session_state.tens += st.session_state.units // 10
    st.session_state.units = st.session_state.units % 10
    st.rerun()

elif st.session_state.tens >= 10:
    st.toast("📦 盒子打包！10个盒子合体！", icon="📦")
    alert_placeholder.markdown("<div class='alert-glow' style='background-color:#e6f2ff; color:#0056b3; border:3px solid #007aff;'>🚧 十位盒子满了！10个盒子正在打包成 1 个大仓库...</div>", unsafe_allow_html=True)
    st.balloons()
    time.sleep(1.5)
    st.session_state.hundreds += st.session_state.tens // 10
    st.session_state.tens = st.session_state.tens % 10
    st.rerun()

elif st.session_state.hundreds >= 10:
    st.toast("🏭 仓库翻新！10个仓库合体！", icon="🏭")
    alert_placeholder.markdown("<div class='alert-glow' style='background-color:#fffce6; color:#856404; border:3px solid #f1c40f;'>🏗️ 百位仓库满了！10个仓库正在扩建为 1 座超级大工厂...</div>", unsafe_allow_html=True)
    st.snow()
    time.sleep(1.8)
    st.session_state.thousands += st.session_state.hundreds // 10
    st.session_state.hundreds = st.session_state.hundreds % 10
    st.rerun()
