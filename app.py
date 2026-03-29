import streamlit as st
import random

st.set_page_config(page_title="数字进化实验室", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .main-title { text-align: center; color: #007aff; font-size: 3.5rem; font-weight: 900; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); margin-bottom: 2rem; }
    
    /* 将控制台第三列的 primary 按钮变成超级大红按钮 */
    div[data-testid="stColumn"]:nth-child(3) button[kind="primary"] {
        background-color: #ff3b30 !important;
        color: white !important;
        font-size: 2rem !important;
        padding: 30px !important;
        border-radius: 20px !important;
        font-weight: 900 !important;
        box-shadow: 0 8px 16px rgba(255,59,48,0.3) !important;
        border: 4px solid #cc2922 !important;
    }
    
    /* Metric 大小定制 */
    [data-testid="stMetricValue"] {
        font-size: 5rem !important;
        font-weight: 900 !important;
        color: #2c3e50 !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.5rem !important;
        font-weight: bold !important;
        color: #7f8c8d !important;
    }
    
    .password-area {
        background-color: #f8f9fa;
        border: 4px dashed #007aff;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin-top: 50px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .password-digits {
        font-family: 'Courier New', monospace;
        font-size: 5rem;
        font-weight: 900;
        letter-spacing: 1.5rem;
        color: #007aff;
        margin: 15px 0;
        padding-left: 1.5rem;
    }
    
    .badge-area {
        text-align: center;
        margin: 20px 0;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

if 'units' not in st.session_state: st.session_state.units = 0
if 'tens' not in st.session_state: st.session_state.tens = 0
if 'hundreds' not in st.session_state: st.session_state.hundreds = 0
if 'thousands' not in st.session_state: st.session_state.thousands = 0
if 'challenge_target' not in st.session_state: st.session_state.challenge_target = None
if 'effects' not in st.session_state: st.session_state.effects = []

def process_energy(amount):
    st.session_state.units += amount
    st.session_state.effects = []
    
    while st.session_state.units >= 10:
        st.session_state.units -= 10
        st.session_state.tens += 1
        st.session_state.effects.append("toast_ten")
        
    while st.session_state.tens >= 10:
        st.session_state.tens -= 10
        st.session_state.hundreds += 1
        st.session_state.effects.append("balloons")
        
    while st.session_state.hundreds >= 10:
        st.session_state.hundreds -= 10
        st.session_state.thousands += 1
        st.session_state.effects.append("snow")

def on_add_1(): process_energy(1)
def on_add_10(): process_energy(10)
def on_add_100(): process_energy(100)

def generate_challenge():
    st.session_state.challenge_target = random.randint(11, 999)
    st.session_state.units = 0
    st.session_state.tens = 0
    st.session_state.hundreds = 0
    st.session_state.thousands = 0

with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🎯 星际挑战中心</h2>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🎲 生成随机挑战电报", type="primary", use_container_width=True):
        generate_challenge()
        
    if st.session_state.challenge_target:
        st.markdown(f"""
        <div style='background-color:#fff3cd; padding:15px; border-radius:15px; text-align:center; border: 3px solid #ffecb5; margin-top:20px;'>
            <h3 style='color:#856404; margin-top:0;'>指挥官，请拼出这个数：</h3>
            <p style='font-size:3.5rem; font-weight:900; margin-bottom:0; color:#d32f2f;'>{st.session_state.challenge_target}</p>
        </div>
        """, unsafe_allow_html=True)
        
        current_total = st.session_state.thousands * 1000 + st.session_state.hundreds * 100 + st.session_state.tens * 10 + st.session_state.units
        if current_total == st.session_state.challenge_target:
            st.success("🎉 太厉害了！你完美达成了秘密配方！")
            st.balloons()
    else:
        st.info("👈 随时点击上方骰子，开启无限挑战！")
        
    st.markdown("---")
    if st.button("🧹 撤退并清空实验室", use_container_width=True):
        st.session_state.units = 0
        st.session_state.tens = 0
        st.session_state.hundreds = 0
        st.session_state.thousands = 0
        st.session_state.challenge_target = None

st.markdown("<p class='main-title'>🚀 数字进化实验室</p>", unsafe_allow_html=True)

if "snow" in st.session_state.effects:
    st.snow()
    st.markdown("<div class='badge-area'><h1 style='font-size:5rem; margin:0;'>🏅</h1><h2 style='color:#8e44ad; font-weight:900;'>太惊人了！你成功解锁【星际最高指挥官】大勋章！</h2></div>", unsafe_allow_html=True)
elif "balloons" in st.session_state.effects:
    st.balloons()
    st.success("🌋 强大的百位融合突破完成！太棒了！")
elif "toast_ten" in st.session_state.effects:
    st.toast('融合大成功！获得 1 根能量棒 🥢！', icon='💥')

st.session_state.effects = []

col1, col2, col3, col4 = st.columns(4)
col1.metric("千位能量工厂 🏭", st.session_state.thousands)
col2.metric("百位能量方块 📦", st.session_state.hundreds)
col3.metric("十位能量棒 🥢", st.session_state.tens)
col4.metric("个位能量球 🔮", st.session_state.units)

st.write("---")

c1, c2, c3 = st.columns([1, 1, 2], gap="large")
with c1: 
    st.button("🥢 直接放入 10", use_container_width=True, on_click=on_add_10)
with c2: 
    st.button("📦 直接放入 100", use_container_width=True, on_click=on_add_100)
with c3: 
    st.button("🔴 发射 1 个能量球 🔮", use_container_width=True, on_click=on_add_1, type="primary")

st.markdown(f"""
<div class='password-area'>
    <h2 style='color:#333; margin-top:0;'>✍️【解锁新任务】书写密码门</h2>
    <p style='font-size:1.3rem; color:#666; font-weight:bold;'>小指挥官，请在你的纸上写下这段通关密码，然后大声念出来交给图图老师吧！</p>
    <div class='password-digits'>
        {st.session_state.thousands} {st.session_state.hundreds} {st.session_state.tens} {st.session_state.units}
    </div>
</div>
""", unsafe_allow_html=True)
