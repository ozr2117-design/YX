import streamlit as st

# --- 页面基本设置 ---
st.set_page_config(
    page_title="数字融合实验室",
    page_icon="🌟",
    layout="centered"
)

# --- 注入卡通化 CSS 样式 ---
st.markdown("""
<style>
    /* 隐藏顶部和主菜单 */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main-title {
        text-align: center;
        color: #ff6b6b;
        font-size: 2.8rem;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .digit-box {
        border-radius: 20px;
        padding: 20px 10px;
        text-align: center;
        margin: 5px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .digit-box:hover {
        transform: scale(1.05);
    }
    /* 马卡龙色系 */
    .thousand-box { background-color: #e0b0ff; border: 5px solid #b366ff; color: #4b0082;}
    .hundred-box { background-color: #ffd085; border: 5px solid #ffa500; color: #cc5500;}
    .ten-box { background-color: #a0c4ff; border: 5px solid #4d94ff; color: #0044cc;}
    .unit-box { background-color: #bbf7d0; border: 5px solid #4ade80; color: #166534;}
    
    .digit-label {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .digit-value {
        font-size: 4rem;
        font-weight: 900;
        line-height: 1;
        font-family: 'Comic Sans MS', 'Arial', sans-serif;
    }
    
    .log-area {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 15px;
        margin-top: 10px;
        border: 4px dashed #ffcccb;
        max-height: 250px;
        overflow-y: auto;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 初始化 Session State ---
if 'units' not in st.session_state: st.session_state.units = 0
if 'tens' not in st.session_state: st.session_state.tens = 0
if 'hundreds' not in st.session_state: st.session_state.hundreds = 0
if 'thousands' not in st.session_state: st.session_state.thousands = 0
if 'logs' not in st.session_state: st.session_state.logs = []
if 'message' not in st.session_state: st.session_state.message = None

def add_log(msg):
    st.session_state.logs.insert(0, msg)
    if len(st.session_state.logs) > 30:
        st.session_state.logs = st.session_state.logs[:30]

def process_energy(amount):
    st.session_state.units += amount
    add_log(f"➕ <b>获得 {amount} 个能量球！</b>")
    
    carry_happened = False

    while st.session_state.units >= 10:
        st.session_state.units -= 10
        st.session_state.tens += 1
        add_log(f"🧨 <b>个位存满！【满十进一】</b> 当前十位：{st.session_state.tens}，剩余个位：{st.session_state.units}")
        carry_happened = True
        
    while st.session_state.tens >= 10:
        st.session_state.tens -= 10
        st.session_state.hundreds += 1
        add_log(f"🌋 <b>十位大爆发！【百倍融合】</b> 当前百位：{st.session_state.hundreds}，剩余十位：{st.session_state.tens}")
        carry_happened = True
        
    while st.session_state.hundreds >= 10:
        st.session_state.hundreds -= 10
        st.session_state.thousands += 1
        add_log(f"🌌 <b>百位终极进阶！【千倍融合】</b> 当前千位：{st.session_state.thousands}，剩余百位：{st.session_state.hundreds}")
        carry_happened = True
        
    if carry_happened:
        st.session_state.message = ("success", "✨ 哇！发生了一连串进位融合！快看看下方战报了解变化！")
    else:
        st.session_state.message = ("info", "💡 能量球已安全加入实验室！")

def on_add_1(): process_energy(1)
def on_add_10(): process_energy(10)
def on_add_custom(): process_energy(st.session_state.custom_amount_input)
def on_reset():
    st.session_state.units = 0
    st.session_state.tens = 0
    st.session_state.hundreds = 0
    st.session_state.thousands = 0
    st.session_state.logs = []
    st.session_state.message = None

# --- 页面 UI 结构 ---
st.markdown("<p class='main-title'>🌟 数字融合实验室 🌟</p>", unsafe_allow_html=True)

if st.session_state.message:
    msg_type, text = st.session_state.message
    if msg_type == "success":
        st.success(text)
    else:
        st.info(text)

col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f"<div class='digit-box thousand-box'><div class='digit-label'>【千】</div><div class='digit-value'>{st.session_state.thousands}</div></div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='digit-box hundred-box'><div class='digit-label'>【百】</div><div class='digit-value'>{st.session_state.hundreds}</div></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='digit-box ten-box'><div class='digit-label'>【十】</div><div class='digit-value'>{st.session_state.tens}</div></div>", unsafe_allow_html=True)
with col4: st.markdown(f"<div class='digit-box unit-box'><div class='digit-label'>【个】</div><div class='digit-value'>{st.session_state.units}</div></div>", unsafe_allow_html=True)

st.write("---")

st.subheader("🎮 控制台的魔法按钮")
c1, c2, c3 = st.columns([1, 1, 2])
with c1: st.button("👆 发射 1 个", use_container_width=True, on_click=on_add_1, type="primary")
with c2: st.button("🚀 发射 10 个", use_container_width=True, on_click=on_add_10, type="primary")
with c3:
    col_input, col_btn = st.columns([2, 1])
    with col_input: st.number_input("想输入多少呢？", min_value=1, max_value=9999, value=15, step=1, label_visibility="collapsed", key="custom_amount_input")
    with col_btn: st.button("🎯 直接发射", use_container_width=True, on_click=on_add_custom)

st.button("🧹 重置实验室", use_container_width=True, on_click=on_reset)

st.write("---")

st.subheader("📜 实验室连环爆破战报")
if not st.session_state.logs:
    st.markdown("<div class='log-area'><p style='text-align:center; color:gray;'>还没有操作记录，快去点击上方按钮发射能量球吧！</p></div>", unsafe_allow_html=True)
else:
    logs_html = "<div class='log-area'>"
    for idx, log in enumerate(st.session_state.logs):
        color = "#000000" if idx == 0 else "#666666"
        logs_html += f"<p style='color: {color}; border-bottom: 1px dotted #ccc; padding-bottom: 5px;'>{log}</p>"
    logs_html += "</div>"
    st.markdown(logs_html, unsafe_allow_html=True)
