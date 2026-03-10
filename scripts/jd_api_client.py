#!/usr/bin/env python3
"""
京东联盟 API 集成模块
使用京东联盟 API 获取商品信息和图片
"""

import json
import re
from typing import Optional, Tuple, List
import jd.api
from jd.api.rest.UnionOpenGoodsQueryRequest import UnionOpenGoodsQueryRequest, GoodsReqDTO


class JDApiClient:
    """京东联盟 API 客户端"""

    def __init__(self, app_key: str, app_secret: str, domain: str = 'gw.api.360buy.com'):
        """
        初始化 API 客户端

        Args:
            app_key: 应用 Key
            app_secret: 应用 Secret
            domain: API 域名
        """
        self.app_key = app_key
        self.app_secret = app_secret
        self.domain = domain

        # 设置默认应用信息
        jd.setDefaultAppInfo(app_key, app_secret)

        print(f"  京东联盟 API 客户端初始化成功")

    def extract_sku_from_url(self, url: str) -> Optional[str]:
        """
        从商品 URL 中提取 SKU ID

        Args:
            url: 商品 URL

        Returns:
            SKU ID 或 None
        """
        # 匹配京东商品 URL: https://item.jd.com/100313528034.html
        match = re.search(r'/(\d+)\.html', url)
        if match:
            return match.group(1)
        return None

    def get_product_info_by_sku(self, sku: str) -> Tuple[Optional[str], List[str], List[str]]:
        """
        通过 SKU 获取商品信息（使用京东联盟 API）

        Args:
            sku: 商品 SKU ID

        Returns:
            (商品标题, 头图列表, 详情图列表)
        """
        try:
            print(f"  正在通过京东联盟 API 获取商品信息 (SKU: {sku})...")

            # 创建请求
            request = UnionOpenGoodsQueryRequest(self.domain, 80)

            # 创建请求参数
            goods_req = GoodsReqDTO()
            goods_req.skuIds = [sku]  # SKU 列表
            goods_req.fields = "skuId,skuName,imageInfo,imagePath"  # 需要的字段

            request.goodsReqDTO = json.dumps(goods_req.__dict__)

            # 发送请求（京东联盟 API 不需要 access_token）
            response = request.getResponse("")

            print(f"  API 响应: {json.dumps(response, ensure_ascii=False)[:200]}...")

            # 解析响应
            if response and 'jd_union_open_goods_query_responce' in response:
                result = response['jd_union_open_goods_query_responce']

                if 'queryResult' in result:
                    query_result = json.loads(result['queryResult'])

                    if query_result.get('code') == 200:
                        data = query_result.get('data', [])

                        if data and len(data) > 0:
                            product = data[0]

                            # 提取商品标题
                            title = product.get('skuName')

                            # 提取图片
                            cover_urls = []

                            # 主图
                            image_info = product.get('imageInfo')
                            if image_info:
                                image_list = image_info.get('imageList', [])
                                for img in image_list:
                                    url = img.get('url')
                                    if url:
                                        cover_urls.append(url)

                            # 如果没有 imageInfo，尝试 imagePath
                            if not cover_urls:
                                image_path = product.get('imagePath')
                                if image_path:
                                    cover_urls.append(image_path)

                            if title:
                                print(f"  ✓ API 获取成功")
                                print(f"  商品标题: {title[:50]}...")
                                print(f"  图片数量: {len(cover_urls)}")
                                return title, cover_urls, []

                    else:
                        error_msg = query_result.get('message', '未知错误')
                        print(f"  ✗ API 返回错误: {error_msg}")

            print(f"  ✗ API 获取失败")
            return None, [], []

        except Exception as e:
            print(f"  ✗ API 请求失败: {e}")
            import traceback
            traceback.print_exc()
            return None, [], []

    def get_product_info(self, url: str) -> Tuple[Optional[str], List[str], List[str]]:
        """
        获取商品完整信息（标题 + 图片）

        Args:
            url: 商品 URL

        Returns:
            (商品标题, 头图列表, 详情图列表)
        """
        # 提取 SKU
        sku = self.extract_sku_from_url(url)
        if not sku:
            print(f"  ✗ 无法从 URL 中提取 SKU: {url}")
            return None, [], []

        print(f"  提取到 SKU: {sku}")

        # 使用京东联盟 API 获取商品信息
        return self.get_product_info_by_sku(sku)


def test_api():
    """测试 API 功能"""
    print("=" * 60)
    print("京东 API 测试")
    print("=" * 60)

    # 从配置文件导入密钥
    try:
        from jd_api_config import APP_KEY, APP_SECRET
    except ImportError:
        print("错误: 无法导入配置文件")
        return

    if APP_KEY == "your_app_key_here":
        print("请先配置 APP_KEY 和 APP_SECRET")
        return

    print(f"App Key: {APP_KEY[:20]}...")
    print(f"App Secret: {APP_SECRET[:20]}...")

    # 初始化客户端
    client = JDApiClient(APP_KEY, APP_SECRET)

    # 测试商品
    test_url = "https://item.jd.com/100313528034.html"
    print(f"\n测试商品: {test_url}")

    # 获取商品信息
    title, cover_urls, detail_urls = client.get_product_info(test_url)

    print("\n" + "=" * 60)
    print("测试结果:")
    print("=" * 60)
    print(f"商品标题: {title}")
    print(f"头图数量: {len(cover_urls)}")
    print(f"详情图数量: {len(detail_urls)}")

    if cover_urls:
        print("\n头图 URL:")
        for i, url in enumerate(cover_urls[:3], 1):
            print(f"  {i}. {url}")


if __name__ == "__main__":
    test_api()
