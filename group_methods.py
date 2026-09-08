
import datetime

def sorted_inverses(words):
    return sorted([w.inverse() for w in words])

def compute_products(left, right):
    prods = set()
    for l in left:
        for r in right:
            prods.add(l*r)
    return sorted(prods)

def cayley_ball(generators, radius):
    generators = list(generators)
    generators += [g.inverse() for g in generators]
    identity = generators[0].identity()
    ball = {identity}
    frontier = {identity}
    for _ in range(radius):
        new_frontier = set()
        for word in frontier:
            for generator in generators:
                new_word = word * generator
                if new_word not in ball:
                    ball.add(new_word)
                    new_frontier.add(new_word)
        frontier = new_frontier
    return sorted(ball)

def compute_table(left, right):
    print(datetime.datetime.now())
    print("starting to compute table")
    print(f"we have {len(left)} left words and {len(right)} right words")
    product_rows = []
    prods = set()
    total = len(left)
    for i, l in enumerate(left, start=1):
        row = []
        for r in right:
            product = l * r
            row.append(product)
            prods.add(product)
        product_rows.append(row)
        percent = 100 * i / total
        print(
            f"\rprogress computing table: {percent:.2f}%",
            end="",
            flush=True,
        )
    print()
    products = sorted(prods)
    print(f"we have {len(products)} products")
    index = {w: i for i, w in enumerate(products)}
    table = [
        [index[product] for product in row]
        for row in product_rows
    ]
    print("table created\n")
    return table

def print_product_statistics(left_set, right_set):
    product_counts = {}
    for left in left_set:
        for right in right_set:
            product = left * right
            if product in product_counts:
                product_counts[product] += 1
            else:
                product_counts[product] = 1
    histogram = {}
    for count in product_counts.values():
        if count in histogram:
            histogram[count] += 1
        else:
            histogram[count] = 1
    print(f"Distinct products: {len(product_counts)}")
    for count in sorted(histogram):
        print(f"{count}: {histogram[count]}")


def has_no_unique_product(left_set, right_set):
    product_counts = {}
    for left in left_set:
        for right in right_set:
            product = left * right
            if product in product_counts:
                product_counts[product] += 1
            else:
                product_counts[product] = 1
    for count in product_counts.values():
        if count == 1:
            return False
    return True

def multiply_to_identity(left_set, right_set):
    product_counts = {}
    for left in left_set:
        for right in right_set:
            product = left * right
            if product in product_counts:
                product_counts[product] += 1
            else:
                product_counts[product] = 1
    for product in product_counts:
        product_counts[product] %= 2
    identity = left_set[0].identity()
    for product, coefficient in product_counts.items():
        if product == identity:
            if coefficient != 1:
                return False
        else:
            if coefficient != 0:
                return False
    return True

#######

import creating_sat_problems as cre_sat

def create_nupp_problem(left, right, problem_path):
    table = compute_table(left, right)
    print(datetime.datetime.now())
    print("starting to generate problem")
    cre_sat.create_nupp_problem_from_table(table, problem_path)
    print("problem generated\n")

def create_unit_problem(left, right, problem_path):
    table = compute_table(left, right)
    print(datetime.datetime.now())
    print("starting to generate problem")
    cre_sat.create_unit_problem_from_table(table, problem_path)
    print("problem generated\n")

############

import running_sat_problems as run_sat

def run_nupp_problem(left, right, problem_path, result_path, kernels):
    print("\n")
    create_nupp_problem(left, right, problem_path)
    print(datetime.datetime.now())
    print("starting to run glucose\n")
    code = run_sat.run_glucose(problem_path, result_path, kernels)
    print(datetime.datetime.now())
    print("glucose finished")
    if code  == 10:
        print("SAT\n")
        #
        result = run_sat.read_glucose_result(result_path, len(left), len(right))
        sol_left = [left[i] for i in result[1]]
        sol_right = [right[i] for i in result[2]]
        if has_no_unique_product(sol_left, sol_right):
            print("verification successful \n")
            return [sol_left, sol_right]
        else:
            print("verification failed \n")
            return -1
    else:
        print("UNSAT\n")
        return -1

def run_unit_problem(left, right, problem_path, result_path, kernels):
    print("\n")
    create_unit_problem(left, right, problem_path)
    print(datetime.datetime.now())
    print("starting to run glucose\n")
    code = run_sat.run_glucose(problem_path, result_path, kernels)
    print(datetime.datetime.now())
    print("glucose finished")
    if code  == 10:
        print("SAT\n")
        #
        result = run_sat.read_glucose_result(result_path, len(left), len(right))
        sol_left = [left[i] for i in result[1]]
        sol_right = [right[i] for i in result[2]]
        if multiply_to_identity(sol_left, sol_right):
            print("verification successful \n")
            return [sol_left, sol_right]
        else:
            print("verification failed \n")
            return -1
    else:
        print("UNSAT\n")
        return -1

#############
