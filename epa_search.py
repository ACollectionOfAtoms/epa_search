import cx_Oracle
import wx


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
            self.query()
            return None

        elif response == 'Visualize Data':
            self.vis()
            return None

        dlg.Destroy()

        return True


    def query(self):
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
                print cities
                dlg = wx.TextEntryDialog(None,"Type the city you would like to search for","City","Type City Here")
                if dlg.ShowModal() == wx.ID_OK:
                    response = dlg.GetValue()
                    for city in cities:
                        print city
                        if response.lower() == city.lower():
                            city = city.upper()
                            state = state.upper()
                            self.results(city,state)
                            dlg.Destroy()
                            return None
                        
                else:
                    dlg.Desroy()

            else:
                return None
        else:
            dlg.Destroy()
            self.query()
            return None
        
    def results(self,city,state):
        print 'runnin'
        sql = 'SELECT FAC_NAME, FAC_ZIP FROM FRS_FAC WHERE FAC_CITY=:c and FAC_STATE=:s'
        cur.execute(sql, c=city, s=state)
        res = cur.fetchall()
        panel = wx.Panel(self, wx.ID_ANY)
        self.list_ctrl = wx.ListCtrl(panel, size=(-1,100), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'Facility Name')
        self.list_ctrl.InsertColumn(1, 'Facility Zip')

        btn1 = wx.Button(panel, label="OK")
        btn2 = wx.Button(panel, label="Visualize!")            

        return True

def main():
    app = App(False, "output")
    app.MainLoop()
main()
cur.close()
con.close()
