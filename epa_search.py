import cx_Oracle
import wx
import csv

con = cx_Oracle.connect('dah3227_project/Oradah3227@//net6.cs.utexas.edu:1521/orcl')
cur = con.cursor()

class App(wx.App):

    def __init__(self, redirect=True, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.main_m()

    def main_m(self):
        dlg = wx.SingleChoiceDialog(None,
                'What would you like to do?', 'EPA Analyzer',
               ['Construct A Query', 'Visualize Data'])

        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetStringSelection()
        else:
            dlg.Destroy()
            return None

        if response == 'Construct A Query':
            self.query(None)
            return None

        elif response == 'Visualize Data':
            self.vis()
            return None

        dlg.Destroy()

        return True


    def query(self,event):
        if event != None:
            self.results(None,None)

            
        dlg = wx.SingleChoiceDialog(None,'Select Scope', 'Query Construction',
                                    ['City Comparison', 'State Comparison'])
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetStringSelection()
        else:
            dlg.Destroy()
            self.main_m()
            return None


        if response == 'City Comparison':
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
            dlg.Destroy()
            self.query(None)
            return None
        return False
        

    def results(self,city,state):
        #SQL Query
        sql = 'SELECT i.fac_name, j.violations from frs_fac i, water j where i.registry_id = j.registry_id and i.fac_city =:c and i.fac_state =:s order by violations desc'

        cur.execute(sql, c=city, s=state)
        res = cur.fetchall()

        #Initialize frame!
        top = wx.Frame(None, wx.ID_ANY, title='Results', size=(800,200))
        top.index = 0
        panel = wx.Panel(top, wx.ID_ANY)
        top.list_ctrl = wx.ListCtrl(panel, size=(-1,100), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        top.list_ctrl.InsertColumn(0, 'Facility Name')
        top.list_ctrl.InsertColumn(1, 'Number Of Violations')

        btn1 = wx.Button(panel, label="OK")
        btn2 = wx.Button(panel, label="Visualize!")

        btn1.Bind(wx.EVT_BUTTON, self.query)

        btn2.Bind(wx.EVT_BUTTON, csvgen(res))
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(top.list_ctrl,0,wx.ALL|wx.EXPAND,5)
        sizer.Add(btn1, 0, wx.ALL|wx.CENTER,5)
        sizer.Add(btn2, 0, wx.ALL|wx.CENTER,8)
        panel.SetSizer(sizer)

        #populate table
        for i in res:
            top.list_ctrl.InsertStringItem(top.index,i[0])              
            for j in range(1,len(i)):
                #print i[0] , str(i[j])
                top.list_ctrl.SetStringItem(top.index, j, str(i[j]))
            top.index += 1
        
        top.Show()
    

def csvgen(res):
    f = open('results.csv', 'wb')
    csvwriter = csv.writer(f)
    for i in res:
        for j in range(1,len(i)):
            row = [i[0] ,str(i[j])]
            csvwriter.writerow(row)
    f.close()

def main():
    app = App(False, "output")
    app.MainLoop()

main()
cur.close()
con.close()
