
def time_to_milisecond(time, unit):
    if unit in ['second', 's']:
        return time * 1000
    if unit in ['hour', 'h']:
        return time * 36000000
    if unit in ['minute', 'm']:
        return time * 60000
    if unit in ['milliseconds', 'ms']:
        return time