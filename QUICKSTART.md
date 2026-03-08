# Product Image Downloader - 快速参考

## 安装(首次使用)
```bash
cd /Users/fangyaxin/qa-community/product-image-downloader
./install.sh
```

## 使用

### Claude Code Skill
```
/product-image-downloader
```

### 命令行
```bash
cd /Users/fangyaxin/qa-community/product-image-downloader/scripts
python3 downloader.py "商品链接"
```

## 示例

### 单个商品
```bash
python3 downloader.py "https://item.jd.com/100171737237.html"
```

### 多个商品
```bash
python3 downloader.py \
  "https://item.jd.com/100171737237.html" \
  "https://detail.tmall.com/item.htm?id=123456"
```

### 关键词搜索
```bash
python3 downloader.py "小米手机"
```

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
A: 提供多个链接,用空格分隔

## 文档
- USAGE.md - 完整使用指南
- OPTIMIZATION.md - 优化记录
- TEST_REPORT.md - 测试报告
