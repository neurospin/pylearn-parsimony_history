# -*- coding: utf-8 -*-
"""
The :mod:`parsimony.functions.objectives.functions` module contains rady-made
common combinations of loss functions and penalties that can be used right
away to analyse real data.

Created on Mon Apr 22 10:54:29 2013

@author:  Tommy Löfstedt, Vincent Guillemot, Edouard Duchesnay and
          Fouad Hadj-Selem
@email:   lofstedt.tommy@gmail.com, edouard.duchesnay@cea.fr
@license: BSD 3-clause.
"""
import numpy as np

import parsimony.functions.interfaces as interfaces
from parsimony.functions.losses import RidgeRegression
from parsimony.functions.losses import RidgeLogisticRegression
import parsimony.functions.penalties as penalties
#from parsimony.functions.penalties import ZeroFunction
#from parsimony.functions.penalties import L1
import parsimony.functions.nesterov.interfaces as nesterov_interfaces
from parsimony.functions.nesterov.L1 import L1 as SmoothedL1
from parsimony.functions.nesterov.L1TV import L1TV
from parsimony.functions.nesterov.tv import TotalVariation
from parsimony.functions.nesterov.gl import GroupLassoOverlap
import parsimony.utils.consts as consts

__all__ = ["CombinedFunction",
           "RR_L1_TV", "RLR_L1_TV", "RR_L1_GL", "RR_SmoothedL1TV"]


class CombinedFunction(interfaces.CompositeFunction,
                       interfaces.Gradient,
                       interfaces.ProximalOperator,
                       interfaces.StepSize):
    """Combines one or more loss functions, any number of penalties and zero
    or one proximal operator.

    This function thus represents

        f(x) = f_1(x) [ + f_2(x) ... ] [ + p_1(x) ... ] [ + P(x)],

    where f_i are differentiable Functions, p_j are differentiable penalties
    and P is a ProximalOperator. All functions and penalties must thus be
    Gradient, unless it is a ProximalOperator.

    If ProximalOperator is not given, then prox is the identity.
    """
    def __init__(self):

        self._f = []
        self._p = []
        self._prox = penalties.ZeroFunction()
#        self._c = []  # Not yet used.

    def reset(self):

        for f in self._f:
            f.reset()

        for p in self._p:
            p.reset()

#        for c in self._c:
#            c.reset()

        self._prox.reset()

    def add_function(self, function):

        if not isinstance(function, interfaces.Gradient):
            raise ValueError("Functions must have gradients.")

        self._f.append(function)

    def add_penalty(self, penalty, proximal_operator=False):

        if proximal_operator:
            if not isinstance(penalty, interfaces.ProximalOperator):
                raise ValueError("Not a proximal operator.")
            else:
                self._prox = penalty
        else:
            if not isinstance(penalty, interfaces.Gradient):
                raise ValueError("Penalties must have gradients.")
            else:
                self._p.append(penalty)

#    def add_constraint(self, constraint):
#
#        self._c.append(constraint)

    def f(self, x):
        """Function value.
        """
        val = 0.0
        for f in self._f:
            val += f.f(x)

        for p in self._p:
            val += p.f(x)

        val += self._prox.f(x)

        return val

    def grad(self, x):
        """Gradient of the differentiable part of the function.

        From the interface "Gradient".
        """
        grad = 0.0

        # Add gradients from the loss functions.
        for f in self._f:
            grad += f.grad(x)

        # Add gradients from the penalties.
        for p in self._p:
            grad += p.grad(x)

        return grad

    def prox(self, x, factor=1.0):
        """The proximal operator of the non-differentiable part of the
        function.

        From the interface "ProximalOperator".
        """
        return self._prox.prox(x, factor=factor)

    def step(self, x):
        """The step size to use in descent methods.

        From the interface "StepSize".

        Parameters
        ----------
        x : Numpy array. The point at which to evaluate the step size.
        """
        all_lipschitz = True
        for f in self._f:
            if not isinstance(f, interfaces.LipschitzContinuousGradient):
                all_lipschitz = False
                break

        for p in self._p:
            if not isinstance(p, interfaces.LipschitzContinuousGradient):
                all_lipschitz = False
                break

        step = 1.0
        if all_lipschitz:
            L = 0.0
            for f in self._f:
                L += f.L()
            for p in self._p:
                L += p.L()

        if all_lipschitz and L > 0.0:
            step = 1.0 / L
        else:
            # If not all functions have Lipschitz continuous gradients, try
            # to find the step size through backtracking line search.
            from algorithms import BacktrackingLineSearch
            import parsimony.functions.penalties as penalties

            p = -self.grad(x)
            line_search = BacktrackingLineSearch(
                condition=penalties.SufficientDescentCondition, max_iter=30)
            step = line_search(self, x, p, rho=0.5, a=0.1, c=1e-4)

        return step


