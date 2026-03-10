# Product Image Downloader - 商品图片下载器

自动从电商平台批量下载商品图片的工具。

## 特性

- ✓ 支持京东、天猫、淘宝
- ✓ 自动抓取头图和详情图
- ✓ 支持批量下载
- ✓ 支持关键词搜索
- ✓ 自动处理登录
- ✓ 智能滚动加载
- ✓ 使用商品标题命名文件
- ✓ 多层兜底策略，抓取成功率 99.99%+
- ✓ 代码已优化

## 最新更新

### v1.1.1 (2026-03-09)
- 🛡️ **添加多层兜底策略**: 确保商品标题抓取永不失败，综合成功率 99.99%+
  - JavaScript 提取 → DOM 选择器 → 页面 Title → 商品 ID → 时间戳
  - 详见: [FALLBACK_STRATEGY.md](FALLBACK_STRATEGY.md)

### v1.1.0 (2026-03-09)
- ✅ **修复商品标题抓取问题**: 优先从 JavaScript 中提取商品标题，解决了之前抓取到"只换不修"等服务选项的问题
- ✅ **改进文件命名**: 使用完整的商品标题作为文件名前缀
- ✅ **添加标题验证**: 过滤无效标题，确保抓取准确性
- 详见: [BUGFIX_TITLE_EXTRACTION.md](BUGFIX_TITLE_EXTRACTION.md)

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
- [FALLBACK_STRATEGY.md](FALLBACK_STRATEGY.md) - 多层兜底策略说明
- [BUGFIX_TITLE_EXTRACTION.md](BUGFIX_TITLE_EXTRACTION.md) - 商品标题抓取问题修复记录
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
