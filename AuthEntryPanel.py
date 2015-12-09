# -*- coding: utf-8 -*-

import wx

class AuthEntryPanel( wx.Panel ):

    ##_first_event_type = wx.EVT_WINDOW_CREATE
    _first_event_type = wx.EVT_SIZE

    def __init__( self ):
        pre = wx.PrePanel()
        self.PostCreate( pre )
        self.Bind( self._first_event_type, self.OnCreate )


    def OnCreate( self, event ):
        self.Unbind( self._first_event_type )

        self.Refresh()


    # TODO Auth code panel class
