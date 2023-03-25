import tkinter as tk
import mysql.connector,random

#main window values
main=tk.Tk()
main.title("Tax Calculator")
main.geometry("1500x1000")
main.config(bg="#86ADFF")
load=tk.Label(main,text="LOADING DATABASE",bg="#86ADFF")

taxvalues=["Regime","First Name","Last Name","Basic Salary","HRA","Special Allowance","LTA","Standard Deduction","Income from other sources"\
            
       #     "Basic Deductions - 80C",\
        #    "Medical Insurance - 80D ",\
         #   "Bank Accounts Intrest-80TTA "
            
            ]

#Tools
def connecterfxn(script,fxn):
    conn = mysql.connector.connect(host = "localhost",user = "root",passwd = "root",database = "taxcalc")
    cursor = conn.cursor()
    cursor.execute(script)
    

    if fxn=="commit":
        conn.commit()
    elif fxn=="fetchall":
        return(cursor.fetchall())



#Pages
def gotologin():
    global frame0,registerframe
    try:
        frame0.destroy()
    except:
        registerframe.destroy()
    try:
        registerframe.destroy()
    except:
        frame0.destroy()
    
    loginsection()

def registersection(id,pswrd):
    global registerframe,loginsection,taxvalues,entrylist,var1


    class taxwidgets:
        def __init__(self,i):
            self.et=tk.Entry(registerframe,width=54,justify='right')
            self.lb=tk.Label(registerframe,text=taxvalues[i],bg="#86ADFF")
    registerframe = tk.Frame(main,bg="#86ADFF")
    
    
    def finalpage(message,color):
        finalframe=tk.Frame(main,bg="#86ADFF")
        finalframe.grid(row=0,column=0,padx=(200,0))
        def tologinpage():
            finalframe.destroy()
            loginsection()
        finallabel=tk.Label(finalframe,text=message,fg=color,bg="#86ADFF")
        finallabel.grid(row=0,column=0)
        finalbutton=tk.Button(finalframe,text="TO LOGIN PAGE",command=tologinpage,bg="#34897F",fg="white")
        finalbutton.grid(row=1,column=0)


    def saver(confirmlabel):
        global confirmframe
        if confirmlabel[0]=="New Regime(2022-2023)":
            confirmlabel[0]="2"
        elif confirmlabel[0]=="Old Regime(2021-2022)":
            confirmlabel[0]="1"
        confirmlabel[0],confirmlabel[1],confirmlabel[2]="'"+confirmlabel[1]+"'","'"+confirmlabel[2]+"'",confirmlabel[0]
        confirmframe.destroy()
        
        script="insert into taxtable values("+id+","+pswrd+","
        for i in range(0,len(confirmlabel)):
            script+=confirmlabel[i]+","

        script=script[:-1]+")"
        try:
            connecterfxn(script,"commit")
            finalpage("SUCCESS","green")
        except :
            finalpage("ERROR","red")
            print("SCRIPT:",script)
    
    def confirmer(entrylist):
        global confirmframe, errormessage
        try:
            errormessage.destroy()
        except:
            pass
        valuelist=[]
        if var1.get()==1:
            valuelist.append("Old Regime(2021-2022)")
        elif var1.get()==2:
            valuelist.append("New Regime(2022-2023)")
        elif var1.get()==0:
            errormessage=tk.Label(registerframe,fg="red",text="Please enter a regime",bg="#86ADFF")
            errormessage.grid(row=0,column=2)
            return
        
        
        for i in range(len(entrylist)):
            if i<2:
                valuelist.append(entrylist[i].et.get())
                continue
            if not entrylist[i].et.get().isdigit() or int(entrylist[i].et.get())<0:
                
                errormessage=tk.Label(registerframe,fg="red",text="Please enter valid values",bg="#86ADFF")
                errormessage.grid(row=0,column=2)
                
                return
            if int(entrylist[i].et.get())>2000000000:
                    errormessage=tk.Label(registerframe,fg="red",text="Please enter values less than 20,00,00,000",bg="#86ADFF")
                    errormessage.grid(row=0,column=2)
                    return
                
            valuelist.append(entrylist[i].et.get())


        registerframe.destroy()
        confirmframe=tk.Frame(main,bg="#86ADFF")
        confirmframe.grid(row=0,column=0,padx=(200,0))
        
        

        def cancel():
            confirmframe.destroy()
            registersection(id,pswrd)

        confirmlabel=[]
        accountid=tk.Label(confirmframe,text="Account ID: "+id,bg="#86ADFF")
        pswrdid=tk.Label(confirmframe,text="Password: "+pswrd,bg="#86ADFF")
        accountid.grid(row=0,column=0)
        pswrdid.grid(row=1,column=0)
        
        for i in range(0,len(taxvalues)):
            confirmlabel.append(tk.Label(confirmframe,text=taxvalues[i]+": "+valuelist[i],bg="#86ADFF"))
            confirmlabel[i].grid(row=i+2,column=0)
            lastval=i
        cancelbutton=tk.Button(confirmframe,text="CANCEL",command=cancel,bg="#34897F",fg="white")
        cancelbutton.grid(row=lastval+3,column=0)
        confirmbutton=tk.Button(confirmframe,text="CONFIRM",command=lambda:saver(valuelist),bg="#34897F",fg="white")
        confirmbutton.grid(row=lastval+3,column=1)

        
        

            
    var1=tk.IntVar()
    
    R1 = tk.Radiobutton(registerframe,value=1, text="Old Regime(2021-2022)", variable=var1,bg="#86ADFF")
    R1.grid(row=0,column=1)
    R2 = tk.Radiobutton(registerframe,value=2, text="New Regime(2022-2023)", variable=var1,bg="#86ADFF")
    R2.grid(row=0,column=1,padx=(300,0))
    
    
    entrylist=[]
    for i in range(len(taxvalues)):
        
        entrylist.append(taxwidgets(i))
        entrylist[i].lb.grid(row=i,column=0)
        entrylist[i].et.insert(0,"0")
        entrylist[i].et.grid(row=i+1,column=1,padx=(130,0))
    entrylist[len(taxvalues)-1].et.destroy()
    entrylist.pop()
    tologinbutton=tk.Button(registerframe,text="Go back to login page",command=gotologin,bg="#34897F",fg="white")
    tologinbutton.grid(row=11,column=0,pady=10)

    save=tk.Button(registerframe,text="Save",command=lambda:confirmer(entrylist),bg="#34897F",fg="white")
    save.grid(row=11,column=1,pady=10)
    
    
    registerframe.grid()

