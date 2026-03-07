# Product Image Downloader

自动从电商平台抓取商品图片的工具。

## 功能

- 支持批量处理多个商品链接
- 自动识别平台（京东、天猫、淘宝）
- 抓取商品标题、头图和详情图
- 自动创建规范的文件夹结构
- 智能处理文件名和错误

## 使用方法

```bash
/product-image-downloader
```

然后输入商品链接（每行一个），或者直接粘贴多个链接。

## 输出结构

```
商品标题/
├── cover/      # 头图
└── detail/     # 详情图
```

## 支持平台

- 京东 (jd.com)
- 天猫 (tmall.com)
- 淘宝 (taobao.com)
