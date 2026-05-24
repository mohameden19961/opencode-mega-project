def calculate_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total


def format_address(address):
    parts = [
        address.street,
        address.city,
        address.zip_code,
        address.country,
    ]
    return ", ".join(p for p in parts if p)


class OrderProcessor:
    def __init__(self, tax_rate=0.0):
        self.tax_rate = tax_rate

    def process(self, order):
        subtotal = calculate_total(order.items)
        tax = subtotal * self.tax_rate
        total = subtotal + tax
        return {"subtotal": subtotal, "tax": tax, "total": total}
