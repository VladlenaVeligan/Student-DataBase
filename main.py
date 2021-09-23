import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
	def __init__(self, root):
			super().__init__(root)
			self.init_main()
			self.db = db


	def init_main(self):
		self.tree = ttk.Treeview(self, columns=('ID', 'firstName', 'lastName', 'groups', 'course', 'subject', 'teacher'), height=15, show='headings')

		vsb = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
		vsb.place(x=763.5, y=83.5, height=283+20)
		
		self.tree.configure(yscrollcommand=vsb.set)	
		
		self.tree.column('ID', width=30, anchor=tk.CENTER)
		self.tree.column('firstName', width=130, anchor=tk.CENTER)
		self.tree.column('lastName', width=130, anchor=tk.CENTER)
		self.tree.column('groups', width=100, anchor=tk.CENTER)
		self.tree.column('course', width=100, anchor=tk.CENTER)
		self.tree.column('subject', width=130, anchor=tk.CENTER)
		self.tree.column('teacher', width=130, anchor=tk.CENTER)
			
		self.tree.heading('ID', text='ID')
		self.tree.heading('firstName', text='First name')
		self.tree.heading('lastName', text='Last name')
		self.tree.heading('groups', text='Group')
		self.tree.heading('course', text='Course')
		self.tree.heading('subject', text='Subject')
		self.tree.heading('teacher', text='Teacher')
		self.tree.pack(pady= 60)

		btn_show = ttk.Button(self, text='Show Table', command=self.view_records)
		btn_show.pack(side=tk.LEFT, padx = 30)

		btn_edit = ttk.Button(self, text = 'Edit', command=self.update_dialog)
		btn_edit.pack(side=tk.LEFT, padx = 30)

		btn_add = ttk.Button(self, text='Add', command=self.add_dialog)
		btn_add.pack(side=tk.LEFT, padx = 30)

		btn_delete = ttk.Button(self, text='Delete', command=self.delete_records)
		btn_delete.pack(side=tk.LEFT, padx = 30)

		btn_search = ttk.Button(self, text='Search', command=self.open_search_dialog)
		btn_search.pack(side=tk.LEFT, padx = 30)


	def records(self, firstName, lastName, groups, course, subject, teacher):
		self.db.insert_data(firstName, groups, lastName, course, subject, teacher)
		self.view_records()	
	
	def update_records(self, firstName, lastName, groups, course, subject, teacher):
		self.db.c.execute('''UPDATE student SET firstName = ?, lastName = ?, groups = ?, course = ?, subject = ?, teacher =? WHERE ID = ?''',
		                   (firstName, groups, lastName, course, subject, teacher, self.tree.set(self.tree.selection()[0], '#1')))
		self.db.conn.commit()
		self.view_records()
	
	def delete_records(self):
		for selection_item in self.tree.selection():
			self.db.c.execute('''DELETE FROM student WHERE id=?''', (self.tree.set(selection_item, '#1'), ))
		self.db.conn.commit()
		self.view_records()

	def view_records(self):
		self.db.c.execute('''SELECT * FROM student''')
		[self.tree.delete(i) for i in self.tree.get_children()]
		[self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

	def search_records(self, lastname):
		lastname = ('%' + lastname + '%',)
		self.db.c.execute('''SELECT * FROM student WHERE lastName LIKE ?''', lastname)
		[self.tree.delete(i) for i in self.tree.get_children()]
		[self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]
		
	def add_dialog(self):
		Child()

	def update_dialog(self):
		Update()	

	def open_search_dialog(self):
		Search()


class Child(tk.Toplevel):
	def __init__(self):
		super().__init__(root)
		self.init_child()
		self.view = app
			
	def init_child(self):
		self.title('Add new data')
		self.geometry('400x280+400+300')
		self.resizable(False, False)
		
		label_firstName = tk.Label(self, text='First name:')
		label_firstName.place(x=50, y=50)
		label_lastName = tk.Label(self, text='Last name:')
		label_lastName.place(x=50, y=80)
		label_groups = tk.Label(self, text='Group:')
		label_groups.place(x=50, y=110)
		label_course = tk.Label(self, text='Course:')
		label_course.place(x=50, y=140)
		label_subject = tk.Label(self, text='Subject:')
		label_subject.place(x=50, y=170)
		label_teacher = tk.Label(self, text='Teacher:')
		label_teacher.place(x=50, y=200)
		
		self.entry_firstName = ttk.Entry(self)
		self.entry_firstName.place(x=200, y=50)
		
		self.entry_lastName = ttk.Entry(self)
		self.entry_lastName.place(x=200, y=110)
		
		self.entry_groups = ttk.Entry(self)
		self.entry_groups.place(x=200, y=80)

		self.entry_course = ttk.Entry(self)
		self.entry_course.place(x=200, y=140)

		self.entry_subject = ttk.Entry(self)
		self.entry_subject.place(x=200, y=170)

		self.entry_teacher = ttk.Entry(self)
		self.entry_teacher.place(x=200, y=200)
		
		btn_cancel = ttk.Button(self, text='Close', command=self.destroy)
		btn_cancel.place(x=200, y=250)
		
		self.btn_ok = ttk.Button(self, text='Ok', command=self.destroy)
		self.btn_ok.place(x=110, y=250)
		self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_firstName.get(),
																																self.entry_lastName.get(),
																																self.entry_groups.get(),
																																self.entry_course.get(),
																																self.entry_subject.get(),
																																self.entry_teacher.get()))

																																
		self.grab_set()
		self.focus_set()		

																																
