# -*- coding: utf-8 -*-
"""
The :mod:`parsimony.functions.nesterov.interfaces` module contains the
necessary interfaces for Nesterov functions.

Created on Mon Feb  3 10:51:33 2014

@author:  Tommy Löfstedt
@email:   lofstedt.tommy@gmail.com
@license: BSD 3-clause.
"""
import abc

import numpy as np

import parsimony.utils.consts as consts

__all__ = ["NesterovFunction"]


# TODO: We need a superclass for NesterovFunction wrappers.
class NesterovFunction(object):
    """
    Parameters
    ----------
    l : The Lagrange multiplier, or regularisation constant, of the function.

    c : Float. The limit of the constraint. The function is feasible if
            sqrt(x'Mx) <= c. The default value is c=0, i.e. the default is a
            regularisation formulation.

    A : The linear operator for the Nesterov formulation. May not be None!

    mu: The regularisation constant for the smoothing
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, l, c=0.0, A=None, mu=consts.TOLERANCE):

        self.l = float(l)
        self.c = float(c)
        self._A = A
        self.mu = float(mu)

    def fmu(self, beta, mu=None):
        """Returns the smoothed function value.

        Parameters
        ----------
        beta : A weight vector

        mu : The regularisation constant for the smoothing
        """
        if mu is None:
            mu = self.get_mu()

        alpha = self.alpha(beta)
        alpha_sqsum = 0.0
        for a in alpha:
            alpha_sqsum += np.sum(a ** 2.0)

        Aa = self.Aa(alpha)

        return self.l * ((np.dot(beta.T, Aa)[0, 0]
                          - (mu / 2.0) * alpha_sqsum) - self.c)

    @abc.abstractmethod
    def phi(self, alpha, beta):
        """ Function value with known alpha.
        """
        raise NotImplementedError('Abstract method "phi" must be '
                                  'specialised!')

    def grad(self, beta):
        """ Gradient of the function at beta.

        Parameters
        ----------
        beta : The point at which to evaluate the gradient.
        """
        if self.l < consts.TOLERANCE:
            return 0.0

        alpha = self.alpha(beta)

        grad = self.l * self.Aa(alpha)

#        approx_grad = utils.approx_grad(self.f, beta, eps=1e-6)
#        print "NesterovFunction:", maths.norm(grad - approx_grad)

        return grad

    def get_mu(self):
        """Return the regularisation constant for the smoothing.
        """
        return self.mu

    def set_mu(self, mu):
        """Set the regularisation constant for the smoothing.

        Parameters
        ----------
        mu: The regularisation constant for the smoothing to use from now on.

        Returns
        -------
        old_mu: The old regularisation constant for the smoothing that was
                overwritten and is no longer used.
        """
        old_mu = self.get_mu()

        self.mu = mu

        return old_mu

    def alpha(self, beta):
        """ Dual variable of the Nesterov function.
        """
        A = self.A()
        mu = self.get_mu()
        alpha = [0] * len(A)
        for i in xrange(len(A)):
            alpha[i] = A[i].dot(beta) / mu

        # Apply projection
        alpha = self.project(alpha)

        return alpha

    def A(self):
        """ Linear operator of the Nesterov function.
        """
        return self._A

    def Aa(self, alpha):
        """ Compute A^\T\alpha.
        """
        A = self.A()
        Aa = A[0].T.dot(alpha[0])
        for i in xrange(1, len(A)):
            Aa += A[i].T.dot(alpha[i])

        return Aa

    @abc.abstractmethod
    def project(self, a):
        """ Projection onto the compact space of the Nesterov function.
        """
        raise NotImplementedError('Abstract method "project" must be '
                                  'specialised!')

    @abc.abstractmethod
    def M(self):
        """ The maximum value of the regularisation of the dual variable. We
        have

            M = max_{\alpha \in K} 0.5*|\alpha|²_2.
        """
        raise NotImplementedError('Abstract method "M" must be '
                                  'specialised!')

    @abc.abstractmethod
    def estimate_mu(self, beta):
        """ Compute a "good" value of \mu with respect to the given \beta.
        """
        raise NotImplementedError('Abstract method "mu" must be '
                                  'specialised!')