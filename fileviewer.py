import wx
import wx.grid as gridlibs
import csv
import io

# CSV Source = https://gist.github.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6

class MyApp(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)
        
        self.InitFrame()

    def InitFrame(self):
        frame = MyFrame(parent=None, title="CSV Viewer")
        frame.Show(True)

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title)
        self.OnInit()

    def OnInit(self):
        titlePanel = MyPanel(parent=self)

        # Control Layout
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        gridSizer = wx.BoxSizer(wx.HORIZONTAL)

        titleSizer.Add(titlePanel, 0, wx.ALL, 5)
        mainSizer.Add(titleSizer, 0, wx.CENTER, 5)
        titleSizer.Add(wx.StaticLine(self,), 0, wx.ALL|wx.EXPAND, 5)

        # Data Viewer
        grid = GridTable(self)
        grid.LoadFile()
        grid.SetColReadOnly(0)
        gridSizer.Add(grid, 1, wx.ALL|wx.EXPAND,5)
        mainSizer.Add(gridSizer, 0, wx.ALL|wx.EXPAND,5)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)


class MyPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        welcomeText = wx.StaticText(self, label="CSV Display", pos=(20,20))

class GridTableSource(gridlibs.GridTableBase):
    def __init__(self):
        super().__init__()
        self._data = None
        self._header = None
        self._readOnly = list()

    def LoadFile(self, fileName='./pokemon.csv'):
        fileName='./pokemon.csv'
        reader = csv.reader(open(fileName, 'r'))
        self._data = [row for row in reader]
        self._header = self._data.pop(0)
        self._readOnly = list()

    def Sort(self, col, ascending):
        pass

    def SetColReadOnly(self, col):
        self._readOnly.append(col)

    def GetNumberRows(self):
        return len(self._data) if self._data else 0

    def GetNumberCols(self):
        return len(self._header) if self._header else 0

    def GetValue(self, row, col):
        if not self._data:
            return ""
        else:
            return self._data[row][col]

    def SetValue(self, row, col, value):
        if self._data:
            self._data[row][col] = value

    def GetColLabelValue(self, col):
        return self._header[col] if self._header else None

class GridTable(gridlibs.Grid):
    def __init__(self, parent):
        super().__init__(parent)

        self._data = GridTableSource()
        self.SetTable(self._data)

        # Need to Implement sorting event, else segmentation fault error
        self.Bind(gridlibs.EVT_GRID_COL_SORT, self.OnSort)

    def OnSort(self, event):
        self._data.Sort(event.Col, self.IsOrderAscending())

    def LoadFile(self, fileName='./pokemon.csv'):
        self._data.LoadFile(fileName)
        self.SetTable(self._data)
        self.AutoSizeColumns()

    def SetColReadOnly(self, col):
        self._data.SetColReadOnly(col)

if __name__=="__main__":
    app = MyApp()
    app.MainLoop()