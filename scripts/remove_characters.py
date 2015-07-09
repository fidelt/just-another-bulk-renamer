# Remove Characters script for JABR
# Author: Fidel Tamondong
# License: GNU General Public License v3

try:
  # Python 3.3
  import tkinter
except ImportError:
  # Python 2.7
  import Tkinter as tkinter
  
def init(jabr, update_newname):
  init.rename = 1
  init.update_newname = update_newname
  beg_label = tkinter.Label(jabr, text='Start From:')
  beg_label.grid(column=0, row=0, sticky='e')
  init.beg_spinbox = tkinter.Spinbox(jabr, from_=0, to=9999, command=check_inputs)
  init.beg_spinbox.grid(column=1, row=0, sticky='ew')
  init.beg_spinbox.bind("<KeyRelease>", check_inputs)
  
  end_label = tkinter.Label(jabr, text='To:')
  end_label.grid(column=0, row=1, sticky='e')
  init.end_spinbox = tkinter.Spinbox(jabr, from_=0, to=9999, command=check_inputs)
  init.end_spinbox.grid(column=1, row=1, sticky='ew')
  init.end_spinbox.bind("<KeyRelease>", check_inputs)
  
  init.from_options = ['From the Left', 'From the Right']
  init.fromvar = tkinter.StringVar()
  init.fromvar.set(init.from_options[0])
  from_optionmenu = tkinter.OptionMenu(
      jabr,
      init.fromvar,
      *init.from_options,
      command=update_filename
      )
  from_optionmenu.configure(width=15)
  from_optionmenu.grid(column=1, row=2, sticky='ew')
  
  jabr.grid_columnconfigure(1, weight=1)
  
def check_inputs(key=''):
  if init.beg_spinbox.get().isdigit() and init.end_spinbox.get().isdigit():
    init.beg_spinbox.config(bg='white')
    init.end_spinbox.config(bg='white')
    init.rename = 1
  else:
    init.beg_spinbox.config(bg='red')
    init.end_spinbox.config(bg='red')
    init.rename = 0
  init.update_newname()
    
def update_filename(string):
  from_where = init.fromvar.get()
  
  if init.rename == 0:
    return
  from_num = int(init.beg_spinbox.get())
  to_num = int(init.end_spinbox.get())
  
  if from_num < to_num:
    if from_where == init.from_options[0]:
      return string[:from_num] + string[to_num:]
    else:
      from_num = -(len(string)) if (from_num == 0) else from_num
      return string[:-(to_num)] + string[-(from_num):]