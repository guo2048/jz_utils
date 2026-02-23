import unittest

from jz_utils.singleton import singleton


@singleton
class TestClass:
    def __init__(self, v1, v2, v3=None, v4=10):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4


class TestSingleton(unittest.TestCase):
    def test_singleton(self):
        instance1 = TestClass(v1=10, v2=30, v4=60)
        instance2 = TestClass(20, 20)
        instance3 = TestClass(10, 30, v4=60)

        self.assertIsNot(instance1, instance2)
        self.assertIs(instance1, instance3)
        self.assertEqual(instance1.v1, 10)
        self.assertEqual(instance3.v2, 30)
        self.assertEqual(instance2.v2, 20)


if __name__ == "__main__":
    unittest.main()
