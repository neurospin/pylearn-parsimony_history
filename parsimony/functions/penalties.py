# -*- coding: utf-8 -*-
"""
The :mod:`parsimony.functions.penalties` module contains the penalties used to
constrain the loss functions. These represent mathematical functions and
should thus have properties used by the corresponding algorithms. These
properties are defined in :mod:`parsimony.functions.interfaces`.

Penalties should be stateless. Penalties may be shared and copied and should
therefore not hold anything that cannot be recomputed the next time it is
called.

Created on Mon Apr 22 10:54:29 2013

@author:  Tommy Löfstedt, Vincent Guillemot, Edouard Duchesnay and
          Fouad Hadj-Selem
@email:   lofstedt.tommy@gmail.com, edouard.duchesnay@cea.fr
@license: BSD 3-clause.
"""
import numpy as np

from . import interfaces
import parsimony.utils.maths as maths

__all__ = ["ZeroFunction", "L1", "L2",
           "QuadraticConstraint", "RGCCAConstraint",
           "SufficientDescentCondition"]


class ZeroFunction(interfaces.AtomicFunction,
                   interfaces.Gradient,
                   interfaces.Penalty,
                   interfaces.Constraint,
                   interfaces.ProximalOperator,
                   interfaces.ProjectionOperator):

    def __init__(self, l=1.0, c=0.0, penalty_start=0):

        self.l = float(l)
        self.c = float(c)
        self.penalty_start = int(penalty_start)

        self.reset()

    def reset(self):

        self._zero = None

    def f(self, x):
        """Function value.
        """
        return 0.0

    def grad(self, x):
        """Gradient of the function.

        From the interface "Gradient".
        """
        if self._zero is None:
            self._zero = np.zeros(x.shape)

        return self._zero

    def prox(self, x, factor=1.0):
        """The corresponding proximal operator.

        From the interface "ProximalOperator".
        """
        return x

    def proj(self, x):
        """The corresponding projection operator.

        From the interface "ProjectionOperator".
        """
        return x

    def feasible(self, x):
        """Feasibility of the constraint.

        From the interface "Constraint".
        """
        # When c is non-negative, the function is always feasible.
        return self.c >= 0.0


class L1(interfaces.AtomicFunction,
         interfaces.Penalty,
         interfaces.Constraint,
         interfaces.ProximalOperator,
         interfaces.ProjectionOperator):
    """The proximal operator of the L1 function with a penalty formulation

        f(\beta) = l * (||\beta||_1 - c),

    where ||\beta||_1 is the L1 loss function. The constrained version has the
    form

        ||\beta||_1 <= c.

    Parameters
    ----------
    l : Non-negative float. The Lagrange multiplier, or regularisation
            constant, of the function.

    c : Float. The limit of the constraint. The function is feasible if
            ||\beta||_1 <= c. The default value is c=0, i.e. the default is a
            regularisation formulation.

    penalty_start : Non-negative integer. The number of columns, variables
            etc., to except from penalisation. Equivalently, the first index
            to be penalised. Default is 0, all columns are included.
    """
    def __init__(self, l=1.0, c=0.0, penalty_start=0):

        self.l = float(l)
        self.c = float(c)
        self.penalty_start = int(penalty_start)

    def f(self, beta):
        """Function value.
        """
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta
        return self.l * (maths.norm1(beta_) - self.c)

    def prox(self, beta, factor=1.0):
        """The corresponding proximal operator.

        From the interface "ProximalOperator".
        """
        l = self.l * factor
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta
        prox = (np.abs(beta_) > l) * (beta_ - l * np.sign(beta_ - l))

        prox = np.vstack((beta[:self.penalty_start, :], prox))

        return prox

    def proj(self, beta):
        """The corresponding projection operator.

        From the interface "ProjectionOperator".
        """
        if self.feasible(beta):
            return beta

        from algorithms import Bisection
        bisection = Bisection(force_negative=True, eps=1e-8)

        class F(interfaces.Function):
            def __init__(self, beta, c):
                self.beta = beta
                self.c = c

            def f(self, l):
                beta = (np.abs(self.beta) > l) \
                    * (self.beta - l * np.sign(self.beta - l))

                return maths.norm1(beta) - self.c

        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        func = F(beta_, self.c)
        l = bisection(func, [0.0, np.max(np.abs(beta_))])

        return (np.abs(beta_) > l) * (beta_ - l * np.sign(beta_ - l))

    def feasible(self, beta):
        """Feasibility of the constraint.

        From the interface "Constraint".
        """
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        return maths.norm1(beta_) <= self.c


