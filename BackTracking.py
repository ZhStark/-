# ===========================Problem 282==========================
# =========== Expression Add Operators =========
# step1
# 对输入的数字有不同的切分方式，所以要想办法遍历所有可能的组合。
# 类似有分治排序的分割方法，不同是每次分割都会去组合一遍，而不是把全部分割为单个数字后再组合
# 分割过程还要注意“00”的存在

# step2
# 遍历所有+ - * 运算。
# 对于‘*’， 需要保存前面挨着的乘法得到的数（没有乘法运算就是上一个数）
# A+B*C 为上一步的表达式，值为curr， 这一步 *d
# 在上一步要保存 prev=B*C 传递到下一次迭代。
# A+B*C*d=(A+B*C)-prev+prev*d
# 更新 prev=prev*d


class Solution:
    def addOperators(self, num, target):
        """
        :type num: str
        :type target: int
        :rtype: List[str]
        """
        if not num:
            return []
        self.target = target
        l = []

        for i in range(1, len(num)+1):
            if i == 1 or (i > 1 and num[0] != '0'):
                self.helper(int(num[:i]), int(num[:i]), num[i:],  num[:i], l)

        return l

    def helper(self, pre, curr, num, ans, l):
            if not num:
                if curr == self.target:
                    l.append(ans)
                return

            for i in range(1, len(num)+1):
                if i == 1 or (i > 1 and num[0] != '0'):
                    temp = num[:i]
                    # +
                    self.helper(int(temp), curr+int(temp),
                                num[i:], ans+'+'+temp, l)
                    # -
                    self.helper(-int(temp), curr-int(temp),
                                num[i:], ans+'-'+temp, l)
                    # *
                    self.helper(pre*int(temp), curr-pre+pre *
                                int(temp), num[i:],  ans+'*'+temp, l)


# ===========================Problem 39==========================
# =========== Combination Sum =========
# 犯了2个错误：
# 1.
# 最开始传数组：
# temp.append(candidates[i])
# self.f(candidates[i:], target-candidates[i], l, temp)
# 这种情况会对上一个 f(x,xx,xxxx)中的 temp 造成影响。所以传数组注意不要对上一个迭代结果产生影响
# 2.
# 想象每次迭代的 i：
# 1-2-1 与 1-1-2重复了，所以要注意不要重复
class Solution:
    def combinationSum(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        if not candidates:
            return []

        l = []
        candidates.sort()
        temp = []

        self.f(candidates, target, l, temp)
        return l

    def f(self, candidates, target, l, temp):
        for i in range(len(candidates)):
            if candidates[i] > target:
                temp = []
                break
            elif candidates[i] == target:
                l.append(temp+[candidates[i]])
                break
            else:
                self.f(candidates[i:], target-candidates[i],
                       l, temp+[candidates[i]])


# ===========================Problem 46==========================
# =========== Permutations =========
# f(nums) 是传该数组，在原数组上更改
# f(nums[:]) 是传数据，原数组不变
# 这个题的方法排名倒数，discuss 有很多其他方法，现在还不能理解
# 其他 backtrack 的题：
# 78，90，47，39，40，131
class Solution:
    def permute(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        if not nums:
            return []
        ans = []
        visited = set()

        self.backtrack(ans, [], nums, visited)
        return ans

    def backtrack(self, l, temp, nums, visited):
        if len(temp) == len(nums):
            l.append(temp)
            return

        for i in range(len(nums)):
            if nums[i] not in visited:
                self.backtrack(l, temp+[nums[i]], nums,
                               visited.union(set([nums[i]])))

# ===========================Problem 47==========================
# =========== Permutations II =========
# 方法比上一个优化了一些
# 这个问题里有重复的数，要想如何才能去掉重复的过程
# 其实第 i 次 backtrack 就是给数组的第 i 个空填数。
# 所以思路是如果我这次填了 A，下次还是 A， 那么下次再填 A 的时候我就应该跳过。
# 但这种方法实现起来总是有 bug，（这个理论的缺陷是：如果这次是 A， 那么下次 A 只有在这个 A 没有用过的时候才能用）
# 所以转换思路，如果这次该填 A，而且下次还是该填 A，那么我就跳过这次的递归，直接进入下次好了

class Solution:
    def permuteUnique(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        if not nums:
            return []

        nums.sort()
        ans = []
        self.backtrack(nums, ans, [])
        return ans

    def backtrack(self, nums, ans, temp):
        if len(nums) == 0:
            ans.append(temp[:])
            return

        for i in range(len(nums)):
            if i+1 < len(nums) and nums[i] == nums[i+1]:
                continue
            self.backtrack(nums[:i]+nums[i+1:], ans, temp+[nums[i]])


# ===========================Problem 40==========================
# =========== Combination Sum II =========
# 假设我们 temp 为四个 "_ _ _ _"
# 现在是 "A _ _ _"
# 下一次填 B： "A B _ _"
# 等回溯结束，又该填第二个位置时，我们怎么知道这次填的是该位置的第二次或第三次:
# 在那个 for loop 里， i>0

class Solution:
    def combinationSum2(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        if not candidates:
            return [[]]

        candidates.sort()
        ans = []
        self.backtrack(candidates, target, ans, [])
        return ans

    def backtrack(self, ca, target, ans, temp):
        if target == 0:
            ans.append(temp)
            return
        if target < 0:
            return
        for i in range(len(ca)):
            if i > 0 and ca[i] == ca[i-1]:
                continue
            self.backtrack(ca[i+1:], target-ca[i], ans, temp+[ca[i]])
