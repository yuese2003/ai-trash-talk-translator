markdown
# 🎩 AI 垃圾话翻译官 Pro

把你最想骂人的话，翻译成最高级的表达方式。支持多风格对比！

## ✨ 功能特色

- 🔥 **10种翻译风格**：优雅贵族、莎士比亚戏剧、鲁迅体、霸道总裁、王家卫电影……
- 🎨 **多风格对比模式**：一句话同时翻译成多种风格，反差笑点拉满
- 🔑 **API Key 本地存储**：首次输入后自动记住，打开即用，安全不泄露
- 📜 **历史记录**：保留最近5次翻译，方便回顾
- 🎉 **隐藏彩蛋**：输入“彩蛋”试试

## 🚀 快速开始

1. **克隆仓库**
   ```bash
   git clone https://github.com/yuese2003/ai-trash-talk-translator.git
   cd ai-trash-talk-translator
安装依赖

bash
pip install streamlit openai
运行

bash
streamlit run translator_pro.py
获取 API Key

去 platform.deepseek.com 免费注册并获取 API Key

打开网页后，在左侧边栏输入 Key 并点击“保存”

以后打开自动加载，无需重复输入

🛠 技术栈
前端/后端框架：Streamlit

大模型 API：DeepSeek Chat

本地存储：JSON 文件（API Key 持久化）

📝 设计思路
每个翻译风格都遵循“角色设定 + 任务描述 + 风格要求 + 限制条件”的提示词公式，确保翻译结果稳定、有趣、且不会直接复述不文明用语。

⚠️ 注意事项
首次使用需要 DeepSeek API Key，免费额度足够日常使用

API Key 保存在本地 api_key.json，已加入 .gitignore，不会被上传到 GitHub

📸 效果截图
（运行后截图放这里）

📝 License
MIT

text

---

## 第三步：保存

页面往下拉，找到绿色按钮 **"Commit new file"**，**直接点击它**。不需要改任何东西。

---

## 完成

页面刷新后，你的仓库主页就会出现这个README介绍了。以后想改，点README文件 → 点笔的图标，修改后点绿色按钮保存就行。
