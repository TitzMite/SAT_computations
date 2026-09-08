
from pysat.formula import CNF

def collect_pairs(table):
    n = max(max(row) for row in table) + 1
    pairs = [[] for _ in range(n)]
    for i, row in enumerate(table):
        for j, value in enumerate(row):
            pairs[value].append((i, j))
    return pairs

##############################

def add_nupp_constraint_for_product(cnf, pairs, variablesX, variablesY):
    ###
    next_var = cnf.nv +1
    ###
    if len(pairs) == 1:
        i, j = pairs[0]
        cnf.append([-variablesX[i], -variablesY[j]])
    else:
        #collecting the variables that encode the pairs that can possibly be true
        #we need either no pair to be true or at least two
        vars_for_product_constraint = [] 
        for (i, j) in pairs:
            conj_var = next_var
            next_var += 1
            vars_for_product_constraint.append(conj_var)
            # conj_var is true if and only if x[i] and y[j] are both true
            cnf.append([-conj_var, variablesX[i]])
            cnf.append([-conj_var, variablesY[j]])
            cnf.append([conj_var, -variablesX[i], -variablesY[j]])
        for conj_var in vars_for_product_constraint:
            cnf.append([-conj_var] + [z for z in vars_for_product_constraint if z!= conj_var])

def create_nupp_problem_from_table(table, problem_path):
    num_rows = len(table)
    num_cols = len(table[0])
    product_pairs = collect_pairs(table)
    variablesX = list(range(1, num_rows + 1))                
    variablesY = list(range(num_rows + 1, num_rows + num_cols + 1))
    cnf = CNF()
    # next line means: at least one X is true
    cnf.append(variablesX)
    # next line means: at least one Y is true
    cnf.append(variablesY)
    # next block means forbid exactly one X true
    for xi in variablesX:
        others = [xj for xj in variablesX if xj != xi]
        cnf.append([-xi] + others)
    # next block means forbid exactly one Y true
    for yi in variablesY:
        others = [yj for yj in variablesY if yj != yi]
        cnf.append([-yi] + others)
    #next blocks treat non-uniqueness of products
    for v_idx, pairs in enumerate(product_pairs):
        add_nupp_constraint_for_product(cnf, pairs, variablesX, variablesY)
    cnf.to_file(problem_path)

##########################################

def add_xor_constraint(cnf, variables, parity):
    next_var = cnf.nv + 1
    a, b = variables[0], variables[1]
    z = next_var
    next_var += 1
    # z = a XOR b
    cnf.extend([
        [-a, -b, -z],
        [ a,  b, -z],
        [ a, -b,  z],
        [-a,  b,  z],
    ])
    for c in variables[2:]:
        z2 = next_var
        next_var += 1
        # z2 = z XOR c
        cnf.extend([
            [-z, -c, -z2],
            [ z,  c, -z2],
            [ z, -c,  z2],
            [-z,  c,  z2],
        ])
        z = z2
    if parity == 0:
        cnf.append([-z])
    else:
        cnf.append([z])

