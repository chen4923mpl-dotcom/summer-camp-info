#!/usr/bin/env python3
"""
搜索985高校和中科院夏令营信息的Python脚本
"""

import requests
from bs4 import BeautifulSoup
import json
import time

# 985高校列表
top_universities = [
    "北京大学", "清华大学", "复旦大学", "上海交通大学", "浙江大学", 
    "南京大学", "中国科学技术大学", "哈尔滨工业大学", "西安交通大学",
    "武汉大学", "华中科技大学", "中山大学", "四川大学", "南开大学",
    "天津大学", "东南大学", "同济大学", "北京航空航天大学",
    "北京理工大学", "中国人民大学", "北京师范大学", "厦门大学",
    "山东大学", "中南大学", "吉林大学", "大连理工大学",
    "西北工业大学", "电子科技大学", "重庆大学", "兰州大学"
]

# 搜索关键词
search_keywords = [
    "夏令营", "招生", "研究生", "暑期科研", "研究生暑期学校"
]

# 相关专业
specialties = [
    "生命科学", "生物科学", "生物学", "脑科学", "神经科学",
    "基础医学", "医学", "生物医学工程", "生物技术", "生物信息学"
]

def search_site(base_url):
    """尝试搜索特定网站"""
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 查找包含夏令营的链接
        links = soup.find_all('a', string=lambda text: any(keyword in str(text) for keyword in search_keywords))
        
        results = []
        for link in links:
            href = link.get('href')
            if href:
                full_url = href if href.startswith('http') else base_url + href
                results.append({
                    'title': link.text.strip(),
                    'url': full_url,
                    'source': base_url
                })
        
        return results
    except Exception as e:
        print(f"搜索 {base_url} 失败: {e}")
        return []

def main():
    """主搜索函数"""
    all_results = []
    
    # 尝试搜索一些主要大学的网站
    test_urls = [
        "https://www.pku.edu.cn",
        "https://www.tsinghua.edu.cn",
        "https://www.fudan.edu.cn",
        "https://www.zju.edu.cn",
        "https://www.nju.edu.cn",
        "https://www.ucas.ac.cn",  # 中国科学院大学
    ]
    
    print("开始搜索夏令营信息...")
    
    for url in test_urls:
        print(f"搜索: {url}")
        results = search_site(url)
        if results:
            all_results.extend(results)
            print(f"在 {url} 找到 {len(results)} 个结果")
    
    # 保存结果
    with open('/root/.openclaw/workspace/camp_results.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"总共找到 {len(all_results)} 个结果")
    
    return all_results

if __name__ == "__main__":
    main()