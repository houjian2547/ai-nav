import yaml

with open('links.yml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

print("="*70)
print("links.yml 中的所有分类统计")
print("="*70)

total_links = 0
for i, category in enumerate(data['categories'], 1):
    category_name = category['category']
    links_count = len(category['links'])
    total_links += links_count
    print(f"{i:2d}. {category_name:<30} {links_count:3d} 个链接")

print("="*70)
print(f"总计: {len(data['categories'])} 个分类, {total_links} 个链接")
print("="*70)

# 显示几个新添加的分类示例
print("\n示例：查看 'AI绘画生成-文生图' 分类的前3个链接:")
print("-"*70)
for category in data['categories']:
    if category['category'] == 'AI绘画生成-文生图':
        for i, link in enumerate(category['links'][:3], 1):
            print(f"{i}. {link['title']}")
            print(f"   网址: {link['url']}")
            print(f"   描述: {link['description'][:50]}...")
            print()
        break
