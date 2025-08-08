# icm20948_tofile.py


from icm20948 import *
import time
from time import perf_counter
from argparse import ArgumentParser
import numpy as np


if __name__ == "__main__":
    
    import os
    import sys
    
    parser = ArgumentParser()
    parser.add_argument("traceFile", help="rel. File for data storage (*.npz)" )
    parser.add_argument("n_measurements", type=int, help="number of measurements")
    parser.add_argument("wait_between_measurements", type=float, help="waiting time between consecutive measurements")
    args = parser.parse_args()
    
    # check if dir of trace file exists
    if not os.path.exists(os.path.dirname(args.traceFile)):
        sys.exit(f"os.path.dirname(args.traceFile) does not exist -> must be created before usage")
    
    wait_time_init = 2.0
    imu = ICM20948(i2c_addr=I2C_ADDR_ALT, i2c_bus=None)
    time.sleep(wait_time_init)
    
    # initialise numpy arrays
    t_vec = np.zeros(args.n_measurements, dtype=np.double)
    t_diff_vec = np.zeros(args.n_measurements, dtype=np.double)
    accel_xyz = np.zeros((args.n_measurements, 3), dtype=np.double)
    deg_ps_xyz = np.zeros((args.n_measurements, 3), dtype=np.double)
    mag_xyz = np.zeros((args.n_measurements, 3), dtype=np.double)


    for k in range(args.n_measurements):
        mx, my, mz = imu.read_magnetometer_data()
        t1 = perf_counter()
        ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
        t2 = perf_counter()
        
        t_vec[k] = t1
        t_diff_vec[k] = t2- t1
        accel_xyz[k, :] = np.array([ax, ay, az])
        deg_ps_xyz[k, :] = np.array([gx, gy, gz])
        mag_xyz[k,:] = np.array([mx, my, mz])

        time.sleep(arg.wait_between_measurements)
    
    # first measurments shall a time stamp 0
    t_vec = t_vec - t_vec[0]
    
    print(f"finished -> save to file: {args.traceFile}")
    np.savez(args.traceFile, t_vec=t_vec, t_diff_vec=t_diff_vec, accel_xyz=accel_xyz , deg_ps_xyz=deg_ps_xyz, mag_xyz=mag_xyz)