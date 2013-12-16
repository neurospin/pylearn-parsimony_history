# -*- coding: utf-8 -*-
"""
The :mod:`parsimony.algorithms` module includes several algorithms used
throughout the package.

Algorithms may not store states. I.e., if they are classes, do not keep
references to objects with state in the algorithm objects. It should be
possible to copy and share algorithms between estimators, and thus they should
not depend on any state.

There are currently two types of algorithms: implicit and explicit. The
difference is whether they run directly on the data (implicit) or if they have
an actual loss function than is minimised (explicit). Implicit algorithms take
the data as input, and then run on the data. Explicit algorithms take a loss
function and a start vector as input, and then minimise the function value
starting from the point of the start vector.

Created on Fri Feb  8 17:24:11 2013

@author:  Tommy Löfstedt
@email:   tommy.loefstedt@cea.fr
@license: TBD.
"""
import abc
from time import time, clock

import numpy as np

import parsimony.utils.consts as consts
import parsimony.utils.maths as maths
import parsimony.functions as functions

#TODO: This depends on the OS. We should try to be clever here ...
time_func = clock
#time_func = time

__all__ = ['BaseAlgorithm',
           'ImplicitAlgorithm',
           'FastSVD', 'FastSparseSVD',

           'ExplicitAlgorithm',
           'FISTA', 'CONESTA', 'StaticCONESTA', 'DynamicCONESTA',
           'ExcessiveGapMethod']


class BaseAlgorithm(object):

    def check_compatibility(self, function, interfaces):
        """Check if the function considered implements the given interfaces
        """
        for interface in interfaces:
            if not isinstance(function, interface):
                raise ValueError("%s does not implement interface %s" %
                                (str(function), str(interface)))

    def set_params(self, **kwargs):

        for k in kwargs:
            self.__setattr__(k, kwargs[k])


class ImplicitAlgorithm(BaseAlgorithm):
    """Implicit algorithms are algorithms that do not use a loss function, but
    instead minimise or maximise some underlying function implicitly, from the
    data.

    Parameters
    ----------
    X : Regressor
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(X, **kwargs):
        raise NotImplementedError('Abstract method "__call__" must be ' \
                                  'specialised!')


class ExplicitAlgorithm(BaseAlgorithm):
    """Explicit algorithms are algorithms that minimises a given function
    explicitly from properties of the function.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(function, beta, **kwargs):
        """Call this object to obtain the variable that gives the minimum.

        Parameters
        ----------
        function : The function to minimise.

        beta : A start vector.
        """
        raise NotImplementedError('Abstract method "__call__" must be ' \
                                  'specialised!')


class FastSVD(ImplicitAlgorithm):

    def __call__(self, X, max_iter=100, start_vector=None):
        """A kernel SVD implementation.

        Performs SVD of given matrix. This is always faster than np.linalg.svd.
        Particularly, this is a lot faster than np.linalg.svd when M << N or
        M >> N, for an M-by-N matrix.

        Parameters
        ----------
        X : The matrix to decompose.

        max_iter : maximum allowed number of iterations

        start_vector : a start vector

        Returns
        -------
        v : The right singular vector of X that corresponds to the largest
                singular value.

        Example
        -------
        >>> import numpy as np
        >>> from parsimony.algorithms import FastSVD
        >>> np.random.seed(0)
        >>> X = np.random.random((10,10))
        >>> fast_svd = FastSVD()
        >>> fast_svd(X)
        array([[-0.3522974 ],
               [-0.35647707],
               [-0.35190104],
               [-0.34715338],
               [-0.19594198],
               [-0.24103104],
               [-0.25578904],
               [-0.29501092],
               [-0.42311297],
               [-0.27656382]])

        """
        M, N = X.shape
        if M < 80 and N < 80:  # Very arbitrary threshold for my computer ;-)
            _, _, V = np.linalg.svd(X, full_matrices=True)
            v = V[[0], :].T
        elif M < N:
            K = np.dot(X, X.T)
            # TODO: Use module for this!
            t = np.random.rand(X.shape[0], 1)
    #        t = start_vectors.RandomStartVector().get_vector(Xt)
            for it in xrange(max_iter):
                t_ = t
                t = np.dot(K, t_)
                t /= np.sqrt(np.sum(t ** 2.0))

                if np.sqrt(np.sum((t_ - t) ** 2.0)) < consts.TOLERANCE:
                    break

            v = np.dot(X.T, t)
            v /= np.sqrt(np.sum(v ** 2.0))

        else:
            K = np.dot(X.T, X)
            # TODO: Use module for this!
            v = np.random.rand(X.shape[1], 1)
            v /= maths.norm(v)
    #        v = start_vectors.RandomStartVector().get_vector(X)
            for it in xrange(max_iter):
                v_ = v
                v = np.dot(K, v_)
                v /= np.sqrt(np.sum(v ** 2.0))

                if np.sqrt(np.sum((v_ - v) ** 2.0)) < consts.TOLERANCE:
                    break

        return v


