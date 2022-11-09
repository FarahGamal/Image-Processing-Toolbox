def lcs(a, b):
   
    # Write your code here

    m = len(a)
    n = len(b)
 
    L = [[None]*(n + 1) for i in range(m + 1)]
 
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif a[i-1] == b[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
              if L[i-1][j] > L[i][j-1]:
                L[i][j] = L[i-1][j]
              else:
                L[i][j] = L[i][j-1]

          
 
    return L[m][n]