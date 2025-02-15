import os

def path_distance(path1, path2):
    """
    Calculate the distance between two file paths.
    """
    abs_path1 = os.path.abspath(path1)
    abs_path2 = os.path.abspath(path2)

    path1_parts = abs_path1.split(os.sep)
    path2_parts = abs_path2.split(os.sep)

    min_len = min(len(path1_parts), len(path2_parts))
    common_prefix_len = 0

    for i in range(min_len):
        if path1_parts[i] == path2_parts[i]:
            common_prefix_len += 1
        else:
            break

    distance = (len(path1_parts) - common_prefix_len) + (len(path2_parts) - common_prefix_len)

    return distance
