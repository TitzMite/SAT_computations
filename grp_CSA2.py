
import group_methods as grp

#rewriting rules for word problem

shortenings = {
    # -------------------------------------------------
    # Cancellation
    # -------------------------------------------------
    (1, -1): [],
    (2, -2): [],
    (3, -3): [],
    (4, -4): [],
    (5, -5): [],
    (6, -6): [],
    (7, -7): [],
    (-1, 1): [],
    (-2, 2): [],
    (-3, 3): [],
    (-4, 4): [],
    (-5, 5): [],
    (-6, 6): [],
    (-7, 7): [],
    # -------------------------------------------------
    # Positive: [i,j] -> [-k]
    # -------------------------------------------------
    (1, 4): [-2],
    (4, 2): [-1],
    (2, 1): [-4],
    #
    (3, 3): [-1],
    (3, 1): [-3],
    (1, 3): [-3],
    #
    (5, 5): [-4],
    (5, 4): [-5],
    (4, 5): [-5],
    #
    (6, 6): [-2],
    (6, 2): [-6],
    (2, 6): [-6],
    #
    (7, 1): [-6],
    (1, 6): [-7],
    (6, 7): [-1],
    #
    (7, 2): [-5],
    (2, 5): [-7],
    (5, 7): [-2],
    #
    (7, 4): [-3],
    (4, 3): [-7],
    (3, 7): [-4],
     # -------------------------------------------------
    # Negative: [-i,-j] -> [k]
    # -------------------------------------------------
    (-4, -1): [2],
    (-2, -4): [1],
    (-1, -2): [4],
    #
    (-3, -3): [1],
    (-1, -3): [3],
    (-3, -1): [3],
    #
    (-5, -5): [4],
    (-4, -5): [5],
    (-5, -4): [5],
    #
    (-6, -6): [2],
    (-2, -6): [6],
    (-6, -2): [6],
    #
    (-1, -7): [6],
    (-6, -1): [7],
    (-7, -6): [1],
    #
    (-2, -7): [5],
    (-5, -2): [7],
    (-7, -5): [2],
    #
    (-4, -7): [3],
    (-3, -4): [7],
    (-7, -3): [4],
}

rewritings = {
    (-1, 2): [6, -5],
    (-1, 3): [3, -1],
    (-1, 4): [6, -3],
    (-1, 5): [4, -7],
    (-1, 6): [4, -6],
    (-1, 7): [3, -4],
    #
    (-2, 1): [5, -6],
    (-2, 3): [1, -7],
    (-2, 4): [5, -3],
    (-2, 5): [1, -5],
    (-2, 6): [6, -2],
    (-2, 7): [6, -1],
    #
    (-3, 1): [1, -3],
    (-3, 2): [7, -1],
    (-3, 4): [3, -2],
    (-3, 5): [7, -5],
    (-3, 6): [3, -7],
    (-3, 7): [1, -4],
    #
    (-4, 1): [3, -6],
    (-4, 2): [3, -5],
    (-4, 3): [2, -3],
    (-4, 5): [5, -4],
    (-4, 6): [2, -7],
    (-4, 7): [5, -2],
    #   
    (-5, 1): [7, -4],
    (-5, 2): [5, -1],
    (-5, 3): [5, -7],
    (-5, 4): [4, -5],
    (-5, 6): [7, -6],
    (-5, 7): [4, -2],
    #
    (-6, 1): [6, -4],
    (-6, 2): [2, -6],
    (-6, 3): [7, -3],
    (-6, 4): [7, -2],
    (-6, 5): [6, -7],
    (-6, 7): [2, -1],
    #
    (-7, 1): [4, -3],
    (-7, 2): [1, -6],
    (-7, 3): [4, -1],
    (-7, 4): [2, -5],
    (-7, 5): [2, -4],
    (-7, 6): [1, -2],
}

class A2Word:
    
    def __init__(self, letters, normal=False):
        self.letters = list(letters)
        self.normal = normal
        if not self.normal:
            self.normal_form()

    def __repr__(self):
        return f"A2Word({self.letters})"

    @classmethod
    def identity(cls):
        return cls([], normal=True)

    def normal_form(self):
        if self.normal:
            return self
        else:
            changed = True
            while changed:
                changed = False
                i = 0
                while i < len(self.letters) - 1:
                    pair = (self.letters[i], self.letters[i + 1])
                    if pair in shortenings:
                        self.letters[i:i + 2] = shortenings[pair]
                        changed = True
                        i = max(i - 1, 0)
                    elif pair in rewritings:
                        self.letters[i:i + 2] = rewritings[pair]
                        changed = True
                        i = max(i - 1, 0)
                    else:
                        i += 1
            self.normal = True
            return self

    def __mul__(self, other):
        return A2Word(self.letters + other.letters)

    def __eq__(self, other):
        return self.letters == other.letters
    
    def __lt__(self, other):
        return (len(self.letters),tuple(self.letters)) < (len(other.letters),tuple(other.letters))

    def __hash__(self):
        return hash(tuple(self.letters))
    
    def inverse(self):
        return A2Word([-x for x in reversed(self.letters)])

