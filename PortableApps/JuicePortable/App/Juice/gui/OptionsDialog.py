import wx

CHECKBOX = 0
RADIOBOX = 1

class OptionsDialog(wx.Dialog):
    def __init__(self,parent,translator,title,message,opts,optstyle=CHECKBOX,prompt_ask=True,defaults=[]):
        wx.Dialog.__init__(self,parent,-1,translator(title),style=wx.DEFAULT_DIALOG_STYLE)
        
        self.value = []
        self.optstyle = optstyle
        self.optcontrols = []
        self.prompt_ask = prompt_ask
        self.prompt_ask_ctl = None
        self.buttondict = {}
        self._ = translator
        self.defaults = defaults
        self.rb = None
        
        #Translate the opts
        for i in range(len(opts)):
            opts[i] = self._(opts[i])
            
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(wx.Size(-1,10))

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2.Add(wx.Size(10,-1))

        self.sizer3 = wx.BoxSizer(wx.VERTICAL)

        self.text = wx.StaticText(self,wx.ID_ANY,self._(message))
        
        self.sizer3.Add(self.text)
        self.sizer3.Add(wx.Size(-1,10))

        if optstyle == RADIOBOX:
            self.rb = rb = wx.RadioBox(
                self, -1, "", wx.DefaultPosition, wx.DefaultSize,
                opts, 1, wx.RA_SPECIFY_COLS
                )
            self.sizer3.Add(rb)
            if len(defaults) > 0:
                rb.SetSelection(defaults[0])
        else:
            for i in range(len(opts)):
                opt = opts[i]
                chk = wx.CheckBox(self,wx.ID_ANY,opt)
                chk.SetValue(defaults.count(i) > 0)
                self.optcontrols.append(chk)
                self.sizer3.Add(chk)
                self.sizer3.Add(wx.Size(-1,3))
            
        if prompt_ask:
            self.sizer3.Add(wx.Size(-1,15))
            chk = wx.CheckBox(self,wx.ID_ANY,self._("str_dont_ask"))
            self.prompt_ask_ctl = chk
            self.sizer3.Add(chk)

        self.sizer3.Add(wx.Size(-1,10))
           
        self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        
        btn = wx.Button(self,wx.NewId(),self._("str_ok"))
        self.buttondict[btn] = wx.ID_OK
        wx.EVT_BUTTON(self,btn.GetId(),self.OnButton)
        self.sizer4.Add(btn)

        self.sizer4.Add(wx.Size(5,-1))
        
        btn = wx.Button(self,wx.NewId(),self._("str_cancel"))
        self.buttondict[btn] = wx.ID_CANCEL
        wx.EVT_BUTTON(self,btn.GetId(),self.OnButton)
        self.sizer4.Add(btn)

        #ESC cancels the operation.
        self.SetAcceleratorTable(
            wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, btn.GetId())
            ]))

        self.sizer4.Add(wx.Size(5,-1))
        
        self.sizer3.Add(self.sizer4, flag=wx.ALIGN_RIGHT)
        
        self.sizer2.Add(self.sizer3)
        self.sizer2.Add(wx.Size(10,-1))
        
        self.sizer.Add(self.sizer2)

        self.sizer.Add(wx.Size(-1,10))

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        
    def OnButton(self, event):
        self.value = []
        if self.optstyle == RADIOBOX:
            self.value.append(self.rb.GetSelection())
        else:
            for i in range(0,len(self.optcontrols)):
                ctl = self.optcontrols[i]
                if ctl.GetValue():
                    self.value.append(i)
        self.EndModal(self.buttondict[event.GetEventObject()])

    def GetValue(self):
        return self.value

    def AskAgain(self):
        if self.prompt_ask:
            return not self.prompt_ask_ctl.GetValue()
        else:
            return True
