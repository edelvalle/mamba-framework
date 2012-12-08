
# Copyright (c) 2012 - Oscar Campos <oscar.campos@member.fsf.org>
# Ses LICENSE for more details

"""
Tests for mamba.core.module
"""

from twisted.trial import unittest

from mamba.core.interfaces import INotifier
from mamba.core.module import ModuleManager


class ModuleManagerTest(unittest.TestCase):

    def test_module_manager_implements_inotifier(self):
        self.assertTrue(INotifier.implementedBy(ModuleManager))
