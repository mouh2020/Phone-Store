from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time,sqlite3,datetime
from suggestion import Suggestion
db = sqlite3.connect('store.db')
cursor = db.cursor()
#cursor.execute('''insert into historique (produit,date) values (?,?)''',('samsung m32',datetime.datetime.today().strftime('%d-%m-%y')))
#db.commit()

def get_current_date() :
    return datetime.datetime.today().strftime('%d-%m-%y')




class Frontend():
    def __init__(self,root):
        self.root = root
        self.root.title('Bechatta Phone')
        self.root.geometry('1280x720')
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('times new roman', 12,'bold'),foreground='blue')
        self.db = 'historique'
        self.root.resizable(False, False)
        self.transaction_type = StringVar()
        self.transaction_type.set('0')
        self.treeviewtype = StringVar()
        self.treeviewtype.set('stock')
        title_label = Label(self.root,bd=20,text='Bechatta Phone',fg="white",bg='blue',font=("times new roman",50,'bold'))
        title_label.pack(side=TOP,fill=X)
        self.dataframe = Frame(self.root,bd=20).place(x=0,y=130,width=1080,height=500)
        self.treeview_label= LabelFrame(self.dataframe,bd=10,padx=20,relief=RIDGE,font=("times new roman",15,'bold'),text=self.treeviewtype.get())
        self.treeview_label.place(x=500,y=130,width=580,height=500)
        self.transaction_section()
        self.admin_section()
        
        self.treeview_button_section()
        self.treeview_section()
        self.shopping_cart = [] 

    def transaction_type_check(self) :
        
        if self.transaction_type.get() == 'Facility' :
            self.customer_name_entry.config(state=NORMAL)
            self.paid_amount_entry.config(state=NORMAL)
            self.left_amount_entry.config(state=NORMAL)
            self.quantity_entry.delete(0,END)
            self.quantity_entry.insert(0,1)
            self.quantity_entry.config(state=NORMAL)
            self.left_amount_entry.config(state=DISABLED)
            self.buy_price_entry.config(state=NORMAL)
            self.checkout_name_entry.config(state=DISABLED)
            self.checkout_amount_entry.config(state=DISABLED)
            self.checkout_note_entry.config(state=DISABLED)
        elif self.transaction_type.get() == 'Retirer de caisse' :
            self.checkout_name_entry.config(state=NORMAL)
            self.checkout_amount_entry.config(state=NORMAL)
            self.checkout_note_entry.config(state=NORMAL)
            self.customer_name_entry.config(state=DISABLED)
            self.paid_amount_entry.config(state=DISABLED)
            self.left_amount_entry.config(state=DISABLED)
        else :
            self.buy_price_entry.config(state=NORMAL)
            self.quantity_entry.config(state=NORMAL)
            self.customer_name_entry.config(state=DISABLED)
            self.paid_amount_entry.config(state=DISABLED)
            self.left_amount_entry.config(state=DISABLED)
            self.checkout_name_entry.config(state=DISABLED)
            self.checkout_amount_entry.config(state=DISABLED)
            self.checkout_note_entry.config(state=DISABLED)


            
    def edit(self) :
        #values = self.treeview.item(self.treeview.focus())['values']
        data = self.treeview.item(self.treeview.focus())['values']
        data.insert(0,self.product_name.get())
        data.insert(1,self.buy_price.get())
        data.insert(2,self.sell_price.get())
        data.insert(3,self.quantity.get())
        print(data)
        cursor.execute('update stock set produit =? ,prix_d_achat = ? ,prix_de_vente = ? , quantite = ? where produit = ? and prix_d_achat = ? and prix_de_vente = ? and quantite = ?',
                       tuple(data))
        db.commit()
        self.treeviewtype.set('stock')
        self.treeview_section()
        
        

        
    def prooduct_callback(self,a=None,b=None,c=None) :
        self.query_with_suggestion(query_type='stock')
        
    def client_callback(self,a=None,b=None,c=None) :
        self.query_with_suggestion(query_type='facilite')
    def keypressed (self,event) :
        if event.keysym == 'F1' :
            
            self.buy()
        elif event.keysym == 'F2' :
            if len(self.shopping_cart) == 0 :
                self.sell()
            else:
                sum_shopping_cart = sum([sp['price'] for sp in self.shopping_cart])
                message = ''
                for sp in self.shopping_cart :
                    message+=f'\n - {sp["product"]} : {sp["price"]} '
                message+=f'\n\n -  Total : {sum_shopping_cart}'
                self.messagebox_window('Facture',message=message)
                self.shopping_cart = []
                
                
        elif event.keysym == 'F3' :      ########### shopping cart
            #self.shopping_cart.append({'product':self.product_name.get(),"price":self.sell_price.get()*self.quantity.get()})
            
            self.sell(evnt=event.keysym)
            
        elif event.keysym == 'F4' :
            self.treeview_section(product=True)
            
        elif event.keysym == 'F5' :
            self.treeviewtype.set('historique')
            self.treeview_section()
        elif event.keysym == 'F6' :
            self.treeviewtype.set('facilite')
            self.treeview_section()
        elif event.keysym == 'F7' :
            self.treeviewtype.set('retirer')
            self.treeview_section()
        elif event.keysym == 'F8' :
            self.treeviewtype.set('stock')
            self.treeview_section()
        elif event.keysym == 'F9' :
            self.query_stats()
        elif event.keysym == 'F11' :
            self.delete_record()
        elif event.keysym == 'F12' :
            self.edit()
            
            
    def transaction_section(self) :
        
        transaction_label= LabelFrame(self.dataframe,bd=10,padx=20,relief=RIDGE,font=("times new roman",15,'bold'),text='Operation')
        transaction_label.place(x=0,y=130,width=500,height=500)
        Label(transaction_label,padx=2,pady=6,relief=RIDGE,font=("times new roman",15,'bold'),text='Nom du produit').grid(row=0,column=0,sticky='nesw')
        #### product name
        self.product_name = StringVar()
        self.product_name_entry = Entry(transaction_label,relief=RIDGE,width =30,textvariable=self.product_name,font=("times new roman",15,'bold'))
        
        self.product_name_entry.grid(row=0,column=1)
        self.product_name.trace("w",self.prooduct_callback)
        suggestion = Suggestion(self.product_name_entry, dataset=list(set([product[0] for product in (cursor.execute('select produit from historique').fetchall())])))
        self.product_name_entry.focus()
        #### Keys binding
        self.root.bind("<KeyRelease>",self.keypressed)
        

        
        #### Buy price
        self.buy_price = IntVar()
        self.buy_price_entry = Entry(transaction_label,relief=RIDGE,width =30,textvariable=self.buy_price,font=("times new roman",15,'bold'))
        self.buy_price_entry.grid(row=1,column=1)
        Label(transaction_label,padx=2,pady=6,relief=RIDGE,font=("times new roman",15,'bold'),text="Prix d'achat").grid(row=1,column=0,sticky='nesw')
        #### Sell price
        self.sell_price = IntVar()
        self.sell_price_entry = Entry(transaction_label,relief=RIDGE,width =30,textvariable=self.sell_price,font=("times new roman",15,'bold'))
        self.sell_price_entry.grid(row=2,column=1)
        Label(transaction_label,padx=2,pady=6,relief=RIDGE,font=("times new roman",15,'bold'),text='Prix de vente').grid(row=2,column=0,sticky='nesw')
        #### Quantity
        self.quantity = IntVar()
        self.quantity_entry = Entry(transaction_label,relief=RIDGE,width =30,textvariable=self.quantity,font=("times new roman",15,'bold'))
        self.quantity_entry.grid(row=3,column=1)
        Label(transaction_label,padx=2,pady=6,relief=RIDGE,font=("times new roman",15,'bold'),text='Quantité').grid(row=3,column=0,sticky='nesw')
        #### Check label
        Label(transaction_label,padx=2,pady=6,relief=RIDGE,font=("times new roman",15,'bold'),text='Facilité').grid(row=5,column=0,sticky='nesw')
        Checkbutton(transaction_label,onvalue = 'Facility',variable=self.transaction_type, command=self.transaction_type_check).grid(row = 5, column = 1,sticky='w') 
        #### Customer Name
        self.customer_name = StringVar()
        self.customer_name_entry = Entry(transaction_label,state=DISABLED,relief=RIDGE,width =30,textvariable=self.customer_name,font=("times new roman",15,'bold'))
        self.customer_name_entry.grid(row=6,column=1)
        self.customer_name.trace("w",self.client_callback)
        Label(transaction_label,padx=2,pady=6,relief=RIDGE,font=("times new roman",15,'bold'),text='Nom du client').grid(row=6,column=0,sticky='nesw')
        suggestion = Suggestion(self.customer_name_entry, dataset=list(set([product[0] for product in (cursor.execute('select client from facilite').fetchall())])))
        #### Paid Amounr (Facility)
        self.paid_amount = IntVar()
        self.paid_amount_entry = Entry(transaction_label,state=DISABLED,relief=RIDGE,width =30,textvariable=self.paid_amount,font=("times new roman",15,'bold'))
        self.paid_amount_entry.grid(row=7,column=1)
        Label(transaction_label,padx=2,pady=6,relief=RIDGE,font=("times new roman",15,'bold'),text='Payé').grid(row=7,column=0,sticky='nesw')
        #### Left Amount (Facility)
        self.left_amount = IntVar()
        self.left_amount_entry =Entry(transaction_label,state=DISABLED,relief=RIDGE,width =30,textvariable=self.left_amount,font=("times new roman",15,'bold'))
        self.left_amount_entry.grid(row=8,column=1)
        Label(transaction_label,padx=2,pady=6,relief=RIDGE,font=("times new roman",15,'bold'),text='Reste').grid(row=8,column=0,sticky='nesw')
        #### Check Label
        Label(transaction_label,padx=2,pady=6,relief=RIDGE,font=("times new roman",15,'bold'),text='Retirer de caisse').grid(row=9,column=0,sticky='nesw')
        Checkbutton(transaction_label, onvalue = 'Retirer de caisse',variable=self.transaction_type, command=self.transaction_type_check).grid(row = 9, column = 1,sticky='w') 
        #### Customer Name
        self.checkout_name = StringVar()
        self.checkout_name_entry = Entry(transaction_label,state=DISABLED,relief=RIDGE,width =30,textvariable=self.checkout_name,font=("times new roman",15,'bold'))
        self.checkout_name_entry.grid(row=10,column=1)
        
        Label(transaction_label,padx=2,pady=6,relief=RIDGE,font=("times new roman",15,'bold'),text='Nom').grid(row=10,column=0,sticky='nesw')
    
        suggestion = Suggestion(self.checkout_name_entry, dataset=list(set([product[0] for product in (cursor.execute('select nom from retirer').fetchall()) ])))
        #### Checkout Amount
        self.checkout_amount = IntVar()
        self.checkout_amount_entry = Entry(transaction_label,state=DISABLED,relief=RIDGE,width =30,textvariable=self.checkout_amount,font=("times new roman",15,'bold'))
        self.checkout_amount_entry.grid(row=11,column=1)
        Label(transaction_label,padx=2,pady=6,relief=RIDGE,font=("times new roman",15,'bold'),text='La somme').grid(row=11,column=0,sticky='nesw')
        #### Checkout note
        self.checkout_note = StringVar()
        self.checkout_note_entry = Entry(transaction_label,state=DISABLED,relief=RIDGE,width =30,textvariable=self.checkout_note,font=("times new roman",15,'bold'))
        self.checkout_note_entry.grid(row=12,column=1)
        Label(transaction_label,padx=2,pady=6,relief=RIDGE,font=("times new roman",15,'bold'),text='Note').grid(row=12,column=0,sticky='nesw')
        self.transaction_button_section()

        pass

    def treeview_section(self,product=None):
        if not(self.treeviewtype.get().isdigit()) :
            self.db = self.treeviewtype.get()
            tree_view_title = self.treeviewtype.get().capitalize()
            self.treeview_label= LabelFrame(self.dataframe,bd=10,padx=20,relief=RIDGE,font=("times new roman",15,'bold'),text=tree_view_title)
            self.treeview_label.place(x=500,y=130,width=580,height=500)
            if product :
                self.treeview_show(product=True)
            else:
                self.treeview_show(product=None)
            
            
        
        
        pass


    
    def transaction_button_section(self) :
        
