def matriu_random(n, m):
    llista = np.arange(0, (n*m), 1)
    vec = np.random.permutation(llista)
    A = np.zeros((n,m))
    print(vec)
    for i in range (n):
        A[i] = vec[i*m:(i+1)*m]
    return A

def matriu_guanyadora(n,m):
    llista = np.arange(0, (n*m), 1)
    A = np.zeros((n,m))
    for i in range(n):
        A[i] = llista[i*m:(i+1)*m]
    
    return A
