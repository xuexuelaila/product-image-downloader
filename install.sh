#!/bin/bash

# Product Image Downloader - 安装脚本

echo "================================"
echo "Product Image Downloader 安装"
echo "================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    echo "请先安装 Python 3"
    exit 1
fi

echo "✓ Python 已安装: $(python3 --version)"
echo ""

# 安装Python依赖
echo "正在安装 Python 依赖..."
cd scripts
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Python 依赖安装成功"
else
    echo "❌ Python 依赖安装失败"
    exit 1
fi

echo ""

# 安装Playwright浏览器
echo "正在安装 Playwright 浏览器..."
playwright install chromium

if [ $? -eq 0 ]; then
    echo "✓ Playwright 浏览器安装成功"
else
    echo "❌ Playwright 浏览器安装失败"
    exit 1
fi

echo ""
echo "================================"
echo "✓ 安装完成!"
echo "================================"
echo ""
echo "使用方法:"
echo "  1. 在 Claude Code 中输入: /product-image-downloader"
echo "  2. 或直接运行: cd scripts && python3 downloader.py <商品链接>"
echo ""
echo "详细文档: 查看 USAGE.md"
echo ""