######################## Transaction label buttons
        transaction_label_buttons= LabelFrame(self.dataframe,bd=10,padx=20,pady=10,relief=RIDGE,font=("times new roman",15,'bold'))
        transaction_label_buttons.place(x=0,y=630,width=500,height=90)
        ################ Buttons change command None to method 
        self.buy_btn= Button(transaction_label_buttons,command=self.buy,activebackground='blue',activeforeground='white',font=('times new roman',13,'bold'),text='Acheter',height=2,width=10)
        self.buy_btn.grid(row=0,column=0,sticky='nesw')
        self.sell_btn= Button(transaction_label_buttons,command=self.sell,activebackground='blue',activeforeground='white',font=('times new roman',13,'bold'),text='Vendre',height=2,width=10)
        self.sell_btn.grid(row=0,column=1,sticky='nesw')
        self.facility_btn= Button(transaction_label_buttons,command=self.facility,activebackground='blue',activeforeground='white',font=('times new roman',13,'bold'),text='Facilité',height=2,width=10)
        self.facility_btn.grid(row=0,column=2,sticky='nesw')
        self.checkout_btn= Button(transaction_label_buttons,command=self.checkout,activebackground='blue',activeforeground='white',font=('times new roman',13,'bold'),text='Retirer',height=2,width=10)
        self.checkout_btn.grid(row=0,column=3,sticky='nesw')
  
        pass

    def query_stats(self) :
        operations = cursor.execute('select * from historique where date BETWEEN ? and ?',(self.from_date.get(),self.to_date.get())).fetchall()
        income  = 0
        expense = 0
        profite = 0
        for operation in operations :
            if operation[1] == 'achat' or operation[1] == 'retirer' :
                expense+=operation[4]
            elif operation[1] == 'vente' or operation[1] == 'facilite' :
                income+=operation[4]
                if isinstance(operation[5],int):
                    profite+=operation[5]


        message = f'\n - Revenue   : {income} \n - Déspense : {expense} \n - Profite       : {profite}\n - Produits out of stock : '
        data = cursor.execute('select produit from stock where quantite = ?',(0,)).fetchall()
        if data is not None :
          for row in data :
              message+=f'\n * {row[0]}'
        else :
            message+=f'\n * Rien'
        self.messagebox_window('Statistiques',message)
        

    def delete_record(self) :
        #self.treeview.item(self.treeview.focus())['values'][0]
        row = self.treeview.item(self.treeview.selection()[0])['values']
        if self.treeviewtype.get() == "historique" :
            if self.username.get() == '12345678' and self.password.get() == "123456789" : ### To change
                cursor.execute('delete from historique where produit = ?',(row[0],))
                
                
            else :
                self.messagebox_window('Attention',"Le responsable ne permet pas de supprimer les donnés de l'hstorique")
                return
        
        if self.treeviewtype.get() == "facilite" :
            cursor.execute('delete from facilite where client = ?',(row[0],))
            cursor.execute('insert into historique (produit,operation,date) values (?,?,?)',(row[0],"supprimé",get_current_date()))
        if self.treeviewtype.get() == "stock" :
            cursor.execute('delete from stock where produit = ?',(row[0],))
            cursor.execute('insert into historique (produit,operation,date) values (?,?,?)',(row[0],"supprimé",get_current_date()))
        if self.treeviewtype.get() == "retirer" :
            cursor.execute('delete from retirer where nom = ?',(row[0],))
            cursor.execute('insert into historique (produit,operation,date) values (?,?,?)',(row[0],"supprimé",get_current_date()))
        self.treeview.delete(self.treeview.selection()[0])
        
        db.commit()
        


        
    def treeview_button_section(self) :
        treeviewer_label_buttons= LabelFrame(self.dataframe,bd=10,padx=20,pady=10,relief=RIDGE,font=("times new roman",15,'bold'))
        treeviewer_label_buttons.place(x=500,y=630,width=580,height=90)
        Label(treeviewer_label_buttons,padx=2,pady=6,font=("times new roman",11,'bold'),text='Historique').grid(row=0,column=1,sticky='w')
        Checkbutton(treeviewer_label_buttons, onvalue = 'historique',variable=self.treeviewtype, command=self.treeview_section).grid(row = 0, column = 0,sticky='w')
        Label(treeviewer_label_buttons,padx=2,pady=6,font=("times new roman",11,'bold'),text='Retirer').grid(row=0,column=5,sticky='w')
        Checkbutton(treeviewer_label_buttons , onvalue = 'retirer',variable=self.treeviewtype, command=self.treeview_section).grid(row = 0, column = 4,sticky='w')
        Label(treeviewer_label_buttons,padx=2,pady=6,font=("times new roman",11,'bold'),text='Clients').grid(row=0,column=3,sticky='w')
        Checkbutton(treeviewer_label_buttons , onvalue = 'facilite',variable=self.treeviewtype, command=self.treeview_section).grid(row = 0, column = 2,sticky='w')
        Label(treeviewer_label_buttons,padx=2,pady=6,font=("times new roman",11,'bold'),text='Stock').grid(row=0,column=6,sticky='nesw')
        Checkbutton(treeviewer_label_buttons , onvalue = 'stock',variable=self.treeviewtype, command=self.treeview_section).grid(row = 0, column =6,sticky='w')
        self.from_date=StringVar()
        self.to_date =StringVar()        # declaring string variable
        Label(treeviewer_label_buttons,padx=2,pady=1,font=("times new roman",11,'bold'),text='De').grid(row=1,column=0,sticky='w')
        Entry(treeviewer_label_buttons,textvariable=self.from_date).grid(row=1,column=1)
        Label(treeviewer_label_buttons,padx=2,pady=1,font=("times new roman",11,'bold'),text='A').grid(row=1,column=2,sticky='w')
        Entry(treeviewer_label_buttons,textvariable=self.to_date).grid(row=1,column=3)
        Button(treeviewer_label_buttons,padx=2,pady=1,command=self.query_stats,activebackground='blue',activeforeground='white',font=('times new roman',11,'bold'),text='Statistiques',height=1,width=10).grid(row=1,column=5)
        Button(treeviewer_label_buttons,padx=2,pady=1,command=self.delete_record,activebackground='blue',activeforeground='white',font=('times new roman',11,'bold'),text='Supprimer',height=1,width=10).grid(row=1,column=6)
                
        pass

    def admin_section(self) :
        self.username = StringVar()
        self.password = StringVar()
        treeviewer_label_admin_buttons= LabelFrame(self.dataframe,bd=10,pady=5,relief=RIDGE,font=("times new roman",15,'bold'))
        treeviewer_label_admin_buttons.place(x=1080,y=630,width=200,height=90)
        Label(treeviewer_label_admin_buttons,padx=2,pady=1,font=("times new roman",10,'bold'),text='User').grid(row=0,column=0,sticky='w')
        self.username_entry = Entry(treeviewer_label_admin_buttons,textvariable=self.username)
        self.username_entry.grid(row=0,column=1)
        Label(treeviewer_label_admin_buttons,padx=2,pady=1,font=("times new roman",10,'bold'),text='Pass').grid(row=1,column=0,sticky='w')
        self.password_entry = Entry(treeviewer_label_admin_buttons,show='*',textvariable=self.password)
        self.password_entry.grid(row=1,column=1)
        Button(treeviewer_label_admin_buttons,padx=2,pady=1,command=self.clairer,activebackground='blue',activeforeground='white',font=('times new roman',10,'bold'),text='Clairer',height=1,width=10).grid(row=3,column=1)

        
    def clairer (self) :
        self.username_entry.delete(0,END)
        self.username_entry.insert(0,'')
        self.password_entry.delete(0,END)
        self.password_entry.insert(0,'')     
        
    def treeview_show(self,product=None) :
        columns = ([name[1].capitalize() for name in cursor.execute("PRAGMA table_info(" + self.db + ")").fetchall()])
        self.treeview = ttk.Treeview(self.treeview_label,height=50,columns=columns, show='headings')
        if product :
            rows = cursor.execute("SELECT * FROM " + self.db + " where produit= ?",(self.product_name.get(),)).fetchall()
        else : 
            rows = cursor.execute("SELECT * FROM " + self.db + "").fetchall()
            self.treeview.bind('<ButtonRelease-1>', self.query_with_treeview)
        
            
        
        for i in range(len(columns)) :
            self.treeview.column(columns[i].capitalize(),width=15)
            self.treeview.heading(columns[i].capitalize(),text=columns[i],anchor='w')
        for row in rows :
            self.treeview.insert("",index=0,iid=None,values=row)
        
        self.treeview.pack(fill='both',expand=True)
    def buy(self) :
        
        try :
            #### insert to stock
            #### commit to 2 tables (historique , facilite)
            if self.product_name.get() =='':
                self.messagebox_window('Produit',"La case de nom du produit est vide")
                return
            product_data = cursor.execute('select quantite from stock where produit = ? and prix_de_vente = ? and prix_d_achat = ?',
                                          (self.product_name.get(),self.sell_price.get(),self.buy_price.get())).fetchone()

            data = self.treeview.item(self.treeview.focus())['values']
            if  product_data is not None :
                data = self.treeview.item(self.treeview.focus())['values']
                data.insert(0,product_data[0]+self.quantity.get())
                data.insert(1,self.buy_price.get())
                data.insert(2,self.sell_price.get())
                cursor.execute('update stock set quantite = ?,prix_d_achat=?,prix_de_vente=? where produit = ? and prix_d_achat = ? and prix_de_vente = ? and quantite = ?'
                               ,tuple(data))
                cursor.execute('insert into historique (produit,operation,quantite,prix,totale,date) values (?,?,?,?,?,?)',
                           (self.product_name.get(),'achat',self.quantity.get(),self.buy_price.get(),self.quantity.get()*self.buy_price.get(),get_current_date()))


            else :
                cursor.execute('''insert into stock (produit,prix_d_achat,prix_de_vente,quantite) values(?,?,?,?)''',
                               (self.product_name.get(),self.buy_price.get(),self.sell_price.get(),self.quantity.get()))
                cursor.execute('''insert into historique (produit,operation,quantite,prix,totale,date) values(?,?,?,?,?,?)''',
                               (self.product_name.get(),'achat',self.quantity.get(),self.buy_price.get(),self.buy_price.get()*self.quantity.get(),get_current_date()))

            db.commit()
            self.transaction_section()
            self.treeviewtype.set('historique')
            self.treeview_section()
            
                
        except Exception as e :
            print(e)

            
    def sell(self,evnt=None) :
        

        if self.product_existance() == False :
            return   
        cursor.execute('insert into historique (produit,operation,quantite,prix,totale,date,profite) values (?,?,?,?,?,?,?)',
                           (self.product_name.get(),'vente',self.quantity.get(),self.sell_price.get(),self.quantity.get()*self.sell_price.get(),get_current_date(),(self.sell_price.get()-self.buy_price.get())*self.quantity.get()))

        left_quantity=self.product_data[0]-self.quantity.get()
        cursor.execute('update stock set quantite = ? where produit = ? and prix_d_achat = ?  ',(left_quantity,self.product_name.get(),self.buy_price.get()))
        
        db.commit()
        if evnt == "F3" :
            self.shopping_cart.append({'product':self.product_name.get(),"price":self.sell_price.get()*self.quantity.get()})
        self.transaction_section()
        self.treeviewtype.set( 'historique')
        self.treeview_section()

        
        
    def messagebox_window (self,title,message) :
        messagebox.showinfo(title,message)  

    def product_existance(self) :
        self.product_data = cursor.execute('select quantite from stock where produit = ? and prix_de_vente = ? and prix_d_achat = ?',(self.product_name.get(),self.sell_price.get(),self.buy_price.get())).fetchone()
        
        if self.product_data is None :
            self.messagebox_window('Produit', f"Pas de {self.product_name.get()} dans le stock" )
            return False
        
        elif self.product_data[0] <= 0  :
            self.messagebox_window('Quantite', f"Pas de {self.product_name.get()} dans le stock" )
            return False
        elif self.quantity.get() > self.product_data[0] :
            self.messagebox_window('Quantite', f"Il y a que {self.product_data[0]} ( {self.product_name.get()} ) dans le stock" )
            return False
        else :
            return True
            
        
    def facility(self) :
        if self.transaction_type.get() == 'Facility' :
            data = cursor.execute('select * from facilite where client = ?',(self.customer_name.get(),)).fetchone()
            if data is None :
                if self.product_existance() == False :
                    return
                cursor.execute('insert into facilite (client,produit,paye,reste,date) values (?,?,?,?,?)',
                               (self.customer_name.get(),self.product_name.get(),self.paid_amount.get(),self.sell_price.get()-self.paid_amount.get(),get_current_date()))
                cursor.execute('insert into historique (produit,operation,quantite,prix,totale,date,profite) values (?,?,?,?,?,?,?)',
                           (self.product_name.get(),'facilite',self.quantity.get(),self.sell_price.get(),self.sell_price.get(),get_current_date(),(self.sell_price.get()-self.buy_price.get())*self.quantity.get()))
                left_quantity=self.product_data[0]-self.quantity.get()
                cursor.execute('update stock set quantite = ? where produit = ? and prix_d_achat = ?',
                               (left_quantity,self.product_name.get(),self.buy_price.get()))
                
                

            else :
                ##### paid his due
                if data[3] <= 0 :
                    self.messagebox_window('Client', f"{self.customer_name.get()} est payé tout les dettes" )

                else : 
                    cursor.execute('update facilite set paye = ? , reste = ? , date = ? where client = ?',(data[2]+self.paid_amount.get(),data[3]-self.paid_amount.get(),get_current_date(),self.customer_name.get()))
                    cursor.execute('insert into historique (produit,operation,quantite,prix,totale,date) values (?,?,?,?,?,?)',
                               (self.product_name.get(),'facilite',1,self.paid_amount.get(),self.paid_amount.get(),get_current_date()))
            
                
            db.commit()
            self.transaction_section()
            self.treeviewtype.set( 'historique')
            self.treeview_section()
        
            
            
    def checkout(self) :
        if self.transaction_type.get() == 'Retirer de caisse' : 
            if isinstance(self.checkout_note.get(),str) :
                cursor.execute('insert into retirer (nom,somme,note,date) values(?,?,?,?)',(self.checkout_name.get(),self.checkout_amount.get(),self.checkout_note.get(),get_current_date()))

            else :
                cursor.execute('insert into retirer (nom,somme,date) values(?,?,?)',(self.checkout_name.get(),self.checkout_amount.get(),self.checkout_note.get(),get_current_date()))
            cursor.execute('insert into historique (produit,totale,operation,date) values(?,?,?,?)',(self.checkout_name.get(),self.checkout_amount.get(),'retirer',get_current_date()))
            
            db.commit()
            self.transaction_section()
            self.treeviewtype.set( 'historique')
            self.treeview_section()
    def query_with_treeview(self,a=None) :    
        if self.db == 'stock':
            self.product_name_entry.delete(0,END)
            self.product_name_entry.insert(0,self.treeview.item(self.treeview.focus())['values'][0])
            self.buy_price_entry.delete(0,END)
            self.buy_price_entry.insert(0,self.treeview.item(self.treeview.focus())['values'][1])
            self.sell_price_entry.delete(0,END)
            self.sell_price_entry.insert(0,self.treeview.item(self.treeview.focus())['values'][2])
            self.quantity_entry.delete(0,END)
            self.quantity_entry.insert(0,1)
        elif self.db == 'facilite' :
            self.buy_price_entry.delete(0,END)
            self.buy_price_entry.insert(0,self.treeview.item(self.treeview.focus())['values'][1])
            self.product_name_entry.delete(0,END)
            self.product_name_entry.insert(0,self.treeview.item(self.treeview.focus())['values'][1])
            self.customer_name_entry.delete(0,END)
            self.customer_name_entry.insert(0,self.treeview.item(self.treeview.focus())['values'][0])
            self.left_amount_entry.delete(0,END)
            self.left_amount_entry.insert(0,self.treeview.item(self.treeview.focus())['values'][3])
        elif self.db == 'retirer' :
            self.checkout_name_entry.delete(0,END)
            self.checkout_name_entry.insert(0,self.treeview.item(self.treeview.focus())['values'][0])

    def query_with_suggestion(self,a=None,query_type=None) :
        if query_type == 'stock' : 
            data  =  cursor.execute('select * from stock where produit = ?',(self.product_name.get(),)).fetchone()
            if data is None :
                return
            else : 
                self.buy_price_entry.delete(0,END)
                self.buy_price_entry.insert(0,data[1])
                self.sell_price_entry.delete(0,END)
                self.sell_price_entry.insert(0,data[2])
                self.quantity_entry.delete(0,END)
                self.quantity_entry.insert(0,1)
        elif query_type == 'facilite' :
            data  =  cursor.execute('select reste,produit from facilite where client = ?',(self.customer_name.get(),)).fetchone()
            if data is None :
                self.sell_price_entry.config(state=NORMAL)
                self.left_amount_entry.config(state=NORMAL)
                self.left_amount_entry.delete(0,END)
                self.left_amount_entry.insert(0,0)
                self.left_amount_entry.config(state=DISABLED)
                return
            else :
                self.left_amount_entry.config(state=NORMAL)
                
                self.left_amount_entry.delete(0,END)
                self.left_amount_entry.insert(0,data[0])
                self.product_name_entry.delete(0,END)
                self.product_name_entry.insert(0,data[1])
                self.sell_price_entry.config(state=DISABLED)
                self.left_amount_entry.config(state=DISABLED)
                
        else :
            data  =  cursor.execute('select reste from retirer where nom = ?',(self.checkout_name.get(),)).fetchone()
            if data is None :
                return
            else :
                self.checkout_name_entry.delete(0,END)
                self.checkout_name_entry.insert(0,data[0])
            
    


root=Tk()
Frontend(root)
root.mainloop()
