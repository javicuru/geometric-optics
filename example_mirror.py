"""
This is a sample script showing how to:
    1) Set the main parameters of spherical_mirror.ray_tracing
    2) Call spherical_mirror.ray_tracing
    3) Show results.
"""

import spherical_mirror as sm

# Parameters

r = -1

x_obj = -1.2
y_obj = 1

# Compute ray tracing

x_im, y_im, M, f = sm.ray_tracing(x_obj, y_obj, r)

print("x_im = " + str(x_im))

print("y_im = " + str(y_im))

print("M = " + str(M))

print("f = " + str(f))
