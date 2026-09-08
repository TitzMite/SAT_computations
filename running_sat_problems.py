
import os
import subprocess

##############

def run_glucose(cnf_path, result_path, kernels):
    """
    Runs Glucose on `cnf_path`, writes solver output to `result_path`,
    and returns Glucose's exit code (10=SAT, 20=UNSAT, else=error).

    Args:
        cnf_path:     Path to the DIMACS CNF file.
        result_path:  Where to write Glucose stdout.
        kernels:      (Optional) Number of kernels to use (default=1).

    Returns:
        int: Glucose return code (10 SAT, 20 UNSAT).
    """
    # Make sure the output folder exists
    d = os.path.dirname(result_path)
    if d:
        os.makedirs(d, exist_ok=True)
    cmd = ["glucose"]
    # Options
    if kernels>0:
        cmd.append(f"-nthreads={kernels}")
    cmd.extend(["-rnd-init", "-model"])
    # Input and output must be last
    cmd.extend([cnf_path, result_path])
    with open(result_path, "w", encoding="utf-8") as out:
        proc = subprocess.run(
            cmd,
            stdout=out,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
    return proc.returncode

def read_glucose_result(result_path, number_left, number_right):
    limit = number_left + number_right
    with open(result_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    low = content.lower()
    if "unsat" in low:
        return ["UNSAT"]
    if "sat" not in low:
        return ["UNKNOWN"]
    # Collect true DIMACS variables in 1..limit
    true_vars = set()
    for line in content.splitlines():
        line = line.strip()
        if not line or line[0] not in "vV":
            continue
        for tok in line.split()[1:]:
            try:
                lit = int(tok)
            except ValueError:
                continue
            if lit > 0 and lit <= limit:  # keep only positive literals within [1..k1+k2]
                true_vars.add(lit)
    relevant_trues  = sorted(x - 1 for x in true_vars if x <= limit)
    relevant_lefts =  [i for i in relevant_trues if i < number_left]
    relevant_right = [i-number_left for i in relevant_trues if i >= number_left]
    return ["SAT", relevant_lefts, relevant_right]
####


