import requests
from bs4 import BeautifulSoup
import os
import re
import json
import requests
import time
import urllib.parse
import random
import hashlib

def check_and_create_config():
    """
    检查当前目录下是否存在config.json文件，如果不存在则创建默认配置文件
    """
    config_file = "config.json"
    input_f = "input.txt"

    if not os.path.exists(input_f):
        print("⚠ 未找到input.txt配置文件")
        print("正在创建默认配置文件...")

        try:
            # 写入默认配置文件
            with open(input_f, 'w', encoding='utf-8') as f:
                json.dump("", f, ensure_ascii=False, indent=4)
            
            print(f"✅ 已创建默认配置文件: {input_f}")

        except Exception as e:
            print(f"❌ 创建input.txt文件失败: {e}")
            return False

    if not os.path.exists(config_file):
        print("⚠ 未找到config.json配置文件")
        print("正在创建默认配置文件...")
        
        salt = ""

        for i in range(16):
            salt = salt + str(random.sample('zyxwvutsrqponmlkjihgfedcba',1)[0])

        # 默认配置内容
        default_config = {
            "API_KEY": "YOUR_DEEPSEEK_API_KEY_HERE",
            "cookie": "YOUR_COOKIE",
            "salt": salt,
            "password": "SOFTWARE_YOUR_PASSWORD",
        }
        
        try:
            # 写入默认配置文件
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=4)
            
            print(f"✅ 已创建默认配置文件: {config_file}")
            print("请编辑此文件，填入您的实际API_KEY（deepseek）和cookie值")
            input("按任意键退出.......")
            os._exit(0)

            
        except Exception as e:
            print(f"❌ 创建配置文件失败: {e}")
            return False
    else:
        print(f"✅ 配置文件 {config_file} 已存在")
        return True

def load_config():
    """
    从config.json文件中读取配置
    """
    config_file = "config.json"
    
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            Salt1 = config.get("salt", "")

            if Salt1:
                global Salt
                Salt = config.get("salt", "")
            else:
                print("⚠ 加载加密salt出错，请删除config.json文件重新配置")
                input("按任意键退出.......")
                os._exit(0)
            
            global password
            password = config.get("password", "")

            # 读取API_KEY
            api_key = config.get("API_KEY", "")
            if api_key and api_key != "YOUR_DEEPSEEK_API_KEY_HERE":
                global API_KEY
                API_KEY = api_key
                print(f"✓ 已从配置文件加载API_KEY（deepseek）")
            else:
                print("⚠ API_KEY未配置或使用默认值，请检查config.json文件")
            
            # 读取cookie
            cookie = config.get("cookie", "")
            if cookie and cookie != "YOUR_COOKIE":
                return cookie
            else:
                print("⚠ cookie未配置或使用默认值，请检查config.json文件")
                return None
        else:
            print(f"⚠ 配置文件 {config_file} 不存在")
            return None
            
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return None

def send_post_from_file(file_path):
    """
    简化版本：直接从文件发送POST请求
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单解析（适用于标准格式）
    lines = content.split('\n')
    
    # 提取URL（第一行）
    url_line = lines[0]
    url = "https://" + lines[1].replace('Host: ', '') + url_line.split(' ')[1]
    
    # 收集headers
    headers = {}
    body_started = False
    body_lines = []
    
    for line in lines[1:]:
        if not line.strip():  # 空行，开始body
            body_started = True
            continue
            
        if body_started:
            body_lines.append(line)
        else:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
    
    # 请求体
    body = '\n'.join(body_lines)
    
    # 发送请求
    response = requests.post(url, data=body, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    
    return response



def read_base_post_from_file(filename):
    """
    从文件中读取POST数据的基础部分（从开始到workTimesEnc=）
    
    Args:
        filename (str): 文件名
        
    Returns:
        str: 基础POST数据部分
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # 查找workTimesEnc=的位置
        if 'workTimesEnc=' not in content:
            print(f"错误：文件 {filename} 中未找到workTimesEnc=")
            return None
        
        # 提取从开始到workTimesEnc=的部分（包含workTimesEnc=）
        base_part = content.split('workTimesEnc=')[0] + 'workTimesEnc='
        
        return base_part
    
    except FileNotFoundError:
        print(f"错误：找不到文件 {filename}")
        return None
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return None

