#!/usr/bin/env python3
"""测试京东 API 是否正常工作"""

import sys
from jd_api_client import JDApiClient
from jd_api_config import APP_KEY, APP_SECRET

def test_api():
    print("=" * 60)
    print("测试京东 API")
    print("=" * 60)

    # 初始化客户端
    print(f"\n1. 初始化 API 客户端...")
    print(f"   APP_KEY: {APP_KEY[:10]}...")
    print(f"   APP_SECRET: {APP_SECRET[:10]}...")

    try:
        client = JDApiClient(APP_KEY, APP_SECRET)
        print("   ✓ 客户端初始化成功")
    except Exception as e:
        print(f"   ✗ 客户端初始化失败: {e}")
        return False

    # 测试获取商品信息
    test_url = "https://item.jd.com/100313528034.html"
    print(f"\n2. 测试获取商品信息...")
    print(f"   测试链接: {test_url}")

    try:
        info = client.get_product_info(test_url)

        if info.get('title'):
            print(f"   ✓ 商品标题: {info['title'][:50]}...")
        else:
            print(f"   ✗ 未获取到商品标题")
            return False

        if info.get('cover_images'):
            print(f"   ✓ 头图数量: {len(info['cover_images'])} 张")
        else:
            print(f"   ⚠ 未获取到头图")

        if info.get('detail_images'):
            print(f"   ✓ 详情图数量: {len(info['detail_images'])} 张")
        else:
            print(f"   ⚠ 未获取到详情图")

        print("\n" + "=" * 60)
        print("✓ API 测试成功！")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"   ✗ API 调用失败: {e}")
        print("\n" + "=" * 60)
        print("✗ API 测试失败")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
