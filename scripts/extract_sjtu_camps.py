#!/usr/bin/env python3
"""
提取上海交通大学夏令营信息的脚本
"""

import requests
from bs4 import BeautifulSoup
import json

def extract_camp_info_from_sjtu():
    """从上海交通大学研究生招生网站提取夏令营信息"""
    url = "https://yzb.sjtu.edu.cn"
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 查找招生动态部分
        camp_info = []
        
        # 查找所有包含夏令营信息的链接
        for element in soup.find_all(['a', 'div', 'span', 'li']):
            text = element.get_text()
            if any(keyword in text for keyword in ['夏令营', '优才夏令营', '优秀大学生夏令营']):
                # 提取详细信息
                camp_data = {
                    '学校': '上海交通大学',
                    '学院': '',
                    '标题': '',
                    '日期': '',
                    '链接': ''
                }
                
                # 查找可能的日期信息
                date_patterns = ['2025.', '2026.', '2025年', '2026年']
                for date_pattern in date_patterns:
                    if date_pattern in text:
                        camp_data['日期'] = date_pattern
                
                # 提取学院信息
                if '学院' in text:
                    # 提取学院名称
                    words = text.split()
                    for i, word in enumerate(words):
                        if '学院' in word:
                            camp_data['学院'] = word
                
                camp_data['标题'] = text.strip()
                
                # 如果有链接
                if element.name == 'a' and element.get('href'):
                    href = element.get('href')
                    full_url = href if href.startswith('http') else url + href
                    camp_data['链接'] = full_url
                
                camp_info.append(camp_data)
        
        # 过滤掉重复和空的信息
        filtered_info = []
        seen_titles = set()
        for camp in camp_info:
            if camp['标题'] and camp['标题'] not in seen_titles:
                seen_titles.add(camp['标题'])
                filtered_info.append(camp)
        
        return filtered_info
    except Exception as e:
        print(f"提取信息失败: {e}")
        return []

def main():
    camp_info = extract_camp_info_from_sjtu()
    
    # 生物相关的夏令营
    biology_camps = []
    biology_keywords = ['生物', '生命', '医学', '脑科学', '神经', '心理学', '农业']
    
    for camp in camp_info:
        if any(keyword in camp['标题'] for keyword in biology_keywords):
            biology_camps.append(camp)
    
    # 保存结果
    with open('/root/.openclaw/workspace/sjtu_biology_camps.json', 'w', encoding='utf-8') as f:
        json.dump(biology_camps, f, indent=2, ensure_ascii=False)
    
    print(f"找到 {len(biology_camps)} 个生物相关的夏令营信息")
    
    # 输出到表格
    print("\n上海交通大学生物相关夏令营信息:")
    for camp in biology_camps:
        print(f"标题: {camp['标题']}")
        print(f"学院: {camp['学院']}")
        print(f"日期: {camp['日期']}")
        print(f"链接: {camp['链接']}")
        print("-" * 50)

if __name__ == "__main__":
    main()