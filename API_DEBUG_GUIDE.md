# 京东 API 签名问题排查指南

## 📋 问题描述

当前 API 调用返回错误：
```
错误代码：12
错误信息：无效签名（Invalid Signature）
```

## 🔍 排查步骤

### 第一步：验证 APP_KEY 和 APP_SECRET

1. **登录京东开放平台**
   - 访问：https://open.jd.com/
   - 使用你的账号登录

2. **找到你的应用**
   - 进入"控制台" → "应用管理"
   - 找到你创建的应用

3. **核对密钥**
   - 查看应用详情，找到 App Key 和 App Secret
   - 对比 `scripts/jd_api_config.py` 中的配置：
     ```python
     APP_KEY = "901a3dbb017ab45074c6dfc66e269a59"
     APP_SECRET = "e11a771e1dfe4c80adfa9e0f71abbc7a"
     ```
   - 确保完全一致（注意空格、大小写）

### 第二步：检查应用状态和权限

1. **应用状态**
   - 确认应用状态为"已上线"或"测试中"
   - 如果是"未上线"，可能无法调用 API

2. **API 权限**
   - 检查应用是否有以下 API 的调用权限：
     - `jd.union.open.goods.query` - 商品基础信息查询
     - `jd.union.open.goods.bigfield.query` - 商品大字段查询

3. **如何申请权限**
   - 在应用详情页面，找到"API 权限管理"
   - 申请上述两个 API 的权限
   - 等待审核通过

### 第三步：检查 API 类型

京东开放平台有多种 API 类型：

1. **京东联盟 API**（推广类）
   - 需要加入京东联盟
   - 主要用于推广、返佣
   - API 域名：`api.jd.com` 或 `router.jd.com`

2. **京东开放平台 API**（商家类）
   - 需要是京东商家
   - 用于店铺管理、商品管理
   - API 域名：`api.jd.com`

3. **京东云市场 API**
   - 第三方服务
   - 需要购买服务

**当前项目使用的是京东联盟 API**，请确认：
- 你的账号已加入京东联盟
- 应用类型选择的是"联盟应用"

### 第四步：测试签名生成

运行签名测试脚本：

```bash
cd /Users/fangyaxin/qa-community/product-image-downloader/scripts
python3 test_signature.py
```

这个脚本会：
1. 显示签名生成的详细过程
2. 帮助你理解签名算法
3. 验证签名是否正确

### 第五步：检查网络和域名

1. **API 域名配置**
   - 当前配置：`gw.api.360buy.com`
   - 可能的其他域名：
     - `api.jd.com`
     - `router.jd.com`

2. **测试网络连接**
   ```bash
   ping gw.api.360buy.com
   curl -I https://gw.api.360buy.com
   ```

### 第六步：查看京东官方文档

1. **签名算法文档**
   - https://open.jd.com/v2/#/doc/guide?listId=533

2. **API 调用文档**
   - https://union.jd.com/openplatform/api

3. **常见问题**
   - https://open.jd.com/v2/#/doc/guide?listId=534

## 🛠️ 可能的解决方案

### 方案 1：重新生成密钥

如果密钥可能泄露或有问题：
1. 在京东开放平台重新生成 App Secret
2. 更新 `scripts/jd_api_config.py` 中的配置
3. 重新测试

### 方案 2：更换 API 域名

尝试不同的 API 域名：

编辑 `scripts/jd_api_config.py`：
```python
# 尝试方案 1
API_DOMAIN = "api.jd.com"

# 或尝试方案 2
API_DOMAIN = "router.jd.com"
```

### 方案 3：检查 SDK 版本

京东 SDK 可能需要更新：
1. 查看 SDK 版本
2. 从京东开放平台下载最新 SDK
3. 替换 `scripts/jd/` 目录

### 方案 4：联系京东技术支持

如果以上方法都不行：
1. 在京东开放平台提交工单
2. 描述问题：API 调用返回"无效签名"错误
3. 提供：App Key、调用的 API 名称、错误信息

## 📝 下一步操作

请按照以下顺序执行：

1. ✅ **第一步**：验证 APP_KEY 和 APP_SECRET（最常见的问题）
2. ✅ **第二步**：检查应用状态和 API 权限
3. ✅ **第三步**：确认应用类型（联盟应用 vs 商家应用）
4. ⏳ **第四步**：运行签名测试脚本（我会帮你创建）
5. ⏳ **第五步**：尝试不同的解决方案

## 💡 提示

- 签名问题 90% 是因为密钥错误或权限不足
- 如果是新创建的应用，可能需要等待审核
- 京东联盟 API 需要先加入京东联盟才能使用

---

**需要帮助？** 告诉我你完成了哪一步，遇到了什么问题，我会继续帮你排查。