def accountcreation():
    global accountcreationframe
    accountcreationframe=tk.Frame(main,bg="#86ADFF")
    accountcreationframe.grid(row=0,column=0,padx=(200,0))

    acclist=[]
    for i in connecterfxn("select account_number from taxtable","fetchall"):
            acclist.append(i[0])

    tester=True
    while tester:
        id=random.randint(1,9999)
        tester=id in acclist
    id=str(id)
    while len(id)<4:
        id="0"+id
        
    def gotoregestersection():
        global loginerror

        pswrd=AccountPswdEntry.get()
        try:
            loginerror.destroy()
        except:
            pass
        if pswrd.isdigit():
            if len(pswrd)==4:
                accountcreationframe.destroy()
                registersection(id,pswrd)
            else:
                loginerror=tk.Label(accountcreationframe,text="Password must have 4 digits",fg="red",bg="#86ADFF")
                loginerror.grid(row=1,column=2)
                return

            
        else:
            loginerror=tk.Label(accountcreationframe,text="Password must be numerical",fg="red")
            loginerror.grid(row=1,column=2)
            return
        
        
    AccountName=tk.Label(accountcreationframe,text="Account ID",bg="#86ADFF")
    AccountNameEntry=tk.Label(accountcreationframe,text=id,bg="#86ADFF")    
    AccountPswd=tk.Label(accountcreationframe,text="Password",bg="#86ADFF")
    AccountPswdEntry=tk.Entry(accountcreationframe)
    
    def tologinpage():
        accountcreationframe.destroy()
        loginsection()

    CreateButton=tk.Button(accountcreationframe,text="CREATE ACCOUNT",command=gotoregestersection,bg="#34897F",fg="white")
    ToLogin=tk.Button(accountcreationframe,text="LOGIN PAGE",command=tologinpage,bg="#34897F",fg="white")
    
    

    AccountName.grid(row=0,column=0,pady=(130,0))
    AccountNameEntry.grid(row=0,column=1,pady=(130,0))
    AccountPswd.grid(row=1,column=0,pady=10)    

    AccountPswdEntry.grid(row=1,column=1)
    CreateButton.grid(row=2,column=1)
    ToLogin.grid(row=2,column=0,padx=(70,0))

