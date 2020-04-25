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
    def __init__(self, key, iv=None, mode=AES.MODE_CFB):
        self.key = self.PadKey(key)
        self.mode = mode  # MODE_CFB为加密模式
        if iv:
            self.iv = iv
        else:
            self.iv = Random.new().read(AES.block_size)
            # self.iv = Random.new().read(16)  # 随机向量，必须是16字节长度

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
        # 加密的字符需要转换为bytes
        data = self.PadText(text)
        aes = AES.new(self.key, self.mode, self.iv)  # 密文生成器,MODE_CFB为加密模式
        result = self.iv + aes.encrypt(data)  # 附加上iv值是为了在解密时找到在加密时用到的随机iv
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return binascii.b2a_hex(result)  # 将二进制密文转换为16机制显示

    # 解密后，去掉补足的空格用strip() 去掉
    def Decryption(self, encrypt_msg):
        text = binascii.a2b_hex(encrypt_msg)
        aes = AES.new(self.key, self.mode, self.iv)  # 解密时必须重新创建新的密文生成器
        return aes.decrypt(text[AES.block_size:]).rstrip(' ')


if __name__ == "__main__":
    k = b"iReadyITiReadyIT"
    pc = EncryptionAndDecryption(k)  # 初始化密钥
    iv = pc.iv
    data = ('我是明文测试')
    e = pc.Encryption(data)
    d = pc.Decryption(e)
    print "加密Key是：" + k, "\n明文是：" + d, "\n密文是：" + e