def generate_answer_section(questions_list):
    """
    根据题目列表生成答案部分（多选题已改为无逗号拼接）
    """
    answer_params = {}
    
    for question in questions_list:
        question_id = question['questionID'].replace('question', '')
        question_type = question['questiontype']
        api_answer = question.get('api_answer', '')
        
        # 设置题型
        answer_params[f'answertype{question_id}'] = str(question_type)
        
        # 选择题（单选0、多选1）共用同一个处理函数，已支持 AB 格式
        if question_type in (0, 1):
            answer_text = map_choice_answer(api_answer)
            answer_params[f'answer{question_id}'] = answer_text
            
        elif question_type == 3:  # 判断题
            answer_text = map_judgment_answer(api_answer)
            answer_params[f'answer{question_id}'] = answer_text
            
        elif question_type == 4:  # 简答题
            answer_text = format_essay_answer(api_answer)
            answer_params[f'answer{question_id}'] = answer_text
    
    return answer_params

def map_choice_answer(answer_text):
    """
    映射选择题答案（单选题返回单个字母，多选题返回无符号拼接的字母组合）
    超星要求：多选题 answer=AB  而不是 A,B
    """
    if not answer_text:
        return ''
    
    # 提取所有大写字母 A-D
    matches = re.findall(r'[A-D]', answer_text.upper())
    
    if not matches:
        # 没提取到就随机兜底
        import random
        return random.choice(['A', 'B', 'C', 'D'])
    
    # 去重 + 按字母顺序排序（超星后台一般按ABCD顺序存）
    unique_options = sorted(set(matches))
    
    # 直接拼接，不加任何符号！这就是关键！
    return ''.join(unique_options)

def map_judgment_answer(answer_text):
    """
    映射判断题答案
    
    Args:
        answer_text (str): API返回的答案
        
    Returns:
        str: 'true' 或 'false'
    """
    if not answer_text:
        return 'false'
    
    # 根据答案内容判断正误
    positive_keywords = ['是', '正确', '对', '可以', '能够', '支持', '同意', 'true', '正确']
    negative_keywords = ['不是', '错误', '错', '不可以', '不能', '反对', '不同意', 'false', '错误']
    
    answer_lower = answer_text.lower()
    
    for keyword in positive_keywords:
        if keyword in answer_lower:
            return 'true'
    
    for keyword in negative_keywords:
        if keyword in answer_lower:
            return 'false'
    
    return 'false'

def format_essay_answer(answer_text):
    """
    格式化简答题答案
    
    Args:
        answer_text (str): API返回的答案
        
    Returns:
        str: HTML格式的答案
    """
    if not answer_text:
        return ''
    
    # 清理答案文本
    answer_text = answer_text.strip()
    
    # 如果答案已经包含HTML标签，直接返回
    if re.search(r'<[^>]+>', answer_text):
        return answer_text
    
    # 将答案按段落分割
    paragraphs = [p.strip() for p in answer_text.split('\n') if p.strip()]
    
    if len(paragraphs) == 1:
        # 单段落使用p标签
        return f'<p>{paragraphs[0]}</p>'
    else:
        # 多段落使用有序列表
        list_items = ''.join([f'<li><p>{p}</p></li>' for p in paragraphs])
        return f'<ol class=" list-paddingleft-2" style="list-style-type: decimal;">{list_items}</ol>'

