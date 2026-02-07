# ChaoXing Automation Tool (LearningX AI Assistant)

## Project Description / 项目描述

**English:**
This project is a Python-based automation tool for the ChaoXing (LearningX) platform. By integrating BeautifulSoup for web parsing and the DeepSeek LLM API, it enables automated question extraction, intelligent answer generation, and form submission. Supporting multiple question types including single-choice, multiple-choice, true/false, and short answers, it provides a comprehensive solution for streamlining academic coursework processing.

**中文：**
本项目是一款基于 Python 开发的超星（学习通）自动化辅助工具。通过结合 BeautifulSoup 网页解析技术与 DeepSeek 大语言模型 API，该工具实现了题目自动抓取、智能答案生成以及数据自动提交功能。它支持单选、多选、判断及简答等多种题型，为课业处理自动化提供了一套完整的解决方案。

## Project Overview
This project is a Python-based automation tool designed for the **ChaoXing (LearningX)** online learning platform. It automates the process of answering quizzes and homework by crawling questions, generating answers using the **DeepSeek LLM**, and submitting them via crafted POST requests.

### Main Technologies
- **Python**: Core scripting language.
- **Requests**: For handling HTTP communications with ChaoXing and the DeepSeek API.
- **BeautifulSoup (bs4)**: For parsing HTML content and extracting questions.
- **DeepSeek API**: Provides AI-generated answers for various question types (Single choice, Multiple choice, Judgment, Essay).
- **PyInstaller**: Used to package the scripts into standalone executables (`.exe`).

## Directory Structure
- `chaoxing_by chuzouX.py` / `chaoxing_1.2 by chuzouX.py`: Main scripts containing the logic for crawling, AI integration, and submission.
- `config.json`: Configuration file containing sensitive data (API keys, cookies, auth salt).
- `input.txt`: A template file where users paste the base POST request data captured from their browser (up to `workTimesEnc=`).
- `password.py`: Likely contains logic for software authorization/verification.
- `build/`, `dist/`, `*.spec`: Artifacts and configuration for the PyInstaller build process.

## Building and Running
### Prerequisites
- Python 3.x
- Required libraries: `requests`, `beautifulsoup4`

### Running the Script
1.  **Configure**: Ensure `config.json` is populated with a valid `API_KEY` (DeepSeek) and `cookie` (from ChaoXing).
2.  **Prepare Input**: Capture a POST request from a ChaoXing quiz submission and paste the content into `input.txt`.
3.  **Execute**:
    ```bash
    python "chaoxing_by chuzouX.py"
    ```
4.  **Workflow**:
    - Provide the quiz URL when prompted.
    - Review extracted questions (saved to `questions.json`).
    - Review AI-generated answers (saved to `questions_with_answers.json`).
    - Confirm submission to send the generated POST data.

### Building Executable
```bash
pyinstaller "chaoxing_by chuzouX.spec"
```

## Development Conventions
- **Functional Structure**: Logic is divided into specialized functions for crawling, extracting, processing, and submitting.
- **Error Handling**: Basic try-except blocks are used for network and file operations.
- **Language**: The user interface (print statements) and some internal logic use Chinese.
- **Security**: Sensitive tokens are stored in `config.json`. **Do not commit this file with real secrets.**

## Key Files Summary
- `questions.json`: Intermediate file storing extracted question metadata.
- `questions_with_answers.json`: Intermediate file storing questions paired with AI-generated responses.
- `generated_post_data.txt`: The final payload ready for submission.
