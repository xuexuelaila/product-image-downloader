#!/usr/bin/env python3
"""
简化 downloader.py，移除详情图抓取功能
"""

import re

# 读取原文件
with open('/Users/fangyaxin/qa-community/product-image-downloader/scripts/downloader.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修改所有返回值，移除 detail_urls
content = re.sub(
    r'return title, cover_urls, detail_urls',
    'return title, cover_urls',
    content
)

# 2. 修改 download_product 方法中的解包
content = re.sub(
    r'title, cover_urls, detail_urls = ',
    'title, cover_urls = ',
    content
)

# 3. 移除详情图下载相关的代码（在 download_product 方法中）
# 查找并替换详情图下载部分
pattern = r'(\s+# 下载详情图.*?detail_results = await asyncio\.gather\(\*detail_tasks\)\s+detail_success = sum\(detail_results\))'
content = re.sub(pattern, '', content, flags=re.DOTALL)

# 4. 修改打印输出，移除详情图信息
content = re.sub(
    r'print\(f"  完成: 头图 \{cover_success\}/\{len\(cover_urls\)\}, 详情图 \{detail_success\}/\{len\(detail_urls\)\}"\)',
    'print(f"  完成: 头图 {cover_success}/{len(cover_urls)}")',
    content
)

content = re.sub(
    r'"detail_count": detail_success,',
    '',
    content
)

# 5. 修改成功信息打印
content = re.sub(
    r'print\(f"    头图: \{item\[\'cover_count\'\]\} 张, 详情图: \{item\[\'detail_count\'\]\} 张"\)',
    'print(f"    头图: {item[\'cover_count\']} 张")',
    content
)

# 保存修改后的文件
with open('/Users/fangyaxin/qa-community/product-image-downloader/scripts/downloader.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ 已移除详情图抓取功能")
print("✓ 备份文件: downloader.py.backup")
