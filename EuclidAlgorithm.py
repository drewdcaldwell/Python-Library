
# Given two positive integers m and n, find their greatest common divisor,
# that is, the largest positive integer that evenly divides both m and n.

def EuclidAlgorithm(m, n):
    d = m / n
    r = m % n
    if r ==0:
        return n
    else:
        m = n 
        n = r
        EuclidAlgorithm(m, n)
            
print(EuclidAlgorithm(50,5))     # 5
print(EuclidAlgorithm(49,7))     # 7
print(EuclidAlgorithm(49,10))    # None