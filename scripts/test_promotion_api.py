#!/usr/bin/env python3
"""
测试京东联盟推广商品信息查询 API
这个 API 可能更适合导购媒体使用
"""

import json
import sys
sys.path.insert(0, '/Users/fangyaxin/qa-community/product-image-downloader/scripts')

import jd.api
from jd.api.rest.UnionOpenGoodsPromotiongoodsinfoQueryRequest import UnionOpenGoodsPromotiongoodsinfoQueryRequest
from jd_api_config import APP_KEY, APP_SECRET

def test_promotion_goods_api():
    print("=" * 80)
    print("测试京东联盟推广商品信息查询 API")
    print("=" * 80)

    # 初始化
    jd.setDefaultAppInfo(APP_KEY, APP_SECRET)
    print(f"\n✓ API 客户端初始化成功")
    print(f"  APP_KEY: {APP_KEY[:10]}...")
    print(f"  APP_SECRET: {APP_SECRET[:10]}...")

    # 测试商品
    sku = "100313528034"
    print(f"\n测试商品 SKU: {sku}")
    print(f"API: jd.union.open.goods.promotiongoodsinfo.query")

    try:
        # 创建请求
        request = UnionOpenGoodsPromotiongoodsinfoQueryRequest()
        request.skuIds = sku  # 注意：这里是字符串，不是列表

        # 发送请求
        print(f"\n发送 API 请求...")
        response = request.getResponse("")

        # 打印响应
        print(f"\nAPI 响应：")
        print(json.dumps(response, ensure_ascii=False, indent=2))

        # 解析响应
        if response and 'jd_union_open_goods_promotiongoodsinfo_query_responce' in response:
            result = response['jd_union_open_goods_promotiongoodsinfo_query_responce']

            if 'code' in result and result['code'] == '0':
                print(f"\n✓ API 调用成功！")

                if 'data' in result:
                    data = json.loads(result['data'])
                    print(f"\n商品信息：")
                    print(json.dumps(data, ensure_ascii=False, indent=2))
                    return True
            else:
                print(f"\n✗ API 调用失败")
                print(f"错误信息: {result}")
                return False
        else:
            print(f"\n✗ 响应格式不正确")
            return False

    except Exception as e:
        print(f"\n✗ 请求失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_promotion_goods_api()
    print("\n" + "=" * 80)
    if success:
        print("✓ 测试成功！这个 API 可以使用")
    else:
        print("✗ 测试失败")
    print("=" * 80)
    sys.exit(0 if success else 1)
