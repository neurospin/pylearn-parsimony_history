# -*- coding: utf-8 -*-
"""
The :mod:`structured` module includes several different structured machine
learning models for one, two or more blocks of data.

@author: Tommy Löfstedt <tommy.loefstedt@cea.fr>
"""

import models
import algorithms
import preprocess
import prox_ops
# TODO: Remove prox_ops, and/or move relevant parts to loss_functions.
import data
import tests
import utils
import loss_functions
import start_vectors

__version__ = '0.0.98'

__all__ = ['models', 'prox_ops', 'algorithms', 'preprocess',
           'data', 'tests', 'utils', 'loss_functions', 'start_vectors']