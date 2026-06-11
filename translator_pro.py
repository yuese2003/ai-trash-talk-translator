import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import json

# ==================== API Key 本地存储 ====================
KEY_FILE = "api_key.json"

def load_api_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("api_key", "")
    return ""

def save_api_key(key):
    with open(KEY_FILE, 'w', encoding='utf-8') as f:
        json.dump({"api_key": key}, f)

if "api_key" not in st.session_state:
    st.session_state.api_key = load_api_key()
if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="AI垃圾话翻译官 Pro", page_icon="🎩", layout="wide")
st.title("🎩 AI 垃圾话翻译官 Pro")
st.markdown("把你最想骂人的话，翻译成最高级的表达方式。支持多风格对比！")

# ==================== 侧边栏 ====================
with st.sidebar:
    st.header("🔑 API设置")
    if not st.session_state.api_key:
        api_key_input = st.text_input("输入你的 DeepSeek API Key", type="password", placeholder="sk-...")
        if st.button("💾 保存 Key", use_container_width=True):
            if api_key_input and api_key_input.startswith("sk-"):
                st.session_state.api_key = api_key_input
                save_api_key(api_key_input)
                st.success("✅ Key 已保存！以后打开直接就能用~")
                st.rerun()
            else:
                st.warning("请输入有效的API Key（以sk-开头）")
    else:
        st.success("✅ Key 已就绪，直接使用！")
        if st.button("🔄 更换 Key", use_container_width=True):
            st.session_state.api_key = ""
            if os.path.exists(KEY_FILE):
                os.remove(KEY_FILE)
            st.rerun()

    st.markdown("---")
    st.header("🎨 翻译风格（可多选）")
    all_styles = ["优雅贵族", "莎士比亚戏剧", "幼儿园老师", "王家卫电影", "宫廷太监宣旨", "霸道总裁", "鲁迅体", "琼瑶体", "东北话", "知乎回答体"]
    selected_styles = st.multiselect("选择一种或多种风格（对比模式）", options=all_styles, default=["优雅贵族"])
    st.markdown("---")
    st.header("📖 风格说明")
    style_descriptions = {
        "优雅贵族": "用优雅繁复的敬语和修辞包装你的愤怒。",
        "莎士比亚戏剧": "用古英语和戏剧化比喻，像哈姆雷特的独白。",
        "幼儿园老师": "用最温柔的语气，像哄小朋友一样纠正你。",
        "王家卫电影": "用王家卫式的独白，把愤怒变成哲学思考。",
        "宫廷太监宣旨": "用太监传旨的口吻，威严中带着谄媚。",
        "霸道总裁": "用霸道总裁的语气，强硬中透着关心。",
        "鲁迅体": "用鲁迅的犀利笔锋和反讽语气表达。",
        "琼瑶体": "用琼瑶式的夸张抒情，撕心裂肺的苦情戏。",
        "东北话": "用东北方言，大碴子味儿接地气。",
        "知乎回答体": "用知乎高赞风格，谢邀开头，最后升华。"
    }
    for style in selected_styles:
        st.caption(f"**{style}**：{style_descriptions.get(style, '')}")

# ==================== 提示词库 ====================
STYLE_PROMPTS = {
    "优雅贵族": "你是一名18世纪法国宫廷的礼仪官。把用户说的任何话都翻译成极其优雅、繁复、充满敬语和修辞的贵族社交辞令。保持原意的同时让每个字都充满贵气。不要直接复述脏话，用高贵的语言包装它。只返回翻译结果，不要加任何解释。",
    "莎士比亚戏剧": "你是威廉·莎士比亚。把用户的话改写成莎士比亚戏剧风格的独白。用古英语、比喻、排比句。用'汝''吾'等古语词。像写《哈姆雷特》的经典独白一样表达。只返回翻译结果，不要加任何解释。",
    "幼儿园老师": "你是一名温柔的幼儿园老师，正在教小朋友文明表达情绪。用户说了粗暴的话，用最温和、最耐心的语气，像哄三岁小孩一样告诉他应该怎么重新表达。用'小宝贝''好孩子'等称呼，大量使用叠词。只返回翻译结果，不要加任何解释。",
    "王家卫电影": "你是王家卫电影里的男主角。把用户的话改写成王家卫式独白。用破碎的短句、文艺的比喻、关于时间与距离的哲学思考。只返回翻译结果，不要加任何解释。",
    "宫廷太监宣旨": "你是一名清朝宫廷太监总管，正在宣读圣旨。把用户的话包装成一道威严中带着谄媚的圣旨。用'奉天承运，皇帝诏曰'开头，用'钦此'结尾。措辞要像太监说话一样尖细做作。只返回翻译结果，不要加任何解释。",
    "霸道总裁": "你是一名霸道总裁，正在对下属或伴侣下达命令。把用户的话翻译成霸道总裁式语录。语气强硬不可拒绝但其实透着关心。用'女人''该死'等霸总高频词汇。只返回翻译结果，不要加任何解释。",
    "鲁迅体": "你是鲁迅，正在写杂文。用犀利的讽刺、反语、文言白话夹杂的方式表达用户的话。喜欢用'大抵''罢了''竟至于此'等词汇。风格参考《狂人日记》。只返回翻译结果，不要加任何解释。",
    "琼瑶体": "你是琼瑶剧的编剧。把用户的话改写成琼瑶式的夸张抒情台词。大量使用'好''极''无比''心痛'等词，多用感叹号和问号，营造撕心裂肺的苦情氛围。只返回翻译结果，不要加任何解释。",
    "东北话": "你是一个东北老铁。用纯正的东北方言翻译用户的话。用'咋地''啥''唠嗑''埋汰''得劲儿'等词汇，语气豪爽接地气。只返回翻译结果，不要加任何解释。",
    "知乎回答体": "你是一个知乎高赞答主。把用户的话改写成知乎回答风格。以'谢邀'开头，进行严谨分析、引用、拆解，最后升华主题加名人名言。只返回翻译结果，不要加任何解释。"
}