class FastSparseSVD(ImplicitAlgorithm):

    def __call__(self, X, max_iter=100, start_vector=None):
        """A kernel SVD implementation for sparse CSR matrices.

        This is usually faster than np.linalg.svd when density < 20% and when
        M << N or N << M (at least one order of magnitude). When M = N >= 10000
        it is faster when the density < 1% and always faster regardless of
        density when M = N < 10000.

        These are ballpark estimates that may differ on your computer.

        Parameters
        ----------
        X : The matrix to decompose

        max_iter : maximum allowed number of iterations

        start_vector : a start vector

        Returns
        -------
        v : The right singular vector.

        Example
        -------
        >>> import numpy as np
        >>> from parsimony.algorithms import FastSparseSVD
        >>> np.random.seed(0)
        >>> X = np.random.random((10,10))
        >>> fast_sparse_svd = FastSparseSVD()
        >>> fast_sparse_svd(X)
        array([[ 0.3522974 ],
               [ 0.35647707],
               [ 0.35190103],
               [ 0.34715338],
               [ 0.19594198],
               [ 0.24103104],
               [ 0.25578904],
               [ 0.29501092],
               [ 0.42311297],
               [ 0.27656382]])


        """
        M, N = X.shape
        if M < N:
            K = X.dot(X.T)
    #        t = X.dot(p)
            # TODO: Use module for this!
            t = np.random.rand(X.shape[0], 1)
            for it in xrange(max_iter):
                t_ = t
                t = K.dot(t_)
                t /= np.sqrt(np.sum(t ** 2.0))

                a = float(np.sqrt(np.sum((t_ - t) ** 2.0)))
                if a < consts.TOLERANCE:
                    break

            v = X.T.dot(t)
            v /= np.sqrt(np.sum(v ** 2.0))

        else:
            K = X.T.dot(X)
            # TODO: Use module for this!
            v = np.random.rand(X.shape[1], 1)
            v /= maths.norm(v)
    #        v = start_vectors.RandomStartVector().get_vector(X)
            for it in xrange(max_iter):
                v_ = v
                v = K.dot(v_)
                v /= np.sqrt(np.sum(v ** 2.0))

                a = float(np.sqrt(np.sum((v_ - v) ** 2.0)))
                if a < consts.TOLERANCE:
                    break

        return v


