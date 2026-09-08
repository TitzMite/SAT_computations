# SAT computations for the no-unique-products property and group algebra units

This repository contains Python code for constructing SAT problems associated with two questions in group theory:

1. finding finite sets with no unique products;
2. finding non-trivial units in group algebras over (\mathbb F_2).

The emphasis is computational. Starting from finite subsets of a group and a method for multiplying group elements, the code computes the relevant multiplication table and translates the problem into a Boolean satisfiability problem in standard DIMACS CNF format.

The resulting `.cnf` files can be used with any compatible SAT solver.

For convenience, the repository also contains code for running the problems directly from Python using **Glucose Syrup** and for independently verifying the solutions returned by the solver. To use the solver interface, Glucose Syrup must be installed separately.

Two concrete groups are included as examples:

* the torsion-free (\widetilde A_2) lattice for q=2 labelled **A.2** by Cartwright–Mantero–Steger–Zappa [1];
* the **Soelberg group**, introduced in Soelberg's thesis [2] and considered in §4 of Gardam's *Non-trivial units of complex group rings* [3].

For these groups, the computations reproduce results due to **Giles Gardam** [3,4]. These mathematical results are **not new results** of this project.

## SAT models

### Sets without unique products

Let (G) be a group and let (X,Y\subseteq G) be finite sets.

An element (g\in XY) is a **unique product** if there is exactly one pair

[
(x,y)\in X\times Y
]

such that

[
xy=g.
]

The first SAT model searches for non-trivial subsets

[
A\subseteq X,
\qquad
B\subseteq Y
]

such that no element of (AB) is a unique product.

Equivalently, every (g\in AB) must have at least two distinct representations

[
g=a_1b_1=a_2b_2
]

with

[
(a_1,b_1)\neq(a_2,b_2).
]

A satisfying assignment therefore gives two subsets (A) and (B) whose product set has no uniquely represented element.

### Non-trivial units in (\mathbb F_2[G])

The second SAT model searches for supports of non-trivial units in the group algebra

[
\mathbb F_2[G].
]

Given finite sets (X,Y\subseteq G), it searches for non-trivial subsets

[
A\subseteq X,
\qquad
B\subseteq Y
]

such that

[
\alpha=\sum_{a\in A}a,
\qquad
\beta=\sum_{b\in B}b
]

satisfy

[
\alpha\beta=1.
]

Over (\mathbb F_2), the coefficient of (g\in G) in (\alpha\beta) is the parity of

[
#{(a,b)\in A\times B : ab=g}.
]

Thus the identity must occur with odd multiplicity, while every non-identity element must occur with even multiplicity.

These parity conditions are encoded as a SAT problem. A satisfying assignment gives the supports of mutually inverse non-trivial elements of (\mathbb F_2[G]).

## Choosing the finite search sets

An important part of the computation is choosing the finite sets

[
X,Y\subseteq G
]

in which the SAT solver searches.

The SAT encoding can only find subsets contained in the prescribed search sets. Choosing (X) and (Y) well is therefore a significant part of the computation.

A natural source of finite search sets is provided by **Cayley balls**. The repository contains a general function for constructing a ball of a given radius from a finite set of generators.

For the examples considered here, Cayley balls for natural generating sets, or for simple variations of natural generating sets, already provide search spaces containing the desired examples.

Thus the supports do not have to be guessed in advance: one chooses a natural finite region of the group and lets the SAT solver search for suitable subsets inside it.

## How the code is organized

The code is divided into a generic SAT/group layer and two concrete group implementations.

### `creating_sat_problems.py`

Contains the SAT encodings.

From an indexed multiplication table it constructs CNF problems for

* the no-unique-products problem;
* the non-trivial-unit problem over (\mathbb F_2).

This part of the code is independent of the particular group and of Glucose Syrup.

### `group_methods.py`

Contains the generic group-level routines connecting a concrete group implementation with the SAT code.

In particular, it provides functions for

* constructing Cayley balls;
* computing multiplication tables for finite subsets;
* generating CNF problems;
* running a generated problem with Glucose Syrup;
* translating a satisfying assignment back into group elements;
* independently verifying that the resulting subsets have no unique products or multiply to the identity in (\mathbb F_2[G]).

A typical computation therefore has the form

```text
concrete group implementation
            |
            v
    choose finite search sets
       (e.g. Cayley balls)
            |
            v
   compute multiplication table
            |
            v
      construct SAT problem
            |
            v
       DIMACS CNF file
            |
            v
          SAT solver
            |
            v
     recover group elements
            |
            v
   direct verification in Python
```