class RR_L1_TV(interfaces.CompositeFunction,
               interfaces.Gradient,
               interfaces.LipschitzContinuousGradient,
               nesterov_interfaces.NesterovFunction,
               interfaces.ProximalOperator,
               interfaces.Continuation,
               interfaces.DualFunction,
               interfaces.StronglyConvex):
    """Combination (sum) of RidgeRegression, L1 and TotalVariation
    """
    def __init__(self, X, y, k, l, g, A=None, mu=0.0, penalty_start=0):
        """
        Parameters:
        ----------
        X : Numpy array. The X matrix for the ridge regression.

        y : Numpy array. The y vector for the ridge regression.

        k : Non-negative float. The Lagrange multiplier, or regularisation
                constant, for the ridge penalty.

        l : Non-negative float. The Lagrange multiplier, or regularisation
                constant, for the L1 penalty.

        g : Non-negative float. The Lagrange multiplier, or regularisation
                constant, of the smoothed TV function.

        A : Numpy array (usually sparse). The linear operator for the Nesterov
                formulation of TV. May not be None!

        mu : Non-negative float. The regularisation constant for the smoothing
                of the TV function.

        penalty_start : Non-negative integer. The number of columns, variables
                etc., to except from penalisation. Equivalently, the first
                index to be penalised. Default is 0, all columns are included.
        """
        self.X = X
        self.y = y

        self.rr = RidgeRegression(X, y, k)
        self.l1 = penalties.L1(l, penalty_start=penalty_start)
        self.tv = TotalVariation(g, A=A, mu=mu, penalty_start=penalty_start)

        self.reset()

    def reset(self):

        self.rr.reset()
        self.l1.reset()
        self.tv.reset()

        self._Xty = None
        self._invXXkI = None
        self._XtinvXXtkI = None

    def set_params(self, **kwargs):

        mu = kwargs.pop("mu", self.get_mu())
        self.set_mu(mu)

        super(RR_L1_TV, self).set_params(**kwargs)

    def get_mu(self):
        """Returns the regularisation constant for the smoothing.

        From the interface "NesterovFunction".
        """
        return self.tv.get_mu()

    def set_mu(self, mu):
        """Sets the regularisation constant for the smoothing.

        From the interface "NesterovFunction".

        Parameters:
        ----------
        mu : Non-negative float. The regularisation constant for the smoothing
                to use from now on.

        Returns:
        -------
        old_mu : Non-negative float. The old regularisation constant for the
                smoothing that was overwritten and is no longer used.
        """
        return self.tv.set_mu(mu)

    def f(self, beta):
        """Function value.
        """
        return self.rr.f(beta) \
             + self.l1.f(beta) \
             + self.tv.f(beta)

    def fmu(self, beta, mu=None):
        """Function value.
        """
        return self.rr.f(beta) \
             + self.l1.f(beta) \
             + self.tv.fmu(beta, mu)

    def phi(self, alpha, beta):
        """ Function value with known alpha.
        """
        return self.rr.f(beta) \
             + self.l1.f(beta) \
             + self.tv.phi(alpha, beta)

    def grad(self, beta):
        """Gradient of the differentiable part of the function.

        From the interface "Gradient".
        """
        return self.rr.grad(beta) \
             + self.tv.grad(beta)

    def L(self):
        """Lipschitz constant of the gradient.

        From the interface "LipschitzContinuousGradient".
        """
        return self.rr.L() \
             + self.tv.L()

    def prox(self, beta, factor=1.0):
        """The proximal operator of the non-differentiable part of the
        function.

        From the interface "ProximalOperator".
        """
        return self.l1.prox(beta, factor)

    def estimate_mu(self, beta):
        """Computes a "good" value of \mu with respect to the given \beta.

        From the interface "NesterovFunction".
        """
        return self.tv.estimate_mu(beta)

    def M(self):
        """The maximum value of the regularisation of the dual variable. We
        have

            M = max_{\alpha \in K} 0.5*|\alpha|²_2.

        From the interface "NesterovFunction".
        """
        return self.tv.M()

    def mu_opt(self, eps):
        """The optimal value of \mu given \epsilon.

        From the interface "Continuation".
        """
        gM = self.tv.l * self.tv.M()

        # Mu is set to 1.0, because it is in fact not here "anymore". It is
        # factored out in this solution.
        old_mu = self.tv.set_mu(1.0)
        gA2 = self.tv.L()  # Gamma is in here!
        self.tv.set_mu(old_mu)

        Lg = self.rr.L()

        return (-gM * gA2 + np.sqrt((gM * gA2) ** 2.0
             + gM * Lg * gA2 * eps)) \
             / (gM * Lg)

    def eps_opt(self, mu):
        """The optimal value of \epsilon given \mu.

        From the interface "Continuation".
        """
        gM = self.tv.l * self.tv.M()

        # Mu is set to 1.0, because it is in fact not here "anymore". It is
        # factored out in this solution.
        old_mu = self.tv.set_mu(1.0)
        gA2 = self.tv.L()  # Gamma is in here!
        self.tv.set_mu(old_mu)

        Lg = self.rr.L()

        return (2.0 * gM * gA2 * mu
             + gM * Lg * mu ** 2.0) \
             / gA2

    def eps_max(self, mu):
        """The maximum value of \epsilon.

        From the interface "Continuation".
        """
        gM = self.tv.l * self.tv.M()

        return mu * gM

    def betahat(self, alphak, betak):
        """ Returns the beta that minimises the dual function. Used when we
        compute the gap.

        From the interface "DualFunction".
        """
        if self._Xty is None:
            self._Xty = np.dot(self.X.T, self.y)

        Ata_tv = self.tv.l * self.tv.Aa(alphak)
        Ata_l1 = self.l1.l * SmoothedL1.project([betak / consts.TOLERANCE])[0]
        v = (self._Xty - Ata_tv - Ata_l1)

        shape = self.X.shape

        if shape[0] > shape[1]:  # If n > p

            # Ridge solution
            if self._invXXkI is None:
                XtXkI = np.dot(self.X.T, self.X)
                index = np.arange(min(XtXkI.shape))
                XtXkI[index, index] += self.rr.k
                self._invXXkI = np.linalg.inv(XtXkI)

            beta_hat = np.dot(self._invXXkI, v)

        else:  # If p > n
            # Ridge solution using the Woodbury matrix identity:
            if self._XtinvXXtkI is None:
                XXtkI = np.dot(self.X, self.X.T)
                index = np.arange(min(XXtkI.shape))
                XXtkI[index, index] += self.rr.k
                invXXtkI = np.linalg.inv(XXtkI)
                self._XtinvXXtkI = np.dot(self.X.T, invXXtkI)

            beta_hat = (v - np.dot(self._XtinvXXtkI, np.dot(self.X, v))) \
                       / self.rr.k

        return beta_hat

    def gap(self, beta, beta_hat=None):
        """Compute the duality gap.

        From the interface "DualFunction".
        """
        alpha = self.tv.alpha(beta)

        P = self.rr.f(beta) \
          + self.l1.f(beta) \
          + self.tv.phi(alpha, beta)

        beta_hat = self.betahat(alpha, beta)

        D = self.rr.f(beta_hat) \
          + self.l1.f(beta_hat) \
          + self.tv.phi(alpha, beta_hat)

        return P - D

    def A(self):
        """Linear operator of the Nesterov function.

        From the interface "NesterovFunction".
        """
        return self.tv.A()

    def Aa(self, alpha):
        """Computes A^\T\alpha.

        From the interface "NesterovFunction".
        """
        return self.tv.Aa(alpha)

    def project(self, a):
        """ Projection onto the compact space of the Nesterov function.

        From the interface "NesterovFunction".
        """
        return self.tv.project(a)