class L2(interfaces.AtomicFunction,
         interfaces.Gradient,
         interfaces.Penalty,
         interfaces.Constraint,
         interfaces.ProximalOperator,
         interfaces.ProjectionOperator):
    """The proximal operator of the L2 function with a penalty formulation

        f(\beta) = l * (||\beta||²_2 - c),

    where ||\beta||²_2 is the squared L2 loss function. The constrained
    version has the form

        ||\beta||²_2 <= c.

    Parameters
    ----------
    l : Non-negative float. The Lagrange multiplier, or regularisation
            constant, of the function.

    c : Float. The limit of the constraint. The function is feasible if
            ||\beta||²_2 <= c. The default value is c=0, i.e. the default is a
            regularisation formulation.

    penalty_start : Non-negative integer. The number of columns, variables
            etc., to except from penalisation. Equivalently, the first index
            to be penalised. Default is 0, all columns are included.

    Example
    -------
    >>> import numpy as np
    >>> from parsimony.functions.penalties import L2

    >>> np.random.seed(42)
    >>> beta = np.random.rand(100,1)
    >>> l2 = L2(l=3.14159, c=2.71828)
    >>> np.linalg.norm(l2.grad(beta) - l2.approx_grad(beta, eps=1e-4))
    5.8179830878866391e-10

    >>> l2 = L2(l=3.14159, c=2.71828, penalty_start=5)
    >>> np.linalg.norm(l2.grad(beta) - l2.approx_grad(beta, eps=1e-4))
    5.0187970725495645e-10
    """
    def __init__(self, l=1.0, c=0.0, penalty_start=0):

        self.l = float(l)
        self.c = float(c)
        self.penalty_start = int(penalty_start)

    def f(self, beta):
        """Function value.

        From the interface "Function".
        """
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        return self.l * (np.dot(beta_.T, beta_)[0, 0] - self.c)

    def grad(self, beta):
        """Gradient of the function.

        From the interface "Gradient".
        """
#        if self.unbiased:
#            n = self.X.shape[0] - 1.0
#        else:
#            n = self.X.shape[0]

        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        grad = np.vstack((np.zeros((self.penalty_start, 1)),
                          (2.0 * self.l) * beta_))

#        approx_grad = utils.approx_grad(self.f, beta, eps=1e-4)
#        print maths.norm(grad - approx_grad)

        return grad

    def prox(self, beta, factor=1.0):
        """The corresponding proximal operator.

        From the interface "ProximalOperator".
        """
        l = self.l * factor
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        prox = np.vstack((beta[:self.penalty_start, :],
                          beta_ / (1.0 + 2.0 * l)))

        return prox

    def proj(self, beta):
        """The corresponding projection operator.

        From the interface "ProjectionOperator".
        """
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        sqnorm = np.dot(beta_.T, beta_)[0, 0]

        if sqnorm <= self.c:
            return beta

        proj = np.vstack((beta[:self.penalty_start, :],
                          beta_ * np.sqrt(self.c / sqnorm)))

        return proj

    def feasible(self, beta):
        """Feasibility of the constraint.

        From the interface "Constraint".
        """
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        sqnorm = np.dot(beta_.T, beta_)[0, 0]

        return sqnorm <= self.c


