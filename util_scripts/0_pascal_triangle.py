def pascal_triangle( line_number ):
    """

    :param line_number: an interger from 2 - n
    :return: coefficients on the given line
    """
    result_list = list()
    result_list.append(1)
    i = 1
    while(i <=line_number):
        j = 1
        l = []
        l.append(1)
        while(j < i):
            l.append(result_list[i-1][j] + result_list[i-1][j-1])
            j +=1
        l.append(1)
        result_list.append(l)
        i+=1
    return result_list