class FISTA(ExplicitAlgorithm):
    """ The fast iterative shrinkage threshold algorithm.

    Parameters
    ----------
    step : Step for each iteration

    output : Boolean. Get output information

    eps : Float. Tolerance

    max_iter : Maximum allowed number of iterations

    min_iter : Minimum allowed number of iterations

    Example
    -------
    import numpy as np
    import parsimony.estimators as estimators
    import parsimony.algorithms as algorithms
    import parsimony.tv
    from parsimony.functions import OLSL2_L1_TV
    from parsimony.algorithms import fista
    from parsimony.start_vectors import RandomStartVector

    shape = (100, 100, 1)
    num_samples = 500

    num_ft = shape[0] * shape[1] * shape[2]
    X = np.random.random((num_samples, num_ft))
    y = np.random.randint(0, 2, (num_samples, 1))
    random_start_vector = np.random.random((X.shape[1], 1))

    def ratio2coef(alpha, tv_ratio, l1_ratio):
        l2_ratio = 1 - tv_ratio - l1_ratio
        l, k, g = alpha * l1_ratio,  alpha * l2_ratio, alpha * tv_ratio
        return l, k, g

    eps = 0.01
    alpha = 10.

    tv_ratio = .05
    l1_ratio = .9

    l, k, g = ratio2coef(alpha=alpha, tv_ratio=tv_ratio, l1_ratio=l1_ratio)

    Ax, Ay, Az, n_compacts = parsimony.tv.tv_As_from_shape(shape)

    tvl1l2_conesta = estimators.LinearRegressionL1L2TV(k, l, g, [Ax, Ay, Az],
                                        algorithm=algorithms.conesta_static)
    tvl1l2_conesta.fit(X, y)

    tvl1l2_fista = estimators.LinearRegressionL1L2TV(k, l, g, [Ax, Ay, Az],
                                        algorithm=algorithms.fista)
    tvl1l2_fista.fit(X, y)

    residual = np.sum(tvl1l2_fista.beta - tvl1l2_conesta.beta)

    import spams
    spams_X = np.asfortranarray(X)
    spams_Y = np.asfortranarray(y)
    W0 = np.asfortranarray(np.random.random((spams_X.shape[1],
                                             spams_Y.shape[1])))
    spams_X = np.asfortranarray(spams_X - np.tile(np.mean(spams_X, 0),
                                                  (spams_X.shape[0], 1)))
    spams_Y = np.asfortranarray(spams_Y - np.tile(np.mean(spams_Y,0),
                                                         (spams_Y.shape[0],1)))
    param = {'numThreads' : 1,'verbose' : True,
         'lambda1' : 0.05, 'it0' : 10, 'max_it' : 200,
         'L0' : 0.1, 'tol' : 1e-3, 'intercept' : False,
         'pos' : False}
    (W, optim_info) = spams.fistaFlat(spams_Y,
                                      spams_X,
                                      W0,
                                      True,
                                      **param)

#    tvl1l2 = estimators.LinearRegressionL1L2TV(k, l, g, [Ax, Ay, Az],
#                                algorithm=algorithms.conesta_static)
#    tvl1l2.fit(X, y)
#    start_beta_vector = random_start_vector.get_vector([X.shape[1], 1])
#    fista(X, y, olsl2_L1_TV, start_beta_vector)

    """
    INTERFACES = [functions.Gradient,
                  # TODO: We should use a step size here instead of the
                  # Lipschitz constant. All functions don't have L, but will
                  # still run in FISTA with a small enough step size.
                  # Updated: Use GradientStep instead!!
                  functions.LipschitzContinuousGradient,
                  functions.ProximalOperator,
                 ]

    def __init__(self, step=None, output=False,
                 eps=consts.TOLERANCE,
                 max_iter=consts.MAX_ITER, min_iter=1):

        self.step = step
        self.output = output
        self.eps = eps
        self.max_iter = max_iter
        self.min_iter = min_iter

    def __call__(self, function, beta):
        """Call this object to obtain the variable that gives the minimum.

        Parameters
        ----------
        function : The function to minimise.

        beta : A start vector.
        """
        self.check_compatibility(function, self.INTERFACES)

        z = betanew = betaold = beta

        if self.step is None:
            self.step = 1.0 / function.L()

        if self.output:
            t = []
            f = []
        for i in xrange(1, self.max_iter + 1):
            if self.output:
                tm = time_func()

            z = betanew + ((i - 2.0) / (i + 1.0)) * (betanew - betaold)
            betaold = betanew
            betanew = function.prox(z - self.step * function.grad(z),
                                    self.step)

            if self.output:
                t.append(time_func() - tm)
                f.append(function.f(betanew))

            if (1.0 / self.step) * maths.norm(betanew - z) < self.eps \
                    and i >= self.min_iter:
                break

        if self.output:
            output = {"t": t, "f": f}
            return betanew, output
        else:
            return betanew


class CONESTA(ExplicitAlgorithm):
    """COntinuation with NEsterov smoothing in a Soft-Thresholding Algorithm,
    or CONESTA for short.

    Parameters
    ----------
    mu_start :

    mu_min :

    tau :

    dynamic : Boolean. Switch for dynamically or statically decreasing \mu

    continuations : maximum iteration

    """
    INTERFACES = [functions.NesterovFunction,
                  functions.Continuation,
                  functions.LipschitzContinuousGradient,
                  functions.ProximalOperator,
                  functions.Gradient,
                  functions.DualFunction
                 ]

    def __init__(self, mu_start=None, mu_min=consts.TOLERANCE, tau=0.5,
                 dynamic=True, continuations=30,

                 output=False,
                 eps=consts.TOLERANCE,
                 max_iter=consts.MAX_ITER, min_iter=1):

        self.mu_start = mu_start
        self.mu_min = mu_min
        self.tau = tau
        self.dynamic = dynamic
        self.continuations = continuations

        self.output = output
        self.eps = eps
        self.max_iter = max_iter
        self.min_iter = min_iter

        self.FISTA = FISTA(output=self.output,
                           eps=self.eps,
                           max_iter=self.max_iter, min_iter=self.min_iter)

    def __call__(self, function, beta):

        self.check_compatibility(function, self.INTERFACES)

        if self.mu_start is not None:
            mu = [self.mu_start]
        else:
            mu = [0.9 * function.estimate_mu(beta)]

#        old_mu = function.get_mu()
        function.set_mu(self.mu_min)
        tmin = 1.0 / function.L()
        function.set_mu(mu[0])

        max_eps = function.eps_max(mu[0])