### `running_sat_problems.py`

Contains the interface to **Glucose Syrup**.

It runs the external `glucose` executable on a generated CNF file and parses the resulting satisfying assignment.

This part is optional: the CNF files produced by the project can instead be passed directly to another SAT solver.

### `grp_CSA2.py`

Implements the CMSZ A.2 (\widetilde A_2) group.

Group elements are represented by words, and rewriting rules are used to put products into normal form.

### `grp_S.py`

Implements the Soelberg group using (3\times3) integer matrices.

Matrix multiplication and inversion are implemented directly, so no external linear-algebra package is required.

## Example groups

### CMSZ A.2 (\widetilde A_2) lattice

The first example is the torsion-free (\widetilde A_2) lattice arising from the Cartwright–Mantero–Steger–Zappa triangle presentation **A.2** for the projective plane of order (2), i.e. the Fano plane [1].

Using a suitable Cayley ball as the finite search space, the no-unique-products SAT model finds finite subsets with no unique products.

This computationally reproduces Gardam's result that this torsion-free (\widetilde A_2) lattice does not have the unique product property [4].

Details of the choice of generating set, Cayley ball, commands, solver output, and running time are given in `EXPERIMENTS.md`.

### Soelberg group

The second example is the **Soelberg group** introduced in [2]; see also [5] and Gardam [3, §4].

It is represented in this repository as a matrix group.

Using a small Cayley ball as the search space, the group-algebra SAT model finds supports of non-trivial units in

[
\mathbb F_2[S].
]

This computationally reproduces Gardam's result that (\mathbb F_2[S]) contains non-trivial units [3, §4].

Details of the generating set, Cayley ball, commands, solver output, and running time are given in `EXPERIMENTS.md`.

## Using another group

The SAT code is not specific to the two groups included in the repository.

To use it with another group, one needs a Python representation of group elements supporting the operations required by `group_methods.py`, in particular:

* multiplication;
* inversion;
* the identity element;
* equality and hashing;
* an ordering that allows finite collections of group elements to be sorted.

One can then construct finite search sets (X,Y), for example using Cayley balls, and pass them to the generic SAT routines.

For the unit problem, the indexed multiplication table must place the identity at index `0`. The included group implementations are ordered so that this happens automatically.

The main practical difficulty is often not constructing the SAT instance itself, but finding finite search sets that are well adapted to the group and large enough to contain the desired supports.

## Requirements

### CNF generation

* Python 3
* PySAT (`python-sat`), providing `pysat.formula.CNF`

No NumPy or symbolic-algebra package is required.

### Solving directly from Python

To use the included solver interface, **Glucose Syrup** must additionally be installed and the `glucose` executable must be available from the command line.

Glucose Syrup is not required for generating the CNF files. The generated files use standard DIMACS CNF and can be passed to another compatible SAT solver.

## Attribution

The mathematical results reproduced in the two included examples are **due to Giles Gardam**:

* the CMSZ A.2 torsion-free (\widetilde A_2) lattice has finite sets with no unique products [4];
* the group algebra (\mathbb F_2[S]) of the Soelberg group contains non-trivial units [3, §4].

These are **not claimed as new mathematical results of this project**.

The purpose of this repository is to provide a computational framework for formulating these questions as SAT problems and to reproduce the known examples using concrete finite search spaces.

## AI assistence

**ChatGPT (OpenAI)** was used as an assistant in writing and refining parts of the Python code and in drafting and editing this README.

## References

[1] D. I. Cartwright, A. M. Mantero, T. Steger, and A. Zappa, *Groups acting simply transitively on the vertices of a building of type (\widetilde A_2). II. The cases (q=2) and (q=3)*, **Geometriae Dedicata** 47 (1993)

[2] Lindsay Jennae Soelberg, *Finding Torsion-free Groups Which Do Not Have the Unique Product Property*, Master's thesis, Brigham Young University, 2018.

[3] Giles Gardam, *Non-trivial units of complex group rings*, arXiv:2312.05240, 2023; revised 2024. See in particular §4, “Beyond virtually abelian groups.”

[4] Giles Gardam, *Solving semidecidable problems in group theory*, SMRI Algebra & Geometry Online Seminar, 5 October 2021, slides.

[5] Pace P. Nielsen and Lindsay Soelberg, *Small sets without unique products in torsion-free groups*, **Journal of Algebra and Its Applications** 23 (2024)
