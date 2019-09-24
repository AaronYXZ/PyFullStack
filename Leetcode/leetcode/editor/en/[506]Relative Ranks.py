#
#Given scores of N athletes, find their relative ranks and the people with the top three highest scores, who will be awarded medals: "Gold Medal", "Silver Medal" and "Bronze Medal". 
#
# Example 1: 
# 
#Input: [5, 4, 3, 2, 1]
#Output: ["Gold Medal", "Silver Medal", "Bronze Medal", "4", "5"]
#Explanation: The first three athletes got the top three highest scores, so they got "Gold Medal", "Silver Medal" and "Bronze Medal". For the left two athletes, you just need to output their relative ranks according to their scores.
# 
# 
#
# Note: 
# 
# N is a positive integer and won't exceed 10,000. 
# All the scores of athletes are guaranteed to be unique. 
# 
# 
#



#leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def findRelativeRanks(self, nums: List[int]) -> List[str]:
        ranked = sorted([(i, num) for i, num in enumerate(nums)], key = lambda x:x[1], reverse = True)
        result = nums[[i for i, num in ranked]]

        return result

        
#leetcode submit region end(Prohibit modification and deletion)