def build_complete_post_data(base_part, answer_params):
    """
    构建完整的POST数据
    
    Args:
        base_part (str): 基础POST数据部分
        answer_params (dict): 答案参数字典
        
    Returns:
        str: 完整的POST数据
    """
    # 将答案参数转换为URL编码格式
    answer_str = urllib.parse.urlencode(answer_params)
    
    # 合并基础部分和答案部分
    complete_data = base_part + '&' + answer_str
    
    return complete_data

def display_generated_content(answer_params, complete_data):
    """
    显示生成的内容
    
    Args:
        answer_params (dict): 答案参数字典
        complete_data (str): 完整的POST数据
    """
    print("\n" + "="*80)
    print("生成的答案部分")
    print("="*80)
    
    # 统计各题型数量
    single_choice = sum(1 for k in answer_params.keys() if k.startswith('answertype') and answer_params[k] == '0')
    multiple_choice = sum(1 for k in answer_params.keys() if k.startswith('answertype') and answer_params[k] == '1')
    judgment = sum(1 for k in answer_params.keys() if k.startswith('answertype') and answer_params[k] == '3')
    essay = sum(1 for k in answer_params.keys() if k.startswith('answertype') and answer_params[k] == '4')
    
    print(f"\n题目类型统计:")
    print(f"  单选题: {single_choice} 题")
    print(f"  多选题: {multiple_choice} 题")
    print(f"  判断题: {judgment} 题")
    print(f"  简答题: {essay} 题")
    
    print(f"\n生成的答案参数数量: {len(answer_params) // 2} 个题目")
    
    # 显示前几个答案参数作为示例
    # print("\n答案参数示例 (前5个):")
    # count = 0
    # for key, value in answer_params.items():
    #     if count >= 10:  # 显示5对参数 (answertype和answer)
    #         break
    #     print(f"  {key} = {value[:50]}{'...' if len(value) > 50 else ''}")
    #     count += 1
    
    print(f"\n完整数据长度: {len(complete_data)} 字符")
    print(f"\n生成的完整POST数据 (前500字符):")
    print(complete_data[:500] + "..." if len(complete_data) > 500 else complete_data)


# DeepSeek API配置
API_URL = "https://api.deepseek.com/v1/chat/completions"

