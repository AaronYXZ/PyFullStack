def pascal_triangle( line_number ):
    """

    :param line_number: an interger from 2 - n
    :return: coefficients on the given line
    """
    result_list = list()
    if (line_number < 0):
        return result_list
    for i in range(line_number + 1):
        result_list.insert(0,1)
        j = 1
        while (j < len(result_list) - 1):
            result_list[j] = result_list[j] + result_list[j+1]
            j+=1
    return result_list