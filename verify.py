import yaml

with open('links.yml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

for category in data['categories']:
    if category['category'] == 'AI写作工具':
        links = category['links']
        print(f'✓ AI写作工具分类共有 {len(links)} 个链接\n')
        print('前5个链接示例:')
        for i, link in enumerate(links[:5], 1):
            print(f'{i}. {link["title"]}')
            print(f'   网址: {link["url"]}')
            print(f'   描述: {link["description"][:50]}...')
            print(f'   标签: {link["tags"]}\n')
        break
