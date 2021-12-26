"""
Classes and functions for computing ray tracing for spherical mirrors.
"""

import matplotlib.pyplot as plt
import numpy as np


class Mirror:

    def __init__(self, f, h_down, h_up, color):
        self.f = f

        self.h_down = h_down

        self.h_up = h_up

        self.color = color

    def plot(self):
        plt.vlines(0, self.h_down, self.h_up, color=self.color, linewidth=.7, linestyles='dashed')


class RayParallel:

    def __init__(self, x_obj, y_obj, x_im, y_im, f, color):
        self.x_obj = x_obj

        self.y_obj = y_obj

        self.x_im = x_im

        self.y_im = y_im

        self.f = f

        self.color = color

    def plot(self):
        plt.hlines(self.y_obj, self.x_obj, 0, color=self.color)

        if self.x_im < self.f < 0:
            plt.plot([0, self.x_im], [self.y_obj, self.y_im], color=self.color)

        elif self.f < self.x_im < 0:
            plt.plot([0, self.f], [self.y_obj, 0], color=self.color)

        elif self.f < 0 < self.x_im:
            plt.plot([0, self.x_im], [self.y_obj, self.y_im], color=self.color, linestyle='dashed')

            plt.plot([0, self.f], [self.y_obj, 0], color=self.color)

        elif 0 < self.x_im < self.f:
            plt.plot([0, self.f], [self.y_obj, 0], color=self.color, linestyle='dashed')

            plt.plot([0, -.5*self.f], [self.y_obj, 1.5*self.y_obj], color=self.color)


class RayFocus:

    def __init__(self, x_obj, y_obj, x_im, y_im, f, color):
        self.x_obj = x_obj

        self.y_obj = y_obj

        self.x_im = x_im

        self.y_im = y_im

        self.f = f

        self.color = color

    def plot(self):
        plt.plot([self.x_obj, 0], [self.y_obj, self.y_im], color=self.color)

        if self.x_im < 0:
            plt.hlines(self.y_im, 0, self.x_im, color=self.color)

        elif self.f < 0 < self.x_im:
            plt.plot([self.f, self.x_obj], [0, self.y_obj], color=self.color)

            plt.hlines(self.y_im, 0, self.x_im, color=self.color, linestyle='dashed')

            plt.hlines(self.y_im, 0, .5*self.f, color=self.color)

        elif 0 < self.x_im < self.f:
            plt.hlines(self.y_im, 0, self.x_im, color=self.color, linestyle='dashed')

            plt.hlines(self.y_im, 0, -self.x_im*.5, color=self.color)

            plt.plot([0, self.f], [self.y_im, 0], color=self.color, linestyle='dotted')


class RayCentre:

    def __init__(self, x_obj, y_obj, x_im, y_im, f, color):
        self.x_obj = x_obj

        self.y_obj = y_obj

        self.x_im = x_im

        self.y_im = y_im

        self.f = f

        self.color = color

    def plot(self):
        plt.plot([self.x_obj, 0], [self.y_obj, 0], color=self.color)

        if self.x_im > 0:
            plt.plot([0, self.x_im], [0, self.y_im], color=self.color, linestyle='dashed')

            plt.plot([0, -.5*self.x_im], [0, -.5*self.y_im], color=self.color)

        elif self.x_im < 0:
            plt.plot([0, self.x_im], [0, self.y_im], color=self.color)


class OptAxis:

    def __init__(self, x_obj, x_im, f):

        self.start = min(x_obj, x_im, f, -f)

        self.end = max(x_obj, x_im, f, -f)

    def plot(self):

        plt.plot([self.start, self.end], [0, 0], 'k', linewidth=.5)


def ray_tracing(x_obj, y_obj, r, invert_x_axis=False, color_mirror='blue', color_ray_focus='red',
                color_ray_parallel='lime', color_ray_centre='gray'):
    """
    Compute ray tracing for spherical mirror

    Rays are assumed to travel from left (negative x) to right (positive x) before reflecting on the mirror. A positive
    radius corresponds to a convex mirror whereas a negative radius corresponds to a concave mirror.

    :param x_obj: location of the object within the optical axis
    :param y_obj: height of the object
    :param r: radius of the mirror, r < 0 for concave mirror, r > 0 for convex mirror
    :param invert_x_axis: True for showing positive x at the left of the origin, else False (default False)
    :param color_mirror: color of the mirror (default "blue")
    :param color_ray_focus: color the ray object-focus-mirror (default "red")
    :param color_ray_parallel: color of the ray object-mirror-focus (default "lime")
    :param color_ray_centre: color of the ray object-mirror centre (default "gray")
    :return:
        - x_im: location of the image within the optical axis
        - y_im: height of the image
        - M: magnification
        - f: location of the focus
    """

    if x_obj > 0:
        raise ValueError("I don't know how to deal with virtual objects yet; please choose x_obj < 0.\nIf you want to "
                         "see rays coming from positive x, you may choose invert_x_axis = True.")

    elif x_obj == 0:
        raise ValueError("The object cannot be placed at the mirror.")

    if r == 0:
        raise ValueError("The radius cannot be zero.")

    if y_obj == 0:
        raise ValueError("The height of the object cannot be zero.")

    f = .5*r

    try:
        x_im = (f**-1 - x_obj**-1)**-1

    except ZeroDivisionError:
        print("The object has been placed at the focus. No image is formed.")

        return None, None, None, f

    else:

        M = -x_im/x_obj

        y_im = M*y_obj

        if y_obj > 0 and y_im > 0:
            h_up = max(y_obj, y_im)

            h_down = 0

        elif y_obj < 0 and y_im < 0:
            h_down = min(y_obj, y_im)

            h_up = 0

        elif y_obj > 0 > y_im:
            h_up = y_obj

            h_down = y_im

        elif y_im > 0 > y_obj:
            h_up = y_im

            h_down = y_obj

        mirror = Mirror(f, h_up, h_down, color_mirror)

        mirror.plot()

        rc = RayCentre(x_obj, y_obj, x_im, y_im, f, color_ray_centre)

        rc.plot()

        r1 = RayFocus(x_obj, y_obj, x_im, y_im, f, color_ray_focus)

        r1.plot()

        r2 = RayParallel(x_obj, y_obj, x_im, y_im, f, color_ray_parallel)

        r2.plot()

        plt.vlines(x_obj, 0, y_obj, 'k', linewidth=2)

        plt.vlines(x_im, 0, y_im, 'k', linewidth=2)

        plt.scatter(f, 0, color='k')

        opt_axis = OptAxis(x_obj, x_im, f)

        opt_axis.plot()

        if invert_x_axis:
            xticks, _ = plt.xticks()

            plt.xticks(xticks, np.round(-xticks, 2))

        plt.show()

        return x_im, y_im, M, f
