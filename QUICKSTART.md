# Product Image Downloader - 快速参考

## 安装(首次使用)
```bash
cd /Users/fangyaxin/qa-community/product-image-downloader
./install.sh
```

## 使用 - 一步完成!

### Claude Code Skill(推荐)

**最简单:**
```
/product-image-downloader https://item.jd.com/100171737237.html
```

**带描述:**
```
/product-image-downloader 下载这个 https://item.jd.com/100171737237.html
```

**批量下载:**
```
/product-image-downloader 下载这些 https://item.jd.com/123.html https://detail.tmall.com/456.html
```

**关键词搜索:**
```
/product-image-downloader 小米手机
```

### 命令行
```bash
cd /Users/fangyaxin/qa-community/product-image-downloader/scripts
python3 downloader.py "商品链接"
```

## 示例

### 单个商品
```
/product-image-downloader https://item.jd.com/100171737237.html
```

### 多个商品
```
/product-image-downloader https://item.jd.com/123.html https://detail.tmall.com/456.html
```

### 关键词搜索
```
/product-image-downloader 小米手机
```

## 智能识别

Skill会自动识别你的输入:
- ✓ 直接链接: `https://item.jd.com/123.html`
- ✓ 带描述: `下载这个 https://item.jd.com/123.html`
- ✓ 多个链接: `https://item.jd.com/123.html https://detail.tmall.com/456.html`
- ✓ 关键词: `小米手机`

## 输出位置
```
scripts/downloads/商品标题/
├── cover/   # 头图
└── detail/  # 详情图
```

## 支持平台
- 京东 (jd.com)
- 天猫 (tmall.com)
- 淘宝 (taobao.com)

## 常见问题

**Q: 需要登录?**
A: 浏览器会自动打开,等待30秒供你登录

**Q: 详情图不全?**
A: 头图通常完整,部分商品详情图可能抓取不全

**Q: 如何批量下载?**
A: 在一条命令中提供多个链接,用空格分隔

## 文档
- USAGE.md - 完整使用指南
- SKILL_SETUP.md - Skill设置说明
- OPTIMIZATION.md - 优化记录
- TEST_REPORT.md - 测试报告