################

gens = [A2Word([i]) for i in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]]

#########

a1 = A2Word([-3])
a2 = A2Word([2])
a3 = A2Word([3])
a4 = A2Word([7])
a5 = A2Word([-6, -5])
a6 = A2Word([-4, -2])
a7 = A2Word([-3, -5])
a8 = A2Word([-3, -2])
a9 = A2Word([1, -4])
a10 = A2Word([2, -7])
a11 = A2Word([2, -5])
a12 = A2Word([2, -1])
a13 = A2Word([2, 4])
a14 = A2Word([2, 7])
a15 = A2Word([3, -7])
a16 = A2Word([3, -6])
a17 = A2Word([3, -2])
a18 = A2Word([3, 6])
a19 = A2Word([7, -5])
a20 = A2Word([7, -2])
a21 = A2Word([7, 6])
a22 = A2Word([7, 7])
a23 = A2Word([-4, -2, -2])
a24 = A2Word([1, -4, -6])
a25 = A2Word([2, -7, -2])
a26 = A2Word([2, -1, -6])
a27 = A2Word([2, 4, -6])
a28 = A2Word([2, 4, -2])
a29 = A2Word([2, 4, 6])
a30 = A2Word([2, 7, -6])
a31 = A2Word([3, -6, -5])
a32 = A2Word([3, -2, -2])
a33 = A2Word([3, 2, -1])
a34 = A2Word([3, 6, -2])
a35 = A2Word([7, -2, -2])
a36 = A2Word([7, 6, -2])
a37 = A2Word([7, 7, -6])
a38 = A2Word([3, 2, -1, -6])


b1 = A2Word([])
b2 = A2Word([-6])
b3 = A2Word([-4])
b4 = A2Word([-3])
b5 = A2Word([-2])
b6 = A2Word([-1])
b7 = A2Word([1])
b8 = A2Word([3])
b9 = A2Word([4])
b10 = A2Word([6])
b11 = A2Word([-7, -4])
b12 = A2Word([-7, -1])
b13 = A2Word([-6, -3])
b14 = A2Word([-2, -1])
b15 = A2Word([2, -3])
b16 = A2Word([3, -4])
b17 = A2Word([3, -1])
b18 = A2Word([4, -1])
b19 = A2Word([6, -4])
b20 = A2Word([6, -1])
b21 = A2Word([7, -3])
b22 = A2Word([7, -2])
b23 = A2Word([7, 3])
b24 = A2Word([7, 7])
b25 = A2Word([-6, -7, -4])
b26 = A2Word([-6, -7, -1])
b27 = A2Word([1, -7, -4])
b28 = A2Word([1, -7, -1])
b29 = A2Word([1, -6, -3])
b30 = A2Word([3, 2, -3])
b31 = A2Word([6, 3, -4])
b32 = A2Word([6, 3, -1])
b33 = A2Word([7, -2, -1])
b34 = A2Word([7, 7, 3])
b35 = A2Word([1, 1, -6, -3])
b36 = A2Word([6, -4, -6, -3])
b37 = A2Word([6, 3, 2, -3])

A = [
    a1, a2, a3, a4, a5, a6, a7, a8, a9, a10,
    a11, a12, a13, a14, a15, a16, a17, a18, a19, a20,
    a21, a22, a23, a24, a25, a26, a27, a28, a29, a30,
    a31, a32, a33, a34, a35, a36, a37, a38,
]

B = [
    b1, b2, b3, b4, b5, b6, b7, b8, b9, b10,
    b11, b12, b13, b14, b15, b16, b17, b18, b19, b20,
    b21, b22, b23, b24, b25, b26, b27, b28, b29, b30,
    b31, b32, b33, b34, b35, b36, b37,
]

# >>> import grp_CSA2 as CSA2
# >>> CSA2.grp.has_no_unique_product(CSA2.A, CSA2.B)
# True