class RLR_L1_TV(RR_L1_TV):
    """Combination (sum) of RidgeLogisticRegression, L1 and TotalVariation.
    """
    def __init__(self, X, y, k, l, g, A=None, mu=0.0, weights=None,
                 penalty_start=0):
        """
        Parameters
        ----------
        X : Numpy array. The X matrix (n-by-p) for the logistic regression.

        y : Numpy array. The y vector for the logistic regression.

        k : Non-negative float. The Lagrange multiplier, or regularisation
                constant, for the ridge penalty.

        l : Non-negative float. The Lagrange multiplier, or regularisation
                constant, for the L1 penalty.

        g : Non-negative float. The Lagrange multiplier, or regularisation
                constant, of the smoothed TV function.

        A : Numpy array (usually sparse). The linear operator for the Nesterov
                formulation for TV. May not be None!

        mu : Non-negative float. The regularisation constant for the smoothing
                of the TV function.

        weights: List with n elements. The sample's weights.

        penalty_start : Non-negative integer. The number of columns, variables
                etc., to except from penalisation. Equivalently, the first
                index to be penalised. Default is 0, all columns are included.
        """
        self.X = X
        self.y = y

        self.rr = RidgeLogisticRegression(X, y, k, weights=weights)
        self.l1 = penalties.L1(l, penalty_start=penalty_start)
        self.tv = TotalVariation(g, A=A, mu=mu, penalty_start=penalty_start)

        self.reset()


