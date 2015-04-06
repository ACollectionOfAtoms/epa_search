import cx_Oracle
import wx
import csv
import rpy2.robjects as robjects

con = cx_Oracle.connect('dah3227_project/Oradah3227@//net6.cs.utexas.edu:1521/orcl')
cur = con.cursor()

class App(wx.App):


    def __init__(self, redirect=True, filename=None):
        #Initialize App
        wx.App.__init__(self, redirect, filename)
        self.query(None)


    def query(self,event):
        # Dialog Box with list of options...
        dlg = wx.SingleChoiceDialog(None,'Select Scope of Query', 'Public EPA Record Analysis',
                                    ['City Wide Analysis', 'State Wide Analysis', 'Country Wide Analysis'])

        # If OK IS clicked, Collect selection in response variable, and go on, else Exit.
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetStringSelection()
            dlg.EndModal(dlg.GetReturnCode())
            dlg.Destroy()
        else:
            dlg.EndModal(dlg.GetReturnCode())
            dlg.Destroy()
            return None
                                    
        # If an option is selected...
        if response == 'City Wide Analysis':
            #SQL to get list of states from EPA database
            cur.execute('select distinct FAC_STATE from frs_fac order by fac_state')
            info = cur.fetchall()

            #Convert list of tuples to list of strings
            info = ["%s" % x for x in info]

            #Put list of strings into new dialog box, for user selection.
            dlg2 = wx.SingleChoiceDialog(None,'Select State', 'Query Construction',
                                    info)

            #If User Clicks OK, store string, else, return to query main menu! This should be a function!
            if dlg2.ShowModal() == wx.ID_OK:
                state = dlg2.GetStringSelection()
                dlg2.EndModal(dlg2.GetReturnCode())
                dlg2.Destroy()



                sql = 'SELECT DISTINCT FAC_CITY FROM FRS_FAC WHERE FAC_STATE=:state'
                cur.execute(sql, state=state)
                cities = cur.fetchall()
                cities = ["%s" % x for x in cities]

                #Create TEXT ENTRY window...
                txdlg = wx.TextEntryDialog(None,"Type the city you would like to search for","City","Type City Here")
                
                check = 0
                #If user clicks OK, pass results to results function otherwise
                #Destroy txdlg and return to main menu!
                if txdlg.ShowModal() == wx.ID_OK:
                    response = txdlg.GetValue()
                    txdlg.EndModal(txdlg.GetReturnCode())
                    for city in cities:
                        if response.lower() == city.lower():
                            check = 1
                            txdlg.Destroy()
                            city = city.upper()
                            state = state.upper()
                            self.results(city,state)
                            return None
                    if check == 0:
                        # If city not found, return to main menu!
                        wx.MessageBox('That city was not found!', 'Error', wx.OK | wx.ICON_EXCLAMATION)
                        txdlg.EndModal(txdlg.GetReturnCode())
                        txdlg.Destroy()
                        self.query(None)
                else:
                    txdlg.EndModal(txdlg.GetReturnCode())
                    txdlg.Destroy()
                    self.query(None)
            else:
                dlg2.Destroy()
                dlg2.EndModal(dlg2.GetReturnCode())
                self.query(None)



        if response == 'State Wide Analysis':
            #SQL to get list of states from EPA database
            cur.execute('select distinct FAC_STATE from frs_fac order by fac_state')
            info = cur.fetchall()

            #Convert list of tuples to list of strings
            info = ["%s" % x for x in info]

            #Put list of strings into new dialog box, for user selection.
            dlg2 = wx.SingleChoiceDialog(None,'Select State', 'Query Construction',
                                    info)

            if dlg2.ShowModal() == wx.ID_OK:
                state = dlg2.GetStringSelection()
                dlg2.EndModal(dlg2.GetReturnCode())
                dlg2.Destroy()
                self.results(None,state)



    
        else:
            self.query(None)
        return None
        
    def results(self,city,state):
        #SQL Query, check if given a city
        if city == None:
            self.state = True
            sql = 'select fac_city, sum(total) as CityTotal from (select i.fac_city, (coalesce(j.violations, 0) + coalesce(k.violations, 0) + coalesce(l.violations, 0)) as total from frs_fac i full join h2o j on i.fac_name = j.fac_name and i.fac_street = j.fac_street and i.fac_city = j.city and i.fac_state = j.state_code full join aire k on i.fac_name = k.fac_name and i.fac_street = k.fac_street and i.fac_city = k.fac_city and i.fac_state = k.fac_state full join haz l on i.fac_name = l.fac_name and i.fac_street = l.fac_street and i.fac_city = l.fac_city and i.fac_state = l.fac_state where i.fac_state =:s order by total desc) group by fac_city order by citytotal desc'
            cur.execute(sql, s=state)
            self.state_res = cur.fetchall()

        else:    
            sql = 'select * from (select i.fac_name,(coalesce(j.violations, 0) + coalesce(k.violations, 0) + coalesce(l.violations, 0)) as total from frs_fac i full join h2o j on i.fac_name = j.fac_name and i.fac_street = j.fac_street and i.fac_city = j.city and i.fac_state = j.state_code full join aire k on i.fac_name = k.fac_name and i.fac_street = k.fac_street and i.fac_city = k.fac_city and i.fac_state = k.fac_state full join haz l on i.fac_name = l.fac_name and i.fac_street = l.fac_street and i.fac_city = l.fac_city and i.fac_state = l.fac_state where i.fac_city =:c and i.fac_state =:s order by total desc) where total > 0'
            cur.execute(sql, c=city, s=state)
            self.res = cur.fetchall()

        #Initialize frame!
        self.top = wx.Frame(None, wx.ID_ANY, title='Results', size=(580,200))
        #Set index of entry into list
        self.top.index = 0

        #Add Panel to store SQL results
        self.panel = wx.Panel(self.top, wx.ID_ANY)

        #Specify the panels' size, and titles
        self.top.list_ctrl = wx.ListCtrl(self.panel, size=(-1,100), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        if city == None:
            self.top.list_ctrl.InsertColumn(0, 'City')
            self.top.list_ctrl.InsertColumn(1, 'Total Violations')

        else:
            self.top.list_ctrl.InsertColumn(0, 'Facility Name')
            self.top.list_ctrl.InsertColumn(1, 'Number Of Violations')

        self.top.list_ctrl.SetColumnWidth(0,350)
        self.top.list_ctrl.SetColumnWidth(1,150)

        #Add some buttons...
        btn1 = wx.Button(self.panel, label="OK")
        btn2 = wx.Button(self.panel, label="Generate Graph of Top 10 EPA Violators In Current Folder")

        #Button events
        btn1.Bind(wx.EVT_BUTTON, self.resClose)
        btn2.Bind(wx.EVT_BUTTON, self.graph)
        
        # Set up layout of buttons
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.top.list_ctrl,0,wx.ALL|wx.EXPAND,5)
        self.sizer.Add(btn1, 0, wx.ALL|wx.CENTER,5)
        self.sizer.Add(btn2, 0, wx.ALL|wx.CENTER,8)
        self.panel.SetSizer(self.sizer)
        #populate table
        if city == None:
            for i in self.state_res:
                self.top.list_ctrl.InsertStringItem(self.top.index,i[0])              
                for j in range(1,len(i)):
                    self.top.list_ctrl.SetStringItem(self.top.index, j, str(i[j]))
                self.top.index += 1

        else:
            for i in self.res:
                self.top.list_ctrl.InsertStringItem(self.top.index,i[0])              
                for j in range(1,len(i)):
                    self.top.list_ctrl.SetStringItem(self.top.index, j, str(i[j]))
                self.top.index += 1
        
        #Display Results Window
        self.top.Show()
        return None
                
        

    def graph(self,event):
        #Open new .csv file...
        f = open('results.csv', 'wb')

        #Use CSV writer method to generate csv.
        if self.state == True:
                    csvwriter = csv.writer(f)
                    for i in self.state_res:
                        for j in range(1,len(i)):
                            row = [i[0] ,str(i[j])]
                            csvwriter.writerow(row)
                    f.close()
                    
                    #R to generate graph from csv!
                    r = robjects.r
                    r('''
                            source('state_vis.r')
                    ''')
                    r_graph = robjects.globalenv['graph']
                    r_graph() 
                    return None

        else:
            csvwriter = csv.writer(f)
            for i in self.res:
                for j in range(1,len(i)):
                    row = [i[0] ,str(i[j])]
                    csvwriter.writerow(row)
            f.close()
            
            #R to generate graph from csv!
            r = robjects.r
            r('''
                    source('vis.r')
            ''')
            r_graph = robjects.globalenv['graph']
            r_graph() 
            return None
        

    def resClose(self,event):
        #Closes the results window
        # calling self.query(None) here results in a bug! Cannot run the program multiple times...
        self.top.Destroy()
        return None


def main():
    app = App(False, "output")
    app.MainLoop()

main()
cur.close()
con.close()