class Update(Child):
	def __init__(self):
		super().__init__()
		self.init_edit()
		self.view = app
		self.db = db
		self.default_data()

	
	def init_edit(self):
		self.title('Edit data')
		btn_edit = ttk.Button(self, text='Edit', command=self.destroy)
		btn_edit.place(x=110, y=250)
		btn_edit.bind('<Button-1>', lambda event: self.view.update_records(self.entry_firstName.get(),
                                                                          self.entry_lastName.get(),
                                                                          self.entry_groups.get(),
																																					self.entry_course.get(),
																																					self.entry_subject.get(),
																																					self.entry_teacher.get()))
		self.btn_ok.destroy()
	
	def default_data(self):
		self.db.c.execute('''SELECT * FROM student WHERE id=?''', (self.view.tree.set(self.view.tree.selection()[0], '#1' ),))
		row = self.db.c.fetchone()
		self.entry_firstName.insert(0, row[1])
		self.entry_lastName.insert(0, row[3])
		self.entry_groups.insert(0, row[2])
		self.entry_course.insert(0, row[4])
		self.entry_subject.insert(0, row[5])
		self.entry_teacher.insert(0, row[6])

class Search(tk.Toplevel):
	def __init__(self):
		super().__init__()
		self.init_search()
		self.view = app
		
	def init_search(self):
		self.title('Search data')
		self.geometry('350x120+400+300')
		self.resizable(False, False)
		
		label_search = tk.Label(self, text='Search by last lame')
		label_search.place(x=20, y=20)

		# label_search1 = ttk.Combobox(self, values=[u'First name', u'Last Name', u'Group', u'Course', u'Subject', u'Teacher'])
		# label_search1.current(0)
		# label_search1.place(x=105, y=20)

		self.entry_search = ttk.Entry(self)
		self.entry_search.place(x=155, y=20, width=150)

		btn_cancel = ttk.Button(self, text='Close', command=self.destroy)
		btn_cancel.place(x=185, y=80)

		btn_search = ttk.Button(self, text='Search')
		btn_search.place(x=100, y=80)
		btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
		btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

class DB:
	def __init__(self):
			self.conn = sqlite3.connect('student.db')
			self.c = self.conn.cursor()
			self.c.execute(
					'''CREATE TABLE IF NOT EXISTS student (id integer primary key, firstName text, lastName text, groups integer, course integer, subject text, teacher text)''')
			self.conn.commit()

	def insert_data(self, firstName, lastName, groups, course, subject, teacher):
			self.c.execute('''INSERT INTO student(firstName, lastName, groups, course, subject, teacher) VALUES (?, ?, ?, ?, ?, ?)''',
											(firstName, lastName, groups, course, subject, teacher))
			self.conn.commit()

if __name__ == "__main__":
	root = tk.Tk()
	db = DB()
	app = Main(root)
	app.pack()
	root.title("Students Data Base")
	root.geometry("782x510+300+200")
	root.resizable(False, False)
	root.mainloop()