def graphmaker(biglist,frame,rowx,columny,paddingx,paddingy,size,specific_column_num,specific_column_size):
    global graphframe,table1,table2,graphframe2
    calculatelist=[]
    listval=0
    for i in range(len(biglist)):
        for j in range(len(biglist[i])):
            val=str(biglist[i][j])
            calculatelist.append(tk.Entry(frame,width=size,justify='center'))
            calculatelist[listval].insert(0,val)
            calculatelist[listval].grid(row=rowx+j,column=columny+i)
            calculatelist[listval].config(state="readonly")
            if j==0:
                calculatelist[listval].grid(row=rowx+j,column=columny+i,pady=paddingy)
            if i==0:
                calculatelist[listval].grid(row=rowx+j,column=columny+i,padx=paddingx)
            
            if specific_column_num:
                if i in specific_column_num:
                    calculatelist[listval].config(width=specific_column_size[specific_column_num.index(i)])
            listval+=1

def graph(id):
    global graphframe,graphframe2
    graphframe=tk.Frame(main,height=1500,width=1500,bg="#86ADFF")
    graphframe.grid_propagate(0)
    graphframe.grid()
    graphframe2=tk.Frame(graphframe,height=3000,width=3000,bg="#86ADFF")
    graphframe2.place(x=150)
    
    

    def tologin():
        graphframe.destroy()
        loginsection()
    

    def editdetails():
        for x in graphframe2.winfo_children():
            x.destroy()
        
        viewbutton.config(state=tk.NORMAL,bg="#34897F")
        editbutton.config(state=tk.DISABLED,bg="#FF897F")
        imagerybutton.config(state=tk.NORMAL,bg="#34897F")
        
        graphframe2.config(height=3000,width=3000)
        sql=connecterfxn("select * from taxtable where account_number="+str(id),"fetchall")
        sql=sql[0]
        val=list(sql[2::])

        val[0],val[1],val[2]=val[2],val[0],val[1]
        val.append(val.pop(0))
        class taxwidgets:
            def __init__(self,i):
                self.et=tk.Entry(graphframe2,width=54,justify='right')
                self.lb=tk.Label(graphframe2,text=taxvalues[i],bg="#86ADFF")
        def togotologin():
            graphframe.destroy()
            loginsection()
        
        def finalpage(message,color):
            finallabel=tk.Label(graphframe2,text=message,fg=color,bg="#86ADFF")
            finallabel.grid(row=0,column=0)
            finalbutton=tk.Button(graphframe2,text="TO LOGIN PAGE",command=togotologin,bg="#34897F",fg="white")
            finalbutton.grid(row=1,column=0)


        def updater(confirmlabel):
            if confirmlabel[0]=="New Regime(2022-2023)":
                confirmlabel[0]="2"
            elif confirmlabel[0]=="Old Regime(2021-2022)":
                confirmlabel[0]="1"
            for x in graphframe2.winfo_children():
                x.destroy()
            confirmlabel[0],confirmlabel[1],confirmlabel[2]="'"+confirmlabel[1]+"'","'"+confirmlabel[2]+"'",confirmlabel[0]
        
            script1="delete from taxtable where account_number="+str(id)+";"
            script="insert into taxtable values("+str(id)+","+str(sql[1])+","
            for i in range(0,len(confirmlabel)):
                script+=confirmlabel[i]+","

            script=script[:-1]+");"
            try:
                connecterfxn(script1,"commit")
                connecterfxn(script,"commit")
                finalpage("SUCCESS","green")
            except :
                finalpage("ERROR","red")
                print("SCRIPT:",script)
        
        def confirmer(entrylist):
            global errormessage
            try:
                errormessage.destroy()
            except:
                pass
            valuelist=[]
            if var1.get()==1:
                valuelist.append("Old Regime(2021-2022)")
            elif var1.get()==2:
                valuelist.append("New Regime(2022-2023)")
            elif var1.get()==0:
                errormessage=tk.Label(graphframe2,fg="red",text="Please enter a regime",bg="#86ADFF")
                errormessage.grid(row=0,column=2)
                return
            
            
            for i in range(len(entrylist)):
                if i<2:
                    valuelist.append(entrylist[i].et.get())
                    continue
                if not entrylist[i].et.get().isdigit() or int(entrylist[i].et.get())<0:
                    
                    errormessage=tk.Label(graphframe2,fg="red",text="Please enter valid values",bg="#86ADFF")
                    errormessage.grid(row=0,column=2)
                    
                    return
                if int(entrylist[i].et.get())>2000000000:
                    errormessage=tk.Label(graphframe2,fg="red",text="Please enter values less than 20,00,00,000",bg="#86ADFF")
                    errormessage.grid(row=0,column=2)
                    return
                valuelist.append(entrylist[i].et.get())


            
            
            for x in graphframe2.winfo_children():
                x.destroy()
        
            
            confirmlabel=[]
            accountid=tk.Label(graphframe2,text="Account ID: "+str(id),bg="#86ADFF")
            accountid.grid(row=0,column=0)
            
            for i in range(0,len(taxvalues)):
                confirmlabel.append(tk.Label(graphframe2,text=taxvalues[i]+": "+valuelist[i],bg="#86ADFF"))
                confirmlabel[i].grid(row=i+2,column=0)
                lastval=i
            confirmbutton=tk.Button(graphframe2,text="CONFIRM",command=lambda:updater(valuelist),bg="#34897F",fg="white")
            confirmbutton.grid(row=lastval+3,column=1)
            
              
        var1=tk.IntVar()
        var1.set(sql[4])
        R1 = tk.Radiobutton(graphframe2,value=1, text="Old Regime(2021-2022)", variable=var1,bg="#86ADFF")
        R1.grid(row=0,column=1)
        R2 = tk.Radiobutton(graphframe2,value=2, text="New Regime(2022-2023)", variable=var1,bg="#86ADFF")
        R2.grid(row=0,column=1,padx=(300,0))
        
        
        entrylist=[]
        for i in range(len(taxvalues)):
            
            entrylist.append(taxwidgets(i))
            entrylist[i].lb.grid(row=i,column=0)
            entrylist[i].et.insert(0,val[i])
            entrylist[i].et.grid(row=i+1,column=1,padx=(130,0))
        entrylist[len(taxvalues)-1].et.destroy()
        entrylist.pop()
        
        save=tk.Button(graphframe2,text="Save",command=lambda:confirmer(entrylist),bg="#34897F",fg="white")
        save.grid(row=11,column=1,pady=10)  
    
    #saankhya
    def imageryfxn():
        for x in graphframe2.winfo_children():
            x.destroy()
        viewbutton.config(state=tk.NORMAL,bg="#34897F")
        editbutton.config(state=tk.NORMAL,bg="#34897F")
        imagerybutton.config(state=tk.DISABLED,bg="#FF897F")
        
        graphframe2.config(height=3000,width=3000)
        sql=connecterfxn("select * from taxtable where account_number="+str(id),"fetchall")
        sql=sql[0]
        usermessage=tk.Label(graphframe2,text="Welcome "+sql[2],bg="#86ADFF",font=("Arial",20))
        usermessage.place(x=0,y=0)
        myCanvas = tk.Canvas(graphframe2, bg="#86ADFF", height=500, width=1000)

        coord = 10, 10, 300, 300
        column=100
        row=500
        square=15
        canvaslist=["red","blue","yellow","green","orange","pink"]
        for i in range(len(taxvalues[3::])):
        
            x=i*30
            
            canvaslist.append(myCanvas.create_polygon([row,column+x,row+square,column+x,row+square,column+square+x,row,column+square+x]\
                , fill=canvaslist[i]))
            
            myCanvas.create_text(row+30,column+8+x, text=taxvalues[i+3], fill="black",anchor="w",font=(10))
        total=0
        for i in sql[5::]:
            total+=i
        biglist=[]
        newsql=sql[5::]
        
        

        for i in range(len(newsql)):
            if total==0:
                break
            if i==0:
                initialvalue=0
            else:   
                initialvalue=biglist[i-1][1]+biglist[i-1][0]
            newvalue=(newsql[i]/total)*360
            
            initialvalue=int(initialvalue*10)/10
            newvalue=int(newvalue*10)/10
            
            biglist.append([initialvalue,newvalue])
        arclist=[]
        for i in range(len(newsql)):
            if total==0:
                break
            arclist.append(myCanvas.create_arc(coord, start=biglist[i][0], extent=biglist[i][1], fill=canvaslist[i]))
        
        
        myCanvas.place(x=0,y=50)
    
    def viewtable():
        for x in graphframe2.winfo_children():
            x.destroy()
        viewbutton.config(state=tk.DISABLED,bg="#FF897F")
        editbutton.config(state=tk.NORMAL,bg="#34897F")
        imagerybutton.config(state=tk.NORMAL,bg="#34897F")
        graphframe2.config(height=3000,width=3000)
        sql=connecterfxn("select * from taxtable where account_number="+str(id),"fetchall")
        sql=sql[0]
        val=list(sql[5::])
        
        finalval=0
        
        column1=list(taxvalues)
        valcopy=list(val)
        valcopy.pop()
        
        for i in valcopy:
            finalval+=i
        valcopy.append(finalval)
        val.append(finalval)
        table1=tk.Frame(graphframe2,bg="#86ADFF")
        table1.place(x=50,y=50)
        table2=tk.Frame(graphframe2,bg="#86ADFF")
        table2.place(x=50,y=190)
        table3=tk.Frame(graphframe2,bg="#86ADFF")
        table3.place(x=50,y=310)
        usermessage=tk.Label(graphframe2,text="Welcome "+sql[2],bg="#86ADFF",font=("Arial",20))
        usermessage.place(x=0,y=0)

        column1.remove("Income from other sources")
        column1.remove("Regime")
        column1.remove("First Name")
        column1.remove("Last Name")
        
        column1.append("Gross Total")
        
        box1=[["Nature"]+column1,\
            ["Amount"]+valcopy,\
            ["Exemption/Deduction"]+["Invalid-New Regime"]*6,\
            ["Taxable(New Region)"]+valcopy]
        cess=final=0
        grosstotalincome=val[6]+val[5]
        column2=["Exempt from tax",r"5% (5% of Rs 5,00,000 less Rs 2,50,000)",r"10% (10% of Rs 7,50,000 less Rs 5,00,000)",r"15% (15% of Rs 10,00,000 less Rs 7,50,000)",r"20% (20% of Rs 12,50,000 less Rs 10,00,000)",r"25% (25% of Rs 15,00,000 less Rs 12,50,000)",r"30% (30% of "+str(grosstotalincome)+ " less Rs 5,00,000)",cess,final]
        column3=[0]
        
        if grosstotalincome<250000:
            column2=8*["Exempt from tax"]+[0]
            cess="Exempt from tax"
            column3=[0]*9
            grosstotaltax=0
            
        else:
            if grosstotalincome>250000 and grosstotalincome<500000:
                startval=r"05% (5% of Rs " 
                endval=250000
                position=1
                cess=str(grosstotalincome)
            elif grosstotalincome>500000 and grosstotalincome<750000:
                startval=r"10% (10% of Rs " 
                endval=500000
                position=2
                cess="Rs 12500 + Rs "+str(grosstotalincome)
                column3.extend([12500])
            elif grosstotalincome>750000 and grosstotalincome<1000000:
                startval=r"15% (15% of Rs " 
                endval=750000
                position=3
                cess="Rs 12500 + Rs 25000 + Rs "+str(grosstotalincome)
                column3.extend([12500,25000])
            elif grosstotalincome>1000000 and grosstotalincome<1250000:
                startval=r"20% (20% of Rs " 
                endval=1000000
                position=4
                cess="Rs 12500 + Rs 25000 + Rs 37500 + Rs "+str(grosstotalincome)
                column3.extend([12500,25000,37500])
            elif grosstotalincome>1250000 and grosstotalincome<1500000:
                startval=r"25% (25% of Rs " 
                endval=1000000
                position=5
                cess="Rs 12500 + Rs 25000 + Rs 37500 + Rs 50000 + Rs "+str(grosstotalincome)
                column3.extend([12500,25000,37500,50000])
            elif grosstotalincome>1500000 :
                startval=r"30% (30% of Rs " 
                endval=1500000
                position=6
                cess="Rs 12500 + Rs 25000 + Rs 37500 + Rs 50000 + Rs 62500 + Rs "+str(grosstotalincome)
                
                column3.extend([12500,25000,37500,50000,62500])
                
            finalval=int((grosstotalincome-endval)*int(startval[:2])/100)
            column3.extend([finalval])
            addition=startval+str(grosstotalincome)+" less Rs "+str(endval)
            column2[position]=addition
            cess=r"4% of total tax (4% of "+cess
            column2=column2[:position+1]+["Exempt from tax"]*(6-position)+[cess]
            total=0
            grosstotaltax=0
            for i in column3:
                total+=i
            column3=column3+[0]*(6-position)+[int(total*0.04)]
            column2.extend([column2[-1][23:]+" + Rs "+str(column3[7])])
            for i in column3:
                grosstotaltax+=i
            
            column3=column3+[grosstotaltax]
        grosstotalincome=val[6]+val[5]
        box2=[["Nature","Income from Salary","Income from Other Sources","Gross Total Income","Total tax on above(including cess)"],\
            ["Amount",val[6],val[5],grosstotalincome,grosstotaltax]
        ]
        
        

        box3=[["Up to Rs 2,50,000","Rs 2,50,000 to Rs 5,00,000","Rs 5,00,000 to Rs 75,50,000","Rs 75,50,000 to Rs 10,00,000","Rs 10,00,000 to Rs 12,50,000","Rs 12,50,000 to Rs 15,00,000","More than Rs 15,00,000","Cess","Total Income Tax"],\
            column2,\
            column3\
        ]
        graphmaker(box1,table1,1,0,0,0,20,[],[])
        graphmaker(box2,table2,8,0,0,(20,0),20,[0],[30])
        graphmaker(box3,table3,7,0,0,(20,0),90,[0,2],[30,20])

    accountid=tk.Label(graphframe,text="Account ID: "+str(id),bg="#86ADFF")
    accountid.grid(row=0,column=0)

    loginbutton=tk.Button(graphframe,text="LOGIN PAGE",command=tologin,bg="#34897F",fg="white")
    loginbutton.grid(row=2,column=0)
    editbutton=tk.Button(graphframe,text="EDIT DETAILS",command=editdetails,bg="#34897F",fg="white")
    editbutton.grid(row=4,column=0)
    viewbutton=tk.Button(graphframe,text="View Taxtable",command=viewtable,bg="#34897F",fg="white")
    viewbutton.grid(row=3,column=0)
    
    imagerybutton=tk.Button(graphframe,text="Graph",command=imageryfxn,bg="#34897F",fg="white")
    imagerybutton.grid(row=5,column=0)

    viewbutton.invoke()
    #imagerybutton.invoke()
    graphframe.mainloop()
    
