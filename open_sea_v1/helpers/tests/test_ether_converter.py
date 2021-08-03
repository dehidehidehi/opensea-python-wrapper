from unittest import TestCase

from open_sea_v1.helpers.ether_converter import EtherConverter, EtherUnit


class TestEtherUnitConverter(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = EtherConverter(quantity=35, unit=EtherUnit.GWEI)

    def test_to_wei(self):
        self.assertEqual(35_000_000_000, self.converter.wei)

    def test_to_kwei(self):
        self.assertEqual(35_000_000, self.converter.kwei)

    def test_to_mwei(self):
        self.assertEqual(35_000, self.converter.mwei)

    def test_to_gwei(self):
        self.assertEqual(35, self.converter.gwei)

    def test_to_twei(self):
        self.assertEqual(0.035, self.converter.twei)

    def test_to_pwei(self):
        self.assertEqual(0.000_035, self.converter.pwei)

    def test_to_ether(self):
        self.assertEqual(0.000_000_035, self.converter.ether)
