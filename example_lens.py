"""
This is a sample script showing how to:
    1) Set the main parameters of thin_lens.ray_tracing
    2) Call thin_lens.ray_tracing
    3) Show results.
"""

import thin_lens as tl

# Parameters

r1 = .2
r2 = -.3

x_obj = -.8
y_obj = 1

n0 = 1
n = 1.5

# Compute ray tracing

x_im, y_im, M, f1 = tl.ray_tracing(x_obj, y_obj, n0, n, r1, r2)

print("x_im = " + str(x_im))

print("y_im = " + str(y_im))

print("M = " + str(M))

print("f1 = " + str(f1))
