#!/usr/bin/env python3
"""
京东 API 签名测试脚本
帮助理解和调试签名生成过程
"""

import hashlib
import time
import json
from jd_api_config import APP_KEY, APP_SECRET

def generate_signature(secret, parameters):
    """
    生成京东 API 签名

    签名算法：
    1. 将所有参数按照参数名的字典序排序
    2. 拼接成字符串：secret + key1 + value1 + key2 + value2 + ... + secret
    3. 对拼接后的字符串进行 MD5 加密
    4. 转换为大写
    """
    # 按字典序排序参数
    sorted_keys = sorted(parameters.keys())

    # 拼接字符串
    sign_string = secret
    for key in sorted_keys:
        sign_string += key + str(parameters[key])
    sign_string += secret

    # MD5 加密并转大写
    signature = hashlib.md5(sign_string.encode("utf-8")).hexdigest().upper()

    return signature, sign_string

def test_signature():
    """测试签名生成"""
    print("=" * 80)
    print("京东 API 签名测试")
    print("=" * 80)

    # 显示配置
    print(f"\\n【配置信息】")
    print(f"APP_KEY: {APP_KEY}")
    print(f"APP_SECRET: {APP_SECRET[:10]}...{APP_SECRET[-10:]} (已部分隐藏)")
    print(f"APP_SECRET 长度: {len(APP_SECRET)} 字符")

    # 检查密钥格式
    print(f"\\n【密钥检查】")
    if len(APP_KEY) != 32:
        print(f"⚠️  警告：APP_KEY 长度不是 32 位（当前 {len(APP_KEY)} 位）")
        print(f"   标准的京东 APP_KEY 应该是 32 位十六进制字符串")
    else:
        print(f"✓ APP_KEY 长度正确（32 位）")

    if len(APP_SECRET) != 32:
        print(f"⚠️  警告：APP_SECRET 长度不是 32 位（当前 {len(APP_SECRET)} 位）")
        print(f"   标准的京东 APP_SECRET 应该是 32 位十六进制字符串")
    else:
        print(f"✓ APP_SECRET 长度正确（32 位）")

    # 检查是否包含非法字符
    if not APP_KEY.replace('_', '').replace('-', '').isalnum():
        print(f"⚠️  警告：APP_KEY 包含特殊字符")

    if not APP_SECRET.replace('_', '').replace('-', '').isalnum():
        print(f"⚠️  警告：APP_SECRET 包含特殊字符")

    # 模拟一个 API 请求参数
    print(f"\\n【签名生成测试】")
    print(f"模拟调用 API: jd.union.open.goods.query")

    # 构造请求参数
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    parameters = {
        "app_key": APP_KEY,
        "method": "jd.union.open.goods.query",
        "timestamp": timestamp,
        "format": "json",
        "v": "1.0",
        "360buy_param_json": json.dumps({"skuIds": [100313528034]})
    }

    print(f"\\n请求参数：")
    for key, value in sorted(parameters.items()):
        if key == "360buy_param_json":
            print(f"  {key}: {value}")
        else:
            print(f"  {key}: {value}")

    # 生成签名
    signature, sign_string = generate_signature(APP_SECRET, parameters)

    print(f"\\n【签名生成过程】")
    print(f"1. 参数排序后的顺序：")
    for i, key in enumerate(sorted(parameters.keys()), 1):
        print(f"   {i}. {key}")

    print(f"\\n2. 拼接字符串（部分显示）：")
    if len(sign_string) > 200:
        print(f"   {sign_string[:100]}...")
        print(f"   ...{sign_string[-100:]}")
    else:
        print(f"   {sign_string}")

    print(f"\\n3. 拼接字符串长度：{len(sign_string)} 字符")

    print(f"\\n4. MD5 加密后的签名：")
    print(f"   {signature}")

    print(f"\\n5. 签名长度：{len(signature)} 字符")

    # 验证签名格式
    print(f"\\n【签名验证】")
    if len(signature) == 32:
        print(f"✓ 签名长度正确（32 位）")
    else:
        print(f"✗ 签名长度错误（应该是 32 位，当前 {len(signature)} 位）")

    if signature.isupper():
        print(f"✓ 签名已转换为大写")
    else:
        print(f"✗ 签名未转换为大写")

    if signature.isalnum():
        print(f"✓ 签名只包含字母和数字")
    else:
        print(f"✗ 签名包含特殊字符")

    # 完整的请求参数（包含签名）
    print(f"\\n【完整请求参数】")
    parameters["sign"] = signature
    print(f"最终发送给京东 API 的参数：")
    for key, value in sorted(parameters.items()):
        if key == "360buy_param_json":
            print(f"  {key}: {value}")
        elif key == "sign":
            print(f"  {key}: {value} ← 这是生成的签名")
        else:
            print(f"  {key}: {value}")

    print(f"\\n" + "=" * 80)
    print(f"签名测试完成")
    print(f"=" * 80)

    # 给出建议
    print(f"\\n【排查建议】")
    print(f"1. 如果签名格式正确，但仍然报错，可能是：")
    print(f"   - APP_KEY 或 APP_SECRET 不正确")
    print(f"   - 应用未获得 API 调用权限")
    print(f"   - 应用状态不正常（未上线、已禁用等）")
    print(f"\\n2. 请登录京东开放平台检查：")
    print(f"   - https://open.jd.com/")
    print(f"   - 进入【控制台】→【应用管理】")
    print(f"   - 核对 APP_KEY 和 APP_SECRET")
    print(f"   - 检查应用状态和 API 权限")
    print(f"\\n3. 如果是新应用，可能需要：")
    print(f"   - 等待应用审核通过")
    print(f"   - 申请相应的 API 权限")
    print(f"   - 加入京东联盟（如果使用联盟 API）")

if __name__ == "__main__":
    test_signature()