def loginsection():
    
    loginframe=tk.Frame(main,bg="#86ADFF")
    loginframe.grid(row=0,column=0,padx=(200,0))
    loginframeb=tk.Frame(loginframe,bg="#86ADFF")    
    loginframeb.grid(row=0,column=2,pady=(130,0))
    
    def accountsubmit():
        global loginerror
        
        
        try:
            loginerror.destroy()
        except:
            pass
        acclist=[]
        pswdlist=[]
        for i in connecterfxn("select account_number from taxtable","fetchall"):
            acclist.append(i[0])
        for i in connecterfxn("select password from taxtable","fetchall"):
            pswdlist.append(i[0])

        if AccountNameEntry.get()=="admin":
            if AccountPswdEntry.get()=="0000":
                loginframe.destroy()
                adminsection()

        if AccountNameEntry.get().isdigit():
            
            if AccountPswdEntry.get().isdigit():
                
                if len(AccountNameEntry.get())==4:
                    if len(AccountPswdEntry.get())==4:
                        AccountNameVar=int(AccountNameEntry.get())
                        AccountPswdVar=int(AccountPswdEntry.get())
                    else:
                        loginerror=tk.Label(loginframeb,bg="#86ADFF",text="Account Password must be 4 digits long",fg="red")
                        loginerror.grid(row=0,column=2)
                        return
                else:
                    loginerror=tk.Label(loginframeb,text="Account ID must be 4 digits long",fg="red",bg="#86ADFF")
                    loginerror.grid(row=0,column=2)
                    return
            else:
                loginerror=tk.Label(loginframeb,text="Password must be numerical",fg="red",bg="#86ADFF")
                loginerror.grid(row=0,column=2)
                return
        else:
            loginerror=tk.Label(loginframeb,text="Account ID must be numerical",fg="red",bg="#86ADFF")
            loginerror.grid(row=0,column=2)
            return

        if int(AccountNameEntry.get()) in acclist:

            if int(AccountPswdEntry.get())==pswdlist[acclist.index(int(AccountNameEntry.get()))]:
                value=AccountNameEntry.get()
                loginframe.destroy()
                graph(int(value))
                
                
            else:
                loginerror=tk.Label(loginframeb,text="Password doesn't match",fg="red",bg="#86ADFF")
                loginerror.grid(row=0,column=2)
        else:
            loginerror=tk.Label(loginframeb,text="Invalid Account ID",fg="red",bg="#86ADFF")
            loginerror.grid(row=0,column=2)

    def gotoaccountcreationsection():
        loginframe.destroy()
        accountcreation()
    AccountName=tk.Label(loginframe,text="Account ID",bg="#86ADFF")
    AccountPswd=tk.Label(loginframe,text="Password",bg="#86ADFF")
    AccountNameEntry=tk.Entry(loginframe)
    AccountPswdEntry=tk.Entry(loginframe)
    AccountSubmitButton=tk.Button(loginframe,command=accountsubmit,text="LOG IN",bg="#34897F",fg="white")
    AccountCreateButton=tk.Button(loginframe,command=gotoaccountcreationsection,text="REGISTER",bg="#34897F",fg="white")
    

    AccountName.grid(row=0,column=0,pady=(130,0))
    AccountPswd.grid(row=1,column=0,pady=10)    
    AccountNameEntry.grid(row=0,column=1,pady=(130,0))
    AccountPswdEntry.grid(row=1,column=1)
    AccountSubmitButton.grid(row=2,column=0,padx=(70,0))
    AccountCreateButton.grid(row=2,column=1)


