# Replace script for JABR
# Author: Fidel Tamondong
# License: GNU General Public License v3

import re

try:
  # Python 3.3
  import tkinter
except ImportError:
  # Python 2.7
  import Tkinter as tkinter
  
def init(jabr, update_newname):  
  replace_label = tkinter.Label(jabr, text='Replace:')
  replace_label.grid(column=0, row=0, sticky='e')
  init.replace_entry = tkinter.Entry(jabr, width=1)
  init.replace_entry.grid(column=1, row=0, sticky='ew')
  init.replace_entry.bind("<KeyRelease>", update_newname)
  
  init.regxvar = tkinter.IntVar()
  regx_chkbx = tkinter.Checkbutton(jabr, text='Regex', variable=init.regxvar, command=update_newname)
  regx_chkbx.grid(column=2, row=0, sticky='w')
  
  with_label = tkinter.Label(jabr, text='With:')
  with_label.grid(column=0, row=1, sticky='e')
  init.withentry = tkinter.Entry(jabr, width=1)
  init.withentry.grid(column=1, row=1, sticky='ew')
  init.withentry.bind("<KeyRelease>", update_newname)
  
  jabr.grid_columnconfigure(1, weight=1)
  
def update_filename(string):
  regx = init.regxvar.get()
  bfore = init.replace_entry.get()
  after = init.withentry.get()
  if not bfore:
    return string
  
  if regx:
    try:
      return re.sub(bfore, after, string)
    except re.error:
      return string
  else:
    return string.replace(bfore, after)