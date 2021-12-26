import matplotlib.pyplot as plt
import numpy as np


class Lens:

    def __init__(self, r1, r2, n, h_up, h_down, color):

        self.r1 = r1

        self.r2 = r2

        self.n = n

        self.color = color

        self.h_up = h_up

        self.h_down = h_down

    def plot(self):

        plt.vlines(0, self.h_down, self.h_up, color=self.color, linewidth=.7, linestyles='dashed')


class RayCentre:

    def __init__(self, x_obj, y_obj, x_im, y_im, color):

        self.x_obj = x_obj

        self.y_obj = y_obj

        self.x_im = x_im

        self.y_im = y_im

        self.color = color

    def plot(self):

        plt.plot([self.x_obj, self.x_im], [self.y_obj, self.y_im], color=self.color)

        if self.x_obj < self.x_im < 0:
            plt.plot([self.x_obj, 0], [self.y_obj, 0], color=self.color)

        elif self.x_im < self.x_obj < 0:
            plt.plot([self.x_im, 0], [self.y_im, 0], color=self.color)

        elif self.x_obj < 0 < self.x_im:
            plt.plot([self.x_obj, self.x_im], [self.y_obj, self.y_im], color=self.color)


class RayFi:

    def __init__(self, x_obj, y_obj, x_im, y_im, f2, color):

        self.x_obj = x_obj

        self.y_obj = y_obj

        self.x_im = x_im

        self.y_im = y_im

        self.f2 = f2

        self.color = color

    def plot(self):

        plt.hlines(self.y_obj, self.x_obj, 0, color=self.color)

        if 0 < self.f2 < self.x_im:
            plt.plot([0, self.x_im], [self.y_obj, self.y_im], color=self.color)

        elif 0 < self.x_im < self.f2:
            plt.plot([0, self.f2], [self.y_obj, 0], color=self.color)

        elif self.f2 < self.x_im < 0:
            plt.plot([0, self.f2], [self.y_obj, 0], color=self.color, linestyle='dashed')

            plt.plot([0, -.5 * self.f2], [self.y_obj, 1.5 * self.y_obj], color=self.color)

        elif self.x_im < self.f2 < 0:
            plt.plot([0, self.x_im], [self.y_obj, self.y_im], color=self.color, linestyle='dashed')

        elif self.x_im < 0 < self.f2:
            plt.plot([0, self.f2], [self.y_obj, 0], color=self.color)

            plt.plot([0, self.x_im], [self.y_obj, self.y_im], color=self.color, linestyle='dashed')


class RayFo:

    def __init__(self, x_obj, y_obj, x_im, y_im, f1, color):
        self.x_obj = x_obj

        self.y_obj = y_obj

        self.x_im = x_im

        self.y_im = y_im

        self.f1 = f1

        self.color = color

    def plot(self):

        if self.x_obj < self.f1 < 0:
            plt.plot([self.x_obj, 0], [self.y_obj, self.y_im], color=self.color)

            plt.hlines(self.y_im, 0, self.x_im, color=self.color)

        elif self.f1 < self.x_obj < 0:
            plt.plot([self.f1, 0], [0, self.y_im], color=self.color)

            plt.hlines(self.y_im, 0, -.5 * self.f1, color=self.color)

            plt.hlines(self.y_im, 0, self.x_im, color=self.color, linestyle='dashed')

        elif self.x_obj < 0 < self.f1:

            plt.plot([self.x_obj, 0], [self.y_obj, self.y_im], color=self.color)

            plt.hlines(self.y_im, 0, self.f1, color=self.color)

            plt.plot([0, self.f1], [self.y_im, 0], color=self.color, linestyle='dotted')

            plt.hlines(self.y_im, 0, self.x_im, color=self.color, linestyle='dashed')


class OptAxis:

    def __init__(self, x_obj, x_im, f1):

        self.start = min(x_obj, x_im, f1, -f1)

        self.end = max(x_obj, x_im, f1, -f1)

    def plot(self):

        plt.plot([self.start, self.end], [0, 0], 'k', linewidth=.5)


def ray_tracing(x_obj, y_obj, n0, n, r1, r2, invert_x_axis, color_lens='blue', color_ray_f1='red', color_ray_f2='lime',
                color_ray_centre='gray'):
    """
    Compute ray tracing for thin lens

    Rays are assumed to travel from left (negative x) to right (positive x) before refracting on the lens. A positive
    radius corresponds to a convex surface whereas a negative radius corresponds to a concave surface (from left to
    right.)

    :param x_obj: location of the object within the optical axis
    :param y_obj: height of the object
    :param n0: refractive index of the medium
    :param n: refractive index of the lens
    :param r1: radius of the first surface encountered by the rays, r1 > 0 for convex surface and r1 < 0 for concave
        surface (from left to right.)
    :param r2: radius of the second surface encountered by the rays, r2 > 0 for convex surface and r2 < 0 for concave
        surface (from left to right.)
    :param invert_x_axis: True for showing positive x at the left of the origin, else False (default False)
    :param color_lens: color of the lens (default "blue")
    :param color_ray_f1: color the ray object-principal focus-lens (default "red")
    :param color_ray_f2: color of the ray object-lens-secondary focus (default "lime")
    :param color_ray_centre: color of the ray object-lens centre (default "gray")
    :return:
        - x_im: location of the image within the optical axis
        - y_im: height of the image
        - M: magnification
        - f1: location of the principal focus
    """
    if x_obj > 0:
        raise ValueError("I don't know how to deal with virtual objects yet; please choose x_obj < 0.\nIf you want to "
                         "see rays coming from positive x, you may choose invert_x_axis = True.")

    elif x_obj == 0:
        raise ValueError("The object cannot be placed at the lens.")

    if r1 == 0 or r2 == 0:
        raise ValueError("Neither of the radii can be zero.")

    if y_obj == 0:
        raise ValueError("The height of the object cannot be zero.")

    # Foci

    f1 = n0 / (n - n0) * (r1 * r2) / (r1 - r2)

    f2 = -f1

    # Imagen

    try:
        x_im = (-1 / f1 + 1 / x_obj) ** -1

    except ZeroDivisionError:
        print("The object has been placed at the principal focus. No image is formed.")

        return None, None, None, f1

    else:
        M = x_im / x_obj

        y_im = M * y_obj

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

        lens = Lens(r1, r2, n, h_up, h_down, color_lens)

        lens.plot()

        ray_centre = RayCentre(x_obj, y_obj, x_im, y_im, color_ray_centre)

        ray_centre.plot()

        ray_f2 = RayFi(x_obj, y_obj, x_im, y_im, f2, color_ray_f2)

        ray_f2.plot()

        ray_f1 = RayFo(x_obj, y_obj, x_im, y_im, f1, color_ray_f1)

        ray_f1.plot()

        plt.vlines(x_obj, 0, y_obj, 'k', linewidth=2)

        plt.vlines(x_im, 0, y_im, 'k', linewidth=2)

        plt.scatter([f1, f2], [0, 0], color='k')

        opt_axis = OptAxis(x_obj, x_im, f1)

        opt_axis.plot()

        if invert_x_axis:
            xticks, _ = plt.xticks()

            plt.xticks(xticks, np.round(-xticks, 2))

        plt.show()

        return x_im, y_im, M, f1
