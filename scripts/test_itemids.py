#!/usr/bin/env python3
"""
测试不同的 API 调用方式
"""

import json
import sys
sys.path.insert(0, '/Users/fangyaxin/qa-community/product-image-downloader/scripts')

import jd.api
from jd.api.rest.UnionOpenGoodsBigfieldQueryRequest import UnionOpenGoodsBigfieldQueryRequest, GoodsReq
from jd_api_config import APP_KEY, APP_SECRET

def test_with_itemids():
    """使用 itemIds 而不是 skuIds"""
    print("=" * 80)
    print("测试使用 itemIds 调用 bigfield.query API")
    print("=" * 80)

    jd.setDefaultAppInfo(APP_KEY, APP_SECRET)

    sku = "100192762770"  # 使用你测试成功的 SKU
    print(f"\n测试商品 SKU: {sku}")

    try:
        request = UnionOpenGoodsBigfieldQueryRequest()

        goods_req = GoodsReq()
        # 尝试使用 itemIds 而不是 skuIds
        goods_req.itemIds = [sku]  # 注意：这里用字符串
        goods_req.fields = [
            "baseBigFieldInfo",
            "imageInfo",
            "categoryInfo"
        ]

        request.goodsReq = goods_req

        print(f"\n发送 API 请求（使用 itemIds）...")
        response = request.getResponse("")

        print(f"\nAPI 响应：")
        print(json.dumps(response, ensure_ascii=False, indent=2)[:1000])

        if response and 'jd_union_open_goods_bigfield_query_responce' in response:
            result = response['jd_union_open_goods_bigfield_query_responce']
            if 'queryResult' in result:
                query_result = json.loads(result['queryResult'])
                print(f"\nqueryResult:")
                print(json.dumps(query_result, ensure_ascii=False, indent=2)[:500])

                if query_result.get('code') == 200:
                    print(f"\n✓ API 调用成功！")
                    return True
                else:
                    print(f"\n✗ API 返回错误: {query_result.get('message')}")
                    return False

        return False

    except Exception as e:
        print(f"\n✗ 请求失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_with_itemids()
    print("\n" + "=" * 80)
    if success:
        print("✓ 测试成功！")
    else:
        print("✗ 测试失败")
    print("=" * 80)
    sys.exit(0 if success else 1)
