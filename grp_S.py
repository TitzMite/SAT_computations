
import group_methods as grp

class S:

    def __init__(self, coeffs):
        self.coeffs = tuple(coeffs)

    def __eq__(self, other):
        return self.coeffs == other.coeffs

    def __hash__(self):
        return hash(self.coeffs)

    def __repr__(self):
        c = [str(x) for x in self.coeffs]
        w = max(len(x) for x in c)
        return (
            "\n"
            f"[{c[0]:>{w}} {c[1]:>{w}} {c[2]:>{w}}]\n"
            f"[{c[3]:>{w}} {c[4]:>{w}} {c[5]:>{w}}]\n"
            f"[{c[6]:>{w}} {c[7]:>{w}} {c[8]:>{w}}]\n"
        )

    @classmethod
    def identity(cls):
        return cls( ( 1,0,0, 0,1,0, 0,0,1 ) )

    def __lt__(self, other):
        return self._key() < other._key()

    def _key(self):
        identity = (1,0,0,0,1,0,0,0,1)
        if self.coeffs == identity:
            return (0,)
        return (1, sum(abs(x) for x in self.coeffs), self.coeffs)

    def __mul__(self, other):
        a = self.coeffs
        b = other.coeffs
        return S((
            a[0]*b[0] + a[1]*b[3] + a[2]*b[6],
            a[0]*b[1] + a[1]*b[4] + a[2]*b[7],
            a[0]*b[2] + a[1]*b[5] + a[2]*b[8],

            a[3]*b[0] + a[4]*b[3] + a[5]*b[6],
            a[3]*b[1] + a[4]*b[4] + a[5]*b[7],
            a[3]*b[2] + a[4]*b[5] + a[5]*b[8],

            a[6]*b[0] + a[7]*b[3] + a[8]*b[6],
            a[6]*b[1] + a[7]*b[4] + a[8]*b[7],
            a[6]*b[2] + a[7]*b[5] + a[8]*b[8],
        ))

    def inverse(self):
        a = self.coeffs
        return S((
            a[4]*a[8] - a[5]*a[7],
            a[2]*a[7] - a[1]*a[8],
            a[1]*a[5] - a[2]*a[4],

            a[5]*a[6] - a[3]*a[8],
            a[0]*a[8] - a[2]*a[6],
            a[2]*a[3] - a[0]*a[5],

            a[3]*a[7] - a[4]*a[6],
            a[1]*a[6] - a[0]*a[7],
            a[0]*a[4] - a[1]*a[3],
        ))
    
    def __pow__(self, n):
        if n < 0:
            return (self.inverse()) ** (-n)
        else:
            result = S.identity()
            for _ in range(n):
                result *= self
            return result

    def transpose_inverse(self):
        c = self.coeffs
        transpose = S((c[0], c[3], c[6], c[1], c[4], c[7], c[2], c[5], c[8]))
        return transpose.inverse()

    def conjugate_by(self, g):
    #return g^-1 x g
        g_inv = g.inverse()
        return g_inv * self * g

    def tau(self):
        j = S((0,0,1,0,1,0,1,0,0))
        con = self.conjugate_by(j)
        return con.transpose_inverse()

################

s1 = S((
    -1, -1,  0,
     0, -1,  0,
     0,  0,  1,
))

s2 = S((
    -1,  1,  0,
     0, -1,  0,
     0,  0,  1,
))

s3 = S((
     1,  0, -1,
     0,  1,  0,
     0,  0,  1,
))

s4 = S((
     1,  0,  0,
     0, -1, -1,
     0,  0, -1,
))

s5 = S((
     1,  0,  0,
     0, -1,  1,
     0,  0, -1,
))

s6 = S((
     1,  0,  1,
     0,  1,  0,
     0,  0,  1,
))

gens = [s1, s2, s3, s4, s5, s6]

#result

a1 = S((
    -1, -1,  0,
     0, -1,  0,
     0,  0,  1,
))

a2 = S((
    -1,  1,  0,
     0, -1,  0,
     0,  0,  1,
))

a3 = S((
     1,  0,  0,
     0, -1, -1,
     0,  0, -1,
))

a4 = S((
     1,  0,  0,
     0, -1,  1,
     0,  0, -1,
))

a5 = S((
     1,  0,  1,
     0,  1,  0,
     0,  0,  1,
))

a6 = S((
    -1, -1, -1,
     0, -1,  0,
     0,  0,  1,
))

a7 = S((
    -1, -1,  0,
     0,  1, -1,
     0,  0, -1,
))

a8 = S((
    -1, -1,  0,
     0,  1,  1,
     0,  0, -1,
))

a9 = S((
    -1, -1,  1,
     0, -1,  0,
     0,  0,  1,
))

a10 = S((
    -1,  1, -1,
     0, -1,  0,
     0,  0,  1,
))

a11 = S((
    -1,  1,  0,
     0,  1, -1,
     0,  0, -1,
))

a12 = S((
    -1,  1,  0,
     0,  1,  1,
     0,  0, -1,
))

a13 = S((
    -1,  1,  1,
     0, -1,  0,
     0,  0,  1,
))

a14 = S((
     1,  0, -1,
     0, -1, -1,
     0,  0, -1,
))

a15 = S((
     1,  0, -1,
     0, -1,  1,
     0,  0, -1,
))

a16 = S((
     1,  0,  1,
     0, -1, -1,
     0,  0, -1,
))

a17 = S((
     1,  0,  1,
     0, -1,  1,
     0,  0, -1,
))

a18 = S((
    -1, -1, -1,
     0,  1,  1,
     0,  0, -1,
))

a19 = S((
    -1, -1,  1,
     0,  1, -1,
     0,  0, -1,
))

a20 = S((
    -1,  1, -1,
     0,  1, -1,
     0,  0, -1,
))

a21 = S((
    -1,  1,  1,
     0,  1,  1,
     0,  0, -1,
))

a22 = S((
     1, -2,  1,
     0,  1,  0,
     0,  0,  1,
))

a23 = S((
     1,  0, -1,
     0,  1, -2,
     0,  0,  1,
))

a24 = S((
     1,  0, -1,
     0,  1,  2,
     0,  0,  1,
))

a25 = S((
     1,  2,  1,
     0,  1,  0,
     0,  0,  1,
))

a26 = S((
    -1, -1, -1,
     0, -1, -2,
     0,  0,  1,
))

a27 = S((
    -1,  1, -1,
     0, -1,  2,
     0,  0,  1,
))

a28 = S((
     1, -2,  1,
     0, -1,  1,
     0,  0, -1,
))

a29 = S((
     1,  2,  1,
     0, -1, -1,
     0,  0, -1,
))

A = [
    a1, a2, a3, a4, a5, a6, a7, a8, a9, a10,
    a11, a12, a13, a14, a15, a16, a17, a18, a19, a20,
    a21, a22, a23, a24, a25, a26, a27, a28, a29,
]

B = [a.tau() for a in A]

# >>> import grp_S as S
# >>> S.grp.multiply_to_identity(S.A, S.B)
# True