import wx
import wx.html2 as webview

def browse_into_web(url):
    app = wx.App()
    frame = wx.Frame(None, title="Web Browser", size=(1550, 750))
    browser = webview.WebView.New(frame)
    browser.LoadURL(url)
    frame.Show()
    app.MainLoop()
