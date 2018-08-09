from tkinter import *
import sqlite3 as sq


class BookStore:
    
    def __init__(self,master):
        self.master = master
        master.title("BookStore")
        master.geometry("400x250")
        
        
        master.grid_rowconfigure(index = (0,1,2,3,4,5,6,7,8,9),weight = 1)
        master.grid_columnconfigure(index = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23),weight = 1)
        
        self.title = StringVar()
        self.Author = StringVar()
        self.Year = StringVar()
        self.isbn = StringVar()
        self.Details = StringVar()
        
        
        self.label1 = Label(master,text = "Title")
        self.label1.grid(row = 0,column = 0)
        
        self.label1 = Label(master,text = "Year")
        self.label1.grid(row = 1,column = 0)
        
        self.label1 = Label(master,text = "Author")
        self.label1.grid(row = 0,column = 10,sticky = E)
        
        self.label1 = Label(master,text = "ISBN")
        self.label1.grid(row = 1,column = 10,sticky  = E)
        
        self.entry_title = Entry(master,bd =10,justify = LEFT,textvariable = self.title,fg = "red")
        self.entry_title.grid(row  = 0,column = 1)
        
        self.entry_year = Entry(master,bd =10,justify = LEFT,textvariable = self.Year,fg = "red")
        self.entry_year.grid(row  = 1,column = 1)
        
        self.entry_author = Entry(master,bd =10,justify = LEFT,textvariable = self.Author,fg = "red")
        self.entry_author.grid(row  = 0,column = 12)
        
        self.entry_isbn = Entry(master,bd =10,justify = LEFT,textvariable = self.isbn,fg = "red")
        self.entry_isbn.grid(row  = 1,column = 12)
        
        self.list1 = Listbox(master,height = 10,width = 30,cursor = "hand1")
        self.list1.grid(row = 2,column = 0,rowspan = 10,columnspan = 2)
        self.list1.bind("<<ListboxSelect>>",self.get_selcted)
                        
        self.scrollbar_v = Scrollbar(master,bg = "blue",activebackground = "#45f46b")
        self.scrollbar_v.grid(row = 2,column = 2,rowspan = 10)        
        self.scrollbar_v.config(command = self.list1.yview)
        self.list1.config(yscrollcommand = self.scrollbar_v.set)
        
        self.scrollbar_h = Scrollbar(master,orient = HORIZONTAL)
        self.scrollbar_h.grid(row = 13,column = 1)        
        self.scrollbar_h.config(command = self.list1.xview)
        self.list1.config(xscrollcommand = self.scrollbar_h.set)

        
        
        self.view_all = Button(master,text = "View All",width = 10,cursor = "hand2",command = self.viewAll)
        self.view_all.grid(row = 4,column = 12,sticky = E)
        
        self.search_entry = Button(master,text = "Search Entry",cursor = "hand2",command = self.searchEntry)
        self.search_entry.grid(row = 5,column = 12,sticky = E)
        
        self.add_entry = Button(master,text = "Add Entry",cursor = "hand2",command = self.addEntry)
        self.add_entry.grid(row = 6,column = 12,sticky = E)
        
        self.update_selected = Button(master,text = "Update Selected",cursor = "hand2",command = self.updateSelected)
        self.update_selected.grid(row = 7,column = 12,sticky = E)
        
        self.delete_selected = Button(master,text = "Delete_Selected",cursor = "hand2",command = self.del_selected)
        self.delete_selected.grid(row = 8,column = 12,sticky = E)
        
        self.clear = Button(master,text = "Clear All",cursor = "hand2",command = self.clearAll)
        self.clear.grid(row = 13,column = 12,sticky = E)

        
        
    def viewAll(self):
        sql_query = "Select * from store ;"
        data = self.sqlEntry(sql_query,receive = True)
        self.list1.delete(0, END)
        for dat in  data:
            self.list1.insert(0,dat)
            
        
    def searchEntry(self):
        #self.clearAll()
        sql_query = "Select * from store where isbn = ? or title = ? or author = ? or isbn = ? ;"
        tup = (self.entry_isbn.get(),self.title.get(),self.Author.get(),self.Year.get())
        data = self.sqlEntry(sql_query,tup, receive = True)
        self.list1.delete(0, END)
        for row in data:
            self.list1.insert(0,row)
        
    def addEntry(self):
        sql_query = "Create table if not exists store (isbn integer primary key,title text,author text,year integer);"
        self.sqlEntry(sql_query)
        if self.title.get() != "" and self.Author.get() != "" and self.isbn.get() != "" and self.Year.get() != "" :
            sql = "Insert into store values(?,?,?,?);"
            params = (self.isbn.get(),self.title.get(),self.Author.get(),self.Year.get())
            self.sqlEntry(sql, data = params, receive = False)
        
        
    def updateSelected(self):
        sql_query = "Update store set author = ? title = ? year = ? where isbn = ?"
        params = (self.Author.get(),self.title.get(),self.Year.get(),self.selected[0])
        self.sqlEntry(sql_query,params)
        
    def del_selected(self):
         sql_query = "Delete from store where isbn = ?"
         params = (self.selected[0],)
         self.sqlEntry(sql_query, params)
            
        
    def clearAll(self):
        self.list1.delete(0,END)
        self.entry_author.delete(0,END)
        self.entry_isbn.delete(0,END)
        self.entry_title.delete(0,END)
        self.entry_year.delete(0,END)
            
    def sqlEntry(self,sql_query,data = None,receive = False):
        conn = sq.connect("BookStore.db")
        cursor = conn.cursor()
        if data:
            cursor.execute(sql_query,data)
        else:
            cursor.execute(sql_query)
            
        if receive:
            return cursor.fetchall()
        else:
            conn.commit()
            
        conn.close()

    def get_selcted(self,event):
        try:
            index =self.list1.curselection()[0]
            self.selected = self.list1.get(index)
            self.entry_isbn.delete(0, END)
            self.entry_isbn.insert(0, self.selected[0])
            self.entry_title.delete(0, END)
            self.entry_title.insert(0, self.selected[1])
            self.entry_author.delete(0, END)
            self.entry_author.insert(0, self.selected[2])
            self.entry_year.delete(0, END)
            self.entry_year.insert(0, self.selected[3])
        except IndexError as e:
            pass
        
        
        
root = Tk()
bookstore = BookStore(root)
root.mainloop()