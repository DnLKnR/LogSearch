import os, wx,sys

class Window(wx.Frame):
	def __init__(self,parent,id,title):
		self.data, self.marked = [],[]
		wx.Frame.__init__(self,parent,style=wx.DEFAULT_FRAME_STYLE)
		self.menubar = wx.MenuBar()
		self.filemenu = wx.Menu()
		self.m_load = self.filemenu.Append(wx.ID_ANY,'Load\tCtrl-L','')
		self.menubar.Append(self.filemenu, 'File')
		self.Bind(wx.EVT_MENU, self.on_load, self.m_load)
		self.LC = wx.ListCtrl(self,-1,style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
		self.LC.InsertColumn(0,'Line #',format=wx.LIST_FORMAT_LEFT)
		self.LC.InsertColumn(1,'String',format=wx.LIST_FORMAT_LEFT)
		# mainbox = wx.BoxSizer(wx.VERTICAL)
		self.input = wx.TextCtrl(self,value='')
		gs = wx.FlexGridSizer(2,1,1,1)
		gs.Add(self.input,flag = wx.ALL | wx.GROW)
		gs.Add(self.LC,flag = wx.ALL | wx.GROW)
		gs.AddGrowableCol(0)
		gs.AddGrowableRow(1)
		self.SetMenuBar(self.menubar)
		self.Bind(wx.EVT_TEXT,self.refresh,self.input)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.mark,self.LC)
		self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.mark,self.LC)
		# mainbox.Add(gs,flag = wx.GROW | wx.EXPAND)
		self.SetSizer(gs)
		gs.Fit(self)
		
	def on_load(self, event):
		openFileDialog = wx.FileDialog(self, "Open log file", "", "","", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		if openFileDialog.ShowModal() == wx.ID_CANCEL: return
		file = openFileDialog.GetPath()
		self.data,self.marked = Parser().read(file),[]
		self.refresh(-1)
	
	def refresh(self,event):
		search,count = self.input.GetValue().lower().strip(),0
		self.LC.DeleteAllItems()
		for line in self.data:
			if search in line[1].strip().lower():
				self.LC.Append((line[0],line[1]))
				if line[0] in self.marked:
					self.LC.SetItemBackgroundColour(count,'yellow')
				count += 1
		self.LC.SetColumnWidth(0,-1)
		self.LC.SetColumnWidth(1,-1)

	def mark(self,event):
		index = event.GetIndex()
		line = self.LC.GetItemText(index)
		if line in self.marked:
			self.LC.SetItemBackgroundColour(index,'white')
			self.marked.remove(line)
		else:
			self.LC.SetItemBackgroundColour(index,'yellow')
			self.marked.append(line)
		
class Parser:
	def __init__(self):
		self.data = []
		
	def read(self, file):
		if file == '':
			return
		with open(file,'r') as log:
			text = log.read()
		self.data = text.split('\n')
		for index,line in enumerate(self.data):
			line = line.replace('\n','')
			line = line.replace('\r','')
			self.data[index] = [str(index),line]
		return self.data

app = wx.App()
app.Window = Window(None,-1,"File Search")
app.Window.on_load(-1)
app.Window.Show()
app.MainLoop()