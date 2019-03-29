"""
Module for generating figures.
"""

import matplotlib
from matplotlib import pyplot
from matplotlib.figure import Figure



#%% Main class

class Plot:
    """
    Plot class. Ultimately the aim is to pass this on to the GUI.
    """
    
    def __init__(self, data=None, backend=None):
        """
        Create a Plot object.
        Argument 'data' supplies a pandas.DataFrame with data to be plotted.
        Argument 'backend' is a str determining what backend the figure is for.
        This is passed on to matplotlib.use().
        (Perhaps 'Qt5Agg'?)
        Default is to plot with the console's backend, so as to enable easier
        interactive testing.
        """
        
        # Initialize some attributes.
        self.data = data
        if data is None:
            self.x = None
            self.y = None
        else:
            self.x = data.columns[0]
            self.y = data.columns[1]
        
        # Create the figure object that will be passed on,
        # depending on the requested mode.
        # Probably better not to determine the figure dimensions here,
        # but rather let the GUI alter them afterwards.
        if backend is None:
            self.fig = pyplot.figure()
            self.mode = 'console'
        else:
            matplotlib.use(backend)
            self.fig = Figure()
            self.mode = 'GUI'
        
        # Add the axes object to the figure.
        self.axes = self.fig.add_subplot(1, 1, 1)
    
    def clear(self):
        """
        Clear the axes of data, ready for a new plot.
        """
        
        self.fig.delaxes(self.axes)
        self.axes = self.fig.add_subplot(1, 1, 1)

    def get_figure(self):
        """
        Get the current plot and return it as a matplotlib Figure.
        """
        
        return self.fig
    
    def plot(self, x=None, y=None):
        """
        Draw the data onto the axes.
        Arguments 'x' and 'y' are str names of columns in data.
        Default is to plot the first two columns as x and y.
        Multiple calls to plot() will plot over existing data.
        Use clear() to clear the axes for a new plot.
        """
        
        # Use defaults if no input arguments.
        if x is None or y is None:
            x = self.x
            y = self.y
        
        # Draw.
        self.axes.plot(self.data[x], self.data[y])
    
    def set_data(self, data):
        """
        Change the data for the figure.
        Argument 'data' is a new pandas.DataFrame.
        """
        
        self.data = data



#%% Development tests
    
if __name__ == '__main__':
    
    import file
    
    # Define which datasets to plot.
    x = 'eVEnerg:io1200000cff'
    y = 'A2980:23303chan1'
    
    # Get data from the example file via file module.
    f = file.File('00149.h5')
    d = f.get_data_frame(x, y)
    d['test'] = d[y] * 1.1
    
    # Confirm we can create a plot.
    fig = Plot(d)
    fig.plot()
    fig.fig
    
    # Confirm we can overlay a new data series.
    fig.plot(x, 'test')
    fig.fig
    
    # Confirm we can clear and restart.
    fig.clear()
    fig.plot()
    fig.fig
    
    
    