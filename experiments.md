# Experiments

This file describes the two example computations included in the repository.

The experiments reproduce known results due to **Giles Gardam**:

1. the CMSZ torsion-free (\widetilde A_2)  lattice labelled with A.2 for q=2 has finite sets with no unique products;
2. the group algebra (\mathbb F_2[S]) of the Soelberg group contains non-trivial units.

The purpose of these experiments is to demonstrate that the SAT code in this repository can find and independently verify these examples.

## General setup

Both experiments follow the same basic procedure:

```text
choose finite search sets X and Y
             |
             v
     compute all products xy
             |
             v
    construct the SAT problem
             |
             v
      write DIMACS CNF file
             |
             v
        run Glucose Syrup
             |
             v
     read satisfying assignment
             |
             v
      recover subsets A and B
             |
             v
    verify the result directly
```

The final verification is performed directly in Python and is independent of the SAT encoding.

## Choice of search sets

Choosing the finite search sets is an important part of these computations.

Given finite sets

[
X,Y\subseteq G,
]

the SAT solver only searches for subsets

[
A\subseteq X,
\qquad
B\subseteq Y.
]

A `SAT` result produces an explicit witness which can then be verified directly.

For the two examples below, suitable finite search sets are obtained from Cayley balls with respect to natural generating sets, or simple variations of them.

---

# Experiment 1: CMSZ A.2 (\widetilde A_2) lattice

## Goal

The first experiment searches for finite subsets with no unique products in the torsion-free (\widetilde A_2) lattice arising from the Cartwright–Mantero–Steger–Zappa triangle presentation labelled **A.2** for the Fano plane.

The group is implemented in `grp_CSA2.py`.

Group elements are represented by words, and rewriting rules are used to compute normal forms.

## Constructing the search set

Import the group and select four generators:

```python
>>> import grp_CSA2 as A2
>>> selected_gens = [A2.gens[i] for i in [7, 8, 9, 12]]
>>> selected_gens
[A2Word([1]), A2Word([2]), A2Word([3]), A2Word([6])]
```

Thus the selected generators are represented by the words

[
1,\ 2,\ 3,\ 6.
]

The successful search uses the Cayley ball of radius (4):

```python
>>> ball = A2.grp.cayley_ball(selected_gens, 4)
```

The `cayley_ball` function automatically adds inverses of the supplied generators. Thus the ball is taken with respect to the symmetric generating set

[
{1,2,3,6,-1,-2,-3,-6}.
]

The ball contains `979` group elements.

The same ball is used for both search sets:

[
X=Y=\texttt{ball}.
]

This illustrates the importance of the choice of finite search set: a fairly simple modification of the natural generating set gives a manageable Cayley ball containing a no-unique-products witness.

## Running the SAT problem

The computation is run with

```python
>>> result = A2.grp.run_nupp_problem(
...     ball,
...     ball,
...     "nupp_problem.cnf",
...     "nupp_result.txt",
...     16
... )
```

Here

* `nupp_problem.cnf` is the generated DIMACS CNF problem;
* `nupp_result.txt` contains the Glucose output;
* `16` requests 16 Glucose threads.

## Example output

The following run was performed with Python 3.12.3 on Linux:

```text
2026-09-08 16:30:30.562538
starting to compute table
we have 979 left words and 979 right words
progress computing table: 100.00%
we have 246329 products
table created

2026-09-08 16:30:35.634152
starting to generate problem
problem generated

2026-09-08 16:30:44.419452
starting to run glucose

2026-09-08 17:06:37.494643
glucose finished
SAT

verification successful
```

Thus the multiplication table is computed from

[
979\times979
]

pairs and contains `246329` distinct products.

In this run, computing the table takes about 5 seconds and generating the CNF problem takes about 9 seconds. Glucose takes approximately **35 minutes 53 seconds**.

The complete computation takes approximately **36 minutes**. The precise running time depends on the hardware and solver configuration.

## Returned witness

The satisfying assignment gives two subsets of sizes

[
|A|=38,
\qquad
|B|=37.
]

They can be inspected directly with

```python
>>> result[0]
>>> result[1]
```

For this run, the first set is

```text
[
    [-3],
    [2],
    [3],
    [7],
    [-6, -5],
    [-4, -2],
    [-3, -5],
    [-3, -2],
    [1, -4],
    [2, -7],
    [2, -5],
    [2, -1],
    [2, 4],
    [2, 7],
    [3, -7],
    [3, -6],
    [3, -2],
    [3, 6],
    [7, -5],
    [7, -2],
    [7, 6],
    [7, 7],
    [-4, -2, -2],
    [1, -4, -6],
    [2, -7, -2],
    [2, -1, -6],
    [2, 4, -6],
    [2, 4, -2],
    [2, 4, 6],
    [2, 7, -6],
    [3, -6, -5],
    [3, -2, -2],
    [3, 2, -1],
    [3, 6, -2],
    [7, -2, -2],
    [7, 6, -2],
    [7, 7, -6],
    [3, 2, -1, -6]
]
```

and the second set is

