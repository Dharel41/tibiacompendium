def count_exp_speed(exp_on_hour: int, exp_factor: int) -> int:
    return int((exp_on_hour / exp_factor) * 100)
