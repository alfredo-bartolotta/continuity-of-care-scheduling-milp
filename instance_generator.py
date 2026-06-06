import pandas as pd
import numpy as np
import os

def generate_instance(n_patients =100  ,n_therapists =10,n_rooms =4, n_machines = 4,n_days =5, n_slots = 12, seed=666):
    if seed is not None:
        np.random.seed(seed)

    I = list(range(1, n_patients+1))
    print("Patients:", I)

    mu = {i: np.random.randint(1, 11) for i in I}
    print("Urgency level of patient i:", mu)

    omega = {i: np.random.randint(1, 5) for i in I}
    print("Waiting days for patient i:", omega)


    K = list(range(1, n_therapists+1))
    print("Therapists:", K)

    D = list(range(1, n_days+1))
    print("Days:", D)

    T = list(range(1, n_slots+1))
    print("Time slots per day:", T)

    J = [1, 2]
    print("Visits type:", J)

    N = {(i, j): np.random.randint(0, 4) if j == 1 else np.random.randint(0, 4) for i in I for j in J}
    for i in I:
        #for j in J:
            if N[i ,1] == 0 and N[i, 2] == 0:
                x = np.random.choice([1 ,2])
                N[i, x] = np.random.randint(1, 4)

    print("Number of sessions for patient i of type j:", N)

    
    p_absent = 0.10          # prob. of being obsent on day t
    p_full_contract = 0.60   # prob. of FULL-TIME contract
    block = 4                # 4 slot = 1 block
    align_to_blocks = True   

    is_full_time = {k: (np.random.rand() < p_full_contract) for k in K}

    shift_start = {}
    shift_len = {}

    for k in K:
        L = 8 if is_full_time[k] else 4
        shift_len[k] = L

        if align_to_blocks:
            possible_starts = list(range(1, n_slots - L + 2, block))
        else:
            possible_starts = list(range(1, n_slots - L + 2))

        shift_start[k] = np.random.choice(possible_starts)

    sigma = {}
    for k in K:
        L = shift_len[k]
        start = shift_start[k]

        for d in D:
            if np.random.rand() < p_absent:
                for t in T:
                    sigma[(k, d, t)] = 0
                continue

            for t in T:
                sigma[(k, d, t)] = 1 if start <= t < start + L else 0
        
        tau = {(i, d, t): np.random.choice([0, 1], p=[0.4, 0.6]) for i in I for d in D for t in T}
    #print("Patient i availability in day d at time t:", tau)

    availability_patient = {i: sum(tau[i, d, t] for d in D for t in T) for i in I}
    for i in I:
        if availability_patient[i] < sum(N[i, j] for j in J):
            print(f"Warning: Patient {i} has insufficient availability for required sessions.")
        else:
            print("TUTTO OK")

    data = {'I': I,
            'K': K,
            'D': D,
            'T': T, 
            'J': J, 
            'N': N, 
            'Ns': n_rooms, 
            'Nm': n_machines, 
            'mu': mu,
            'omega': omega, 
            'sigma': sigma, 
            'tau': tau}
    
    return data

def write_instance_dat(data, filename):
    with open(filename, 'w') as f:
        f.write(f"NI: {len(data['I'])}\n")
        f.write(f"NK: {len(data['K'])}\n")
        f.write(f"ND: {len(data['D'])}\n")
        f.write(f"NT: {len(data['T'])}\n")
        f.write(f"NS: {data['Ns']}\n")
        f.write(f"NM: {data['Nm']}\n\n")

        # Patient data: mu, omega, N
        f.write("mui: [")
        f.write(" ".join(str(data['mu'][i]) for i in data['I']))
        f.write("]\n")

        f.write("omegai: [")
        f.write(" ".join(str(data['omega'][i]) for i in data['I']))
        f.write("]\n")

        f.write("Nij: [")
        values = [f"({i} {j}) {data['N'][(i, j)]}" for i in data['I'] for j in [1, 2]]
        f.write(" ".join(values))
        f.write("]\n\n")

        # Patient availability tau(i,d,t)
        f.write("tauidt: [")
        values = [f"({i} {d} {t}) {data['tau'][(i, d, t)]}" 
                  for i in data['I'] for d in data['D'] for t in data['T']]
        f.write(" ".join(values))
        f.write("]\n\n")

        # Therapist availability sigma(k,d,t)
        f.write("sigmakdt: [")
        values = [f"({k} {d} {t}) {data['sigma'][(k, d, t)]}" 
                  for k in data['K'] for d in data['D'] for t in data['T']]
        f.write(" ".join(values))
        f.write("]\n")

    
data = generate_instance(n_patients=10, n_therapists=5, n_rooms=5, n_machines=3, n_days=7, n_slots=10, seed=42)
write_instance_dat(data, r"C:\Users\alfri\OneDrive\Desktop\Tesi\tesi.dat")

COMBINATIONS = [
    (  100,10, 4, 4, 5,12),
    #(20, 4, 3, 7, 10, 10),
    #(30, 5, 4, 10, 14, 12),
]

BASE_PATH = r"C:\Users\alfri\OneDrive\Desktop\Tesi"
import os
instances_dir = os.path.join(BASE_PATH, "instances")
os.makedirs(instances_dir, exist_ok=True)
    
for n_patients, n_therapists, n_rooms, n_machines, n_days, n_slots in COMBINATIONS:
    for i in range(1,11):
        data = generate_instance(n_patients=n_patients, n_therapists=n_therapists, n_rooms=n_rooms, n_machines=n_machines, n_days=n_days, n_slots=n_slots, seed=i)
        filename = os.path.join(instances_dir,f"P{n_patients}_T{n_therapists}_R{n_rooms}_M{n_machines}_D{n_days}_S{n_slots}_{i}.dat")
        write_instance_dat(data, filename)
