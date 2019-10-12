class Solution:
    def countArrangement(self, N: int) -> int:
        nums = [i + 1 for i in range(N)]
        result = []
        def backtrack(index,path, avl):
            if index == N:
                result.append(path)
                return
            for i in range(len(avl)):
                num = avl[i]
                if num % (index +1) != 0 and (index + 1) % num != 0:
                    break
                else:
                    backtrack(index +1,path + [num], avl[:i] + avl[i+1:])
        backtrack(0, [], nums)
        return result

print(Solution().countArrangement(4))

