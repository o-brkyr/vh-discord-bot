def weekday_from_python_to_go(py_day: int) -> int:
    # Python: Monday(0) -> Sunday(6)
    # Go: Sunday(0) -> Saturday(6)

    return (py_day + 1) % 7


def weekday_from_go_to_python(go_day: int) -> int:
    return (go_day - 1) % 7
