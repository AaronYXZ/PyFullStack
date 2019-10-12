#A binary watch has 4 LEDs on the top which represent the hours (0-11), and the 6 LEDs on the bottom represent the minutes (0-59). 
# Each LED represents a zero or one, with the least significant bit on the right. 
#
# For example, the above binary watch reads "3:25". 
#
# Given a non-negative integer n which represents the number of LEDs that are currently on, return all possible times the watch could represent. 
#
# Example:
# Input: n = 1 Return: ["1:00", "2:00", "4:00", "8:00", "0:01", "0:02", "0:04", "0:08", "0:16", "0:32"] 
# 
#
# Note: 
# 
# The order of output does not matter. 
# The hour must not contain a leading zero, for example "01:00" is not valid, it should be "1:00". 
# The minute must be consist of two digits and may contain a leading zero, for example "10:2" is not valid, it should be "10:02". 
# 
# Related Topics Backtracking Bit Manipulation



#leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def readBinaryWatch(self, num: int) -> List[str]:
        times = [480, 240, 120, 60, 32, 16, 8, 4, 2, 1]

        def backtrack(result, path, num, times):
            if len(path) == num:
                hour = sum(path) // 60
                minute = sum(path) % 60
                time = str(hour) + ":" + ("0" if minute < 10 else "") + str(minute)
                # time = str(sum(path) // 60) + ":" + str(sum(path) % 60)
                result.append(time)
                return
            if not times:
                return
            else:
                for i in times:
                    new_times = times.copy()
                    backtrack(result, path + [i], num, new_times.remove(i))

        result = []
        backtrack(result, [], num, times)
        return result

#leetcode submit region end(Prohibit modification and deletion)