# ==================== 主界面 ====================
user_input = st.text_area("💬 输入你想说的话", height=120, placeholder="例如：我真想骂我老板，他今天又让我加班改需求...")
col1, col2, col3 = st.columns([1,1,1])
with col2:
    translate_btn = st.button("🎩 开始翻译", type="primary", use_container_width=True)

# ==================== 翻译逻辑 ====================
if translate_btn:
    if not st.session_state.api_key:
        st.warning("⚠️ 请先在左侧输入并保存API Key")
    elif not user_input:
        st.warning("⚠️ 请输入你想翻译的话")
    elif not selected_styles:
        st.warning("⚠️ 请至少选择一种翻译风格")
    else:
        results = {}
        with st.spinner("🎩 翻译官正在为您净化语言..."):
            try:
                client = OpenAI(api_key=st.session_state.api_key, base_url="https://api.deepseek.com")
                for style in selected_styles:
                    response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {"role": "system", "content": STYLE_PROMPTS[style]},
                            {"role": "user", "content": f"请把下面这句话翻译成目标风格，只返回翻译结果，不要加任何解释：\n\n{user_input}"}
                        ],
                        temperature=0.9
                    )
                    results[style] = response.choices[0].message.content

                # 历史记录
                record = {"time": datetime.now().strftime("%H:%M:%S"), "input": user_input, "styles": selected_styles, "results": results}
                st.session_state.history.insert(0, record)
                if len(st.session_state.history) > 5:
                    st.session_state.history.pop()

                # 显示结果
                st.markdown("---")
                st.subheader("📝 翻译结果")
                st.info(f"🗣️ 原文：{user_input}")
                if len(selected_styles) == 1:
                    style = selected_styles[0]
                    st.success(results[style])
                    st.caption(f"🎨 风格：{style}")
                else:
                    cols = st.columns(len(selected_styles))
                    for i, style in enumerate(selected_styles):
                        with cols[i]:
                            st.markdown(f"**{style}**")
                            st.success(results[style])

                # 分享卡片（改用 st.code 显示纯文本，避免 HTML 解析错误）
                st.markdown("---")
                st.subheader("📸 分享卡片")
                share_text = f"🎩 AI 垃圾话翻译官 Pro\n原文：{user_input}\n"
                for s in selected_styles:
                    share_text += f"\n【{s}】\n{results[s]}\n"
                st.code(share_text, language="text")
                st.caption("👆 可以直接复制文字分享！")

            except Exception as e:
                st.error(f"❌ 翻译失败：{e}")

# ==================== 彩蛋 ====================
if user_input and "彩蛋" in user_input:
    st.balloons()
    st.success("🎉 你发现了彩蛋！嘘，别告诉别人~")

# ==================== 历史记录 ====================
if st.session_state.history:
    with st.expander("📜 最近翻译记录"):
        for i, record in enumerate(st.session_state.history):
            st.caption(f"**{record['time']}** 原文：{record['input'][:50]}...")
            for style in record['styles']:
                st.text(f"  {style}：{record['results'][style][:80]}...")
            if i < len(st.session_state.history)-1:
                st.divider()

st.markdown("---")
st.caption("💡 灵感来源：文明社会需要文明的表达方式。本工具仅供娱乐。 | 彩蛋提示：输入'彩蛋'试试")