class QuadraticConstraint(interfaces.AtomicFunction,
                          interfaces.Gradient,
                          interfaces.Penalty,
                          interfaces.Constraint):
    """The proximal operator of the quadratic function

        f(x) = l * (x'Mx - c),

    or

        f(x) = l * (x'M'Nx - c),

    where M or M'N is a given symmatric positive-definite matrix. The
    constrained version has the form

        x'Mx <= c,

    or

        x'M'Nx <= c

    if two matrices are given.

    Parameters
    ----------
    l : Non-negative float. The Lagrange multiplier, or regularisation
            constant, of the function.

    c : Float. The limit of the constraint. The function is feasible if
            x'Mx <= c. The default value is c=0, i.e. the default is a
            regularisation formulation.

    M : Numpy array. The given positive definite matrix. It is assumed that
            the first penalty_start columns must be excluded.

    N : Numpy array. The second matrix if the factors of the positive-definite
            matrix are given. It is assumed that the first penalty_start
            columns must be excluded.

    penalty_start : Non-negative integer. The number of columns, variables
            etc., to be exempt from penalisation. Equivalently, the first index
            to be penalised. Default is 0, all columns are included.
    """
    def __init__(self, l=1.0, c=0.0, M=None, N=None, penalty_start=0):

        self.l = float(l)
        self.c = float(c)
        if self.penalty_start > 0:
            self.M = M[:, self.penalty_start:]  # NOTE! We slice M here!
            self.N = N[:, self.penalty_start:]  # NOTE! We slice N here!
        else:
            self.M = M
            self.N = N
        self.penalty_start = penalty_start

    def f(self, beta):
        """Function value.
        """
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        if self.N is None:
            val = self.l * (np.dot(beta_.T, np.dot(self.M, beta_)) - self.c)
        else:
            val = self.l * (np.dot(beta_.T, np.dot(self.M.T,
                                                   np.dot(self.N, beta_))) \
                    - self.c)

        return val

    def grad(self, beta):
        """Gradient of the function.

        From the interface "Gradient".
        """
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        if self.N is None:
            grad = (2.0 * self.l) * np.dot(self.M, beta_)
        else:
            grad = (2.0 * self.l) * np.dot(self.M.T, np.dot(self.N, beta_))

        grad = np.vstack(np.zeros((self.penalty_start, 1)), grad)

        return grad

    def feasible(self, beta):
        """Feasibility of the constraint.

        From the interface "Constraint".
        """
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        if self.N is None:
            bMb = np.dot(beta_.T, np.dot(self.M, beta_))
        else:
            bMb = np.dot(beta_.T, np.dot(self.M.T, np.dot(self.N, beta_)))

        return bMb <= self.c


class RGCCAConstraint(QuadraticConstraint,
                      interfaces.ProjectionOperator):
    """The proximal operator of the quadratic function

        f(x) = l * (x'(\tau * I + ((1 - \tau) / n) * X'X)x - c),

    where \tau is a given regularisation constant. The constrained version has
    the form

        x'(\tau * I + ((1 - \tau) / n) * X'X)x <= c.

    Parameters
    ----------
    l : Non-negative float. The Lagrange multiplier, or regularisation
            constant, of the function.

    c : Float. The limit of the constraint. The function is feasible if
            x'(\tau * I + ((1 - \tau) / n) * X'X)x <= c. The default value is
            c=0, i.e. the default is a regularisation formulation.

    tau : Non-negative float. The regularisation constant.

    unbiased : Boolean. Whether the sample variance should be unbiased or not.
            Default is unbiased.

    penalty_start : Non-negative integer. The number of columns, variables
            etc., to be exepmt from penalisation. Equivalently, the first index
            to be penalised. Default is 0, all columns are included.
    """
    def __init__(self, l=1.0, c=0.0, tau=1.0, X=None, unbiased=True,
                 penalty_start=0):

        self.l = float(l)
        self.c = float(c)
        self.tau = max(0.0, min(float(tau), 1.0))
        if penalty_start > 0:
            self.X = X[:, penalty_start:]  # NOTE! We slice X here!
        else:
            self.X = X
        self.unbiased = unbiased
        self.penalty_start = penalty_start

        self.reset()

    def reset(self):

        self._VU = None
        self._Vt = None
        self._UV = None

#        self._Ip = None
        self._M = None

        self._D = None
        self._V = None

    def f(self, beta):
        """Function value.
        """
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        xtMx = self._compute_value(beta_)

        return self.l * (xtMx - self.c)

    def grad(self, beta):
        """Gradient of the function.

        From the interface "Gradient".
        """
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        if self.unbiased:
            n = self.X.shape[0] - 1.0
        else:
            n = self.X.shape[0]

        if self.tau < 1.0:
            XtXbeta = np.dot(self.X.T, np.dot(self.X, beta_))
            grad = (self.tau * 2.0) * beta_ \
                 + ((1.0 - self.tau) * 2.0 / float(n)) * XtXbeta
        else:
            grad = (self.tau * 2.0) * beta_

        grad = np.vstack(np.zeros((self.penalty_start, 1)), grad)

