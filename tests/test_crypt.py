import unittest

from jz_utils.crypt import des3_decrypt, des3_encrypt


class TestCrypt(unittest.TestCase):
    def test_des3(self):
        key = "d10b9dfdccb743788508ar20"
        raw_txt = (
            "server=127.0.0.1,999;uid=AAAAA;pwd=AAAAA;database=shark;max pool size=5000;MultipleActiveResultSets=True"
        )
        ciphertext_base64 = "llREXHnWxpPCUXjoidE66YGWA7uyjWJKFAh4TvQvp9XnFRKLxPtRKvBA2KxE9nrjZJeQYp2UmOh99GIIB+5rB74KxwtB1+L3u5Ak3Yz16irJ4qUkoQy9NQZSlibsWOgv4uRqEcb03ztEzYDsOs2g2Q=="

        encrypted_text = des3_encrypt(raw_txt, key)
        self.assertEqual(encrypted_text, ciphertext_base64)

        decrypted_text = des3_decrypt(ciphertext_base64, key)
        self.assertEqual(decrypted_text, raw_txt)


if __name__ == "__main__":
    unittest.main()
