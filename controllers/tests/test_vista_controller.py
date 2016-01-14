import unittest
from controllers import VistaController


class TestVistaController(unittest.TestCase):

    def test_set_vista_params(self):
        controller = VistaController()
        self.assertEqual('vista.ann-arbor.med.va.gov', controller.host)
