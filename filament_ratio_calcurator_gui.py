import wx
import os
import cv2
import numpy as np



class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Filament ratio Calcurator", size=(700, 600))
        self.folder = os.path.dirname(os.path.abspath(__file__))
        p = wx.Panel(self,wx.ID_ANY)

        # ファイル参照ボタン設定
        btn1 = wx.Button(p, wx.ID_ANY, "Filament")
        btn1.Bind(wx.EVT_BUTTON, self.select_file)

        # ファイル参照ボタン設定(1)
        btn2 = wx.Button(p, wx.ID_ANY, "Whole Area")
        btn2.Bind(wx.EVT_BUTTON, self.select_file2)

        # 
        btn3 = wx.Button(p, wx.ID_ANY, "Calcurate!")
        btn3.Bind(wx.EVT_BUTTON, self.calc)


        # テキストボックス設定
        self.text1 = wx.TextCtrl(p, -1, "", size=(250, -1))
        self.text2 = wx.TextCtrl(p, -1, "", size=(250, -1))
        self.text3 = wx.TextCtrl(p, -1, "", size=(150, -1))

        # ラベル設定
        label1 = wx.StaticText(p, -1, "Filement area:")
        label2 = wx.StaticText(p, -1, "Whole Area:")

        label3 = wx.StaticText(p, -1, "Filement Area")
        label4 = wx.StaticText(p, -1, "Whole Area")

        label5 = wx.StaticText(p, -1, "Result:")
        


        # 画像表示パネル設定
        self.p1 = wx.Panel(p, wx.ID_ANY, size=(300, 300)) # フィラメント画像表示パネル
        self.p2 = wx.Panel(p, wx.ID_ANY, size= (300, 300)) # 全体画像表示パネル

        # テキスト，ボタンレイアウト（１）
        s_1 = wx.BoxSizer(wx.HORIZONTAL)
        s_1.Add(label1, 0, wx.ALL, 10)
        s_1.Add(self.text1, 0, wx.ALL, 10)
        s_1.Add(btn1, 0, wx.ALL, 10)
        s_1.Add(btn3, 0, wx.ALL, 10)

        # テキスト，ボタンレイアウト（２）
        s_2 = wx.BoxSizer(wx.HORIZONTAL)
        s_2.Add(label2, 0, wx.ALL, 10)
        s_2.Add(self.text2, 0, wx.ALL, 10)
        s_2.Add(btn2, 0, wx.ALL, 10)
        s_2.Add(label5, 0, wx.ALL, 10)
        s_2.Add(self.text3)


        s_3 = wx.BoxSizer(wx.VERTICAL)
        s_3.Add(s_1, 0, wx.ALL, 10)
        s_3.Add(s_2, 0, wx.ALL, 10)
        

        # フィラメント表示レイアウト(1)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(label3, 0)
        sizer1.Add(self.p1, 0)

        # フィラメント表示レイアウト（２）
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        sizer2.Add(label4, 0)
        sizer2.Add(self.p2, 0)

        # フィラメント表示全体レイアウト
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(sizer1, 0)
        sizer3.Add(sizer2, 0)

        # 全体レイアウト
        S = wx.BoxSizer(wx.VERTICAL)
        S.Add(s_3, 0, wx.ALL, 10)
        S.Add(sizer3, 0, wx.ALL, 10)



        p.SetSizer(S)
        self.Show()


# btn1を押したときの動作設定
    def select_file(self, event):
        file = wx.FileDialog(None, u'ファイルを選択してください')
        if file.ShowModal() == wx.ID_OK:
            self.name = file.GetPath()
        file.Destroy()

        # 画像の配置
        img = wx.Image(self.name)
        width_1 = img.GetWidth()
        height_1 = img.GetHeight()
        img = img.Scale(300*(width_1/(width_1 + height_1)), 300*(height_1/(width_1 + height_1)), wx.IMAGE_QUALITY_HIGH) # 画像の縮小表示
        self.bitmap = img.ConvertToBitmap() # ImageをBitmapに変換
        wx.StaticBitmap(self.p1, -1, self.bitmap)
        self.text1.SetLabel(self.name)
    
# btn2を押したときの動作設定
    def select_file2(self, event):
        file2 = wx.FileDialog(None, u'ファイルを選択してください')
        if file2.ShowModal() == wx.ID_OK:
            self.name2 = file2.GetPath()
        file2.Destroy()

        # 画像の配置
        img2 = wx.Image(self.name2)
        width_2 = img2.GetWidth()
        height_2 = img2.GetHeight()
        img2 = img2.Scale(300*(width_2/(width_2 + height_2)), 300*(height_2/(width_2 + height_2)), wx.IMAGE_QUALITY_HIGH) # 画像の縮小表示
        self.bitmap2 = img2.ConvertToBitmap() # ImageをBitmapに変換
        wx.StaticBitmap(self.p2, -1, self.bitmap2) 
        self.text2.SetLabel(self.name2)

# btn3を押したときの動作設定
    def calc(self, event):
        img1 = cv2.imread(self.name)
        img2 = cv2.imread(self.name2)

        # 2値化処理
        gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)  # フィラメント領域の2値化処理
        gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)  # 全体の2値化処理

        # 黒ピクセルの数を計測
        num1 = np.sum(gray1 == 0)
        num2 = np.sum(gray2 == 0)

        ratio = num1 / num2
        self.text3.SetLabel(str(ratio))

    

if __name__ == '__main__':
    app = wx.App()
    MyFrame()
    app.MainLoop()