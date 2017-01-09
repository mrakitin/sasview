import sys
import unittest
import numpy

from PyQt4 import QtGui
from PyQt4 import QtCore
from mock import MagicMock

# set up import paths
import path_prepare

from UnitTesting.TestUtils import QtSignalSpy
from sas.sasgui.guiframe.dataFitting import Data1D
import sas.qtgui.Plotter as Plotter

# Local
from LinearFit import LinearFit

app = QtGui.QApplication(sys.argv)

class LinearFitTest(unittest.TestCase):
    '''Test the LinearFit'''
    def setUp(self):
        '''Create the LinearFit'''
        self.data = Data1D(x=[1.0, 2.0, 3.0],
                           y=[10.0, 11.0, 12.0],
                           dx=[0.1, 0.2, 0.3],
                           dy=[0.1, 0.2, 0.3])
        plotter = Plotter.Plotter(None, quickplot=True)
        self.widget = LinearFit(parent=plotter, data=self.data, xlabel="log10(x^2)", ylabel="log10(y)")

    def tearDown(self):
        '''Destroy the GUI'''
        self.widget.close()
        self.widget = None

    def testDefaults(self):
        '''Test the GUI in its default state'''
        self.assertIsInstance(self.widget, QtGui.QDialog)
        self.assertEqual(self.widget.windowTitle(), "Linear Fit")
        self.assertEqual(self.widget.txtA.text(), "1")
        self.assertEqual(self.widget.txtB.text(), "1")
        self.assertEqual(self.widget.txtAerr.text(), "0")
        self.assertEqual(self.widget.txtBerr.text(), "0")

        self.assertEqual(self.widget.lblRange.text(), "Fit range of log10(x^2)")

    def testFit(self):
        '''Test the fitting wrapper '''
        # Catch the update signal
        self.widget.parent.emit = MagicMock()

        # Set some initial values
        self.widget.txtRangeMin.setText("1.0")
        self.widget.txtRangeMax.setText("3.0")
        self.widget.txtFitRangeMin.setText("1.0")
        self.widget.txtFitRangeMax.setText("3.0")
        # Run the fitting
        self.widget.fit(None)
        return_values = self.widget.parent.emit.call_args[0][1]
        # Compare
        self.assertItemsEqual(return_values[0], [1.0, 3.0])
        self.assertItemsEqual(return_values[1], [10.004054329087303, 12.030439848443539])

        # Set the log scale
        self.widget.x_is_log = True
        self.widget.fit(None)
        return_values = self.widget.parent.emit.call_args[0][1]
        # Compare
        self.assertItemsEqual(return_values[0], [1.0, 3.0])
        self.assertItemsEqual(return_values[1], [9.9877329376711437, 11.843650824649025])

    def testOrigData(self):
        ''' Assure the un-logged data is returned'''
        # log(x), log(y)
        self.widget.xminFit, self.widget.xmaxFit = self.widget.range()
        orig_x = [ 1.,  2.,  3.]
        orig_y = [1.0, 1.0413926851582251, 1.0791812460476249]
        orig_dy = [0.01, 0.018181818181818184, 0.024999999999999998]
        x, y, dy = self.widget.origData()

        self.assertItemsEqual(x, orig_x)
        self.assertItemsEqual(y, orig_y)
        self.assertItemsEqual(dy, orig_dy)

        # x, y
        self.widget.x_is_log = False
        self.widget.y_is_log = False
        self.widget.xminFit, self.widget.xmaxFit = self.widget.range()
        orig_x = [ 1.,  2.,  3.]
        orig_y = [10., 11., 12.]
        orig_dy = [0.1, 0.2, 0.3]
        x, y, dy = self.widget.origData()

        self.assertItemsEqual(x, orig_x)
        self.assertItemsEqual(y, orig_y)
        self.assertItemsEqual(dy, orig_dy)

        # x, log(y)
        self.widget.x_is_log = False
        self.widget.y_is_log = True
        self.widget.xminFit, self.widget.xmaxFit = self.widget.range()
        orig_x = [ 1.,  2.,  3.]
        orig_y = [1.0, 1.0413926851582251, 1.0791812460476249]
        orig_dy = [0.01, 0.018181818181818184, 0.024999999999999998]
        x, y, dy = self.widget.origData()

        self.assertItemsEqual(x, orig_x)
        self.assertItemsEqual(y, orig_y)
        self.assertItemsEqual(dy, orig_dy)

    def testCheckFitValues(self):
        '''Assure fit values are correct'''
        # Good values
        self.assertTrue(self.widget.checkFitValues(self.widget.txtFitRangeMin))
        self.assertEqual(self.widget.txtFitRangeMin.palette().color(10).name(), "#f0f0f0")
        # Bad values
        self.widget.x_is_log = True
        self.widget.txtFitRangeMin.setText("-1.0")
        self.assertFalse(self.widget.checkFitValues(self.widget.txtFitRangeMin))
       

    def testFloatInvTransform(self):
        '''Test the helper method for providing conversion function'''
        self.widget.xLabel="x"
        self.assertEqual(self.widget.floatInvTransform(5.0), 5.0)
        self.widget.xLabel="x^(2)"
        self.assertEqual(self.widget.floatInvTransform(25.0), 5.0)
        self.widget.xLabel="x^(4)"
        self.assertEqual(self.widget.floatInvTransform(81.0), 3.0)
        self.widget.xLabel="log10(x)"
        self.assertEqual(self.widget.floatInvTransform(2.0), 100.0)
        self.widget.xLabel="ln(x)"
        self.assertEqual(self.widget.floatInvTransform(1.0), numpy.exp(1))
        self.widget.xLabel="log10(x^(4))"
        self.assertEqual(self.widget.floatInvTransform(4.0), 10.0)
      
if __name__ == "__main__":
    unittest.main()
