from __future__ import division

from abc import ABCMeta, abstractmethod

from numba import jit
import numpy as np

class Forcefield(object):
    __metaclass__ = ABCMeta
    def __init__(self):
        self.constraints = []

    @abstractmethod
    def calc_potential(self, r):
        pass

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

class Mie(Forcefield):
    def __init__(self, sigma, epsilon, n, m):
        super(Mie, self).__init__()

        self.sigma = sigma
        self.epsilon = epsilon
        self.n = n
        self.m = m

        self.add_constraint(self.constr1)

    def calc_potential(self, r):
        if not hasattr(r, "__iter__"):
            r = [r]

        sigma = self.sigma.value
        epsilon = self.epsilon.value
        n = self.n.value
        m = self.m.value

        C = (n / (n - m)) * ((n / m) ** (m / (n - m)))

        return C * epsilon * (((sigma/r) ** n) - ((sigma/r) ** m))

    def constr1(self):
        return self.n > self.m

class Parameter(object):
    def __init__(self, value, upper=None, lower=None, fixed=False):
        super(Parameter, self).__init__()

        self.value = value
        self.fixed = fixed
        if not (fixed or (upper is not None and lower is not None)):
            raise ValueError("Must set fixed=True or define upper and lower bounds")
        if upper is not None:
            self.upper = upper
            self.lower = lower

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

if __name__ == "__main__":
    sigma = Parameter(value=0.8, upper=1.2, lower=0.6)
    epsilon = Parameter(value=0.4, upper=0.6, lower=0.3)
    n = Parameter(value=12, upper=25, lower=10)
    m = Parameter(value=20, fixed=True)

    ff = Mie(sigma=sigma, epsilon=epsilon, n=n, m=m)
    import pdb;pdb.set_trace()