class RR_L1_GL(RR_L1_TV):
    """Combination (sum) of RidgeRegression, L1 and Overlapping Group Lasso.
    """
    def __init__(self, X, y, k, l, g, A=None, mu=0.0, penalty_start=0):
        """
        Parameters:
        ----------
        X : Numpy array (n-by-p). The X matrix for the ridge regression.

        y : Numpy array (n-by-1). The y vector for the ridge regression.

        k : Non-negative float. The Lagrange multiplier, or regularisation
                constant, for the ridge penalty.

        l : Non-negative float. The Lagrange multiplier, or regularisation
                constant, for the L1 penalty.

        g : Non-negative float. The Lagrange multiplier, or regularisation
                constant, of the overlapping group L1-L2 function.

        A : Numpy array (usually sparse). The linear operator for the Nesterov
                formulation for group L1-L2. May not be None!

        mu : Non-negative float. The regularisation constant for the smoothing
                of the overlapping group L1-L2 function.

        penalty_start : Non-negative integer. The number of columns, variables
                etc., to except from penalisation. Equivalently, the first
                index to be penalised. Default is 0, all columns are included.
        """
        self.X = X
        self.y = y

        self.rr = RidgeRegression(X, y, k)
        self.l1 = penalties.L1(l, penalty_start=penalty_start)
        self.gl = GroupLassoOverlap(g, A=A, mu=mu, penalty_start=penalty_start)

        self.reset()

    def reset(self):

        self.rr.reset()
        self.l1.reset()
        self.gl.reset()

        self._Xty = None
        self._invXXkI = None
        self._XtinvXXtkI = None

    def set_params(self, **kwargs):

        # TODO: This is not good. Solve this better!
        mu = kwargs.pop("mu", self.get_mu())
        self.set_mu(mu)

        super(RR_L1_TV, self).set_params(**kwargs)

    def get_mu(self):
        """Returns the regularisation constant for the smoothing.

        From the interface "NesterovFunction".
        """
        return self.gl.get_mu()

    def set_mu(self, mu):
        """Sets the regularisation constant for the smoothing.

        From the interface "NesterovFunction".

        Parameters:
        ----------
        mu : Non-negative float. The regularisation constant for the smoothing
                to use from now on.

        Returns:
        -------
        old_mu : Non-negative float. The old regularisation constant for the
                smoothing that was overwritten and is no longer used.
        """
        return self.gl.set_mu(mu)

    def f(self, beta):
        """Function value.
        """
        return self.rr.f(beta) \
             + self.l1.f(beta) \
             + self.gl.f(beta)

    def fmu(self, beta, mu=None):
        """Function value.
        """
        return self.rr.f(beta) \
             + self.l1.f(beta) \
             + self.gl.fmu(beta, mu)

    def phi(self, alpha, beta):
        """ Function value with known alpha.
        """
        return self.rr.f(beta) \
             + self.l1.f(beta) \
             + self.gl.phi(alpha, beta)

    def grad(self, beta):
        """Gradient of the differentiable part of the function.

        From the interface "Gradient".
        """
        return self.rr.grad(beta) \
             + self.gl.grad(beta)

    def L(self):
        """Lipschitz constant of the gradient.

        From the interface "LipschitzContinuousGradient".
        """
        return self.rr.L() \
             + self.gl.L()

    def prox(self, beta, factor=1.0):
        """The proximal operator of the non-differentiable part of the
        function.

        From the interface "ProximalOperator".
        """
        return self.l1.prox(beta, factor)

    def estimate_mu(self, beta):
        """Computes a "good" value of \mu with respect to the given \beta.

        From the interface "NesterovFunction".
        """
        return self.gl.estimate_mu(beta)

    def M(self):
        """The maximum value of the regularisation of the dual variable. We
        have

            M = max_{\alpha \in K} 0.5*|\alpha|²_2.

        From the interface "NesterovFunction".
        """
        return self.gl.M()

    def mu_opt(self, eps):
        """The optimal value of \mu given \epsilon.

        From the interface "Continuation".
        """
        gM = self.gl.l * self.gl.M()

        # Mu is set to 1.0, because it is in fact not here "anymore". It is
        # factored out in this solution.
        old_mu = self.gl.set_mu(1.0)
        gA2 = self.gl.L()  # Gamma is in here!
        self.gl.set_mu(old_mu)

        Lg = self.rr.L()

        return (-gM * gA2 + np.sqrt((gM * gA2) ** 2.0
             + gM * Lg * gA2 * eps)) \
             / (gM * Lg)

    def eps_opt(self, mu):
        """The optimal value of \epsilon given \mu.

        From the interface "Continuation".
        """
        gM = self.gl.l * self.gl.M()

        # Mu is set to 1.0, because it is in fact not here "anymore". It is
        # factored out in this solution.
        old_mu = self.gl.set_mu(1.0)
        gA2 = self.gl.L()  # Gamma is in here!
        self.gl.set_mu(old_mu)

        Lg = self.rr.L()

        return (2.0 * gM * gA2 * mu
             + gM * Lg * mu ** 2.0) \
             / gA2

    def eps_max(self, mu):
        """The maximum value of \epsilon.

        From the interface "Continuation".
        """
        gM = self.gl.l * self.gl.M()

        return mu * gM

    def betahat(self, alphak, betak):
        """ Returns the beta that minimises the dual function. Used when we
        compute the gap.

        From the interface "DualFunction".
        """
        if self._Xty is None:
            self._Xty = np.dot(self.X.T, self.y)

        Ata_tv = self.gl.l * self.gl.Aa(alphak)
        Ata_l1 = self.l1.l * SmoothedL1.project([betak / consts.TOLERANCE])[0]
        v = (self._Xty - Ata_tv - Ata_l1)

        shape = self.X.shape

        if shape[0] > shape[1]:  # If n > p

            # Ridge solution
            if self._invXXkI is None:
                XtXkI = np.dot(self.X.T, self.X)
                index = np.arange(min(XtXkI.shape))
                XtXkI[index, index] += self.rr.k
                self._invXXkI = np.linalg.inv(XtXkI)

            beta_hat = np.dot(self._invXXkI, v)

        else:  # If p > n
            # Ridge solution using the Woodbury matrix identity:
            if self._XtinvXXtkI is None:
                XXtkI = np.dot(self.X, self.X.T)
                index = np.arange(min(XXtkI.shape))
                XXtkI[index, index] += self.rr.k
                invXXtkI = np.linalg.inv(XXtkI)
                self._XtinvXXtkI = np.dot(self.X.T, invXXtkI)

            beta_hat = (v - np.dot(self._XtinvXXtkI, np.dot(self.X, v))) \
                       / self.rr.k

        return beta_hat

    def gap(self, beta, beta_hat=None):
        """Compute the duality gap.

        From the interface "DualFunction".
        """
        alpha = self.gl.alpha(beta)

        P = self.rr.f(beta) \
          + self.l1.f(beta) \
          + self.gl.phi(alpha, beta)

        beta_hat = self.betahat(alpha, beta)

        D = self.rr.f(beta_hat) \
          + self.l1.f(beta_hat) \
          + self.gl.phi(alpha, beta_hat)

        return P - D

    def A(self):
        """Linear operator of the Nesterov function.

        From the interface "NesterovFunction".
        """
        return self.gl.A()

    def Aa(self, alpha):
        """Computes A^\T\alpha.

        From the interface "NesterovFunction".
        """
        return self.gl.Aa()

    def project(self, a):
        """ Projection onto the compact space of the Nesterov function.

        From the interface "NesterovFunction".
        """
        return self.gl.project(a)


