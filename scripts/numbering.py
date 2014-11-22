# Numbering script for JABR
# Author: Fidel Tamondong

try:
  # Python 3.3
  import tkinter
  import tkinter.filedialog as filedialog
  import tkinter.messagebox as messagebox
except ImportError:
  # Python 2.7
  import Tkinter as tkinter
  import tkFileDialog as filedialog
  import tkMessageBox as messagebox
  
def init(jabr, update_newname):
  init.update_newname = update_newname
  
  numformat_label = tkinter.Label(jabr, text='Numbering:')
  numformat_label.grid(column=0, row=0, sticky='e')
  init.numformat_options = ['1, 2, 3...',
                            '01, 02, 03...',
                            '001, 002, 003...',
                            '0001, 0002, 0003...']
  init.numvar = tkinter.StringVar()
  init.numvar.set(init.numformat_options[0])
  numformat_optionmenu = tkinter.OptionMenu(jabr,
                                            init.numvar,
                                            *init.numformat_options,
                                            command=update_newname)
  numformat_optionmenu.configure(width=15)
  numformat_optionmenu.grid(column=1, row=0, sticky='w')
  
  start_label = tkinter.Label(jabr, text='Start With:')
  start_label.grid(column=2, row=0, sticky='e')
  init.startentry = tkinter.Entry(jabr, width=1)
  init.startentry.grid(column=3, row=0, sticky='ew')
  init.startentry.bind("<KeyRelease>", check_startentry)
  init.startentry.insert(0, '1')
  
  strformat_label = tkinter.Label(jabr, text='Filename:')
  strformat_label.grid(column=0, row=1, sticky='e')
  init.strformat_options = ['OldName Text Number',
                            'Number Text OldName',
                            'Text Number',
                            'Number Text']
  init.strvar = tkinter.StringVar()
  init.strvar.set(init.strformat_options[0])
  strformat_optionmenu = tkinter.OptionMenu(jabr,
                                            init.strvar,
                                            *init.strformat_options,
                                            command=update_newname)
  strformat_optionmenu.configure(width=20)
  strformat_optionmenu.grid(column=1, row=1, sticky='w')
  
  txt_label = tkinter.Label(jabr, text='Text:')
  txt_label.grid(column=2, row=1, sticky='e')
  init.txtentry = tkinter.Entry(jabr, width=1)
  init.txtentry.grid(column=3, row=1, sticky='ew')
  init.txtentry.bind("<KeyRelease>", update_newname)
  
  jabr.grid_columnconfigure(3, weight=1)
  
  init.counter = init.startentry.get()
  init.rename = 1
  
def update_filename(string):
  if init.rename == 0:
    return
  numf_index = init.numformat_options.index(init.numvar.get())
  strf_index = init.strformat_options.index(init.strvar.get())
  text = init.txtentry.get()
  
  if numf_index == 0:
    init.counter = "%01d" % (int(init.counter),)
  elif numf_index == 1:
    init.counter = "%02d" % (int(init.counter),)
  elif numf_index == 2:
    init.counter = "%03d" % (int(init.counter),)
  elif numf_index == 3:
    init.counter = "%04d" % (int(init.counter),)
  
  if strf_index == 0:
    filename = [string, text, str(init.counter)]
  elif strf_index == 1:
    filename = [str(init.counter), text, string]
  elif strf_index == 2:
    filename = [text, str(init.counter)]
  elif strf_index == 3:
    filename = [str(init.counter), text]
  filename = ''.join(filter(None, filename))
  init.counter = int(init.counter) + 1
  return str(filename)
  
def check_startentry(key):
  if init.startentry.get().isdigit():
    init.rename = 1
    init.startentry.config(bg='white')
    init.counter = init.startentry.get()
  else:
    init.rename = 0
    init.startentry.config(bg='red')
  init.update_newname()
  
def cleanup():
  init.counter = init.startentry.get()