def get_answer_from_deepseek(question, question_type):
    """
    调用DeepSeek API获取问题答案
    
    Args:
        question (str): 问题内容
        question_type (int): 题目类型 (0=单选题, 1=多选题, 3=判断题, 4=简答题)
        
    Returns:
        str: API返回的答案内容
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 根据题目类型构建不同的提示语
    if question_type == 0:  # 单选题
        prompt = f"题目为：{question}，请用直接回答A或B或C或D"
    elif question_type == 1:  # 多选题
        prompt = f"题目为：{question}，请用直接回答正确的多个选项，如答案选择A和B，你将回答AB"
    elif question_type == 3:  # 判断题
        prompt = f"题目为：{question}，请用直接回答正确或错误"
    elif question_type == 4:  # 简答题
        prompt = f"题目为：{question}，请用150字内语言回答，且不使用标序号等排列方式"
    else:
        prompt = f"题目为：{question}，请回答"
    
    # 构建请求数据
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        answer = result["choices"][0]["message"]["content"].strip()
        return answer
        
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"解析API响应失败: {e}")
        return None

def process_questions(questions_list):
    """
    处理题目列表，为每个题目添加API答案
    
    Args:
        questions_list (list): 题目列表
        
    Returns:
        list: 处理后的题目列表
    """
    processed_questions = []
    
    for i, question_data in enumerate(questions_list):
        print(f"正在处理第 {i+1}/{len(questions_list)} 个题目...")
        
        # 复制原始题目数据
        processed_question = question_data.copy()
        
        # 获取题目内容和类型
        question_content = processed_question.get("content", "")
        question_type = processed_question.get("questiontype", -1)
        
        if question_content:
            # 调用API获取答案
            answer = get_answer_from_deepseek(question_content, question_type)
            
            if answer:
                processed_question["api_answer"] = answer
                print(f"✓ 成功获取第 {i+1} 题答案")
            else:
                processed_question["api_answer"] = "获取答案失败"
                print(f"✗ 第 {i+1} 题答案获取失败")
        else:
            processed_question["api_answer"] = "题目内容为空"
            print(f"! 第 {i+1} 题内容为空")
        
        processed_questions.append(processed_question)
        
        # 添加延迟避免频繁调用
        time.sleep(1)
    
    return processed_questions


def crawl_chaoxing_page(cookie_string=None):
    # 目标URL
    url = str(input("请输入URL(请自行设置cookie)："))
    
    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    # 准备Cookie
    cookies = {}
    if cookie_string:
        # 将Cookie字符串转换为字典
        cookie_items = cookie_string.split(';')
        for item in cookie_items:
            if '=' in item:
                key, value = item.strip().split('=', 1)
                cookies[key] = value
    
    try:
        # 发送GET请求
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        
        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 获取页面标题
            title = soup.title.string if soup.title else "无标题"
            
            # 获取页面文本内容（去除多余空白）
            text_content = soup.get_text(separator='\n', strip=True)
            
            return {
                'status': 'success',
                'title': title,
                'content': text_content,
                'html': response.text  # 保留原始HTML内容
            }
        else:
            return {
                'status': 'error',
                'message': f'请求失败，状态码: {response.status_code}',
                'status_code': response.status_code
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'status': 'error',
            'message': f'请求异常: {str(e)}'
        }

def extract_questions_from_html(html_content):
    """
    从HTML内容中直接提取题目信息，包括选项
    
    Args:
        html_content (str): HTML内容
        
    Returns:
        list: 包含题目信息的字典列表
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    questions = []
    question_divs = soup.find_all('div', class_='questionLi')
    
    for div in question_divs:
        number = extract_question_number_from_div(div)
        qtype = div.get('typename', '')
        
        timu = div.find('div', class_='TiMu')
        if not timu:
            continue
        
        # 提取问题文本
        problem_div = timu.find('div', class_='Zy_ulTop')
        problem = problem_div.text.strip() if problem_div else ''
        
        # 提取选项
        options_div = timu.find('div', class_='Zy_ulBottom')
        options = []
        if options_div:
            for opt in options_div.find_all('a', class_='ansA'):
                letter_span = opt.find('span', class_='letter_num')
                letter = letter_span.text.strip() if letter_span else ''
                text = opt.text.replace(letter, '').strip()
                options.append(f"{letter} {text}")
        
        # 构建完整内容
        full_content = problem
        if options:
            full_content += '\n' + '\n'.join(options)
        
        full_content = re.sub(r'\s+', ' ', full_content).strip()
        
        questions.append({
            "number": number,
            "type": qtype,
            "content": full_content,
            "full_question": f"{number}. ({qtype}) {full_content}"
        })
    
    return questions

