# 期待输出:
# A --> C
# A --> B
# C --> B
# A --> C
# B --> A
# B --> C
# A --> C
def move(rank,s1,s2,s3):
    if(rank == 1):
        print("移动%d盘子%c到%c",rank,s1,s3)
    else:
        move(rank-1,s1,s3,s2)
        print("移动%d盘子%c到%c", rank, s1, s3)
        move(rank-1,s2,s1,s3)
move(3, 'A', 'B', 'C')