#        approx_grad = utils.approx_grad(self.f, beta, eps=1e-4)
#        print maths.norm(grad - approx_grad)

        return grad

    def feasible(self, beta):
        """Feasibility of the constraint.

        From the interface "Constraint".
        """
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        xtMx = self._compute_value(beta_)

        return xtMx <= self.c

    def proj(self, beta):
        """The projection operator corresponding to the function.

        From the interface "ProjectionOperator".
        """
        if self.penalty_start > 0:
            beta_ = beta[self.penalty_start:, :]
        else:
            beta_ = beta

        xtMx = self._compute_value(beta_)
        if xtMx <= self.c:
            return beta

        n, p = self.X.shape
        if p > n:
#            In = np.eye(n)                    # n-by-n
            U = self.X.T                      # p-by-n
#            V = self.X                        # n-by-p
            Vx = np.dot(self.X, beta_)        # n-by-1
            if self._VU is None:
                self._VU = np.dot(self.X, U)  # XX', n-by-n

#                self._V, self._D, self._Vt = np.linalg.svd(self._VU)
                self._D, self._V = np.linalg.eig(self._VU)
#                self._Vt = np.linalg.pinv(self._V)
                self._Vt = self._V.T
                self._UV = np.dot(U, self._V)

            if self.unbiased:
                n_ = float(n - 1.0)
            else:
                n_ = float(n)

            def prox(x, l):
                k = 0.5 * l * self.tau + 1.0
                m = 0.5 * l * ((1.0 - self.tau) / n_)

#                invIVU = np.linalg.inv((k / m) * In + self._VU)
#                invIVU = np.dot(self._V * np.reciprocal(self._D + (k / m)), self._Vt)
                VtinvIVU = (np.reciprocal(self._D + (k / m)) * self._Vt.T).T

#                invIMx = (x - np.dot(U, np.dot(invIVU, Vx))) / k
                invIMx = (x - np.dot(self._UV, np.dot(VtinvIVU, Vx))) / k

                return invIMx

            from parsimony.algorithms import Bisection
            bisection = Bisection(force_negative=True,
                                  parameter_positive=True,
                                  parameter_negative=False,
                                  parameter_zero=False,
                                  eps=1e-3)

            class F(interfaces.Function):
                def __init__(self, x, c, val):
                    self.x = x
                    self.c = c
                    self.val = val
                    self.y = None

                def f(self, l):

                    # We avoid one evaluation of prox by saving it here.
                    self.y = prox(self.x, l)

                    return self.val(self.y) - self.c

            func = F(beta_, self.c, self._compute_value)

            # TODO: Tweak these magic numbers on real data. Or even better,
            # find theoretical bounds. Convergence is faster if these bounds
            # are close to accurate when we start the bisection algorithm.
            if p >= 600000:
                low = (p / 100.0) - np.log10(n) * 5.0
                high = (p / 80.0) - np.log10(n) * 5.0
            elif p >= 500000:
                low = p / 85.71
                high = (p / 76.9) - np.log10(n) * 5.0
            elif p >= 400000:
                low = p / 78.125
                high = (p / 68.97) - np.log10(n) * 5.0
            elif p >= 300000:
                low = p / 70.17
                high = (p / 59.4) - np.log10(n) * 5.0
            elif p >= 200000:
                low = p / 61.22
                high = (p / 48.78) - np.log10(n) * 5.0
            elif p >= 150000:
                low = p / 50.0
                high = (p / 41.66) - np.log10(n) * 5.0  # ^^
            elif p >= 100000:
                low = p / 42.86
                high = (p / 34.5) - np.log10(n) * 6.0  # !
            elif p >= 75000:
                low = p / 35.71
                high = (p / 29.9) - np.log10(n) * 6.0  # !
            elif p >= 50000:
                low = p / 31.25
                high = (p / 23.81) - np.log10(n) * 6.0  # !
            elif p >= 25000:
                low = p / 25.0
                high = (p / 16.67) - np.log10(n) * 7.0  # !
            elif p >= 10000:
                low = p / 17.86
                high = (p / 10.87) - np.log10(n) * 7.0  # !
            elif p >= 5000:
                low = p / 11.63
                high = (p / 7.69) - np.log10(n) * 7.0  # !
            elif p >= 1000:
                low = p / 8.62
                high = (p / 3.45) - np.log10(n) * 8.0  # !
            else:
                low = p / 4.75
                high = p / 2.25

            l = bisection(func, [low, high])

            y = func.y

        else:  # The case when: p <= n

