from abc import ABC, abstractmethod
from exceptions import NegativeConsumptionError

class WaterConsumer(ABC):
    def __init__(self, cid, consumption, tariff):
        self.cid = cid
        self.consumption = consumption
        self.tariff = tariff

    @abstractmethod
    def compute_bill(self):
        pass


class ResidentialConsumer(WaterConsumer):
    def compute_bill(self):
        return calculate_slab(self.consumption, self.tariff)


class CommercialConsumer(WaterConsumer):
    def compute_bill(self):
        return calculate_slab(self.consumption, self.tariff)


class IndustrialConsumer(WaterConsumer):
    def compute_bill(self):
        return calculate_slab(self.consumption, self.tariff)


def calculate_slab(units, slabs):
    if units < 0:
        raise NegativeConsumptionError("Negative consumption not allowed")

    bill = 0
    prev = 0

    for slab in slabs:
        limit = slab["limit"]
        rate = slab["rate"]

        if limit == "above":
            bill += (units - prev) * rate
            break

        if units > limit:
            bill += (limit - prev) * rate
            prev = limit
        else:
            bill += (units - prev) * rate
            break

    return bill
