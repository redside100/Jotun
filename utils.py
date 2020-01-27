"""
A collection of useful functions that can be used anywhere.
"""


def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    time_msg = ''

    if h > 0:
        time_msg += "{}h {:02d}m".format(h, m)
    elif m > 0:
        time_msg += "{} min".format(m)
    else:
        time_msg += "{} sec".format(s)

    return time_msg