# Product Image Downloader - 商品图片下载器

自动从电商平台批量下载商品图片的工具。

## 特性

- ✓ 支持京东、天猫、淘宝
- ✓ 自动抓取头图和详情图
- ✓ 支持批量下载
- ✓ 支持关键词搜索
- ✓ 自动处理登录
- ✓ 智能滚动加载
- ✓ 代码已优化

## 快速开始

### 1. 安装

```bash
cd /Users/fangyaxin/qa-community/product-image-downloader
./install.sh
```

或手动安装:

```bash
cd scripts
pip install -r requirements.txt
playwright install chromium
```

### 2. 使用

#### 方式A: Claude Code Skill(推荐)

```
/product-image-downloader
```

然后输入商品链接。

#### 方式B: 命令行

```bash
cd scripts
python3 downloader.py "https://item.jd.com/100171737237.html"
```

## 文档

- [USAGE.md](USAGE.md) - 详细使用指南
- [OPTIMIZATION.md](OPTIMIZATION.md) - 代码优化记录
- [TEST_REPORT.md](TEST_REPORT.md) - 测试报告
- [DETAIL_IMAGE_ISSUE.md](DETAIL_IMAGE_ISSUE.md) - 详情图问题说明

## 输出结构

```
downloads/
└── 商品标题/
    ├── cover/      # 头图
    └── detail/     # 详情图
```

## 支持平台

- 京东 (jd.com)
- 天猫 (tmall.com)
- 淘宝 (taobao.com)

## 许可证

MIT License
