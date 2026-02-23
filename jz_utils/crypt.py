import base64

from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad, pad


def des3_encrypt(plaintext, key):
    """
    该函数用于对明文进行3DES加密，并返回Base64编码的密文
    :param plaintext: 需要加密的明文字符串
    :param key: 3DES使用的密钥，长度必须是16或24字节
    :return: 经过Base64编码的3DES密文
    """
    # 检查密钥长度是否符合要求
    if len(key) not in [16, 24]:
        raise ValueError("3DES key must be 16 or 24 bytes long.")

    # 创建3DES加密器对象，使用ECB模式
    cipher = DES3.new(key.encode("utf-8"), DES3.MODE_ECB)

    # 对明文进行PKCS7填充
    padded_data = pad(plaintext.encode("utf-8"), DES3.block_size)

    # 执行加密操作
    ciphertext = cipher.encrypt(padded_data)

    # 对加密后的数据进行Base64编码
    ciphertext_base64 = base64.b64encode(ciphertext).decode("utf-8")

    return ciphertext_base64


def des3_decrypt(ciphertext_base64, key):
    """
    该函数用于对Base64编码的3DES密文进行解密
    :param ciphertext_base64: 经过Base64编码的3DES密文
    :param key: 3DES使用的密钥，长度可以是16或24字节
    :return: 解密后的明文
    """
    # 检查密钥长度是否符合要求
    if len(key) not in [16, 24]:
        raise ValueError("3DES key must be 16 or 24 bytes long.")
    # 对Base64编码的密文进行解码
    ciphertext = base64.b64decode(ciphertext_base64)
    # 创建3DES解密器对象，使用ECB模式
    cipher = DES3.new(key.encode("utf-8"), DES3.MODE_ECB)
    # 执行解密操作
    decrypted_data = cipher.decrypt(ciphertext)
    # 去除填充
    plaintext = unpad(decrypted_data, DES3.block_size)
    return plaintext.decode("utf-8")


if __name__ == "__main__":
    # 3DES密钥，长度可以是16或24字节
    key = "d10b9dfdccb743788508ar20"
    raw_txt = "server=127.0.0.1,999;uid=AAAAA;pwd=AAAAA;database=shark;max pool size=5000;MultipleActiveResultSets=True"
    # 假设这是经过Base64编码的3DES加密密文
    ciphertext_base64 = "llREXHnWxpPCUXjoidE66YGWA7uyjWJKFAh4TvQvp9XnFRKLxPtRKvBA2KxE9nrjZJeQYp2UmOh99GIIB+5rB74KxwtB1+L3u5Ak3Yz16irJ4qUkoQy9NQZSlibsWOgv4uRqEcb03ztEzYDsOs2g2Q=="

    try:
        encrypted_text = des3_encrypt(raw_txt, key)
        print("加密后的密文: ", encrypted_text)
        print(encrypted_text == ciphertext_base64)
        # 调用解密函数
        decrypted_text = des3_decrypt(ciphertext_base64, key)
        print("解密后的明文: ", decrypted_text)
        print(decrypted_text == raw_txt)
    except ValueError as e:
        print("解密出错: ", e)