```text
[
    [],
    [-6],
    [-4],
    [-3],
    [-2],
    [-1],
    [1],
    [3],
    [4],
    [6],
    [-7, -4],
    [-7, -1],
    [-6, -3],
    [-2, -1],
    [2, -3],
    [3, -4],
    [3, -1],
    [4, -1],
    [6, -4],
    [6, -1],
    [7, -3],
    [7, -2],
    [7, 3],
    [7, 7],
    [-6, -7, -4],
    [-6, -7, -1],
    [1, -7, -4],
    [1, -7, -1],
    [1, -6, -3],
    [3, 2, -3],
    [6, 3, -4],
    [6, 3, -1],
    [7, -2, -1],
    [7, 7, 3],
    [1, 1, -6, -3],
    [6, -4, -6, -3],
    [6, 3, 2, -3]
]
```

Each list represents the letters of an `A2Word`; the empty list represents the identity.

After recovering these subsets from the SAT assignment, the program computes all products (ab) directly and checks that none occurs exactly once.

Hence

```text
verification successful
```

confirms independently that these two finite sets have no unique products.

This reproduces Gardam's result that the CMSZ A.2 group does not have the unique product property.

---

# Experiment 2: Soelberg group

## Goal

The second experiment searches for non-trivial units in

[
\mathbb F_2[S],
]

where (S) is the Soelberg group.

The group is implemented in `grp_S.py` using (3\times3) integer matrices.

## Generating set and search set

Import the group:

```python
>>> import grp_S as S
```

The generating set is

[
\begin{aligned}
s_1&=
\begin{pmatrix}
-1&-1&0\
0&-1&0\
0&0&1
\end{pmatrix},
&
s_2&=
\begin{pmatrix}
-1&1&0\
0&-1&0\
0&0&1
\end{pmatrix},[1em]
s_3&=
\begin{pmatrix}
1&0&-1\
0&1&0\
0&0&1
\end{pmatrix},
&
s_4&=
\begin{pmatrix}
1&0&0\
0&-1&-1\
0&0&-1
\end{pmatrix},[1em]
s_5&=
\begin{pmatrix}
1&0&0\
0&-1&1\
0&0&-1
\end{pmatrix},
&
s_6&=
\begin{pmatrix}
1&0&1\
0&1&0\
0&0&1
\end{pmatrix}.
\end{aligned}
]

This generating set is already symmetric:

[
s_2=s_1^{-1},
\qquad
s_6=s_3^{-1},
\qquad
s_5=s_4^{-1}.
]

The search set is the Cayley ball of radius (3):

```python
>>> ball = S.grp.cayley_ball(S.gens, 3)
>>> len(ball)
83
```

Thus

[
|X|=|Y|=83,
\qquad
X=Y=\texttt{ball}.
]

## Running the SAT problem

The computation is run with

```python
>>> result = S.grp.run_unit_problem(
...     ball,
...     ball,
...     "unit_problem.cnf",
...     "unit_result.txt",
...     8
... )
```

Here

* `unit_problem.cnf` is the generated DIMACS CNF problem;
* `unit_result.txt` contains the Glucose output;
* `8` requests 8 Glucose threads.

## Example output

The following run was performed with Python 3.12.3 on Linux:

```text
2026-09-08 16:09:39.856403
starting to compute table
we have 83 left words and 83 right words
progress computing table: 100.00%
we have 697 products
table created

2026-09-08 16:09:39.869651
starting to generate problem
problem generated

2026-09-08 16:09:39.934589
starting to run glucose

2026-09-08 16:09:41.355135
glucose finished
SAT

verification successful
```

The search uses an

[
83\times83
]

multiplication table with `697` distinct products.

For this run, computing the table and generating the SAT problem are essentially instantaneous. Glucose takes approximately **1.4 seconds**, and the complete computation takes approximately **1.5 seconds**.

## Returned unit

The satisfying assignment produces supports of sizes

[
|A|=|B|=29.
]

The matrices in the two supports can be displayed directly with

```python
>>> result[0]
>>> result[1]
```

The corresponding group-algebra elements are

[
\alpha=\sum_{a\in A}a,
\qquad
\beta=\sum_{b\in B}b.
]

After recovering the supports from the satisfying assignment, the program computes their product directly in the group algebra over (\mathbb F_2) and verifies that

[
\alpha\beta=1.
]

Thus

```text
verification successful
```

confirms independently that the returned supports define mutually inverse non-trivial units in

[
\mathbb F_2[S].
]

This reproduces Gardam's result that the (\mathbb F_2)-group algebra of the Soelberg group contains non-trivial units.

---

# Comparison

The two successful runs have quite different computational sizes:

| Experiment                   | Search-set size | Witness sizes | Distinct products | Threads | Solver time in recorded run |
| ---------------------------- | --------------: | ------------: | ----------------: | ------: | --------------------------: |
| CMSZ A.2, no unique products |             979 |     38 and 37 |            246329 |      16 |         about 35 min 53 sec |
| Soelberg, non-trivial unit   |              83 |     29 and 29 |               697 |       8 |               about 1.4 sec |
