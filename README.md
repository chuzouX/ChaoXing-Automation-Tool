# ChaoXing Automation Tool (LearningX AI Assistant)

[中文](#中文) | [English](#english)

---

## English

### ⚠️ IMPORTANT: FOR CODE LEARNING ONLY
**This project is strictly for programming educational purposes and code logic research.** It demonstrates how to integrate web scraping (BeautifulSoup), API communication (Requests), and Large Language Models (DeepSeek) into a cohesive Python workflow. **DO NOT use this tool for any actual academic activities.**

### Disclaimer
**This tool is for educational and research purposes only.**  
1. The author does not encourage, support, or condone any form of academic misconduct or cheating.
2. Using this tool on live platforms may violate the Terms of Service of the ChaoXing (LearningX) platform and could lead to severe consequences, including account suspension or academic disciplinary action.
3. **The user assumes all responsibility** for any consequences arising from the use of this software.
4. The author shall not be held liable for any direct or indirect losses, penalties, or damages incurred.
5. By downloading or using this code, you agree to use it only as a reference for learning Python automation and AI integration.

### Project Introduction
An educational demonstration of a Python-based automation assistant. It showcases how to:
- Use **BeautifulSoup** to parse complex HTML structures.
- Integrate **DeepSeek LLM API** to process natural language queries.
- Manage session-based HTTP requests and data submission.

### Features
- Question extraction logic for structured and unstructured web content.
- Support for mapping AI responses to specific API formats (Single/Multiple choice, etc.).
- Demonstration of secure configuration management.

### Supported Question Types
The tool demonstrates processing logic for:
- **Single Choice** (Type 0): AI mapping to A/B/C/D.
- **Multiple Choice** (Type 1): Concatenation logic (e.g., "AB").
- **True/False** (Type 3): Keyword mapping to boolean states.
- **Essay/Short Answer** (Type 4): HTML content generation.

### Configuration Tutorial
1. **API Key**: For testing, obtain a key from [DeepSeek Platform](https://platform.deepseek.com/).
2. **Cookie**: For learning request headers, find the `Cookie` in Browser DevTools -> Network.
3. **Salt & Password**: 
   - Uses `salt` for local verification logic.
   - Run `python password.py` to see how SHA-512 hashing is implemented.

---

## 中文

### ⚠️ 重要说明：仅用于代码学习
**本项目严格仅限用于编程教学、研究代码逻辑及学术探讨。** 它展示了如何将网页爬虫 (BeautifulSoup)、API 通信 (Requests) 以及大语言模型 (DeepSeek) 整合到 Python 工作流中。**严禁将此工具用于任何真实的课程学习、测验或考试。**

### 免责声明
**本工具仅供教育与研究使用。**  
1. 作者不鼓励、不支持、也不容忍任何形式的学术不端或作弊行为。
2. 在实际平台使用此工具可能违反超星（学习通）平台的服务条款，并可能导致严重后果，包括但不限于账号封禁或学术处分。
3. **用户需自行承担**因使用本软件而产生的一切后果。
4. 作者对因使用本工具而造成的任何直接或间接损失、处分或损害概不负责。
5. 下载或使用本代码即表示您同意仅将其作为学习 Python 自动化和 AI 集成的参考资料。

### 项目介绍
一个用于教学演示的 Python 自动化辅助案例。它展示了以下技术实现：
- 使用 **BeautifulSoup** 解析复杂的 HTML 结构。
- 集成 **DeepSeek LLM API** 处理自然语言查询。
- 管理基于 Session 的 HTTP 请求与数据提交。

### 功能特性
- 针对结构化和非结构化网页内容的题目抓取逻辑。
- 将 AI 响应映射到特定 API 格式（单选/多选等）的逻辑。
- 演示安全的配置管理方案。

### 支持题型
本工具演示了以下题型的处理逻辑：
- **单选题** (类型 0)：AI 结果映射为 A/B/C/D。
- **多选题** (类型 1)：无符号拼接逻辑（如 "AB"）。
- **判断题** (类型 3)：关键词映射为布尔状态。
- **简答题** (类型 4)：HTML 内容生成与格式化。

### 配置教程
1. **API Key**: 仅供测试，从 [DeepSeek 开放平台](https://platform.deepseek.com/) 获取。
2. **Cookie**: 用于学习请求头构造，从浏览器开发者工具 -> 网络中获取。
3. **Salt 与密码**: 
   - 展示本地校验逻辑。
   - 运行 `python password.py` 查看 SHA-512 哈希的实现方式。
