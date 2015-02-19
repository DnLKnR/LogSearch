import os, wx,sys

class Window(wx.Frame):
	def __init__(self,parent,id,title):
		wx.Frame.__init__(self,parent,style=wx.DEFAULT_FRAME_STYLE)
		self.menubar = wx.MenuBar()
		self.filemenu = wx.Menu()
		self.m_load = self.filemenu.Append(wx.ID_ANY,'Load\tCtrl-L','')
		self.menubar.Append(self.filemenu, 'File')
		self.Bind(wx.EVT_MENU, self.on_load, self.m_load)
		self.LC = wx.ListCtrl(self,-1,style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
		self.LC.InsertColumn(0,'Line #',format=wx.LIST_FORMAT_LEFT)
		self.LC.InsertColumn(1,'String',format=wx.LIST_FORMAT_LEFT)
		box = wx.BoxSizer(wx.VERTICAL)
		self.input = wx.TextCtrl(self,value='')
		box.Add(self.input,flag = wx.ALL | wx.GROW)
		box.Add(self.LC,flag = wx.ALL | wx.GROW)
		self.SetMenuBar(self.menubar)
		self.Bind(wx.EVT_TEXT,self.refresh,self.input)
		self.SetSizer(box)
		box.Fit(self)
		self.box = box
		
	def on_load(self, event):
		openFileDialog = wx.FileDialog(self, "Open log file", "", "","", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		if openFileDialog.ShowModal() == wx.ID_CANCEL: return
		file = openFileDialog.GetPath()
		self.data = Parser().read(file)
		self.refresh(-1)
		
	def refresh(self,event):
		search = self.input.GetValue().strip()
		self.LC.DeleteAllItems()
		for index,line in enumerate(self.data):
			if search in line[1]:
				self.LC.Append((line[0],line[1]))
		self.LC.SetColumnWidth(0,-1)
		self.LC.SetColumnWidth(1,-1)
		self.SetSizerAndFit(self.box)
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
app.Window = Window(None,-1,"LogSearch")
app.Window.Show()
app.MainLoop()