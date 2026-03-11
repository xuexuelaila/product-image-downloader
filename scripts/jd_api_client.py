#!/usr/bin/env python3
"""
京东联盟 API 集成模块
使用京东联盟 API 获取商品信息：标题、头图、详情图、视频
"""

import json
import re
import os
import asyncio
import aiohttp
from typing import Optional, Tuple, List, Dict, Any
from bs4 import BeautifulSoup

import jd.api
from jd.api.rest.UnionOpenGoodsQueryRequest import UnionOpenGoodsQueryRequest, GoodsReqDTO
from jd.api.rest.UnionOpenGoodsBigfieldQueryRequest import UnionOpenGoodsBigfieldQueryRequest, GoodsReq


class JDApiClient:
    """京东联盟 API 客户端"""

    def __init__(self, app_key: str, app_secret: str, domain: str = 'gw.api.360buy.com'):
        self.app_key = app_key
        self.app_secret = app_secret
        self.domain = domain
        jd.setDefaultAppInfo(app_key, app_secret)
        print(f"  京东联盟 API 客户端初始化成功")

    def extract_sku_from_url(self, url: str) -> Optional[str]:
        """从商品 URL 中提取 SKU ID"""
        match = re.search(r'/(\d+)\.html', url)
        if match:
            return match.group(1)
        return None

    # ==================== 基础商品查询 ====================

    def query_goods_info(self, sku: str) -> Optional[Dict[str, Any]]:
        """
        使用 jd.union.open.goods.query 获取商品基础信息（标题、头图）

        Returns:
            商品信息字典 或 None
        """
        try:
            print(f"  [API] 查询商品基础信息 (SKU: {sku})...")
            request = UnionOpenGoodsQueryRequest(self.domain, 80)

            goods_req = GoodsReqDTO()
            goods_req.skuIds = [int(sku)]

            request.goodsReqDTO = goods_req

            response = request.getResponse("")
            print(f"  [API] goods.query 响应: {json.dumps(response, ensure_ascii=False)[:300]}...")

            if response and 'jd_union_open_goods_query_responce' in response:
                result = response['jd_union_open_goods_query_responce']
                if 'queryResult' in result:
                    query_result = json.loads(result['queryResult'])
                    if query_result.get('code') == 200:
                        data = query_result.get('data', [])
                        if data and len(data) > 0:
                            return data[0]
                    else:
                        print(f"  [API] 错误: {query_result.get('message', '未知错误')}")
            return None

        except Exception as e:
            print(f"  [API] goods.query 请求失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    # ==================== 大字段查询 ====================

    def query_bigfield_info(self, sku: str) -> Optional[Dict[str, Any]]:
        """
        使用 jd.union.open.goods.bigfield.query 获取商品大字段信息（详情图、视频）

        Returns:
            大字段信息字典 或 None
        """
        try:
            print(f"  [API] 查询商品大字段信息 (SKU: {sku})...")
            request = UnionOpenGoodsBigfieldQueryRequest(self.domain, 80)

            goods_req = GoodsReq()
            goods_req.skuIds = [int(sku)]
            # 请求所有大字段：基础大字段(详情图)、视频大字段、图片信息
            goods_req.fields = [
                "baseBigFieldInfo",
                "bookBigFieldInfo",
                "videoBigFieldInfo",
                "imageInfo",
                "categoryInfo"
            ]

            request.goodsReq = goods_req

            response = request.getResponse("")
            print(f"  [API] bigfield.query 响应: {json.dumps(response, ensure_ascii=False)[:500]}...")

            if response and 'jd_union_open_goods_bigfield_query_responce' in response:
                result = response['jd_union_open_goods_bigfield_query_responce']
                if 'queryResult' in result:
                    query_result = json.loads(result['queryResult'])
                    if query_result.get('code') == 200:
                        data = query_result.get('data', [])
                        if data and len(data) > 0:
                            return data[0]
                    else:
                        print(f"  [API] 错误: {query_result.get('message', '未知错误')}")
            return None

        except Exception as e:
            print(f"  [API] bigfield.query 请求失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    # ==================== 数据提取方法 ====================

    @staticmethod
    def extract_title(goods_info: Dict) -> Optional[str]:
        """从 goods.query 结果中提取商品标题"""
        return goods_info.get('skuName')

    @staticmethod
    def extract_cover_images(goods_info: Dict) -> List[str]:
        """从 goods.query 结果中提取商品头图列表"""
        cover_urls = []

        # 从 imageInfo.imageList 获取
        image_info = goods_info.get('imageInfo')
        if image_info:
            image_list = image_info.get('imageList', [])
            for img in image_list:
                url = img.get('url')
                if url:
                    if not url.startswith('http'):
                        url = 'https:' + url if url.startswith('//') else 'https://' + url
                    cover_urls.append(url)

        # 兜底：从 imagePath 获取主图
        if not cover_urls:
            image_path = goods_info.get('imagePath')
            if image_path:
                if not image_path.startswith('http'):
                    image_path = 'https:' + image_path if image_path.startswith('//') else 'https://' + image_path
                cover_urls.append(image_path)

        return cover_urls

    @staticmethod
    def extract_detail_images(bigfield_info: Dict) -> List[str]:
        """从 bigfield.query 结果中提取商品详情图"""
        detail_urls = []

        base_info = bigfield_info.get('baseBigFieldInfo')
        if not base_info:
            return detail_urls

        # wdis 字段：PC端商品详情（HTML格式，含图片）
        wdis_html = base_info.get('wdis', '')
        if wdis_html:
            detail_urls.extend(JDApiClient._extract_images_from_html(wdis_html))

        # wdisDesc 字段：移动端商品详情
        wdis_desc = base_info.get('wdisDesc', '')
        if wdis_desc and not detail_urls:
            detail_urls.extend(JDApiClient._extract_images_from_html(wdis_desc))

        # 去重并保持顺序
        seen = set()
        unique_urls = []
        for url in detail_urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)

        return unique_urls

    @staticmethod
    def _extract_images_from_html(html_content: str) -> List[str]:
        """从 HTML 内容中提取所有图片 URL"""
        urls = []

        # 方法1：用 BeautifulSoup 解析 img 标签
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src') or img.get('data-lazyload')
                if src:
                    src = JDApiClient._normalize_url(src)
                    if src and JDApiClient._is_valid_image_url(src):
                        urls.append(src)
        except Exception:
            pass

        # 方法2：正则匹配（兜底，捕获HTML解析遗漏的URL）
        if not urls:
            img_pattern = re.compile(
                r'(?:src|data-src|data-lazyload)\s*=\s*["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp)(?:\?[^"\']*)?)["\']',
                re.IGNORECASE
            )
            for match in img_pattern.finditer(html_content):
                url = JDApiClient._normalize_url(match.group(1))
                if url and JDApiClient._is_valid_image_url(url):
                    urls.append(url)

        return urls

    @staticmethod
    def extract_video_info(bigfield_info: Dict) -> List[Dict[str, str]]:
        """
        从 bigfield.query 结果中提取商品视频信息

        Returns:
            视频信息列表，每项包含:
            - playUrl: 视频播放地址
            - imageUrl: 视频封面图
            - duration: 视频时长
            - width/height: 视频宽高
        """
        videos = []

        video_info = bigfield_info.get('videoBigFieldInfo')
        if not video_info:
            return videos

        video_list = video_info.get('videoList', [])
        for video in video_list:
            video_data = {}

            play_url = video.get('playUrl', '')
            if play_url:
                video_data['playUrl'] = JDApiClient._normalize_url(play_url)

            image_url = video.get('imageUrl', '')
            if image_url:
                video_data['imageUrl'] = JDApiClient._normalize_url(image_url)

            # 其他视频信息
            for key in ['duration', 'width', 'height', 'playType', 'videoType']:
                if video.get(key):
                    video_data[key] = str(video[key])

            if video_data.get('playUrl'):
                videos.append(video_data)

        return videos

    # ==================== 辅助方法 ====================

    @staticmethod
    def _normalize_url(url: str) -> str:
        """标准化 URL"""
        url = url.strip()
        if url.startswith('//'):
            return 'https:' + url
        if not url.startswith('http'):
            return 'https://' + url
        return url

    @staticmethod
    def _is_valid_image_url(url: str) -> bool:
        """检查是否是有效的图片 URL"""
        # 排除小图标、logo等
        invalid_patterns = [
            'icon', 'logo', '1x1', 'pixel', 'blank',
            'loading', 'placeholder', '.gif'
        ]
        url_lower = url.lower()
        for pattern in invalid_patterns:
            if pattern in url_lower:
                return False
        return True

    # ==================== 核心方法：获取完整商品信息 ====================

    def get_product_info(self, url: str) -> Dict[str, Any]:
        """
        获取商品完整信息（标题 + 头图 + 详情图 + 视频）

        Args:
            url: 商品 URL

        Returns:
            {
                'title': str,           # 商品标题
                'sku': str,             # SKU ID
                'cover_images': [],     # 头图 URL 列表
                'detail_images': [],    # 详情图 URL 列表
                'videos': [],           # 视频信息列表
            }
        """
        result = {
            'title': None,
            'sku': None,
            'cover_images': [],
            'detail_images': [],
            'videos': [],
        }

        # 1. 提取 SKU
        sku = self.extract_sku_from_url(url)
        if not sku:
            print(f"  ✗ 无法从 URL 中提取 SKU: {url}")
            return result
        result['sku'] = sku
        print(f"  提取到 SKU: {sku}")

        # 2. 查询基础信息（标题 + 头图）
        goods_info = self.query_goods_info(sku)
        if goods_info:
            result['title'] = self.extract_title(goods_info)
            result['cover_images'] = self.extract_cover_images(goods_info)
            print(f"  ✓ 商品标题: {result['title']}")
            print(f"  ✓ 头图数量: {len(result['cover_images'])}")
        else:
            print(f"  ✗ 基础信息获取失败")

        # 3. 查询大字段信息（详情图 + 视频）
        bigfield_info = self.query_bigfield_info(sku)
        if bigfield_info:
            result['detail_images'] = self.extract_detail_images(bigfield_info)
            result['videos'] = self.extract_video_info(bigfield_info)
            print(f"  ✓ 详情图数量: {len(result['detail_images'])}")
            print(f"  ✓ 视频数量: {len(result['videos'])}")

            # 如果基础查询没拿到头图，从大字段的 imageInfo 补充
            if not result['cover_images']:
                image_info = bigfield_info.get('imageInfo')
                if image_info:
                    for img in image_info.get('imageList', []):
                        url_val = img.get('url')
                        if url_val:
                            result['cover_images'].append(self._normalize_url(url_val))
                    print(f"  ✓ 从大字段补充头图: {len(result['cover_images'])}")
        else:
            print(f"  ✗ 大字段信息获取失败")

        return result

    # ==================== 下载方法 ====================

    async def download_product(self, url: str, output_dir: str = 'downloads'):
        """
        下载商品的所有资源（头图、详情图、视频）

        Args:
            url: 商品 URL
            output_dir: 输出根目录
        """
        # 获取商品信息
        info = self.get_product_info(url)

        if not info['title']:
            print(f"\n  ✗ 无法获取商品信息，跳过")
            return

        # 清理标题作为文件夹名
        folder_name = self._sanitize_filename(info['title'])
        product_dir = os.path.join(output_dir, folder_name)

        print(f"\n{'='*60}")
        print(f"  商品: {info['title']}")
        print(f"  SKU: {info['sku']}")
        print(f"  头图: {len(info['cover_images'])} 张")
        print(f"  详情图: {len(info['detail_images'])} 张")
        print(f"  视频: {len(info['videos'])} 个")
        print(f"  保存目录: {product_dir}")
        print(f"{'='*60}\n")

        # 创建目录
        cover_dir = os.path.join(product_dir, 'cover')
        detail_dir = os.path.join(product_dir, 'detail')
        video_dir = os.path.join(product_dir, 'video')
        os.makedirs(cover_dir, exist_ok=True)
        os.makedirs(detail_dir, exist_ok=True)
        if info['videos']:
            os.makedirs(video_dir, exist_ok=True)

        async with aiohttp.ClientSession() as session:
            # 下载头图
            if info['cover_images']:
                print(f"  📥 下载头图...")
                await self._download_images(session, info['cover_images'], cover_dir, '头图')

            # 下载详情图
            if info['detail_images']:
                print(f"  📥 下载详情图...")
                await self._download_images(session, info['detail_images'], detail_dir, '详情图')

            # 下载视频
            if info['videos']:
                print(f"  📥 下载视频...")
                await self._download_videos(session, info['videos'], video_dir)

        print(f"\n  ✅ 商品资源下载完成: {folder_name}")

    async def _download_images(self, session: aiohttp.ClientSession,
                               urls: List[str], save_dir: str, label: str):
        """批量下载图片"""
        total = len(urls)
        success = 0
        for i, url in enumerate(urls, 1):
            ext = self._get_file_extension(url, '.jpg')
            filename = f"{i:03d}{ext}"
            filepath = os.path.join(save_dir, filename)

            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    if resp.status == 200:
                        content = await resp.read()
                        if len(content) > 1024:  # 至少 1KB
                            with open(filepath, 'wb') as f:
                                f.write(content)
                            success += 1
                            print(f"    [{i}/{total}] ✓ {filename} ({len(content)//1024}KB)")
                        else:
                            print(f"    [{i}/{total}] ✗ {filename} 文件太小，跳过")
                    else:
                        print(f"    [{i}/{total}] ✗ HTTP {resp.status}")
            except Exception as e:
                print(f"    [{i}/{total}] ✗ 下载失败: {e}")

        print(f"  {label}: {success}/{total} 张下载成功")

    async def _download_videos(self, session: aiohttp.ClientSession,
                               videos: List[Dict], save_dir: str):
        """下载视频文件"""
        total = len(videos)
        success = 0
        for i, video in enumerate(videos, 1):
            play_url = video.get('playUrl', '')
            if not play_url:
                continue

            ext = self._get_file_extension(play_url, '.mp4')
            filename = f"video_{i:03d}{ext}"
            filepath = os.path.join(save_dir, filename)

            try:
                print(f"    [{i}/{total}] 正在下载视频: {play_url[:80]}...")
                async with session.get(play_url, timeout=aiohttp.ClientTimeout(total=120)) as resp:
                    if resp.status == 200:
                        content = await resp.read()
                        with open(filepath, 'wb') as f:
                            f.write(content)
                        size_mb = len(content) / (1024 * 1024)
                        success += 1
                        print(f"    [{i}/{total}] ✓ {filename} ({size_mb:.1f}MB)")
                    else:
                        print(f"    [{i}/{total}] ✗ HTTP {resp.status}")

                # 下载视频封面
                image_url = video.get('imageUrl', '')
                if image_url:
                    cover_path = os.path.join(save_dir, f"video_{i:03d}_cover.jpg")
                    async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                        if resp.status == 200:
                            with open(cover_path, 'wb') as f:
                                f.write(await resp.read())

            except Exception as e:
                print(f"    [{i}/{total}] ✗ 视频下载失败: {e}")

        print(f"  视频: {success}/{total} 个下载成功")

    @staticmethod
    def _sanitize_filename(name: str, max_length: int = 80) -> str:
        """清理文件名"""
        # 移除非法字符
        name = re.sub(r'[\\/:*?"<>|]', '', name)
        name = name.strip('. ')
        if len(name) > max_length:
            name = name[:max_length]
        return name or 'unknown_product'

    @staticmethod
    def _get_file_extension(url: str, default: str = '.jpg') -> str:
        """从 URL 获取文件扩展名"""
        path = url.split('?')[0]
        ext_match = re.search(r'\.(jpg|jpeg|png|gif|webp|mp4|avi|mov|avif)$', path, re.IGNORECASE)
        if ext_match:
            return '.' + ext_match.group(1).lower()
        return default


# ==================== 独立运行入口 ====================

async def main():
    """主函数 - 支持命令行运行"""
    import sys

    # 导入配置
    try:
        from jd_api_config import APP_KEY, APP_SECRET
    except ImportError:
        print("错误: 无法导入 jd_api_config.py，请确认配置文件存在")
        return

    if APP_KEY == "your_app_key_here":
        print("请先在 jd_api_config.py 中配置 APP_KEY 和 APP_SECRET")
        return

    # 初始化客户端
    client = JDApiClient(APP_KEY, APP_SECRET)

    # 获取商品 URL
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
    else:
        print("=" * 60)
        print("  京东商品资源下载器（API版）")
        print("  支持下载：商品标题、头图、详情图、视频")
        print("=" * 60)
        url_input = input("\n请输入商品 URL（多个用空格分隔）: ").strip()
        urls = url_input.split()

    if not urls:
        print("未输入商品 URL")
        return

    # 确定输出目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'downloads')

    # 逐个下载
    for url in urls:
        url = url.strip()
        if not url:
            continue
        print(f"\n{'#'*60}")
        print(f"  处理商品: {url}")
        print(f"{'#'*60}")
        await client.download_product(url, output_dir)

    print(f"\n🎉 全部完成！文件保存在: {output_dir}")


if __name__ == "__main__":
    asyncio.run(main())
