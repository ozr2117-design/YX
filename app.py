import streamlit as st
import time

st.set_page_config(page_title="数字爆炸实验室 V3.0", page_icon="🌾", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .main-title { text-align: center; color: #e67e22; font-size: 3.5rem; font-weight: 900; margin-bottom: 2rem; text-shadow: 2px 2px 0px #fcf3cf; }
    
    [data-testid="stMetricValue"] {
        font-size: 5rem !important;
        font-weight: 900 !important;
        color: #2c3e50 !important;
        text-align: center;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.3rem !important;
        font-weight: bold !important;
        color: #7f8c8d !important;
        text-align: center;
    }
    
    [data-testid="column"] button {
        height: 120px !important;
        font-size: 1.6rem !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        color: white !important;
        border: none !important;
        transition: transform 0.1s;
    }
    [data-testid="column"] button:active {
        transform: scale(0.95);
    }
    
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
        from { box-shadow: 0 0 10px #fcf3cf; }
        to { box-shadow: 0 0 30px #f39c12; }
    }
</style>
""", unsafe_allow_html=True)

# Custom colors for Rice Theme buttons (Green, Blue, Purple)
st.markdown("""
<style>
    [data-testid="column"]:nth-child(1) button { background-color: #27ae60 !important; box-shadow: 0 8px 15px rgba(39,174,96,0.3) !important; }
    [data-testid="column"]:nth-child(2) button { background-color: #2980b9 !important; box-shadow: 0 8px 15px rgba(41,128,185,0.3) !important; }
    [data-testid="column"]:nth-child(3) button { background-color: #8e44ad !important; box-shadow: 0 8px 15px rgba(142,68,173,0.3) !important; }
    
    /* 领奖按钮的全局样式放大（不受分栏限制） */
    button[kind="primary"] { font-size: 1.8rem !important; font-weight: bold !important; padding: 20px !important; }
</style>
""", unsafe_allow_html=True)

if 'units' not in st.session_state: st.session_state.units = 0
if 'tens' not in st.session_state: st.session_state.tens = 0
if 'hundreds' not in st.session_state: st.session_state.hundreds = 0
if 'thousands' not in st.session_state: st.session_state.thousands = 0
if 'current_level' not in st.session_state: st.session_state.current_level = 0
if 'level_cleared' not in st.session_state: st.session_state.level_cleared = False

rewards = ["🐯","🐰","🐶","🦊","🐻","🐼","🐨","🦁","🐮","🐷","🐸","🐙","🦑","🦀","🐡","🐠","🐬","🐳","🦖","🦄"]
levels = [
    {"target": 5, "desc": "收集 5 粒碎米 🌾"},
    {"target": 12, "desc": "装满 1 勺米 🥄，还要加上 2 粒 🌾"},
    {"target": 20, "desc": "装满 2 勺米 🥄 (可以使用加速发勺子)"},
    {"target": 35, "desc": "装满 3 勺米 🥄 和 5 粒米 🌾"},
    {"target": 50, "desc": "装满半碗饭：5 勺米 🥄"},
    {"target": 99, "desc": "快要溢出来了！装满 9 勺 🥄 和 9 粒 🌾"},
    {"target": 100, "desc": "直接填满 1 大碗米 🍚！"},
    {"target": 108, "desc": "注意空位：装满 1 碗米 🍚 和 8 粒米 🌾 (不需要加勺子哦)"},
    {"target": 120, "desc": "装满 1 碗米 🍚 和 2 勺米 🥄"},
    {"target": 250, "desc": "装满 2 碗米 🍚 和 5 勺米 🥄"},
    {"target": 384, "desc": "多重挑战：3 碗 🍚，8 勺 🥄，4 粒 🌾"},
    {"target": 500, "desc": "半麻袋米：装满 5 碗 🍚！"},
    {"target": 606, "desc": "小心空缺组合：6 碗米 🍚 和 6 粒米 🌾"},
    {"target": 777, "desc": "幸运农场主：777 (7碗，7勺，7粒)"},
    {"target": 880, "desc": "发发发：8 碗米 🍚 和 8 勺米 🥄"},
    {"target": 999, "desc": "极限大满贯！塞满 9碗 9勺 9粒"},
    {"target": 1000, "desc": "大升级！突破容量获得 1 大袋装米 🎒！"},
    {"target": 1005, "desc": "1 大袋装米 🎒 和 5 粒碎米 🌾"},
    {"target": 1250, "desc": "大进货：1 大袋 🎒，2 碗 🍚，5 勺 🥄"},
    {"target": 2026, "desc": "神秘口令：2026 (2袋，0碗，2勺，6粒)"},
]

for i in range(20):
    levels[i]['reward'] = rewards[i]

def add_units(): st.session_state.units += 1
def add_tens(): st.session_state.tens += 1
def add_hundreds(): st.session_state.hundreds += 1
def reset():
    st.session_state.units = 0
    st.session_state.tens = 0
    st.session_state.hundreds = 0
    st.session_state.thousands = 0
    st.session_state.level_cleared = False

with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🎯 大米工坊通缉令</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    if st.session_state.current_level < 20:
        lvl = levels[st.session_state.current_level]
        st.markdown(f"""
        <div style='background-color:#fff3cd; padding:15px; border-radius:15px; text-align:center; border: 3px solid #ffecb5; margin-bottom:20px;'>
            <h3 style='color:#856404; margin-top:0;'>第 {st.session_state.current_level + 1}/20 关：</h3>
            <p style='font-size:1.3rem; font-weight:bold; color:#d32f2f; line-height:1.5;'>{lvl['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("🎉 你已经打通了所有关卡！你是不可思议的大农场主！")
        
    st.button("🧹 倒空所有大米重来", use_container_width=True, on_click=reset, type="primary")

st.markdown("<p class='main-title'>🌾 大米进化工坊</p>", unsafe_allow_html=True)

alert_placeholder = st.empty()

col1, col2, col3, col4 = st.columns(4)
col1.metric("千位米袋 🎒", st.session_state.thousands)
col2.metric("百位米碗 🍚", st.session_state.hundreds)
col3.metric("十位米勺 🥄", st.session_state.tens)
col4.metric("个位米粒 🌾", st.session_state.units)

carry_in_progress = False

if st.session_state.units >= 10:
    carry_in_progress = True
    st.toast("💥 能量聚变！10粒大米合体！", icon="💥")
    alert_placeholder.markdown("<div class='alert-glow' style='background-color:#eafaf1; color:#145a32; border:3px solid #27ae60;'>🚨 盘子装不下了！10 粒大米正在变成 1 勺大米...</div>", unsafe_allow_html=True)
    time.sleep(1.2)
    st.session_state.tens += st.session_state.units // 10
    st.session_state.units = st.session_state.units % 10
    st.rerun()

elif st.session_state.tens >= 10:
    carry_in_progress = True
    st.toast("🍚 勺子装不下！10勺大米合体！", icon="📦")
    alert_placeholder.markdown("<div class='alert-glow' style='background-color:#ebf5fb; color:#154360; border:3px solid #2980b9;'>🚧 勺子装满了！10 勺大米正在倒进 1 个大碗里...</div>", unsafe_allow_html=True)
    st.balloons()
    time.sleep(1.5)
    st.session_state.hundreds += st.session_state.tens // 10
    st.session_state.tens = st.session_state.tens % 10
    st.rerun()

elif st.session_state.hundreds >= 10:
    carry_in_progress = True
    st.toast("🎒 碗装不下了！10碗大米装袋！", icon="🏭")
    alert_placeholder.markdown("<div class='alert-glow' style='background-color:#f4ecf7; color:#512e5f; border:3px solid #8e44ad;'>🏗️ 大碗溢出了！10 碗大米正在装进 1 个巨大的麻袋...</div>", unsafe_allow_html=True)
    st.snow()
    time.sleep(1.8)
    st.session_state.thousands += st.session_state.hundreds // 10
    st.session_state.hundreds = st.session_state.hundreds % 10
    st.rerun()

# 当进位动画彻底结束后，才做胜负结算
if not carry_in_progress and st.session_state.current_level < 20 and not st.session_state.level_cleared:
    target = levels[st.session_state.current_level]['target']
    current_val = st.session_state.thousands * 1000 + st.session_state.hundreds * 100 + st.session_state.tens * 10 + st.session_state.units
    if current_val == target:
        st.session_state.level_cleared = True
        st.rerun()

if st.session_state.level_cleared:
    st.balloons()
    em = levels[st.session_state.current_level]['reward']
    st.markdown(f"""
    <div style='text-align:center; padding: 40px; background-color: #fffaf0; border-radius: 30px; border: 6px dashed #f39c12; margin-top:20px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);'>
        <h1 style='font-size: 8rem; margin:0;'>{em}</h1>
        <h2 style='color:#e67e22; font-size: 2.2rem; font-weight: 900; margin-top:20px;'>绝妙！奖励稀有动物印章一枚！</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    def claim_reward():
        st.session_state.current_level += 1
        st.session_state.units = 0
        st.session_state.tens = 0
        st.session_state.hundreds = 0
        st.session_state.thousands = 0
        st.session_state.level_cleared = False
        
    st.button("➡️ 把它收进书包，挑战下一关！", type="primary", use_container_width=True, on_click=claim_reward)
    
elif not st.session_state.level_cleared:
    st.write("---")
    st.markdown("<h3 style='text-align:center; color:#7f8c8d; margin-bottom: 20px;'>👇 大米搬运操作台</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="large")
    with c1: st.button("➕ 发射 1 粒", use_container_width=True, on_click=add_units)
    with c2: st.button("⏩ 放 1 勺", use_container_width=True, on_click=add_tens)
    with c3: st.button("⚡ 放 1 碗", use_container_width=True, on_click=add_hundreds)
