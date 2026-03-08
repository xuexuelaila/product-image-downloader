# Product Image Downloader - 使用指南

## 快速开始

### 1. 安装依赖(首次使用)

```bash
cd /Users/fangyaxin/qa-community/product-image-downloader/scripts
pip install -r requirements.txt
playwright install chromium
```

### 2. 使用方式

#### 方式A: 通过Claude Code Skill(推荐)

在Claude Code中直接输入:

```
/product-image-downloader
```

然后输入商品链接,例如:
```
https://item.jd.com/100171737237.html
```

#### 方式B: 直接运行脚本

```bash
cd /Users/fangyaxin/qa-community/product-image-downloader/scripts
python3 downloader.py "https://item.jd.com/100171737237.html"
```

#### 方式C: 批量下载

```bash
python3 downloader.py \
  "https://item.jd.com/100171737237.html" \
  "https://detail.tmall.com/item.htm?id=123456" \
  "https://item.taobao.com/item.htm?id=789012"
```

#### 方式D: 关键词搜索(淘宝)

```bash
python3 downloader.py "小米手机"
```

## 功能特性

### 支持的平台
- ✓ 京东 (jd.com)
- ✓ 天猫 (tmall.com)
- ✓ 淘宝 (taobao.com)

### 抓取内容
- **头图**: 商品主图、多角度图片
- **详情图**: 商品详情页的介绍图片

### 智能功能
- 自动识别平台
- 自动点击"商品详情"标签
- 智能滚动加载图片
- 自动处理登录(等待30秒)
- 自动去重
- 自动转换图片格式(avif→jpg)
- 自动清理文件名非法字符

## 输出结构

下载的图片保存在 `scripts/downloads/` 目录:

```
downloads/
└── 商品标题/
    ├── cover/      # 头图
    │   ├── 001.jpg
    │   ├── 002.jpg
    │   └── ...
    └── detail/     # 详情图
        ├── 001.jpg
        ├── 002.jpg
        └── ...
```

## 配置说明

所有配置在 `downloader.py` 的 `Config` 类中:

```python
class Config:
    # 浏览器配置
    USER_AGENT = '...'

    # 超时配置
    PAGE_TIMEOUT = 60000  # 页面加载超时(毫秒)
    IMAGE_TIMEOUT = 30    # 图片下载超时(秒)

    # 滚动配置
    MAX_SCROLLS = 30      # 最大滚动次数
    SCROLL_STEP_MIN = 300 # 最小滚动距离(px)
    SCROLL_STEP_MAX = 500 # 最大滚动距离(px)

    # 图片尺寸过滤
    MIN_IMAGE_SIZE = 200   # 最小图片尺寸(px)
    MIN_DETAIL_SIZE = 400  # 详情图最小尺寸(px)
```

## 常见问题

### Q: 首次运行报错?
A: 确保已安装依赖:
```bash
pip install -r requirements.txt
playwright install chromium
```

### Q: 需要登录怎么办?
A: 脚本会自动检测登录页面,等待30秒供你在浏览器中登录。登录后会自动保存状态,下次不需要重复登录。

### Q: 详情图抓取不全?
A: 某些商品的详情图可能需要特殊的加载条件。当前版本已经优化了滚动和等待逻辑,但部分商品可能仍然无法抓取所有详情图。头图通常都能完整抓取。

### Q: 如何批量下载?
A: 可以在命令行中提供多个链接,或者使用skill时一次输入多个链接(每行一个)。

### Q: 支持关键词搜索吗?
A: 支持!输入关键词(不是URL)会自动在淘宝搜索并下载第一个商品的图片。

### Q: 下载速度慢?
A: 为了模拟真实用户行为,脚本会随机延迟和滚动。这是为了避免被反爬虫机制检测。

### Q: 浏览器窗口会自动关闭吗?
A: 会的,下载完成后浏览器会自动关闭。

## 技术细节

### 优化特性
- Config配置类集中管理
- 辅助方法提高代码复用
- 智能滚动触发懒加载
- 自动点击商品详情标签
- 支持多种图片格式
- 完善的错误处理

### 浏览器特性
- 使用持久化上下文(保存登录状态)
- 隐藏webdriver特征
- 自定义User-Agent
- 模拟真实用户行为

## 示例输出

```
开始处理 1 个商品链接...

正在处理京东商品: https://item.jd.com/100171737237.html
  页面已加载，等待 5 秒...
  商品标题: 只换不修
  开始逐步滚动页面,加载所有图片...
  滚动完成,共滚动 6 次
  已点击'商品详情'标签
  下载头图: 9 张
  下载详情图: 5 张
  完成: 头图 9/9, 详情图 5/5
  保存位置: downloads/只换不修_1

============================================================
处理完成！
成功: 1 个
失败: 0 个

成功的商品:
  ✓ 只换不修
    头图: 9 张, 详情图: 5 张
    位置: downloads/只换不修_1
============================================================
```

## 更新日志

### 2026-03-08
- ✓ 添加Config配置类
- ✓ 添加多个辅助方法
- ✓ 改进滚动和等待逻辑
- ✓ 添加点击"商品详情"标签功能
- ✓ 支持avif格式转换
- ✓ 优化代码结构

## 许可证

MIT License

## 支持

如有问题,请查看:
- OPTIMIZATION.md - 代码优化记录
- DETAIL_IMAGE_ISSUE.md - 详情图抓取问题说明
- TEST_REPORT.md - 测试报告
