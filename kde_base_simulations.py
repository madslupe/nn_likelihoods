# Basic python utilities
import numpy as np
import scipy as scp
from scipy.stats import gamma

# Parallelization
import multiprocessing as mp
from  multiprocessing import Process
from  multiprocessing import Pool
import psutil

# System utilities
from datetime import datetime
import time
import os
import pickle
import uuid

# My own code
import kde_class as kde
import cddm_data_simulation as ds
import boundary_functions as bf

def data_generator(*args):
    # CHOOSE SIMULATOR HERE
    simulator_data = ds.full_ddm(*args)
    
    # CHOOSE TARGET DIRECTORY HERE
    file_dir =  'data_storage/kde/full_ddm/base_simulations/'

    # STORE
    file_name = file_dir + simulator + '_' + uuid.uuid1().hex
    pickle.dump(simulator_data, open( file_name + '.pickle', "wb" ) )
    print('success')

if __name__ == "__main__":
    # Get cpu cnt
    n_cpus = psutil.cpu_count(logical = False)

    # Parameter ranges (for the simulator)
    v = [-1.5, 1.5]
    w = [0.3, 0.7]
    a = [0.3, 2]
    
    # FULL DDM
    dw = [0.0, 0.1]
    sdv = [0.0, 0.5]

    #     c1 = [0, 5]
#     c2 = [1, 1.5]
    # Linear Collapse
#     node = [0, 5]
#     theta = [0, np.pi/2]

    # Weibull Bound
#     node = [0, 5]
#     shape = [1.1, 50]
#     scale = [0.1, 10]

    # Simulator parameters
    simulator = 'full_ddm'
    s = 1
    delta_t = 0.01
    max_t = 20
    n_samples = 20000
    print_info = False
    boundary_multiplicative = False

    # Number of simulators to run
    n_simulators = 2500

    # Make function input tuples
    v_sample = np.random.uniform(low = v[0], high = v[1], size = n_kdes)
    w_sample = np.random.uniform(low = w[0], high = w[1], size = n_kdes)
    a_sample = np.random.uniform(low = a[0], high = a[1], size = n_kdes)

    # Full DDM
    dw_sample = np.random.uniform(low = dw[0], high = dw[1], size = n_kdes)
    sdv_sample = np.random.uniform(low = sdv[0], high = sdv[1], size = n_kdes)
    
    # Exp c1_c2
#     c1_sample = np.random.uniform(low = c1[0], high = c1[1], size = n_kdes)
#     c2_sample = np.random.uniform(low = c2[0], high = c2[1], size = n_kdes)

    # Linear Collapse
#     node_sample = np.random.uniform(low = node[0], high = node[1], size = n_kdes)
#     theta_sample = np.random.uniform(low = theta[0], high = theta[1], size = n_kdes)

    # Weibull
#     node_sample = np.random.uniform(low = node[0], high = node[1], size = n_kdes)
#     shape_sample = np.random.uniform(low = shape[0], high = shape[1], size = n_kdes)
#     scale_sample = np.random.uniform(low = scale[0], high = scale[1], size = n_kdes)

    # Defining main function to iterate over:
    # Folder in which we would like to dump files

    args_list = []
    for i in range(0, n_simulators, 1):
        args_list.append((v_sample[i], # CHOOSE PARAM
                          a_sample[i], # CHOOSE PARAM
                          w_sample[i], ## ....
                          dw_sample[i], # CHOOSE PARAM
                          sdv_sample[i], # CHOOSE PARAM
                          s,
                          delta_t,
                          max_t,
                          n_samples,
                          print_info,
                          bf.constant, # CHOOSE: BOUNDARY FUNCTION
                          boundary_multiplicative, # CHOOSE: IS BOUNDARY MULTIPLICATIVE?
                          {}))

    # Parallel Loop
    with Pool(processes = n_cpus) as pool:
        res = pool.starmap(data_generator, args_list)
