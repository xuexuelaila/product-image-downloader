# Product Image Downloader - 安装和使用指南

## 安装步骤

1. 安装 Python 依赖：
```bash
cd scripts
pip install -r requirements.txt
```

2. 安装 Playwright 浏览器：
```bash
playwright install chromium
```

## 使用方法

### 方式 1: 直接运行脚本

```bash
cd scripts
python downloader.py <商品链接1> <商品链接2> ...
```

示例：
```bash
python downloader.py \
  https://item.jd.com/100012345678.html \
  https://detail.tmall.com/item.htm?id=123456 \
  https://item.taobao.com/item.htm?id=789012
```

### 方式 2: 通过 Claude Code Skill 调用

```bash
/product-image-downloader
```

然后输入商品链接（每行一个）。

## 输出结构

下载的图片会保存在 `downloads/` 目录下，结构如下：

```
downloads/
└── 商品标题/
    ├── cover/      # 商品头图
    │   ├── 001.jpg
    │   ├── 002.jpg
    │   └── ...
    └── detail/     # 商品详情图
        ├── 001.jpg
        ├── 002.jpg
        └── ...
```

## 支持平台

- 京东 (jd.com)
- 天猫 (tmall.com)
- 淘宝 (taobao.com)

## 注意事项

1. 首次运行需要安装 Playwright 浏览器
2. 某些商品可能需要登录才能查看详情
3. 网络不稳定可能导致部分图片下载失败
4. 文件名会自动清理非法字符
5. 重复的商品标题会自动追加序号