def initialize(database,table,table_requirements):
    load.pack()
    conn = mysql.connector.connect(host = "localhost",user = "root",passwd = "root")
    cursor = conn.cursor()
    cursor.execute("show databases;")
    val=cursor.fetchall()
    for i in val:
        if i[0]==database:
            print("database exists:",i[0])
            break
    else:
        cursor.execute("create database "+database+";")
        conn.commit()
    val2=connecterfxn("show tables;","fetchall")
    for i in val2:
        if i[0]==table:
            print("table exists:",i[0])
            break
    else:
        script="create table "+table+" "+table_requirements+";"
        print("creating table:",script)
        connecterfxn(script,"commit")
    load.destroy()
    loginsection()

def adminsection():
    
    adminsectionframe=tk.Frame(main,bg="#86ADFF")
    adminsectionframe.grid()
    
    val=connecterfxn("select * from taxtable;","fetchall")
    
    def tologin():
        adminsectionframe.destroy()
        loginsection()
    
    labels=["account_number","password","first name","last name","regime","salary","hra","allowance","lta","deduction","ifos"]
    val3=[]
    for j in range(len(val[0])):
        val2=[labels[j]]
        for i in val:
            val2.append(i[j])
        val3.append(val2)
    
    graphmaker(val3,adminsectionframe,0,0,0,0,15,[],[])
    tologinbutton=tk.Button(adminsectionframe,text="LOGIN PAGE",command=tologin,bg="#34897F",fg="white")
    tologinbutton.grid(row=0,column=20)

tablereq="(account_number int(4), password int(4), name varchar(11),lastname varchar(11), regime int(11), salary int, hra int, allowance int, lta int, deduction int, ifos int)"
initialize("taxcalc","taxtable",tablereq)
#adminsection()
#graph(9465)
#accountcreation()
#calculatorsection()
#loginsection()
#registersection("0001","0000")
main.mainloop() 