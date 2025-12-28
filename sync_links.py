#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 navigation.md 中的所有 ## 级别分类数据同步到 links.yml
"""

import re
import yaml


def extract_all_categories(md_file):
    """从 navigation.md 中提取所有 ## 级别的分类数据"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到所有 "## " 开头的分类
    category_pattern = r'## ([^\n]+)\s*\n\s*\n\|[^\n]+\|\s*\n\|[^\n]+\|\s*\n((?:\|[^\n]+\|\s*\n)+)'
    matches = re.finditer(category_pattern, content)
    
    all_categories = {}
    
    for match in matches:
        category_name = match.group(1).strip()
        table_content = match.group(2)
        links = []
        
        # 解析每一行数据
        for line in table_content.strip().split('\n'):
            # 匹配格式: | [网站名](URL) | 描述 |
            link_match = re.match(r'\|\s*\[([^\]]+)\]\(([^\)]+)\)\s*\|\s*([^|]+)\s*\|', line)
            if link_match:
                title = link_match.group(1).strip()
                url = link_match.group(2).strip()
                description = link_match.group(3).strip()
                
                links.append({
                    'title': title,
                    'url': url,
                    'description': description,
                    'tags': category_name
                })
        
        if links:  # 只添加有链接的分类
            all_categories[category_name] = links
            print(f"  - 找到分类 '{category_name}': {len(links)} 个链接")
    
    return all_categories


def update_links_yml(yml_file, all_categories):
    """更新 links.yml 文件，添加或替换所有分类"""
    
    # 读取现有的 YAML 文件
    with open(yml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    if not data:
        data = {}
    
    if 'categories' not in data:
        data['categories'] = []
    
    # 为每个分类更新或添加数据
    for category_name, links in all_categories.items():
        # 查找是否已存在该分类
        category_index = -1
        for i, category in enumerate(data['categories']):
            if category.get('category') == category_name:
                category_index = i
                break
        
        # 构建新的分类数据
        new_category = {
            'category': category_name,
            'icon': 'linecons-doc',
            'links': links
        }
        
        if category_index >= 0:
            # 替换已存在的分类
            data['categories'][category_index] = new_category
            print(f"  ✓ 已更新 '{category_name}' 分类，共 {len(links)} 个链接")
        else:
            # 添加新分类
            data['categories'].append(new_category)
            print(f"  ✓ 已添加 '{category_name}' 分类，共 {len(links)} 个链接")
    
    # 写回 YAML 文件
    with open(yml_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    print(f"\n✓ 已成功更新 {yml_file}")


def main():
    md_file = r'c:\Users\hj\Desktop\ai-nav\navigation.md'
    yml_file = r'c:\Users\hj\Desktop\ai-nav\links.yml'
    
    print("="*60)
    print("正在从 navigation.md 提取所有 ## 级别分类数据...")
    print("="*60)
    
    # 提取所有分类数据
    all_categories = extract_all_categories(md_file)
    
    if not all_categories:
        print("\n未找到任何分类数据")
        return
    
    print(f"\n共找到 {len(all_categories)} 个分类")
    total_links = sum(len(links) for links in all_categories.values())
    print(f"总计 {total_links} 个链接")
    
    # 更新到 links.yml
    print("\n" + "="*60)
    print("正在更新 links.yml...")
    print("="*60)
    update_links_yml(yml_file, all_categories)
    
    print("\n" + "="*60)
    print("✅ 所有分类已成功同步！")
    print("="*60)


if __name__ == '__main__':
    main()
