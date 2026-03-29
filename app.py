import streamlit as st

st.set_page_config(page_title="数字融合实验室", page_icon="🌟", layout="wide")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .main-title { text-align: center; color: #ff6b6b; font-size: 2.8rem; font-weight: 900; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); margin-bottom: 2rem; }
    
    .digit-box { border-radius: 20px; padding: 20px 10px; text-align: center; margin: 5px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); transition: transform 0.2s; }
    .digit-box:hover { transform: scale(1.05); }
    .thousand-box { background-color: #e0b0ff; border: 5px solid #b366ff; color: #4b0082;}
    .hundred-box { background-color: #ffd085; border: 5px solid #ffa500; color: #cc5500;}
    .ten-box { background-color: #a0c4ff; border: 5px solid #4d94ff; color: #0044cc;}
    .unit-box { background-color: #bbf7d0; border: 5px solid #4ade80; color: #166534;}
    
    .digit-label { font-size: 1.5rem; font-weight: bold; margin-bottom: 5px; }
    .digit-value { font-size: 4rem; font-weight: 900; line-height: 1; font-family: 'Comic Sans MS', 'Arial', sans-serif; }
    
    .log-area { background-color: #ffffff; border-radius: 15px; padding: 15px; border: 4px dashed #ffcccb; height: 620px; overflow-y: auto; }
    
    .log-card { border-radius: 15px; padding: 15px; margin-bottom: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .add-card { background-color: #f8f9fa; border: 2px dashed #ced4da; font-size: 1.2rem; font-weight: bold; color: #495057;}
    
    .carry-row { display: flex; align-items: center; justify-content: center; gap: 10px; flex-wrap: nowrap; }
    @media (max-width: 800px) {
        .carry-row { flex-wrap: wrap; }
        .carry-10 { max-width: 100% !important; }
    }
    .carry-10 { font-size: 1.5rem; line-height: 1.3; max-width: 50%; text-align: center;}
    .carry-arrow { font-size: 1.8rem; font-weight: bold; }
    .carry-1 { font-size: 1.8rem; text-align: center;}
    .sub-num { font-size: 1rem; color: #666; font-weight: bold; }
    
    .level-card { background-color:#fff3cd; padding:15px; border-radius:15px; border: 4px solid #ffecb5; margin-bottom: 20px; text-align:center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .level-success { background-color:#d4edda; padding:15px; border-radius:15px; border: 4px solid #c3e6cb; margin-bottom: 20px; text-align:center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

levels = [
    {"u":0, "t":1, "h":0, "th":0, "clear": True, "desc": "魔法初现：获得你的第一条鲸鱼 🐳<br><span style='font-size:1rem;color:gray;'>(一直发射能量球就能见证爆炸)</span>"},
    {"u":2, "t":1, "h":0, "th":0, "clear": True, "desc": "拼图入门：变出 1 条鲸鱼 🐳 + 2 个苹果 🍏"},
    {"u":0, "t":2, "h":0, "th":0, "clear": True, "desc": "捷径法术：变出 2 条鲸鱼 🐳<br><span style='font-size:1rem;color:gray;'>(用大大的🚀按钮试试)</span>"},
    {"u":5, "t":3, "h":0, "th":0, "clear": True, "desc": "灵活搭配：变出 3 条鲸鱼 🐳 + 5 个苹果 🍏"},
    {"u":0, "t":5, "h":0, "th":0, "clear": True, "desc": "一半的百位：凑齐 5 条鲸鱼 🐳"},
    {"u":9, "t":9, "h":0, "th":0, "clear": False, "desc": "大爆炸前夕：铺满 9 条鲸鱼 🐳 + 9 个苹果 🍏<br><span style='font-size:1rem;color:gray;'>(马上就有奇观发生了！)</span>"},
    {"u":0, "t":0, "h":1, "th":0, "clear": True, "desc": "🌋召唤仪式：【别清空！】就在刚才的基础上再发射 1 个，见证变出大橘子 🍊！"},
    {"u":8, "t":0, "h":1, "th":0, "clear": True, "desc": "缺位的谜团：1 个大橘子 🍊 + 8 个苹果 🍏<br><span style='font-size:1rem;color:gray;'>(注意避开鲸鱼哦)</span>"},
    {"u":0, "t":5, "h":2, "th":0, "clear": True, "desc": "三位大拼图：2 个大橘子 🍊 + 5 条鲸鱼 🐳"},
    {"u":0, "t":0, "h":0, "th":1, "clear": True, "desc": "🌌终极密码：使用下面靶子上的【直接发射】，一口气输入超级数字召唤紫葡萄 🍇！"},
]

if 'units' not in st.session_state: st.session_state.units = 0
if 'tens' not in st.session_state: st.session_state.tens = 0
if 'hundreds' not in st.session_state: st.session_state.hundreds = 0
if 'thousands' not in st.session_state: st.session_state.thousands = 0
if 'logs' not in st.session_state: st.session_state.logs = []
if 'message' not in st.session_state: st.session_state.message = None
if 'current_level' not in st.session_state: st.session_state.current_level = 0
if 'level_just_cleared' not in st.session_state: st.session_state.level_just_cleared = False

def get_emoji(level):
    if level == 1: return "🍏"
    elif level == 10: return "🐳"
    elif level == 100: return "🍊"
    elif level == 1000: return "🍇"
    return "⚡"

def html_for_add(amount):
    if amount <= 20:
        icons = " ".join(["🍏"] * amount)
        return f"<div class='log-card add-card'>➕ 获得能量球：<br><span style='font-size: 2.2rem;'>{icons}</span></div>"
    else:
        return f"<div class='log-card add-card'>➕ 获得大量能量球：<span style='font-size: 1.8rem;'>{amount}</span> 个 🍏</div>"

def html_for_carry(from_level, to_level):
    from_emoji = get_emoji(from_level)
    to_emoji = get_emoji(to_level)
    icons_10 = " ".join([from_emoji] * 10)
    bg_color = {1:"#e6f9ec", 10:"#e6f0ff", 100:"#fff3e6"}[from_level]
    border_color = {1:"#4ade80", 10:"#4d94ff", 100:"#ffa500"}[from_level]
    
    return f"""
    <div class='log-card carry-card' style='background-color: {bg_color}; border: 3px solid {border_color};'>
        <div class='carry-row'>
            <div class='carry-10'>
                {icons_10}<br>
                <span class='sub-num'>10 个 {from_emoji}</span>
            </div>
            <div class='carry-arrow'>
                💥 ➡️ 
            </div>
            <div class='carry-1'>
                <span style='font-size: 3rem;'>{to_emoji}</span><br>
                <span class='sub-num'>变成 1 个 {to_emoji}</span>
            </div>
        </div>
    </div>
    """

def add_log(html_msg):
    st.session_state.logs.insert(0, html_msg)
    if len(st.session_state.logs) > 30:
        st.session_state.logs = st.session_state.logs[:30]

def process_energy(amount):
    st.session_state.units += amount
    add_log(html_for_add(amount))
    
    carry_happened = False
    while st.session_state.units >= 10:
        st.session_state.units -= 10
        st.session_state.tens += 1
        add_log(html_for_carry(1, 10))
        carry_happened = True
        
    while st.session_state.tens >= 10:
        st.session_state.tens -= 10
        st.session_state.hundreds += 1
        add_log(html_for_carry(10, 100))
        carry_happened = True
        
    while st.session_state.hundreds >= 10:
        st.session_state.hundreds -= 10
        st.session_state.thousands += 1
        add_log(html_for_carry(100, 1000))
        carry_happened = True
        
    if st.session_state.current_level < len(levels) and not st.session_state.level_just_cleared:
        goal = levels[st.session_state.current_level]
        if (st.session_state.units == goal['u'] and 
            st.session_state.tens == goal['t'] and 
            st.session_state.hundreds == goal['h'] and 
            st.session_state.thousands == goal['th']):
            st.session_state.level_just_cleared = True
            st.session_state.message = None
            return

    if carry_happened:
        st.session_state.message = ("success", "✨ 发生了一连串进位大融合！快向左看图形战报！")
    else:
        st.session_state.message = ("info", "✅ 能量球已安全装入实验室！")

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

# --- 页面 UI 结构 (左右分栏布局) ---
col_left, col_right = st.columns([1, 2.2], gap="large")

with col_left:
    st.subheader("📜 图形化连环战报")
    if not st.session_state.logs:
        st.markdown("<div class='log-area'><p style='text-align:center; color:gray; font-size:1.3rem; margin-top:200px;'>这里空空的，快去右边点击发送能量球吧！👆</p></div>", unsafe_allow_html=True)
    else:
        logs_html = "<div class='log-area'>" + "".join(st.session_state.logs) + "</div>"
        st.markdown(logs_html, unsafe_allow_html=True)

with col_right:
    st.markdown("<p class='main-title'>🌟 数字融合实验室 🌟</p>", unsafe_allow_html=True)
    
    if st.session_state.current_level < len(levels):
        goal = levels[st.session_state.current_level]
        st.markdown(f"""
        <div class='level-card'>
            <h3 style='color:#856404; margin-top:0;'>🏆 闯关任务 (第 {st.session_state.current_level + 1} 关 / 共 10 关)</h3>
            <p style='font-size:1.5rem; font-weight:bold; margin-bottom:0;'>目标：{goal['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='level-success'>
            <h3 style='color:#155724; margin-top:0;'>👑 究极融合之皇！通关啦！</h3>
            <p style='font-size:1.5rem; font-weight:bold; margin-bottom:0;'>所有的十进制魔法拼图都被你解开了！</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(f"<div class='digit-box thousand-box'><div class='digit-label'>【千】🍇</div><div class='digit-value'>{st.session_state.thousands}</div></div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='digit-box hundred-box'><div class='digit-label'>【百】🍊</div><div class='digit-value'>{st.session_state.hundreds}</div></div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='digit-box ten-box'><div class='digit-label'>【十】🐳</div><div class='digit-value'>{st.session_state.tens}</div></div>", unsafe_allow_html=True)
    with col4: st.markdown(f"<div class='digit-box unit-box'><div class='digit-label'>【个】🍏</div><div class='digit-value'>{st.session_state.units}</div></div>", unsafe_allow_html=True)

    if st.session_state.level_just_cleared:
        st.balloons()
        st.success("🎉 太棒啦！你完美拼出了任务要求的图案图案！")
        def next_lvl():
            if levels[st.session_state.current_level]['clear']:
                st.session_state.units = 0
                st.session_state.tens = 0
                st.session_state.hundreds = 0
                st.session_state.thousands = 0
                st.session_state.logs = []
            st.session_state.current_level += 1
            st.session_state.level_just_cleared = False
        st.button("🎁 领取奖励，点击挑战下一关！", type="primary", use_container_width=True, on_click=next_lvl)
    else:
        if st.session_state.message:
            msg_type, text = st.session_state.message
            if msg_type == "success": st.success(text)
            else: st.info(text)

        st.write("---")
        st.subheader("🎮 魔法控制台")
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1: st.button("👆 发射 1 个🍏", use_container_width=True, on_click=on_add_1, type="primary")
        with c2: st.button("🚀 发射 10 个🍏", use_container_width=True, on_click=on_add_10, type="primary")
        with c3:
            col_input, col_btn = st.columns([2, 1])
            with col_input: st.number_input("想要多少个🍏？", min_value=1, max_value=9999, value=15, step=1, label_visibility="collapsed", key="custom_amount_input")
            with col_btn: st.button("🎯 直接发射！", use_container_width=True, on_click=on_add_custom)
            
        st.button("🧹 重置并清空实验室", use_container_width=True, on_click=on_reset, type="secondary")
