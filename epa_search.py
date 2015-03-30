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
                response = dlg.GetStringSelection()
                sql = 'SELECT DISTINCT FAC_CITY FROM FRS_FAC WHERE FAC_STATE= :state'
                cur.execute(sql, state=response)
                cities = cur.fetchall()
                cities = ["%s" % x for x in cities]
                dlg = wx.TextEntryDialog(None,"Type the city you would like to search for","City","Type City Here")
                if dlg.ShowModal() == wx.ID_OK:
                    reponse = dlg.GetValue()
                    for city in cities:
                        if response.lower() == city.lower():
                            print response
                            return None

                else:
                    dlg.Desroy()

            else:
                return None
        else:
            dlg.Destroy()
            self.query()
            return None

        dlg.Destroy()
        return True

def main():
    app = App(False, "output")
    app.MainLoop()
main()
cur.close()
con.close()