#            if self._Ip is None:
#                self._Ip = np.eye(p)  # p-by-p

            if self._M is None:
                XtX = np.dot(self.X.T, self.X)

                if self.unbiased:
                    n_ = float(n - 1.0)
                else:
                    n_ = float(n)

                self._M = self.tau * self._Ip + \
                          ((1.0 - self.tau) / n_) * XtX

                self._D, self._V = np.linalg.eig(self._M)

            def prox2(x, l):

#                y = np.dot(np.linalg.inv(self._Ip + (0.5 * l) * self._M), x)

#                invIM = np.linalg.inv(self._Ip + (0.5 * l) * self._M)
#                print maths.norm(np.linalg.inv(self._Ip + (0.5 * l) * self._M) - \
#                                  np.dot(self._V * np.reciprocal(0.5 * l * self._D + 1.0),
#                                         self._V.T))
#                print maths.norm(self._M - np.dot(self._V, np.dot(np.diag(self._D), self._V.T)))
#                print maths.norm((self._Ip + (0.5 * l) * self._M) - \
#                                  np.dot(self._V,
#                                         np.dot(np.diag(self._D + 1.0 + 0.5 * l),
#                                                self._V.T)))

#                invIM = np.linalg.inv(self._Ip + (0.5 * l) * self._M)
                invIM = np.dot(self._V * \
                                   np.reciprocal(0.5 * l * self._D + 1.0),
                               self._V.T)
                y = np.dot(invIM, x)

#                print "err:", maths.norm(y - yd)

                return y

            from parsimony.algorithms import Bisection
            bisection = Bisection(force_negative=True,
                                  parameter_positive=True,
                                  parameter_negative=False,
                                  parameter_zero=False,
                                  eps=1e-6,
                                  max_iter=100)

            class F(interfaces.Function):
                def __init__(self, x, c, val):
                    self.x = x
                    self.c = c
                    self.val = val
                    self.y = None

                def f(self, l):

                    # We avoid one evaluation of prox by saving it here.
                    self.y = prox2(self.x, l)

                    return self.val(self.y) - self.c

            func = F(beta_, self.c, self._compute_value)

            # TODO: Tweak these magic numbers on real data. Or even better,
            # find theoretical bounds. Convergence is faster if these bounds
            # are close to accurate when we start the bisection algorithm.
            if p >= 950:
                low = p / 5.25
                high = (p / 4.50) - np.log10(n)  # !
            elif p >= 850:
                low = p / 4.65
                high = (p / 4.25) - np.log10(n)  # !
            elif p >= 750:
                low = p / 4.45
                high = (p / 4.00) - np.log10(n)  # !
            elif p >= 650:
                low = p / 4.28
                high = (p / 3.70) - np.log10(n)  # !
            elif p >= 550:
                low = p / 4.10
                high = (p / 3.40) - np.log10(n)  # !
            elif p >= 450:
                low = p / 3.85
                high = (p / 3.05) - np.log10(n)  # !
            elif p >= 350:
                low = p / 3.59
                high = (p / 2.82) - np.log10(n)  # !
            elif p >= 250:
                low = p / 3.16
                high = (p / 2.42) - np.log10(n)  # !
            elif p >= 150:
                low = p / 2.7
                high = (p / 1.85) - np.log10(n)  # !
            elif p >= 50:
                low = p / 2.23
                high = (p / 1.23) - np.log10(n)  # !
            else:
                low = p / 1.1
                high = p / 0.8  # !

            l = bisection(func, [low, high])

            y = func.y

#        print low, ", ", high
#        print l

#        _Ip = np.eye(p)  # p-by-p
#
#        XtX = np.dot(self.X.T, self.X)
#        _M = self.tau * _Ip + ((1.0 - self.tau) / float(n - 1)) * XtX
#
#        l = max(0.0, xtMx - self.c)
#        y_ = np.dot(np.linalg.inv(_Ip + (0.5 * l) * _M), beta_)
#
#        print self._compute_value(y)
#        print self._compute_value(y_)

