#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 links.yml 中的 logo 地址
将 logo 地址从 https://域名/apple-touch-icon.png 格式
修改为 https://api.aitags.cn/favicon/域名.png 格式
"""

import re
from urllib.parse import urlparse

def extract_domain(url):
    """从URL中提取域名"""
    parsed = urlparse(url)
    return parsed.netloc

def fix_logo_urls(input_file, output_file):
    """修复logo URL"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 正则匹配 logo 行和前面的 url 行
    # 需要找到每个链接条目的 url 和 logo
    lines = content.split('\n')
    result_lines = []
    current_url = None
    
    for i, line in enumerate(lines):
        # 检查是否是 url 行
        url_match = re.match(r'^(\s+)url:\s+(https?://[^\s]+)', line)
        if url_match:
            current_url = url_match.group(2)
            result_lines.append(line)
            continue
        
        # 检查是否是 logo 行
        logo_match = re.match(r'^(\s+)logo:\s+(https?://[^\s]+)', line)
        if logo_match and current_url:
            indent = logo_match.group(1)
            old_logo = logo_match.group(2)
            
            # 从当前 url 中提取域名
            domain = extract_domain(current_url)
            
            # 生成新的 logo URL
            new_logo = f"https://api.aitags.cn/favicon/{domain}.png"
            
            # 替换 logo 行
            new_line = f"{indent}logo: {new_logo}"
            result_lines.append(new_line)
            
            print(f"修改: {domain}")
            print(f"  旧: {old_logo}")
            print(f"  新: {new_logo}")
            print()
        else:
            result_lines.append(line)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result_lines))
    
    print(f"修改完成！已保存到: {output_file}")

if __name__ == "__main__":
    input_file = "links.yml"
    output_file = "links.yml"
    
    print("开始修复 logo 地址...")
    print("=" * 60)
    fix_logo_urls(input_file, output_file)