class RR_SmoothedL1TV(interfaces.CompositeFunction,
                      interfaces.LipschitzContinuousGradient,
                      nesterov_interfaces.NesterovFunction,
                      interfaces.GradientMap,
                      interfaces.DualFunction,
                      interfaces.StronglyConvex):
    """
    Parameters
    ----------
    X : Numpy array. The X matrix for the ridge regression.

    y : Numpy array. The y vector for the ridge regression.

    k : Non-negative float. The Lagrange multiplier, or regularisation
            constant, for the ridge penalty.

    l : Non-negative float. The Lagrange multiplier, or regularisation
            constant, for the L1 penalty.

    g : Non-negative float. The Lagrange multiplier, or regularisation
            constant, of the TV function.

    Atv : Numpy array (usually sparse). The linear operator for the Nesterov
            formulation of the smoothed TV function. May not be None!

    Al1 : Numpy array (usually sparse). The linear operator for the Nesterov
            formulation of the smoothed L1 function. May not be None!

    mu : Non-negative float. The regularisation constant for the smoothing of
            the TV function.

    penalty_start : Non-negative integer. The number of columns, variables
            etc., to except from penalisation. Equivalently, the first index
            to be penalised. Default is 0, all columns are included.
    """
    def __init__(self, X, y, k, l, g, Atv=None, Al1=None, mu=0.0,
                 penalty_start=0):

        if k <= consts.TOLERANCE:
            raise ValueError("The L2 regularisation constant must be " + \
                             "non-zero.")

        self.X = X
        self.y = y

        self.g = RidgeRegression(X, y, k)
        self.h = L1TV(l, g, Atv=Atv, Al1=Al1, mu=mu,
                      penalty_start=penalty_start)

        self.penalty_start = int(penalty_start)

        self.mu = float(mu)

        self.reset()

    def reset(self):

        self.g.reset()
        self.h.reset()

        self._Xy = None
        self._XtinvXXtkI = None

    def set_params(self, **kwargs):

        # TODO: This is not good. Solve this better!
        mu = kwargs.pop("mu", self.get_mu())
        self.set_mu(mu)

        super(RR_SmoothedL1TV, self).set_params(**kwargs)

    def get_mu(self):
        """Returns the regularisation constant for the smoothing.

        From the interface "NesterovFunction".
        """
        return self.h.get_mu()

    def set_mu(self, mu):
        """Sets the regularisation constant for the smoothing.

        From the interface "NesterovFunction".

        Parameters:
        ----------
        mu : Non-negative float. The regularisation constant for the smoothing
                to use from now on.

        Returns:
        -------
        old_mu : Non-negative float. The old regularisation constant for the
                smoothing that was overwritten and is no longer used.
        """
        return self.h.set_mu(mu)

    def f(self, beta):
        """ Function value.
        """
        return self.g.f(beta) \
             + self.h.f(beta)

    def phi(self, alpha, beta):
        """ Function value.
        """
        return self.g.f(beta) \
             + self.h.phi(alpha, beta)

    def L(self):
        """Lipschitz constant of the gradient.

        From the interface "LipschitzContinuousGradient".
        """
