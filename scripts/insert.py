# Insert script for JABR
# Author: Fidel Tamondong
# License: GNU General Public License v3

import sys

if (sys.version_info[0] >= 3):
  # Python 3 or greater
  import tkinter
else:
  import Tkinter as tkinter
  
def init(jabr, update_newname):
  init.rename = 1
  init.update_newname = update_newname
  insert_label = tkinter.Label(jabr, text='Insert:')
  insert_label.grid(column=0, row=0, sticky='e')
  init.insert_entry = tkinter.Entry(jabr, width=1)
  init.insert_entry.grid(column=1, row=0, sticky='ew')
  init.insert_entry.bind("<KeyRelease>", update_newname)
  
  position_label = tkinter.Label(jabr, text='At position:')
  position_label.grid(column=0, row=1, sticky='e')
  init.position_spinbox = tkinter.Spinbox(jabr, from_=0, to=9999, command=check_inputs)
  init.position_spinbox.grid(column=1, row=1, sticky='ew')
  init.position_spinbox.bind("<KeyRelease>", check_inputs)
  
  init.from_options = ['From the Left', 'From the Right']
  init.fromvar = tkinter.StringVar()
  init.fromvar.set(init.from_options[0])
  from_optionmenu = tkinter.OptionMenu(
      jabr,
      init.fromvar,
      *init.from_options,
      command=update_newname
      )
  from_optionmenu.configure(width=15)
  from_optionmenu.grid(column=1, row=2, sticky='ew')
  
  jabr.grid_columnconfigure(1, weight=1)
  
def check_inputs(key=''):
  if init.position_spinbox.get().isdigit():
    init.position_spinbox.config(bg='white')
    init.rename = 1
  else:
    init.position_spinbox.config(bg='red')
    init.rename = 0
  init.update_newname()
  
def update_filename(string):
  from_where = init.fromvar.get()
  position = int(init.position_spinbox.get())
  
  if init.rename == 0:
    return
  if position > len(string):
    return string
  
  if from_where == init.from_options[0]:
    return string[0:position] + init.insert_entry.get() + string[position:len(string)]
  else:
    return string[0:len(string)-position] + init.insert_entry.get() + string[len(string)-position:len(string)]