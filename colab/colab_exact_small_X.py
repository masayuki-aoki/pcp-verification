# Colab-ready: exact PCp(X) for X <= Xmax via FFT
import numpy as np

def sieve_isprime(n: int) -> np.ndarray:
    s = np.ones(n+1, dtype=np.bool_); s[:2] = False
    p=2
    while p*p<=n:
        if s[p]:
            s[p*p:n+1:p] = False
        p+=1
    return s

def pcp_exact_up_to_fft(Xmax: int = 80_000):
    # 1) primes up to Xmax+2 (need q+2)
    isprime = sieve_isprime(Xmax + 2)

    # 2) T[q] = 1_{q composite, q>=4, (q+2) prime} on q=0..Xmax
    L = Xmax + 1
    q = np.arange(L)
    comp_q  = (~isprime[:L])
    ge4     = (q >= 4)
    q2prime = isprime[2:L+2]
    T = (comp_q & ge4 & q2prime).astype(np.float64)

    # 3) A[p] = 1_{p prime} for p=0..Xmax
    A = isprime[:L].astype(np.float64)

    # 4) Convolution via FFT: C = T * A of length 2*L - 1
    need = 2*L - 1
    n = 1 << (need - 1).bit_length()
    FA = np.fft.rfft(A, n);  FT = np.fft.rfft(T, n)
    C = np.fft.irfft(FA * FT, n)[:need]

    PCp = np.rint(C).astype(np.int64)[:L]
    zero_set = [int(X) for X in range(6, L, 2) if PCp[X] == 0]
    return PCp, zero_set

PCp, zeroes = pcp_exact_up_to_fft(80_000)
print("Zero-set up to 80,000:", zeroes)
# Expected: [6, 8, 10, 36, 210]