#        if maths.norm(beta_ - (beta_ / np.sqrt(xtMx))) < maths.norm(beta_ - y):
#            print maths.norm(beta_ - (beta_ / np.sqrt(xtMx)))
#            print maths.norm(beta_ - y)

        return y

    def _compute_value(self, beta):
        """Helper function to compute the function value.

        Note that beta must already be sliced!
        """

        if self.unbiased:
            n = self.X.shape[0] - 1.0
        else:
            n = self.X.shape[0]

        Xbeta = np.dot(self.X, beta)
        val = self.tau * np.dot(beta.T, beta) \
            + ((1.0 - self.tau) / float(n)) * np.dot(Xbeta.T, Xbeta)

        return val[0, 0]


class SufficientDescentCondition(interfaces.Function,
                                 interfaces.Constraint):

    def __init__(self, function, p, c):
        """The sufficient condition

            f(x + a * p) <= f(x) + c * a * grad(f(x))'p

        for descent. This condition is sometimes called the Armijo condition.

        Parameters
        ----------
        c : Float, 0 < c < 1. A constant for the condition. Should be small.
        """
        self.function = function
        self.p = p
        self.c = c

    def f(self, x, a):

        return self.function.f(x + a * self.p)

    """Feasibility of the constraint at point x with step a.

    From the interface "Constraint".
    """
    def feasible(self, xa):

        x = xa[0]
        a = xa[1]

        f_x_ap = self.function.f(x + a * self.p)
        f_x = self.function.f(x)
        grad_p = np.dot(self.function.grad(x).T, self.p)[0, 0]
#        print "f_x_ap = %.10f, f_x = %.10f, grad_p = %.10f, feas = %.10f" % (f_x_ap, f_x, grad_p, f_x + self.c * a * grad_p)
#        if grad_p >= 0.0:
#            pass
        feasible = f_x_ap <= f_x + self.c * a * grad_p

        return feasible


#class WolfeCondition(Function, Constraint):
#
#    def __init__(self, function, p, c1=1e-4, c2=0.9):
#        """
#        Parameters:
#        ----------
#        c1 : Float. 0 < c1 < c2 < 1. A constant for the condition. Should be
#                small.
#        c2 : Float. 0 < c1 < c2 < 1. A constant for the condition. Depends on
#                the minimisation algorithms. For Newton or quasi-Newton
#                descent directions, 0.9 is a good choice. 0.1 is appropriate
#                for nonlinear conjugate gradient.
#        """
#        self.function = function
#        self.p = p
#        self.c1 = c1
#        self.c2 = c2
#
#    def f(self, x, a):
#
#        return self.function.f(x + a * self.p)
#
#    """Feasibility of the constraint at point x.
#
#    From the interface "Constraint".
#    """
#    def feasible(self, x, a):
#
#        grad_p = np.dot(self.function.grad(x).T, self.p)[0, 0]
#        cond1 = self.function.f(x + a * self.p) \
#            <= self.function.f(x) + self.c1 * a * grad_p
#        cond2 = np.dot(self.function.grad(x + a * self.p).T, self.p)[0, 0] \
#            >= self.c2 * grad_p
#
#        return cond1 and cond2
#
#
#class StrongWolfeCondition(Function, Constraint):
#
#    def __init__(self, function, p, c1=1e-4, c2=0.9):
#        """
#        Parameters:
#        ----------
#        c1 : Float. 0 < c1 < c2 < 1. A constant for the condition. Should be
#                small.
#        c2 : Float. 0 < c1 < c2 < 1. A constant for the condition. Depends on
#                the minimisation algorithms. For Newton or quasi-Newton
#                descent directions, 0.9 is a good choice. 0.1 is appropriate
#                for nonlinear conjugate gradient.
#        """
#        self.function = function
#        self.p = p
#        self.c1 = c1
#        self.c2 = c2
#
#    def f(self, x, a):
#
#        return self.function.f(x + a * self.p)
#
#    """Feasibility of the constraint at point x.
#
#    From the interface "Constraint".
#    """
#    def feasible(self, x, a):
#
#        grad_p = np.dot(self.function.grad(x).T, self.p)[0, 0]
#        cond1 = self.function.f(x + a * self.p) \
#            <= self.function.f(x) + self.c1 * a * grad_p
#        grad_x_ap = self.function.grad(x + a * self.p)
#        cond2 = abs(np.dot(grad_x_ap.T, self.p)[0, 0]) \
#            <= self.c2 * abs(grad_p)
#
#        return cond1 and cond2