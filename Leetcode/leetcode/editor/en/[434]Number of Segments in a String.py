#Count the number of segments in a string, where a segment is defined to be a contiguous sequence of non-space characters. 
#
# Please note that the string does not contain any non-printable characters. 
#
# Example: 
# 
#Input: "Hello, my name is John"
#Output: 5
# 
# Related Topics String



#leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def countSegments(self, s: str) -> int:
        return len(s.split(" "))
        
#leetcode submit region end(Prohibit modification and deletion)
