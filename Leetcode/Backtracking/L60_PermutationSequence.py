class Solution:
    def getPermutation(self, n: int, k: int) -> str:
        nums = [i+1 for i in range(n)]
        result = []
        def backtracking(path, index, avl):
            if index == n:
                result.append(path)
                return
            for i in range(len(avl)):
                backtracking(path + str(avl[i]), index +1, avl[:i] + avl[i+1:])
        backtracking("", 0, nums)
        return sorted(result)

print(Solution().getPermutation(3, 1))