def extract_questions_info_from_html(html_content):
    """
    从HTML内容中提取题目的questionID和questiontype信息
    
    Args:
        html_content (str): HTML内容
        
    Returns:
        dict: 以题号为键，包含questionID和questiontype的字典为值
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    question_divs = soup.find_all('div', class_='questionLi')
    
    questions_info = {}
    
    # 题型映射字典
    question_type_mapping = {
        '单选题': 0,
        '多选题': 1,
        '判断题': 3, 
        '简答题': 4
    }
    
    for div in question_divs:
        # 提取questionID
        question_id = div.get('id', '')
        if not question_id or not question_id.startswith('question'):
            continue
        
        # 提取题型并转换为数字
        question_type = div.get('typename', '')
        questiontype_num = question_type_mapping.get(question_type, -1)  # -1表示未知题型
        
        # 提取题号
        question_number = extract_question_number_from_div(div)
        
        # 保存题目信息
        questions_info[question_number] = {
            "questionID": question_id,
            "questiontype": questiontype_num
        }
    
    return questions_info

def extract_question_number_from_div(question_div):
    """
    从题目div中提取题号
    
    Args:
        question_div: BeautifulSoup解析的题目div元素
        
    Returns:
        int: 题号
    """
    # 尝试从aria-label中提取题号
    aria_label = question_div.get('aria-label', '')
    if aria_label:
        match = re.search(r'题目\s*(\d+)', aria_label)
        if match:
            return int(match.group(1))
    
    # 如果没有找到，返回0
    return 0

def enhance_questions_with_html_info(questions, html_info):
    """
    使用HTML信息增强题目数据
    
    Args:
        questions (list): 题目列表
        html_info (dict): 从HTML提取的题目信息
        
    Returns:
        list: 增强后的题目列表
    """
    enhanced_questions = []
    
    for question in questions:
        question_number = question["number"]
        
        if question_number in html_info:
            enhanced_question = question.copy()
            enhanced_question.update(html_info[question_number])
            enhanced_questions.append(enhanced_question)
        else:
            # 如果没有找到对应的HTML信息，保持原样
            enhanced_questions.append(question)
    
    return enhanced_questions

def save_questions_to_json(questions, filename="questions.json"):
    """将题目保存为JSON文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"题目已保存到JSON文件: {filename}")

