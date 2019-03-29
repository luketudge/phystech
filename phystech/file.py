"""
Module for reading PTB HDF5 files.
Extends the h5py File class with some convenience methods.

So far this includes:
    A print method showing the attributes and children of the root group.
    Retrieving attributes, children, etc.
    Searching for a group or dataset.
    Reading a dataset into a numpy array.
    Exporting multiple datasets as columns in a pandas dataframe.

Most of the methods take group or dataset names as arguments, and return data
in an easy format (formatted string, array, dataframe etc.)
"""

import h5py
import numpy
from os import path
import pandas



#%% Main class

class File(h5py.File):
    """
    Child class of h5py.File for reading PTB data files.
    """
    
    def __init__(self, fileName, mode='r', posMaster='PosCountTimer', posCounter='PosCounter', **kwArgs):
        """
        Open 'fileName' as an h5py.File object.
        By default read-only, but argument 'mode' can set other file permissions.
        Argument 'posMaster' is the name of the dataset from which to take
        reference PosCounter values.
        Argument 'posCounter' is the name of the PosCounter column in each
        dataset.
        Additional keyword arguments are passed on to h5py.File().
        """
        
        # Initialize the parent class h5py.File.
        super().__init__(name=fileName, mode=mode, **kwArgs)
        
        # Initialize some other attributes.
        self.posCounter = posCounter
        
        # Find the master pos counter.
        self.posMaster = self.search(posMaster)
        if not self.posMaster:
            raise KeyError('Master pos counter dataset %s not found.' % posMaster)
        self.maxPos = numpy.max(self.get_data(self.posMaster)[self.posCounter])
        
        # Get the overall file summary once now,
        # so as not to read the file with every print().
        self.info = '%s\n\n' % path.abspath(self.filename)
        self.info += self.print_attrs()
        self.info += '\n\nMaxPosCounter:\t%i' % self.maxPos
    
    def __str__(self):
        """
        Print the attributes and children of the root group in the HDF5 file.
        """
        
        return self.info
        
    def __match__(self, name, obj):
        """
        Helper function for checking whether a search has reached its target.
        Used only in File.search(), in conjunction with h5py.File.visititems().
        """
        
        if self.lastSearch in name:
            return name
    
    def children(self, groupName='/'):
        """
        Retrieve a list of the names of children of a group.
        Argument 'groupName' is a str naming the parent group.
        Default is the root group.
        """
        
        return list(self[groupName].keys())
    
    def get_attrs(self, name='/'):
        """
        Get the attributes of a group or dataset in the HDF5 file.
        Argument 'name' is a str naming the group or dataset.
        Default is the root group.
        Returns a dict of {field:contents}, where contents have been
        simplified from array to str.
        """
        
        attrItems = self[name].attrs.items()
        return {field:contents[0].decode('UTF-8') for field,contents in attrItems}
    
    def get_data(self, datasetName):
        """
        Retrieve a dataset and allocate into numpy array.
        Argument 'datasetName' is str naming the dataset.
        To retrieve and align multiple datasets, see to_data_frame().
        """
        
        return self[self.search(datasetName)][...]
    
    def print_attrs(self, name='/'):
        """
        Print the attributes of a group or dataset.
        Argument 'name' is a str naming the group or dataset.
        Default is the root group.
        Returns a str containing formatted output.
        To interact with and retrieve individual attributes, see get_attrs().
        """
        
        info = ''
        obj = self[name]
        
        # Add attribute names and values.
        # These are retrieved using get_attrs().
        for x in self.get_attrs(name).items():
            info += '%s:\t%s\n' % x
            
        # Add subgroups (only applicable to a group object).
        if isinstance(obj, h5py.Group):
            info += '\nGroups:\n'
            for group in obj.keys():
                info += '%s\n' % group
        
        info = info.strip()
        return info
    
    def search(self, name):
        """
        Search for a group or dataset.
        Argument 'name' is a str naming the group or dataset.
        Returns a str containing the full name of the first match.
        For example returns 'c1/main/normalized' for search term 'normalized'.
        Returns None if 'name' is not found.
        
        TODO: Handle multiple datasets with the same term in their name?
        """
        
        self.lastSearch = name
        return self.visititems(self.__match__)
    
    def get_data_frame(self, *args, file=None):
        """
        Read multiple datasets into a pandas.DataFrame.
        Arguments are strings naming datasets in the file.
        These will first be searched for using File.search().
        This allows naming datasets without their full HDF5 path.
        Data are aligned according to PosCounter values.
        As well as being returned, DataFrame can also be saved into a csv file
        given by optional argument 'file'.
        """
        
        # Preallocate a numpy array to hold the data.
        # Number of rows equal to maximum PosCounter.
        # Number of columns equal to number of datasets to be retrieved.
        nCols = len(args)
        d = numpy.full((self.maxPos, nCols), numpy.nan)
        
        # Loop through the desired datasets and fill them into the array.
        # Align them into the rows by PosCounter values.
        for col in range(nCols):
            dataset = self.get_data(args[col])
            rowNums = dataset[self.posCounter] - 1 # (-1 to convert to Python index system)
            d[rowNums,col] = dataset[dataset.dtype.names[1]]
        
        # Convert to pandas.DataFrame.
        d = pandas.DataFrame(data=d, columns=args)
        
        # Save to file if requested.
        if file:
            d.to_csv(file, index=False)
        
        return d



#%% Development tests

if __name__ == '__main__':
    
    # Confirm we can open file and print summary.
    f = File('00149.h5')
    print(f)
    
    # Confirm we can get and export datasets.
    d = f.get_data_frame('eVEnerg:io1200000cff',
                         'A2980:23303chan1',
                         'A2980:23303chan1__bIICurrent:Mnt1chan1',
                         file='test.csv')
    print(d)


