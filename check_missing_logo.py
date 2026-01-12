import re

# 读取 YAML 文件
with open('links.yml', 'r', encoding='utf-8') as f:
    lines = f.readlines()

missing_logos = []
current_item = None
current_link = None
logo_line_num = 0

for i, line in enumerate(lines, 1):
    # 检测到新的条目（以 - title: 开头）
    if re.match(r'^\s*-\s*title:', line):
        match = re.search(r'title:\s*(.+)$', line)
        current_item = match.group(1).strip() if match else 'Unknown'
    
    # 检测到 link 字段
    elif re.match(r'^\s+link:', line):
        match = re.search(r'link:\s*(.+)$', line)
        current_link = match.group(1).strip() if match else ''
    
    # 检测到 logo 字段
    elif re.match(r'^\s+logo:', line):
        logo_line_num = i
        # 检查下一行是否有 url 字段
        if i < len(lines):
            next_line = lines[i]  # i+1-1 = i (因为索引从0开始)
            url_match = re.match(r'^\s+url:\s*(.*)$', next_line)
            if url_match:
                url_value = url_match.group(1).strip()
                if not url_value:  # url 字段存在但为空
                    missing_logos.append({
                        'line': logo_line_num,
                        'title': current_item,
                        'link': current_link,
                        'reason': 'url字段为空'
                    })
            else:  # logo 后面没有 url 字段
                missing_logos.append({
                    'line': logo_line_num,
                    'title': current_item,
                    'link': current_link,
                    'reason': '缺少url字段'
                })

# 输出结果
print(f"共找到 {len(missing_logos)} 个缺失 logo URL 的条目：\n")

# 同时保存到文件
with open('missing_logo_urls.txt', 'w', encoding='utf-8') as f:
    f.write(f"共找到 {len(missing_logos)} 个缺失 logo URL 的条目：\n\n")
    for item in missing_logos:
        output = f"行 {item['line']}: {item['title']}\n  链接: {item['link']}\n  原因: {item['reason']}\n\n"
        print(output.strip())
        print()
        f.write(output)

print(f"\n完整结果已保存到 missing_logo_urls.txt")
