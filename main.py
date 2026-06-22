#Smart Water Billing System:
import csv
from datetime import datetime
from tariff_loader import load_tariffs
from consumers import ResidentialConsumer, CommercialConsumer, IndustrialConsumer
from exceptions import InvalidCategoryError, NegativeConsumptionError

tariffs = load_tariffs()

category_map = {
    "Residential": ResidentialConsumer,
    "Commercial": CommercialConsumer,
    "Industrial": IndustrialConsumer
}

def is_late(due_days):
    return due_days > 0


def main():
    revenue = {"Residential": 0, "Commercial": 0, "Industrial": 0}

    with open("bills_report.txt", "w") as report:

        with open("customers.csv", "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    cid = row["id"]
                    ctype = row["type"]
                    consumption = float(row["consumption"])
                    due_days = int(row["due_days"])

                    if ctype not in category_map:
                        raise InvalidCategoryError("Invalid category")

                    consumer_class = category_map[ctype]
                    consumer = consumer_class(cid, consumption, tariffs[ctype])

                    bill = consumer.compute_bill()

                    late_fee = 0
                    if is_late(due_days):
                        late_fee = 0.05 * bill

                    total = bill + late_fee

                    revenue[ctype] += total

                    report.write(
                        f"{cid},{ctype},{consumption},{bill:.2f},{late_fee:.2f},{total:.2f}\n"
                    )

                except (InvalidCategoryError, NegativeConsumptionError) as e:
                    print(f"Error for {row}: {e}")

    
    with open("summary_report.txt", "w") as summary:
        for k, v in revenue.items():
            summary.write(f"{k}: {v:.2f}\n")


if __name__ == "__main__":
    main()
