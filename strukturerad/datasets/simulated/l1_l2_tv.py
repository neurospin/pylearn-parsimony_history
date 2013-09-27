# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 12:32:00 2013

@author:  Tommy Löfstedt
@email:   tommy.loefstedt@cea.fr
@license: TBD.
"""

__all__ = ['load']

import numpy as np
from grad import grad_L1
from grad import grad_L2
from grad import grad_TV


def load(l, k, g, beta, M, e, snr, shape=None):
    """Returns data generated such that we know the exact solution.

    The data generated by this function is fit to the Linear regression + L1 +
    L2  + Total variation function, i.e. to:

        f(b) = (1 / 2).|Xb - y|² + l.|b|_1 + (k / 2).|b|² + g.TV(b),

    where |.|_1 is the L1 norm, |.|² is the squared L2 norm and TV is the
    total variation penalty.

    Parameters
    ----------
    l : The L1 regularisation parameter.

    k : The L2 regularisation parameter.

    g : The total variation regularisation parameter.

    beta : The regression vector to generate data from.

    M : The matrix to use when building data. This matrix carries the desired
            distribution of the generated data. The generated data will be a
            column-scaled version of this matrix.

    e : The error vector e = Xb - y. This vector carries the desired
            distribution of the residual.

    Returns
    -------
    X : The generated X matrix.

    y : The generated y vector.
    """
    l = float(l)
    k = float(k)
    g = float(g)

    if shape == None:
        shape = (beta.shape[0],)

#    seed = np.random.randint(2147483648)
#
#    low = 0.0
#    high = 1.0
#    for i in xrange(30):
#        np.random.seed(seed)
#        X, y, beta = _generate(l, k, gamma, density, high, M, e)
#        val = np.sqrt(np.sum(np.dot(X, beta) ** 2.0) / np.sum(e ** 2.0))
#        if val > snr:
#            break
#        else:
#            low = high
#            high = high * 2.0
#
#    def f(x):
#        np.random.seed(seed)
#        X, y, beta = _generate(l, k, gamma, density, x, M, e)
#        return np.sqrt(np.sum(np.dot(X, beta) ** 2.0) / np.sum(e ** 2.0)) - snr
#
#    bm = algorithms.BisectionMethod(max_iter=20)
#    bm.run(utils.AnonymousClass(f=f), low, high)
#
#    np.random.seed(seed)
#    X, y, beta = _generate(l, k, gamma, density, bm.x, M, e)
#    print "snr = %.5f = %.5f = |X.b| / |e| = %.5f / %.5f" \
#            % (snr, np.linalg.norm(np.dot(X, beta) / np.linalg.norm(e)),
#               np.linalg.norm(np.dot(X, beta)), np.linalg.norm(e))
#
#    return X, y, beta
    return _generate(l, k, g, beta, M, e, shape)


def _generate(l, k, g, beta, M, e, shape):

    p = np.prod(shape)

    gradL1 = grad_L1(beta)
    gradL2 = grad_L2(beta)
    gradTV = grad_TV(beta, shape)

    alpha = -(l * gradL1 + k * gradL2 + g * gradTV)
#    alpha = np.divide(alpha, np.dot(M.T, e))

    X = np.zeros(M.shape)
    for i in xrange(p):
        Mte = np.dot(M[:, i].T, e)
        X[:, i] = M[:, i] * (alpha[i, 0] / Mte)

    y = np.dot(X, beta) - e

    return X, y