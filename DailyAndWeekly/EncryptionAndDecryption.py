# python
# -*- coding:utf-8 -*-

"""
@FileName: EncryptionAndDecryption.py
@Version: v1.0
@Author: Micheal Zhou
@CreateTime: 2020-04-22 14:06
@License: GPL
@Contact: zhougf930@163.com
@See:
"""

import binascii
from Crypto import Random
from Crypto.Cipher import AES


class EncryptionAndDecryption(object):
    def __init__(self, key, mode=AES.MODE_ECB):
        # MODE_ECB为加密模式
        self.key = self.PadKey(key)
        self.mode = mode

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    # 加密内容需要长达16位字符，所以进行空格拼接
    def PadText(self, text):
        while len(text) % AES.block_size != 0:
            text += ' '
        return text

    # 加密密钥需要长达16位字符，所以进行空格拼接
    def PadKey(self, key):
        while len(key) % AES.block_size != 0:
            key += ' '
        return key

    def Encryption(self, text):
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        data = self.PadText(text)
        # 加密的字符需要转换为bytes
        aes = AES.new(self.key, self.mode)
        # 密文生成器,MODE_ECB为加密模式
        result = aes.encrypt(data)
        return binascii.b2a_hex(result)
        # 将二进制密文转换为16机制显示

    # 解密后，去掉补足的空格用strip() 去掉
    def Decryption(self, encrypt_msg):
        aes = AES.new(self.key, self.mode)
        # 解密时必须重新创建新的密文生成器
        return aes.decrypt(binascii.a2b_hex(encrypt_msg)).rstrip(' ')


if __name__ == "__main__":
    k = b"iReadyIT"
    pc = EncryptionAndDecryption(k)  # 初始化密钥
    data = ('这里是测试，我是明文。')
    e = pc.Encryption(data)
    d = pc.Decryption(e)
    print "加密Key是：" + k, "\n明文是：" + d, "\n密文是：" + e
