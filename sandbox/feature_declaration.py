from math import log
from statistics import stdev, mean


def returns_1(price: float, last_price: float) -> float:
    return log(price / last_price)


def vol_3(series:list[float]) -> float:
    if len(series) != 3:
        raise ValueError(f"len(series)={len(series)} != 3.")
    return stdev(series)


def z_score_3(window: list[float]) -> float:
    if len(window) != 3:
        raise ValueError(f"len(window)={len(window)} != 3.")

    value = window[-1]
    m = mean(window)
    sigma = stdev(window)

    if sigma == 0.0:
        raise ValueError("z_score is undefined when standard deviation is zero.")

    return (value - m) / sigma



if __name__ == "__main__":
    prices = [100.0, 110.0, 105.0, 90.0, 92.0, 101.0]

    r1 = returns_1(price=prices[1], last_price=prices[0])
    r2 = returns_1(price=prices[2], last_price=prices[1])
    r3 = returns_1(price=prices[3], last_price=prices[2])
    r4 = returns_1(price=prices[4], last_price=prices[3])
    r5 = returns_1(price=prices[5], last_price=prices[4])

    v1 = vol_3([r1, r2, r3])
    v2 = vol_3([r2, r3, r4])
    v3 = vol_3([r3, r4, r5])

    z = z_score_3([v1, v2, v3])

    print(
        f"prices={prices}\n"
        f"r1={r1:.3f}, r2={r2:.3f}, r3={r3:.3f}, r4={r4:.3f}, r5={r5:.3f}\n"
        f"v1={v1:.3f}, v2={v2:.3f}, v3={v3:.3f}\n"
        f"z_score={z:.3f}"
    )