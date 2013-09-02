# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 17:11:05 2013

@author: Tommy Löfstedt
@email: tommy.loefstedt@cea.fr
"""

__all__ = ['load']

import numpy as np
import structured.utils as utils
import structured.algorithms as algorithms


def load(l, k, density, snr, M, e):
    """Returns data generated such that we know the exact solution.

    The data generated by this function is fit to the Linear regression + L1 +
    L2 loss function, i.e.:

        f(b) = (1 / 2).|Xb - y|² + l.|b|_1 + (k / 2).|b|²,

    where |.|_1 is the L1 norm and |.|² is the squared L2 norm.

    Parameters
    ----------
    l : The L1 regularisation parameter.

    k : The L2 regularisation parameter.

    density : The density of the returned regression vector (fraction of
            non-zero elements). Must be in (0, 1].

    snr : Signal to noise ratio between model and residual.

    M : The matrix to use when building data. This matrix carries the desired
            distribution of the generated data. The generated data will be a
            scaled version of this matrix.

    e : The error vector e = Xb - y. This vector carries the desired
            distribution of the residual.

    Returns
    -------
    X : The generated X matrix.

    y : The generated y vector.

    beta : The generated regression vector.
    """
    seed = np.random.randint(2147483648)

    low = 0.0
    high = 1.0
    for i in xrange(30):
        np.random.seed(seed)
        X, y, beta = _generate(l, k, density, high, M, e)
        val = np.sqrt(np.sum(np.dot(X, beta) ** 2.0) / np.sum(e ** 2.0))
        if val > snr:
            break
        else:
            low = high
            high = high * 2.0

    def f(x):
        np.random.seed(seed)
        X, y, beta = _generate(l, k, density, x, M, e)
        return np.sqrt(np.sum(np.dot(X, beta) ** 2.0) / np.sum(e ** 2.0)) - snr

    bm = algorithms.BisectionMethod(max_iter=20)
    bm.run(utils.AnonymousClass(f=f), low, high)

    np.random.seed(seed)
    X, y, beta = _generate(l, k, density, bm.x, M, e)
    print "snr = %.5f = %.5f = |X.b| / |e| = %.5f / %.5f" \
            % (snr, np.linalg.norm(np.dot(X, beta) / np.linalg.norm(e)),
               np.linalg.norm(np.dot(X, beta)), np.linalg.norm(e))

    return X, y, beta
#    return _generate(l, density, snr, M, e)


def _generate(l1, l2, density, snr, M, e):

    l1 = float(l1)
    l2 = float(l2)
    density = float(density)
    snr = float(snr)
    p = M.shape[1]
    ps = int(round(p * density))

    beta = np.zeros((p, 1))
    for i in xrange(p):
        if i < ps:
            beta[i, 0] = U(-1, 1) * snr / np.sqrt(ps)
        else:
            beta[i, 0] = 0.0
#    beta = np.flipud(np.sort(beta, axis=0))

    X = np.zeros(M.shape)
    for i in xrange(p):
        Mte = np.dot(M[:, i].T, e)
#        if abs(Mte) < utils.TOLERANCE:  # Avoid to make alpha very large
#            Mte = 1.0
        alpha = 0.0

        # L1
        sign_beta = sign(beta[i, 0])
        if i < ps:
            alpha += -l1 * sign_beta
        else:
            alpha += -l1 * U(-1, 1)

        # L2
        alpha += -l2 * beta[i, 0]

        alpha /= Mte

        X[:, i] = alpha * M[:, i]

    y = np.dot(X, beta) - e

    return X, y, beta


def U(a, b):
    t = max(a, b)
    a = float(min(a, b))
    b = float(t)
    return (np.random.rand() * (b - a)) + a


def sign(x):
    if x > 0:
        return 1.0
    elif x < 0:
        return -1.0
    else:
        return 0.0