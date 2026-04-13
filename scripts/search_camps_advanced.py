#!/usr/bin/env python3
"""
更精确地搜索夏令营信息的Python脚本
"""

import requests
from bs4 import BeautifulSoup
import json
import re

# 目标网站列表
target_sites = [
    {
        "name": "北京大学研究生院",
        "url": "https://grad.pku.edu.cn",
        "camp_keywords": ["夏令营", "暑期学校", "优秀大学生夏令营"]
    },
    {
        "name": "清华大学研究生院",
        "url": "https://yz.tsinghua.edu.cn",
        "camp_keywords": ["夏令营", "暑期学校", "优秀大学生夏令营"]
    },
    {
        "name": "复旦大学研究生院",
        "url": "http://www.gsao.fudan.edu.cn",
        "camp_keywords": ["夏令营", "暑期学校", "优秀大学生夏令营"]
    },
    {
        "name": "上海交通大学研究生院",
        "url": "https://yzb.sjtu.edu.cn",
        "camp_keywords": ["夏令营", "暑期学校", "优秀大学生夏令营"]
    },
    {
        "name": "浙江大学研究生院",
        "url": "https://yzw.zju.edu.cn",
        "camp_keywords": ["夏令营", "暑期学校", "优秀大学生夏令营"]
    },
    {
        "name": "中国科学院大学",
        "url": "https://www.ucas.ac.cn",
        "camp_keywords": ["夏令营", "暑期学校", "优秀大学生夏令营"]
    }
]

def search_camp_info(url, keywords):
    """搜索夏令营信息"""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 搜索所有文本
        text_content = soup.get_text()
        
        results = []
        
        # 查找关键词
        for keyword in keywords:
            if keyword in text_content:
                # 找到包含关键词的段落
                paragraphs = []
                for element in soup.find_all(['p', 'div', 'span', 'a', 'li']):
                    if keyword in element.get_text():
                        text = element.get_text().strip()
                        paragraphs.append(text)
                
                if paragraphs:
                    # 获取页面标题
                    title = soup.title.string if soup.title else url
                    
                    results.append({
                        'keyword': keyword,
                        'title': title,
                        'url': url,
                        'paragraphs': paragraphs[:3]  # 取前3个段落
                    })
        
        return results
    except Exception as e:
        print(f"搜索 {url} 失败: {e}")
        return []

def main():
    """主搜索函数"""
    all_results = []
    
    print("开始精确搜索夏令营信息...")
    
    for site in target_sites:
        print(f"搜索: {site['name']} ({site['url']})")
        results = search_camp_info(site['url'], site['camp_keywords'])
        
        if results:
            all_results.extend(results)
            print(f"在 {site['name']} 找到 {len(results)} 个结果")
        else:
            print(f"在 {site['name']} 未找到相关结果")
    
    # 保存结果
    with open('/root/.openclaw/workspace/camp_results_advanced.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"总共找到 {len(all_results)} 个结果")
    
    return all_results

if __name__ == "__main__":
    main()