class Solution:
    def readBinaryWatch(self, num: int):
        times = [480, 240, 120, 60, 32, 16, 8, 4, 2, 1]

        def backtrack(result, path, index, num, times):
            if len(path) == num:
                hour = sum(path) // 60 % 12
                minute = sum(path) % 60
                time = str(hour) + ":" + ("0" if minute < 10 else "") + str(minute)
                # time = str(sum(path) // 60) + ":" + str(sum(path) % 60)
                if not time in result:
                    result.append(time)
                return
            if not times:
                return
            else:
                for i in range(index, len(times)):
                    # new_times = times.copy()
                    # new_times.remove(i)
                    backtrack(result, path + [times[i]],i +1, num, times)

        result = []
        backtrack(result, [],0, num, times)
        return sorted(result)

    def test(self, n):
        print(self.readBinaryWatch(n))


Solution().test(2)