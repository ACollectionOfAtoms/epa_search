import cx_Oracle
import wx
import csv
import rpy2.robjects as robjects

con = cx_Oracle.connect('dah3227_project/Oradah3227@//net6.cs.utexas.edu:1521/orcl')
cur = con.cursor()

class App(wx.App):


    def __init__(self, redirect=True, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.query(None)


    def query(self,event):
        if event != None:
            self.results(None,None)

        dlg = wx.SingleChoiceDialog(None,'Select Scope of Query', 'Public EPA Record Analysis',
                                    ['City Wide Analysis', 'State Wide Analysis', 'Country Wide Analysis'])
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetStringSelection()
        else:
            dlg.Destroy()
            return None


        if response == 'City Wide Analysis':
            cur.execute('select distinct FAC_STATE from frs_fac order by fac_state')
            info = cur.fetchall()
            info = ["%s" % x for x in info]
            dlg = wx.SingleChoiceDialog(None,'Select State', 'Query Construction',
                                    info)
            if dlg.ShowModal() == wx.ID_OK:
                state = dlg.GetStringSelection()
                sql = 'SELECT DISTINCT FAC_CITY FROM FRS_FAC WHERE FAC_STATE=:state'
                cur.execute(sql, state=state)
                cities = cur.fetchall()
                cities = ["%s" % x for x in cities]
                dlg = wx.TextEntryDialog(None,"Type the city you would like to search for","City","Type City Here")
                
                if dlg.ShowModal() == wx.ID_OK:
                    response = dlg.GetValue()
                    for city in cities:
                        if response.lower() == city.lower():
                            city = city.upper()
                            state = state.upper()
                            self.results(city,state)
                            dlg.Destroy()
                            return None
            else:
                return None
        else:
            self.query(None)
            return None
        return False
        

    def results(self,city,state):
        #SQL Query
        sql = 'SELECT i.fac_name, j.violations from frs_fac i, water j where i.registry_id = j.registry_id and i.fac_city =:c and i.fac_state =:s order by violations desc'

        cur.execute(sql, c=city, s=state)
        self.res = cur.fetchall()

        #Initialize frame!
        self.top = wx.Frame(None, wx.ID_ANY, title='Results', size=(580,200))
        self.top.index = 0
        self.panel = wx.Panel(self.top, wx.ID_ANY)
        self.top.list_ctrl = wx.ListCtrl(self.panel, size=(-1,100), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.top.list_ctrl.InsertColumn(0, 'Facility Name')
        self.top.list_ctrl.InsertColumn(1, 'Number Of Violations')
        self.top.list_ctrl.SetColumnWidth(0,350)
        self.top.list_ctrl.SetColumnWidth(1,150)


        btn1 = wx.Button(self.panel, label="OK")
        btn2 = wx.Button(self.panel, label="Visualize!")

        btn1.Bind(wx.EVT_BUTTON, self.Close)
        btn2.Bind(wx.EVT_BUTTON, self.graph)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.top.list_ctrl,0,wx.ALL|wx.EXPAND,5)
        sizer.Add(btn1, 0, wx.ALL|wx.CENTER,5)
        sizer.Add(btn2, 0, wx.ALL|wx.CENTER,8)
        self.panel.SetSizer(sizer)

        #populate table
        for i in self.res:
            self.top.list_ctrl.InsertStringItem(self.top.index,i[0])              
            for j in range(1,len(i)):
                self.top.list_ctrl.SetStringItem(self.top.index, j, str(i[j]))
            self.top.index += 1
        
        self.top.Show()


    def graph(self,event):
        f = open('results.csv', 'wb')
        csvwriter = csv.writer(f)
        for i in self.res:
            for j in range(1,len(i)):
                row = [i[0] ,str(i[j])]
                csvwriter.writerow(row)
        f.close()


        r = robjects.r
        r('''
                source('vis.r')
        ''')
        r_main = robjects.globalenv['main']
        r_main()
        return True


    def Close(self,event):
        self.top.Destroy()
        self.panel.Destroy()
        self.query(None)

def main():
    app = App(False, "output")
    app.MainLoop()

main()
cur.close()
con.close()