#        b = self.g.lambda_min()
        b = self.parameter()
        # TODO: Use max_iter here!!
        a = self.h.lambda_max()  # max_iter=max_iter)

        return a / b

    def parameter(self):
        """Returns the strongly convex parameter for the function.

        From the interface "StronglyConvex".
        """
        return self.g.parameter()

    def V(self, u, beta, L):
        """The gradient map associated to the function.

        From the interface "GradientMap".
        """
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        if L < consts.TOLERANCE:
            L = consts.TOLERANCE

        A = self.h.A()
        a = [0] * len(A)
        a[0] = (1.0 / L) * A[0].dot(beta_)
        a[1] = (1.0 / L) * A[1].dot(beta_)
        a[2] = (1.0 / L) * A[2].dot(beta_)
        a[3] = (1.0 / L) * A[3].dot(beta_)

        u_new = [0] * len(u)
        for i in xrange(len(u)):
            u_new[i] = u[i] + a[i]

        return self.h.project(u_new)

    def betahat(self, alpha, beta=None):
        """ Returns the beta that minimises the dual function.

        From the interface "DualFunction".
        """
        # TODO: Kernelise this function! See how I did in RR_L1_TV._beta_hat.

        A = self.h.A()
        grad = A[0].T.dot(alpha[0])
        grad += A[1].T.dot(alpha[1])
        grad += A[2].T.dot(alpha[2])
        grad += A[3].T.dot(alpha[3])

        if self.penalty_start > 0:
            grad = np.vstack((np.zeros((self.penalty_start, 1)), grad))

