coupons = [
    {"id": 1, "code": "SAVE10", "discount": 10, "active": True},
    {"id": 2, "code": "FLAT50", "discount": 50, "active": True},
    {"id": 3, "code": "EXPIRED", "discount": 5, "active": False},
]

def get_all():
    return coupons

def get_by_code(code):
    return next((c for c in coupons if c["code"] == code.upper()), None)

def create(code, discount):
    new = {
        "id": len(coupons) + 1,
        "code": code.upper(),
        "discount": discount,
        "active": True
    }
    coupons.append(new)
    return new