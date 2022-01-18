"""@package consequtive_repetitions
Used to solve more complex forms of unwanted sequential repetitions.
"""

def consequtive_repetitions(in_list, expected_range=15):
    """Function solves a problem of repeating the same items in a list.
    The repetition is understood as more numbers repeating in certain
    range. As an output, functions returns a list where those
    repetitive items are excluded.

    Args:
    expected_range -- determines how big this range, in which we
                      want to ignore any duplicates, is (default 15)
    """
    out_list = []
    for i in range(0, len(in_list)):
        if i == 0 or i > (len(in_list) - expected_range):
            out_list.append(in_list[i])
            continue
        flag = 0
        for k in range(1, expected_range):
            if in_list[i] == in_list[i+k]:
                flag = 1
        if flag == 1:
            continue
        out_list.append(in_list[i])
    return out_list
