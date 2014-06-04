import os
import unittest

from plone.testing import layered
# from plone.app.testing import PLONE_ZSERVER

from genweb.alternatheme.testing import GENWEBTHEME_ROBOT_TESTING

import robotsuite


def test_suite():
    suite = unittest.TestSuite()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    robot_dir = os.path.join(current_dir, 'robot')
    robot_tests = [
        os.path.join('robot', doc) for doc in
        os.listdir(robot_dir) if doc.endswith('.robot') and
        doc.startswith('test_')
    ]
    for test in robot_tests:
        suite.addTests([
            layered(robotsuite.RobotTestSuite(test),
                    layer=GENWEBTHEME_ROBOT_TESTING),
        ])
    return suite