if __name__ == "__main__":

    check_and_create_config()

    CONFIG_COOKIE = load_config()
    if CONFIG_COOKIE:
        YOUR_COOKIE = CONFIG_COOKIE
        print("✓ 使用配置文件中的cookie")
    else:
        input("按任意键退出.......")
        os._exit(0)

    # 在这里设置你的Cookie值
    # 格式示例: "name1=value1; name2=value2"
    
    # 如果未设置Cookie，使用空值
    if YOUR_COOKIE == "你的Cookie字符串":
        print("请注意：你尚未设置有效的Cookie值")
        use_cookie = input("是否继续不使用Cookie访问？(y/n): ")
        if use_cookie.lower() != 'y':
            input("按任意键退出.......")
            os._exit(0)
        cookie_value = None
    else:
        cookie_value = YOUR_COOKIE
    
    # 执行爬取
    print("="*50)
    print("欢迎使用此脚本 脚本作者：chuzouX/@一只离开出走世界")
    print("请关注作者b站以获得最新版本")
    print("本脚本接入的AI为deepseek")
    print("="*50)
    Salt = Salt[::-1]+"xy521"
    Ypassword = hashlib.sha512(Salt.encode()).hexdigest()
    if password != Ypassword:
        print("⚠ 软件密码错误或未设置，请联系作者授权")
        input("按任意键退出.......")
        os._exit(0)
    print(f"✓ 已验证密码，软件使用已经过作者授权")
    print("="*50)
    print("开始爬取超星页面...")
    result = crawl_chaoxing_page(cookie_value)
    
    # 处理结果
    if result['status'] == 'success':
        print(f"爬取成功！")
        print(f"页面标题: {result['title']}")
        
        # 提取题目
        questions = extract_questions_from_html(result['html'])
        
        if questions:
            print(f"成功提取到 {len(questions)} 个题目")
            
            # 从HTML中提取题目信息
            html_info = extract_questions_info_from_html(result['html'])
            print(f"从HTML中提取到 {len(html_info)} 个题目的ID和类型信息")
            
            # 使用HTML信息增强题目数据
            enhanced_questions = enhance_questions_with_html_info(questions, html_info)
            
            # 统计增强的题目数量
            enhanced_count = sum(1 for q in enhanced_questions if 'questionID' in q)
            print(f"成功增强 {enhanced_count} 个题目的信息")
            
            # 将题目保存为JSON格式的变量
            questions_json = json.dumps(enhanced_questions, ensure_ascii=False, indent=2)
            
            # 显示题目预览
            print("\n题目预览:")
            for i, question in enumerate(enhanced_questions[:3]):  # 只显示前3个题目预览
                print(f"\n题目 {i+1}:")
                print(f"  题号: {question['number']}")
                print(f"  题型: {question['type']}")
                if 'questionID' in question:
                    print(f"  ID: {question['questionID']}")
                if 'questiontype' in question:
                    print(f"  题型代码: {question['questiontype']}")
                content_preview = question['content'][:100] + "..." if len(question['content']) > 100 else question['content']
                print(f"  内容: {content_preview}")
            
            # 特别显示最后一个题目
            if len(enhanced_questions) > 3:
                print(f"\n最后一个题目预览:")
                last_question = enhanced_questions[-1]
                print(f"  题号: {last_question['number']}")
                print(f"  题型: {last_question['type']}")
                if 'questionID' in last_question:
                    print(f"  ID: {last_question['questionID']}")
                print(f"  内容: {last_question['content']}")
            
            # 询问是否保存到文件
            save_file = input("\n是否将题目保存为JSON文件？(y/n): ")
            if save_file.lower() == 'y':
                filename = input("输入文件名（默认: questions.json）: ").strip()
                if not filename:
                    filename = "questions.json"
                save_questions_to_json(enhanced_questions, filename)
            else:
                continue1=input("\n是否继续(y/n): ")
                if continue1.lower() == 'n' or not continue1:
                    input("按任意键退出.......")
                    os._exit(0)

            
            # 显示JSON变量
            print("\n题目JSON变量:")
            print("=" * 50)
            print("questions_json = ", end="")
            print(questions_json)
            print("=" * 50)
            
            # 提示如何使用这个变量
            print("\n使用提示: 你可以将上面的JSON字符串赋值给变量，或者直接使用questions列表")
            
        else:
            print("未找到符合格式的题目")
            print("\n原始内容预览:")
            preview = result['content'][:500] + "..." if len(result['content']) > 500 else result['content']
            print(preview)
            
    else:
        print(f"爬取失败: {result.get('message', '未知错误')}")
    # 检查API密钥
    if API_KEY == "YOUR_DEEPSEEK_API_KEY_HERE":
        print("错误：请先在脚本中设置您的DeepSeek API密钥")
        os._exit(0)

    print("注意：请检查questions.json文件内的题目是否正常！！！")
    print("="*50)
    print("接下来生成答案")
    print("="*50)

    # 输入和输出文件名
    input_file = input("请输入题目json文件（默认: questions.json）: ").strip()
    if not input_file:
        input_file = "questions.json"
    output_file = "questions_with_answers.json"  # 输出的结果文件
    
    try:
        # 读取题目数据
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查数据结构 - 现在期望是一个题目列表
        if not isinstance(data, list):
            print("错误：输入文件格式不正确，期望一个题目列表")
            input("按任意键退出.......")
            os._exit(0)
        
        questions_count = len(data)
        print(f"成功读取数据，题目数量: {questions_count}")
        
        # 统计题目类型
        question_types = {}
        for question in data:
            q_type = question.get("questiontype", -1)
            question_types[q_type] = question_types.get(q_type, 0) + 1
        
        print("题目类型统计:")
        for q_type, count in question_types.items():
            type_name = {0: "单选题", 1: "多选题", 3: "判断题", 4: "简答题"}.get(q_type, f"未知类型({q_type})")
            print(f"  {type_name}: {count} 题")
        
        # 处理题目
        processed_questions = process_questions(data)
        
        # 保存结果
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_questions, f, ensure_ascii=False, indent=2)
        
        print(f"处理完成！结果已保存到: {output_file}")
        
        # 显示统计信息
        success_count = sum(1 for q in processed_questions 
                           if q.get("api_answer") and 
                           q["api_answer"] != "获取答案失败" and 
                           q["api_answer"] != "题目内容为空")
        print(f"成功处理: {success_count}/{len(processed_questions)} 个题目")
        
        # 显示处理后的题目示例
        # print("\n处理后的题目示例:")
        # for i, question in enumerate(processed_questions[:2]):  # 显示前2个题目作为示例
        #     print(f"\n题目 {i+1}:")
        #     print(f"  题号: {question.get('number')}")
        #     print(f"  题型: {question.get('type')}")
        #     print(f"  题型代码: {question.get('questiontype')}")
        #     print(f"  题目ID: {question.get('questionID')}")
        #     print(f"  内容: {question.get('content', '')[:100]}..." if len(question.get('content', '')) > 100 else f"  内容: {question.get('content', '')}")
        #     print(f"  答案: {question.get('api_answer', '')}")
        
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_file}")
    except json.JSONDecodeError:
        print("错误：输入文件不是有效的JSON格式")
    except Exception as e:
        print(f"发生未知错误: {e}")
    
    print("注意：请检查questions_with_answers.json文件内的题目和答案是否正常！！！")
    print("="*50)
    print("接下来生成post文件")
    print("="*50)

    try:
        json_file = input("请输入JSON文件名 (默认: questions_with_answers.json): ").strip()
        if not json_file:
            json_file = "questions_with_answers.json"
        
        with open(json_file, 'r', encoding='utf-8') as f:
            questions_list = json.load(f)
        
        # 检查数据结构是否为列表
        if not isinstance(questions_list, list):
            print("错误：JSON文件格式不正确，期望一个题目列表")
            input("按任意键退出.......")
            os._exit(0)
        
        print(f"成功读取JSON文件，包含 {len(questions_list)} 道题目")
        
        # 显示题目类型统计
        question_types = {}
        for question in questions_list:
            q_type = question.get('questiontype', -1)
            question_types[q_type] = question_types.get(q_type, 0) + 1
        
        print("题目类型统计:")
        for q_type, count in question_types.items():
            type_name = {0: "单选题", 1: "多选题", 3: "判断题", 4: "简答题"}.get(q_type, f"未知类型({q_type})")
            print(f"  {type_name}: {count} 题")
        
    except FileNotFoundError:
        print(f"错误：找不到文件 {json_file}")
        os._exit(0)
    except json.JSONDecodeError:
        print("错误：JSON文件格式不正确")
        os._exit(0)
    
    # 获取包含基础POST数据的文件名
    print("请在input.txt输入在作业页面暂时保存 抓包后的数据（从开始POST到workTimesEnc=）")
    post_data_file = input("请输入包含基础POST数据的文件名（默认: input.txt）: ").strip()
    if not post_data_file:
        post_data_file = "input.txt"
    
    # 从文件中读取基础POST数据
    base_part = read_base_post_from_file(post_data_file)
    if not base_part:
        os._exit(0)
    
    print(f"\n从文件 {post_data_file} 读取基础POST数据成功")
    print(f"基础部分长度: {len(base_part)} 字符")
    
    # 生成答案部分
    print("正在生成答案部分...")
    answer_params = generate_answer_section(questions_list)
    
    # 构建完整POST数据
    complete_data = build_complete_post_data(base_part, answer_params)
    
    # 显示生成的内容
    display_generated_content(answer_params, complete_data)
    
    # 保存结果到文件
    output_file = "generated_post_data.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(complete_data)
    
    print(f"\n完整POST数据已保存到: {output_file}")
    
    # 显示使用说明
    print("\n使用说明:")
    print("1. 可以将生成的完整POST数据直接用于Burp Suite重放")
    print("2. 确保Content-Length头字段与生成的数据长度匹配")
    print("3. 简答题答案已自动格式化为HTML")
    
    print("保存答题前请确认检查完毕questions_with_answers.json文件内的题目和答案是否正常")
    print("="*50)
    print("接下来保存答题")
    print("="*50)

    save_questions = input("是否保存答题？(y/n): ")
    if save_questions.lower() != 'y':
        os._exit(0)
    else:
        send_post_from_file("generated_post_data.txt")
