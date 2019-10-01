class InsertionSort():
    def sort(self, data):
        if data is None:
            raise TypeError("Data shouldn't be None")
        if len(data)< 2:
            return data
        for r in range(1, len(data)):
            for l in range(r):
                if data[r] < data[l]:
                    tmp = data[r]
                    data[l+1:r+1] = data[l:r]
                    data[l] = tmp
        return data
