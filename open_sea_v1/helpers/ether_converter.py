from dataclasses import dataclass
from enum import IntEnum
from typing import Union


class EtherUnit(IntEnum):
    """
    Ether sub-units quantified in Wei.
    """

    WEI = 1
    KWEI = 1_000
    MWEI = 1_000_000
    GWEI = 1_000_000_000
    TWEI = 1_000_000_000_000
    PWEI = 1_000_000_000_000_000
    ETHER = 1_000_000_000_000_000_000


@dataclass
class EtherConverter:
    """
    Convenience class that helps convert Ether and its sub-units (gwei, twei etc.) into other sub-units.
    """

    quantity: Union[str, int, float]
    unit: EtherUnit

    def __post_init__(self):
        if isinstance(self.quantity, str):
            self.quantity = float(self.quantity)

    def convert_to(self, unit: EtherUnit) -> float:
        if unit == self.unit:
            return self.quantity
        return self.unit / unit * self.quantity

    @property
    def ether(self):
        return self.convert_to(EtherUnit.ETHER)

    @property
    def pwei(self):
        return self.convert_to(EtherUnit.PWEI)

    @property
    def twei(self):
        return self.convert_to(EtherUnit.TWEI)

    @property
    def gwei(self):
        return self.convert_to(EtherUnit.GWEI)

    @property
    def mwei(self):
        return self.convert_to(EtherUnit.MWEI)

    @property
    def kwei(self):
        return self.convert_to(EtherUnit.KWEI)

    @property
    def wei(self):
        return self.convert_to(EtherUnit.WEI)