#        G = eps0 = min(max_eps, function.eps_opt(mu[0]))
        G = min(max_eps, function.eps_opt(mu[0]))

        if self.output:
            t = []
            f = []
            Gval = []

        i = 0
        while True:
            stop = False

            tnew = 1.0 / function.L()
            eps_plus = min(max_eps, function.eps_opt(mu[-1]))
            self.FISTA.set_params(step=tnew, eps=eps_plus)
            if self.output:
                (beta, info) = self.FISTA(function, beta)
                fval = info["f"]
                tval = info["t"]
            else:
                beta = self.FISTA(function, beta)

            self.mu_min = min(self.mu_min, mu[-1])
            tmin = min(tmin, tnew)
            function.set_mu(self.mu_min)
            # Take one ISTA step to use in the stopping criterion.
            beta_tilde = function.prox(beta - tmin * function.grad(beta),
                                       tmin)
            function.set_mu(mu[-1])

            if (1.0 / tmin) * maths.norm(beta - beta_tilde) < self.eps \
                    or i >= self.continuations:
#                print "%f < %f" % ((1. / tmin) \
#                                * maths.norm(beta - beta_tilde), self.eps)
#                print "%d >= %d" % (i, self.continuations)
                stop = True

            if self.output:
                gap_time = time_func()
            if self.dynamic:
                G_new = function.gap(beta)
                # TODO: Warn if G_new < 0.
                G_new = abs(G_new)  # Just in case ...

                if G_new < G:
                    G = G_new
                else:
                    G = self.tau * G

            else:  # Static

    #            G_new = eps0 * tau ** (i + 1)
                G = self.tau * G

#            print "Gap:", G
            if self.output:
                gap_time = time_func() - gap_time
                Gval.append(G)

                f = f + fval
                tval[-1] += gap_time
                t = t + tval

            if (G <= consts.TOLERANCE and mu[-1] <= consts.TOLERANCE) or stop:
                break

            mu_new = min(mu[-1], function.mu_opt(G))
            self.mu_min = min(self.mu_min, mu_new)
            if self.output:
                mu = mu + [max(self.mu_min, mu_new)] * len(fval)
            else:
                mu.append(max(self.mu_min, mu_new))
            function.set_mu(mu_new)

            i = i + 1

        if self.output:
            info = {"t": t, "f": f, "mu": mu, "gap": Gval}
            return (beta, info)
        else:
            return beta


class StaticCONESTA(CONESTA):
    """COntinuation with NEsterov smoothing in a Soft-Thresholding Algorithm,
    or CONESTA for short, with a statically decreasing \mu.
    """
    def __init__(self, **kwargs):

        kwargs["dynamic"] = False

        super(StaticCONESTA, self).__init__(**kwargs)


class DynamicCONESTA(CONESTA):
    """COntinuation with NEsterov smoothing in a Soft-Thresholding Algorithm,
    or CONESTA for short, with a dynamically decreasing \mu.
    """
    def __init__(self, **kwargs):

        kwargs["dynamic"] = True

        super(DynamicCONESTA, self).__init__(**kwargs)


class ExcessiveGapMethod(ExplicitAlgorithm):
    """Nesterov's excessive gap method for strongly convex functions.

    Parameters
    ----------
    output : Boolean. Get output information

    eps : Float. Tolerance

    max_iter : Maximum allowed number of iterations

    min_iter : Minimum allowed number of iterations

    """
    INTERFACES = [functions.NesterovFunction,
                  functions.LipschitzContinuousGradient,
                  functions.GradientMap,
                  functions.DualFunction
                 ]

    def __init__(self, output=False,
                 eps=consts.TOLERANCE,
                 max_iter=consts.MAX_ITER, min_iter=1):

        self.output = output
        self.eps = eps
        self.max_iter = max_iter
        self.min_iter = min_iter

    def __call__(self, function, beta=None):
        """The excessive gap method for strongly convex functions.

        Parameters
        ----------
        function : The function to minimise. It contains two parts, function.g
                is the strongly convex part and function.h is the smoothed part
                of the function.

        beta : Regression coefficient vector
        """
        A = function.h.A()

        u = [0] * len(A)
        for i in xrange(len(A)):
            u[i] = np.zeros((A[i].shape[0], 1))

        # L = lambda_max(A'A) / (lambda_min(X'X) + k)
        L = function.L()

        mu = [2.0 * L]
        function.h.set_mu(mu)
        beta0 = function.betahat(u)  # u is zero here
        beta = beta0
        alpha = function.V(u, beta, L)  # u is zero here

        t = []
        f = []
        ubound = []

        k = 0

        while True:
            if self.output:
                tm = time_func()

            tau = 2.0 / (float(k) + 3.0)

            function.h.set_mu(mu[k])
            alpha_hat = function.h.alpha(beta)
            for i in xrange(len(alpha_hat)):
                u[i] = (1.0 - tau) * alpha[i] + tau * alpha_hat[i]

            mu.append((1.0 - tau) * mu[k])
            betahat = function.betahat(u)
            beta = (1.0 - tau) * beta + tau * betahat
            alpha = function.V(u, betahat, L)

            ulim = mu[k + 1] * function.h.M()
            if self.output:
                t.append(time_func() - tm)
                mu_old = function.h.get_mu()
                function.h.set_mu(0.0)
                f.append(function.f(beta))
                function.h.set_mu(mu_old)

