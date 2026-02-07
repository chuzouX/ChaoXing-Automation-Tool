# ChaoXing Automation Tool (LearningX AI Assistant)

[中文](#中文) | [English](#english)

---

## English

### Disclaimer
**This tool is for educational and research purposes only.**  
The author does not encourage or support any form of academic misconduct. Using this tool may violate the Terms of Service of the ChaoXing (LearningX) platform and could lead to account suspension or academic penalties. The user assumes all responsibility for any consequences arising from the use of this software. The author shall not be held liable for any direct or indirect losses incurred.

### Project Introduction
A Python-based automation assistant for the ChaoXing platform. It leverages BeautifulSoup for question extraction and the DeepSeek LLM API for generating high-quality answers.

### Features
- Automated extraction of quiz/homework questions.
- Support for multiple question types: Single choice, Multiple choice, True/False, and Essay.
- AI-powered answer generation using DeepSeek.
- Automated submission capability.

### Configuration Tutorial
1. **API Key**: Obtain your API key from the [DeepSeek Platform](https://platform.deepseek.com/).
2. **Cookie**: 
   - Log in to ChaoXing in your browser.
   - Open Developer Tools (F12) -> Network tab.
   - Refresh the page and find any request to `chaoxing.com`.
   - Copy the value of the `Cookie` header from the Request Headers.
3. **Salt & Password**: 
   - The tool uses a `salt` for internal authorization verification.
   - Run `python password.py` and enter a salt string to generate a corresponding password hash.
   - Fill both the `salt` and the generated `password` hash into `config.json`.

### Purpose of `password.py`
`password.py` is a utility script used to generate the authorization password hash required by the main program. It takes a user-provided `salt`, applies a specific transformation, and produces a SHA-512 hash. This ensures that the software is used with the intended authorization parameters.

### Quick Start
1. **Clone the repository**:
   ```bash
   git clone git@github.com:chuzouX/ChaoXing-Automation-Tool.git
   ```
2. **Install dependencies**:
   ```bash
   pip install requests beautifulsoup4
   ```
3. **Configure**:
   Copy `config.json.example` to `config.json` and fill in your DeepSeek API key, cookies, salt, and generated password.
4. **Run**:
   ```bash
   python "chaoxing_by chuzouX.py"
   ```

---

## 中文

### 免责声明
**本工具仅供教育与研究使用。**  
作者不鼓励也不支持任何形式的学术不端行为。使用本工具可能违反超星（学习通）平台的服务条款，并可能导致账号封禁或学术处分。用户需自行承担因使用本软件而产生的一切后果。作者对因使用本工具而造成的任何直接或间接损失概不负责。

### 项目介绍
一个基于 Python 的超星（学习通）平台自动化辅助工具。它利用 BeautifulSoup 进行题目抓取，并集成 DeepSeek 大语言模型 API 生成高质量答案。

### 功能特性
- 自动抓取测验/作业题目。
- 支持多种题型：单选、多选、判断、简答。
- 使用 DeepSeek AI 生成答案。
- 支持自动化提交功能。

### 配置教程
1. **API Key**: 从 [DeepSeek 开放平台](https://platform.deepseek.com/) 获取您的 API Key。
2. **Cookie**: 
   - 在浏览器中登录学习通。
   - 打开开发者工具 (F12) -> 网络 (Network) 选项卡。
   - 刷新页面，找到任何指向 `chaoxing.com` 的请求。
   - 从请求头 (Request Headers) 中复制 `Cookie` 的值。
3. **Salt（盐值）与密码**: 
   - 本工具使用 `salt` 进行内部授权校验。
   - 运行 `python password.py` 并输入一段字符串（Salt），程序将生成对应的密码哈希。
   - 将该 `salt` 字符串和生成的 `password` 哈希填入 `config.json`。

### `password.py` 的作用
`password.py` 是一个辅助脚本，用于生成主程序所需的授权密码哈希。它接收用户输入的 `salt`，通过特定的逻辑转换后生成 SHA-512 哈希值。这确保了软件在预设的授权参数下运行。

### 快速开始
1. **克隆仓库**:
   ```bash
   git clone git@github.com:chuzouX/ChaoXing-Automation-Tool.git
   ```
2. **安装依赖**:
   ```bash
   pip install requests beautifulsoup4
   ```
3. **配置**:
   将 `config.json.example` 复制为 `config.json`，并填入您的 DeepSeek API Key、学习通 Cookie、Salt 以及生成的密码哈希。
4. **运行**:
   ```bash
   python "chaoxing_by chuzouX.py"
   ```