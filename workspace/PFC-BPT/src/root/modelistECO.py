import wx
 
########################################################################
class PopupUP(wx.PopupWindow):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent, style):
        """Constructor"""
        wx.PopupWindow.__init__(self, parent,style )

        panel = wx.Panel(self)
        self.panel = panel
              
        pngup = wx.Bitmap(u"./icons/Actions-arrow-up-icon.png", wx.BITMAP_TYPE_ANY ) 
        wx.StaticBitmap(self, -1, pngup, (-1, -1), (pngup.GetWidth(), pngup.GetHeight()))
        
        wx.CallAfter(self.Refresh)    
 
########################################################################
########################################################################
class PopupDown(wx.PopupWindow):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent, style):
        """Constructor"""
        wx.PopupWindow.__init__(self, parent, style)

        panel = wx.Panel(self)
        self.panel = panel
      
        pngdown = wx.Bitmap(u"./icons/Actions-arrow-down-icon.png", wx.BITMAP_TYPE_ANY ) 
        wx.StaticBitmap(self, -1, pngdown, (-1, -1), (pngdown.GetWidth(), pngdown.GetHeight()))
               
        wx.CallAfter(self.Refresh)    
    

########################################################################

class TestPanel(wx.Panel):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        btn = wx.Button(self, label="Open Popup")
        btn.Bind(wx.EVT_BUTTON, self.onShowPopup)
        self.x=0

    #----------------------------------------------------------------------
    def onShowPopup(self, event):
        """"""
        if self.x==0:
            self.winup = PopupUP(self.GetTopLevelParent(),  wx.SIMPLE_BORDER)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (300,0) )
            sz =  btn.GetSize()
            self.winup.Position(pos, (0, sz[1]))
            self.winup.Show(True)
            self.x=1
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.onCloseUp, self.timer)
            self.timer.Start(1000)
            print 'timer Up stert'
        elif self.x==1: 
            
            self.win = PopupDown(self.GetTopLevelParent(), wx.SIMPLE_BORDER)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (300,0) )
            sz =  btn.GetSize()
            self.win.Position(pos, (0, sz[1]))
            self.win.Show(True)
            self.x = 0 
            self.timer2 = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.onCloseDown, self.timer2)
            self.timer2.Start(1500)
            print 'timer d stert'
        

    def onCloseUp(self, event):
        print 'oncloseup'
        if self.winup.IsShown():
            self.winup.Show(False)
        self.timer.Stop()
        
    def onCloseDown(self, event):
        print 'onclosedown'
        self.win.Show(False)  
        self.timer2.Stop()
        
        

########################################################################
class TestFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Test Popup")
        panel = TestPanel(self)
        self.Show()

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = TestFrame()
    app.MainLoop()    