#                ulim.append(2.0 * function.h.M() * mu[0] / ((float(k) + 1.0) * (float(k) + 2.0)))
                ubound.append(ulim)

            if ulim < self.eps or k >= self.max_iter:
                break

            k = k + 1

        if self.output:
            output = {"t": t, "f": f, "mu": mu, "upper_bound": ubound,
                      "beta_start": beta0}
            return (beta, output)
        else:
            return beta


class Bisection(ExplicitAlgorithm):
    """Finds a root of the function assumed to be on the line between two
    points.

    Assumes a function f(x) such that |f(x)|_2 < -eps if x is too small,
    |f(x)|_2 > eps if x is too large and |f(x)|_2 <= eps if x is just right.

    Parameters
    ----------
    eps : A positive value such that |f(x)|_2 <= eps. Only guaranteed if
            |f(x)|_2 <= eps in less than maxiter iterations.

    max_iter : The maximum number of iterations.

    min_iter : The minimum number of iterations.
    """
    INTERFACES = [functions.Function,
                 ]

    def __init__(self, eps=consts.TOLERANCE,
                 max_iter=50, min_iter=1):

        self.eps = eps
        self.max_iter = max_iter
        self.min_iter = min_iter

    def __call__(self, function, x=None):
        """
        Parameters
        ----------
        function: The function for which a root is found. The function must be
                increasing for increasing x, and decresing for decreasing x.

        x: A vector or tuple with two elements. The first element is the lower
                end of the interval for which |f(x[0])|_2 < -eps. The second
                element is the upper end of the interfal for which
                |f(x[1])|_2 > eps. If x is None, these values are found.
                Finding them may be slow, though, if the function is expensive
                to evaluate.
        """
        if x != None:
            low = min(x)
            high = max(x)
        else:
            low = 0
            high = 1

        # Find start values. If the low and high
        # values are feasible this will just break
        for i in xrange(self.max_iter):
            f_low = function.f(low)
            f_high = function.f(high)

            if maths.sign(f_low) != maths.sign(f_high):
                break
            else:
                low -= abs(low) * 2.0 ** i
                high += abs(high) * 2.0 ** i

        # Use the bisection method to find where |f(x)|_2 <= eps.
        for i in xrange(self.max_iter):
            mid = (low + high) / 2.0
            f_mid = function.f(mid)

            if maths.sign(f_mid) == maths.sign(f_low):
                low = mid
                f_low = f_mid
            else:
                high = mid
                f_high = f_mid

            if np.sqrt(np.sum((high - low) ** 2.0)) <= self.eps:
                break

        return (low + high) / 2.0


class GeneralisedMultiblockISTA(ExplicitAlgorithm):
    """ The iterative shrinkage threshold algorithm in a multiblock setting.
    """
    INTERFACES = [functions.MultiblockFunction,
                  functions.MultiblockGradient,
                  functions.MultiblockProximalOperator,
                  functions.GradientStep,
                 ]

    def __init__(self, step=None, output=False,
                 eps=consts.TOLERANCE,
                 max_iter=consts.MAX_ITER, min_iter=1):

        self.step = step
        self.output = output
        self.eps = eps
        self.max_iter = max_iter
        self.min_iter = min_iter

    def __call__(self, function, w):

        self.check_compatability(function, self.INTERFACES)

        for it in xrange(10):  # TODO: Get number of iterations!
            print "it:", it

            for i in xrange(len(w)):
                print "  i:", i

                for k in xrange(10000):
                    print "    k:", k

                    t = function.step(w, i)
                    w[i] = w[i] - t * function.grad(w, i)
                    w = function.prox(w, i, t)
#                    = w[:i] + [wi] + w[i+1:]

                    print "    f:", function.f(w)

#                w[i] = wi

        return w


if __name__ == "__main__":
    import doctest
    doctest.testmod()