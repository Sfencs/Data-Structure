
def count_sort(s):
    """计数排序"""
    # 找到最大最小值
    min_num = min(s)
    max_num = max(s)

    # 计数列表
    count_list = [0]*(max_num-min_num+1)
    # 计数
    for i in s:
        count_list[i-min_num] += 1
    s.clear()
    # 填回
    for ind,i in enumerate(count_list):
        while i != 0:
            s.append(ind+min_num)
            i -= 1



if __name__ == '__main__':
    a = [3,6,8,4,2,6,7,3]
    count_sort(a)
    print(a)