import minium

class DomesticFlightTest(minium.MiniTest):

    def test_01(self):
        pass


if __name__ == "__main__":
    import unittest
    loaded_suite = unittest.TestLoader().loadTestsFromTestCase(DomesticFlightTest)
    result = unittest.TextTestRunner().run(loaded_suite)
    print(result)