#        XXkI = np.dot(X.T, X) + self.g.k * np.eye(X.shape[1])

        if self._Xy is None:
            self._Xy = np.dot(self.X.T, self.y)

        Xty_grad = (self._Xy - grad) / self.g.k

#        t = time()
#        XXkI = np.dot(X.T, X)
#        index = np.arange(min(XXkI.shape))
#        XXkI[index, index] += self.g.k
#        invXXkI = np.linalg.inv(XXkI)
#        print "t:", time() - t
#        beta = np.dot(invXXkI, Xty_grad)

        if self._XtinvXXtkI is None:
            XXtkI = np.dot(self.X, self.X.T)
            index = np.arange(min(XXtkI.shape))
            XXtkI[index, index] += self.g.k
            invXXtkI = np.linalg.inv(XXtkI)
            self._XtinvXXtkI = np.dot(self.X.T, invXXtkI)

        beta = (Xty_grad - np.dot(self._XtinvXXtkI, np.dot(self.X, Xty_grad)))

        return beta

    def gap(self, beta, beta_hat):
        """Compute the duality gap.

        From the interface "DualFunction".
        """
        # TODO: Add this function or refactor API!
        raise NotImplementedError("We cannot currently do this!")

    def estimate_mu(self, beta):
        """Computes a "good" value of \mu with respect to the given \beta.

        From the interface "NesterovFunction".
        """
        raise NotImplementedError("We do not use this here!")

    def M(self):
        """ The maximum value of the regularisation of the dual variable. We
        have

            M = max_{\alpha \in K} 0.5*|\alpha|²_2.

        From the interface "NesterovFunction".
        """
        return self.h.M()

    def project(self, a):
        """ Projection onto the compact space of the Nesterov function.

        From the interface "NesterovFunction".
        """
        return self.h.project(a)