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

import binascii  # , sys, os, importlib
# importlib.reload(sys)
# os.environ['NLS_LANG'] = 'Simplified Chinese_CHINA.ZHS16GBK'
# from Crypto import Random
from Crypto.Cipher import AES


class EncryptionAndDecryption(object):
    def __init__(self, key, iv, mode=AES.MODE_CFB):
        # MODE_CFB为加密模式
        self.key = self.PadKey(key)
        self.mode = mode
        self.iv = iv
        """
        if iv:
            self.iv = iv
        else:
            self.iv = b'1234567890123456'
            # self.iv = Random.new().read(AES.block_size)
            # self.iv = Random.new().read(16)  # 随机向量，必须是16字节长度
        """

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    # 加密内容需要长达16位字符，所以进行空格拼接
    def PadText(self, text):
        while len(text) % AES.block_size != 0:
            text += str.encode(' ')
        return text

    # 加密密钥需要长达16位字符，所以进行空格拼接
    def PadKey(self, key):
        key = str.encode(key)
        while len(key) % AES.block_size != 0:
            key += b' '
        return key

    def Encryption(self, text):
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        # 加密的字符需要转换为bytes
        aes = AES.new(self.key, self.mode, self.iv)
        # 密文生成器,MODE_CFB为加密模式
        result = aes.encrypt(self.PadText(text))
        # 附加上iv值是为了在解密时找到在加密时用到的iv
        return binascii.b2a_hex(result)  # 将二进制密文转换为16进制显示

    # 解密后，去掉补足的空格用strip() 去掉
    def Decryption(self, encrypt_msg):
        aes = AES.new(self.key, self.mode, self.iv)
        # 解密时必须重新创建新的密文生成器
        result = aes.decrypt(binascii.a2b_hex(encrypt_msg)).rstrip(b' ')
        return bytes.decode(result)


if __name__ == "__main__":
    key = 'iReadyIT'
    iv = b'1234567890123456'
    # 指定的向量，必须是16字节长度
    pc = EncryptionAndDecryption(key, iv)
    # 初始化密钥
    data = "测试一下，我是明文。"
    e = bytes.decode(pc.Encryption(data.encode('utf-8')))
    d = pc.Decryption(e)
    print("加密Key是：" + key, "\n明文是：" + d, "\n密文是：" + e)
