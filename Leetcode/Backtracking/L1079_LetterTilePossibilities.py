class Solution:
    def numTilePossibilities(self, tiles: str) -> int:
        result = []
        def backtrack(path, index, avl):
            if index > 0 and path not in result:
                result.append(path)
            if index == len(tiles):
                return
            for i in range(len(avl)):
                backtrack(path + avl[i],index +1, avl[:i] + avl[i+1:])
        backtrack("",0, tiles)
        return result

result = Solution().numTilePossibilities("AAB")
print(result)