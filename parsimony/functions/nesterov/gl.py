# -*- coding: utf-8 -*-
"""
The :mod:`parsimony.functions.nesterov.gl` module contains the loss function
and helper functions for overlapping Group lasso, GL, smoothed using
Nesterov's technique.

Created on Mon Feb  3 10:46:47 2014

@author:  Tommy Löfstedt, Edouard Duchesnay
@email:   lofstedt.tommy@gmail.com, edouard.duchesnay@cea.fr
@license: BSD 3-clause.
"""
import scipy.sparse as sparse
import numpy as np

from interfaces import NesterovFunction
import parsimony.functions.interfaces as interfaces
import parsimony.utils.consts as consts
import parsimony.utils.maths as maths

__all__ = ["GroupLassoOverlap", "A_from_groups"]


class GroupLassoOverlap(interfaces.AtomicFunction,
                        NesterovFunction,
                        interfaces.Gradient,
                        interfaces.LipschitzContinuousGradient):

    def __init__(self, l, c=0.0, A=None, mu=0.0):
        """Group L1-L2 function, with overlapping groups. Represents the
        function

            GL(x) = l * (\sum_{g=1}^G \|x_g\|_2 - c),

        where \|.\|_2 is the L2-norm. The coinstrained version has the form

            GL(x) <= c.

        Parameters:
        ----------
        l : The Lagrange multiplier, or regularisation constant, of the
                function.

        c : The limit of the constraint. The function is feasible if
                GL(\beta) <= c. The default value is c=0, i.e. the default is a
                regularised formulation.

        A : A (usually sparse) matrix. The linear operator for the Nesterov
                formulation. May not be None!

        mu : The Nesterov function regularisation constant for the smoothing.
        """
        super(GroupLassoOverlap, self).__init__(l, c, A, mu)

        self.reset()

    def reset(self):

        self._lambda_max = None

    def f(self, beta):
        """ Function value.
        """
        if self.l < consts.TOLERANCE:
            return 0.0

#        alpha = self.alpha(beta)
#        return self.phi(alpha, beta)

        A = self.A()
        normsum = 0.0
        for Ag in A:
            normsum += maths.norm(Ag.dot(beta))

        return self.l * (normsum - self.c)

    def phi(self, alpha, beta):
        """Function value with known alpha.

        From the interface "NesterovFunction".
        """
        if self.l < consts.TOLERANCE:
            return 0.0

        Aa = self.Aa(alpha)

        alpha_sqsum = 0.0
        for a in alpha:
            alpha_sqsum += np.sum(a ** 2.0)

        return self.l * ((np.dot(beta.T, Aa)[0, 0]
                          - (self.mu / 2.0) * alpha_sqsum) - self.c)

    def feasible(self, beta):
        """Feasibility of the constraint.

        From the interface "Constraint".
        """
        A = self.A()
        normsum = 0.0
        for Ag in A:
            normsum += maths.norm(Ag.dot(beta))

        return normsum <= self.c

    def L(self):
        """ Lipschitz constant of the gradient.

        From the interface "LipschitzContinuousGradient".
        """
        if self.l < consts.TOLERANCE:
            return 0.0

        lmaxA = self.lambda_max()

        return self.l * lmaxA / self.mu

    def lambda_max(self):
        """ Largest eigenvalue of the corresponding covariance matrix.

        From the interface "Eigenvalues".
        """
        # Note that we can save the state here since lambda_max(A) is not
        # allowed to change.
        if self._lambda_max is None:
            A = self.A()
            colsum = 0.0
            for Ag in A:
                B = Ag.copy()
                B.data **= 2.0
                colsum += B.sum(axis=0)

            self._lambda_max = np.max(colsum)

        return self._lambda_max

    def project(self, a):

        for i in xrange(len(a)):
            astar = a[i]
            normas = np.sqrt(np.sum(astar ** 2.0))
            if normas > 1.0:
                astar /= normas
            a[i] = astar

        return a

    def M(self):
        """ The maximum value of the regularisation of the dual variable. We
        have

            M = max_{\alpha \in K} 0.5*|\alpha|²_2.

        Since each group may have at most L2-norm 1, M may not exceed the
        number of groups, i.e. the number of groups divided by two is the
        maximum.

        From the interface "NesterovFunction".
        """
        return float(len(self.A())) / 2.0

    """ Computes a "good" value of \mu with respect to the given \beta.

    From the interface "NesterovFunction".
    """
    def estimate_mu(self, beta):

        SS = 0
        A = self.A()
        for i in xrange(len(A)):
            SS += A[i].dot(beta) ** 2.0

        return np.max(np.sqrt(SS))


def A_from_groups(num_variables, groups, weights=None):
    """Generates the linear operator for the group lasso Nesterov function
    from the groups of variables.

    Parameters:
    ----------
    num_variables : Integer. The total number of variables.

    groups : A list of lists. The outer list represents the groups and the
            inner lists represent the variables in the groups. E.g. [[1, 2],
            [2, 3]] contains two groups ([1, 2] and [2, 3]) with variable 1 and
            2 in the first group and variables 2 and 3 in the second group.

    weights : A list. Weights put on the groups. Default is weight 1 for each
            group.
    """
    if weights is None:
        weights = [1.0] * len(groups)

    A = list()
    for g in xrange(len(groups)):
        Gi = groups[g]
        lenGi = len(Gi)
        Ag = sparse.lil_matrix((lenGi, num_variables))
        for i in xrange(lenGi):
            w = weights[g]
            Ag[i, Gi[i]] = w

        # Matrix operations are a lot faster when the sparse matrix is csr
        A.append(Ag.tocsr())

    return A