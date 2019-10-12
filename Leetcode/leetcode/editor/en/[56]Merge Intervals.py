#Given a collection of intervals, merge all overlapping intervals. 
#
# Example 1: 
#
# 
#Input: [[1,3],[2,6],[8,10],[15,18]]
#Output: [[1,6],[8,10],[15,18]]
#Explanation: Since intervals [1,3] and [2,6] overlaps, merge them into [1,6].
# 
#
# Example 2: 
#
# 
#Input: [[1,4],[4,5]]
#Output: [[1,5]]
#Explanation: Intervals [1,4] and [4,5] are considered overlapping. 
#
# NOTE: input types have been changed on April 15, 2019. Please reset to default code definition to get new method signature. 
# Related Topics Array Sort



#leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key = lambda x:x[0])
        result = [intervals[0]]
        for interval in intervals[1:]:
            if result[-1][1] > interval[0]:
                result[-1][1] = max(result[-1][1], interval[1])
            else:
                result.append(interval)
        return result
#leetcode submit region end(Prohibit modification and deletion)
