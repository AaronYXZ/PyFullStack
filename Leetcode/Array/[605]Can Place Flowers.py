#Suppose you have a long flowerbed in which some of the plots are planted and some are not. However, flowers cannot be planted in adjacent plots - they would compete for water and both would die. 
#
# Given a flowerbed (represented as an array containing 0 and 1, where 0 means empty and 1 means not empty), and a number n, return if n new flowers can be planted in it without violating the no-adjacent-flowers rule. 
#
# Example 1: 
# 
#Input: flowerbed = [1,0,0,0,1], n = 1
#Output: True
# 
# 
#
# Example 2: 
# 
#Input: flowerbed = [1,0,0,0,1], n = 2
#Output: False
# 
# 
#
# Note: 
# 
# The input array won't violate no-adjacent-flowers rule. 
# The input array size is in the range of [1, 20000]. 
# n is a non-negative integer which won't exceed the input array size. 
# 
# Related Topics Array



#leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        prev_slots = 0
        avl_slots = 0

        for i, slot in enumerate(flowerbed):
            if (slot == 0):
                if i == 0:
                    prev_slots += 2
                else:
                    prev_slots += 1
            else:
                avl_slots += max(0, (prev_slots - 1) // 2)
                prev_slots = 0
        if prev_slots != 0:
            avl_slots += (prev_slots) // 2
        return avl_slots >= n
        
#leetcode submit region end(Prohibit modification and deletion)