def add_mod_2_constraint_for_product(cnf, pairs, variablesX, variablesY, parity):
    next_var = cnf.nv + 1
    if len(pairs) == 1:
        i, j = pairs[0]
        if parity == 0:
            cnf.append([-variablesX[i], -variablesY[j]])
        else:
            cnf.append([variablesX[i]])
            cnf.append([variablesY[j]])
    elif len(pairs) == 2:
        (i1, j1), (i2, j2) = pairs
        a = variablesX[i1]
        b = variablesY[j1]
        c = variablesX[i2]
        d = variablesY[j2]
        if parity == 0:
            cnf.append([-a, -b,  c,  d])  # forbid (1, 1, 0, 0)
            cnf.append([-a, -b,  c, -d])  # forbid (1, 1, 0, 1)
            cnf.append([-a, -b, -c,  d])  # forbid (1, 1, 1, 0)
            cnf.append([ a,  b, -c, -d])  # forbid (0, 0, 1, 1)
            cnf.append([ a, -b, -c, -d])  # forbid (0, 1, 1, 1)
            cnf.append([-a,  b, -c, -d])  # forbid (1, 0, 1, 1)
        else:
            cnf.append([ a,  b,  c,  d])  # forbid (0, 0, 0, 0)
            cnf.append([ a,  b,  c, -d])  # forbid (0, 0, 0, 1)
            cnf.append([ a,  b, -c,  d])  # forbid (0, 0, 1, 0)
            cnf.append([ a, -b,  c,  d])  # forbid (0, 1, 0, 0)
            cnf.append([ a, -b,  c, -d])  # forbid (0, 1, 0, 1)
            cnf.append([ a, -b, -c,  d])  # forbid (0, 1, 1, 0)
            cnf.append([-a,  b,  c,  d])  # forbid (1, 0, 0, 0)
            cnf.append([-a,  b,  c, -d])  # forbid (1, 0, 0, 1)
            cnf.append([-a,  b, -c,  d])  # forbid (1, 0, 1, 0)
            cnf.append([-a, -b, -c, -d])  # forbid (1, 1, 1, 1)
    else:
        vars_for_product_constraint = []
        for i, j in pairs:
            conj_var = next_var
            next_var += 1
            vars_for_product_constraint.append(conj_var)
            # conj_var <=> variablesX[i] AND variablesY[j]
            cnf.append([-conj_var, variablesX[i]])
            cnf.append([-conj_var, variablesY[j]])
            cnf.append([conj_var, -variablesX[i], -variablesY[j]])
        add_xor_constraint(cnf, vars_for_product_constraint, parity)

#it is very import that the identity appears as a product
def create_unit_problem_from_table(table, problem_path):
    num_rows = len(table)
    num_cols = len(table[0])
    product_pairs = collect_pairs(table)
    variablesX = list(range(1, num_rows + 1))                
    variablesY = list(range(num_rows + 1, num_rows + num_cols + 1))
    cnf = CNF()
    # next line means: at least one X is true
    cnf.append(variablesX)
    # next line means: at least one Y is true
    cnf.append(variablesY)
    # next block means forbid exactly one X true
    for xi in variablesX:
        others = [xj for xj in variablesX if xj != xi]
        cnf.append([-xi] + others)
    # next block means forbid exactly one Y true
    for yi in variablesY:
        others = [yj for yj in variablesY if yj != yi]
        cnf.append([-yi] + others)
    # next line means: number of true X variables must be odd
    add_xor_constraint(cnf, variablesX, 1)
    # next line means: number of true Y variables must be odd
    add_xor_constraint(cnf, variablesY, 1)
    #next blocks treat coefficients of products
    for v_idx, pairs in enumerate(product_pairs):
        #coefficient for identity must be true
        if v_idx == 0:
            add_mod_2_constraint_for_product(cnf, pairs, variablesX, variablesY, 1)
        #other coefficients must be false
        else:
            add_mod_2_constraint_for_product(cnf, pairs, variablesX, variablesY, 0)
    cnf.to_file(problem_path)


#it is very import that the identity appears as a product
def create_zerodiv_problem_from_table(table, problem_path):
    num_rows = len(table)
    num_cols = len(table[0])
    product_pairs = collect_pairs(table)
    variablesX = list(range(1, num_rows + 1))                
    variablesY = list(range(num_rows + 1, num_rows + num_cols + 1))
    cnf = CNF()
    # next line means: at least one X is true
    cnf.append(variablesX)
    # next line means: at least one Y is true
    cnf.append(variablesY)
    # next block means forbid exactly one X true
    for xi in variablesX:
        others = [xj for xj in variablesX if xj != xi]
        cnf.append([-xi] + others)
    # next block means forbid exactly one Y true
    for yi in variablesY:
        others = [yj for yj in variablesY if yj != yi]
        cnf.append([-yi] + others)
    #next blocks treat coefficients of products
    for v_idx, pairs in enumerate(product_pairs):
        add_mod_2_constraint_for_product(cnf, pairs, variablesX, variablesY, 0)
    cnf.to_file(problem_path)