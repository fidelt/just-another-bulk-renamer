#!/usr/bin/env python

#  Just Another Bulk Renamer
#  A simple bulk-renaming tool inspired by Thunar's Bulk Renamer
#
#  Copyright (C) 2014  Genes Fidel Tamondong <fidel.tamondong@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import sys
import traceback

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

class Main(tkinter.Tk):
  def __init__(self, parent):
    tkinter.Tk.__init__(self, parent)
    self.parent = parent
    self.initialize()
    
  def initialize(self):
    self.file_list = [] # FORMAT: [Filename, Full Path]
    self.err = ''
    self.ver = "0.9"
    self.grid()
    
    # About
    self.about = tkinter.Toplevel()
    self.about.title('About')
    self.about.resizable(0, 0)
    self.about.protocol('WM_DELETE_WINDOW', self.about_hide)
    if os.name == 'nt':
      self.about.attributes('-toolwindow', 1)
    self.about.withdraw()
    
    self.about_grp = tkinter.LabelFrame(self.about, padx=5, pady=10, borderwidth=0)
    self.about_grp.grid(column=0, row=0, sticky='news')
    
    about_ver_label = tkinter.Label(self.about_grp, text='Version:')
    about_ver_label.grid(column=0, row=0, sticky='e')
    about_ver = tkinter.Label(self.about_grp, text=self.ver)
    about_ver.grid(column=1, row=0, sticky='w')
    
    about_author_label = tkinter.Label(self.about_grp, text='Author:')
    about_author_label.grid(column=0, row=1, sticky='e')
    about_author = tkinter.Label(self.about_grp, text='Genes Fidel Tamondong')
    about_author.grid(column=1, row=1, sticky='w')
    
    self.about_grp.grid_columnconfigure(0, weight=1)
    self.about_grp.grid_columnconfigure(1, weight=1)
    self.about.grid_columnconfigure(0, weight=1)
    
    # Add, Remove, Clear & About Buttons
    add_files_btn = tkinter.Button(self, text='Add', command=self.add_files, width=6)
    add_files_btn.grid(column=0, row=0, sticky='w')
    
    rem_files_btn = tkinter.Button(self, text='Remove', command=self.remove_files, width=6)
    rem_files_btn.grid(column=1, row=0, sticky='w')
    
    clr_files_btn = tkinter.Button(self, text='Clear', command=self.clear_files, width=6)
    clr_files_btn.grid(column=2, row=0, sticky='w')
    
    abt_btn = tkinter.Button(self, text='About', command=self.about_show, width=6)
    abt_btn.grid(column=19, row=0, columnspan=2, sticky='e')
    
    # Before & After Listboxes
    self.oldname_lstbx = tkinter.Listbox(selectmode='extended', exportselection=0, width=28)
    self.oldname_lstbx.grid(column=0, row=1, columnspan=10, sticky='news')
    self.oldname_lstbx.bind('<<ListboxSelect>>', self.sync_selection)
    
    self.newname_lstbx = tkinter.Listbox(selectmode='extended', exportselection=0, width=28)
    self.newname_lstbx.grid(column=10, row=1, columnspan=10, sticky='news')
    self.newname_lstbx.bind('<<ListboxSelect>>', self.sync_selection)
    
    self.y_scrollbar = tkinter.Scrollbar(orient='vertical', command=self.yscroll)
    self.y_scrollbar.grid(column=20, row=1, sticky='nes')
    self.oldname_lstbx.configure(yscrollcommand=self.scrollsync_1)
    self.newname_lstbx.configure(yscrollcommand=self.scrollsync_2)
    
    # Rename Options Group
    self.rename_options = ['Letter Case']
    self.load_scripts()
    self.rename_var = tkinter.StringVar()
    self.rename_var.set(self.rename_options[0])
    rename_optionmenu = tkinter.OptionMenu(
        self,
        self.rename_var,
        *self.rename_options,
        command=self.show_group
        )
    rename_optionmenu.configure(width=10)
    rename_optionmenu.grid(column=0, row=2, columnspan=10, sticky='news', padx=(5, 0))
    
    # Filename & Extension Group
    self.file_options = ['Filename Only', 'Extension Only', 'Filename & Extension']
    self.file_var = tkinter.StringVar()
    self.file_var.set(self.file_options[0])
    file_optionmenu = tkinter.OptionMenu(
        self,
        self.file_var,
        *self.file_options,
        command=self.update_newname
        )
    file_optionmenu.configure(width=10)
    file_optionmenu.grid(column=11, row=2, columnspan=10, sticky='news', padx=(0, 5))
    
    # Default: Letter Case
    self.lettercase_grp = tkinter.LabelFrame(self, padx=5, pady=5)
    self.lettercase_grp.grid(column=0, row=3, columnspan=21, sticky='news', padx=5, pady=5)
    
    case_label = tkinter.Label(self.lettercase_grp, text='Case:')
    case_label.grid(column=0, row=0, sticky='e')
    self.case_options = ['Capitalization', 'lower case', 'UPPER CASE']
    self.case_var = tkinter.StringVar()
    self.case_var.set(self.case_options[0])
    case_optionmenu = tkinter.OptionMenu(
        self.lettercase_grp,
        self.case_var,
        *self.case_options,
        command=self.update_newname
        )
    case_optionmenu.config(width=15)
    case_optionmenu.grid(column=1, row=0, sticky='w')
    
    # Initialize module group
    self.module_grp = tkinter.LabelFrame(self, padx=5, pady=5)
    
    # Rename Button
    self.rename_btn = tkinter.Button(self, text='Rename', command=self.rename)
    self.rename_btn.config(state='disabled')
    self.rename_btn.grid(column=19, row=4, columnspan=2, sticky='e', padx=5, pady=(0, 5))
    
    # Makes the two Listboxes stretch
    self.grid_columnconfigure(9, weight=1)
    self.grid_columnconfigure(19, weight=1)
    self.grid_rowconfigure(1, weight=1)
    
  def show_error(self):
    msgbox = messagebox
    msgbox.showerror('Error', self.err)
    self.err = ''
    
  def log_error(self, err):
    err_log = open(self.getpath(self.jabr_loc(), 'Error.log'), 'w')
    err_log.write(
        "Just Another Bulk Renamer {0} (Python {1}.{2}.{3}):\n".format(
            self.ver,
            sys.version_info[0],
            sys.version_info[1],
            sys.version_info[2]
            )
        )
    err_log.write(err)
    err_log.close()
    
  def getpath(self, path, file):
    path = os.path.realpath(path)
    path = os.path.join(os.path.dirname(path), file)
    return path.replace('\\', '/')
    
  def jabr_loc(self):
    # Returns dir path to this running application
    if getattr(sys, 'frozen', False):
      return sys.executable
    else:
      return __file__
    
  def get_scripts(self):
    # Returns a list of scripts in 'scripts' directory
    scripts = []
    try:
      files = os.listdir(self.getpath(self.jabr_loc(), 'scripts'))
      for file in files:
        if file.endswith('.py'):
          scripts.append(file)
    except OSError:
      pass
    return scripts
    
  def split_filename(self, file):
    return os.path.splitext(file)
    
  def load_scripts(self):
    # Loads the list of scripts and adds them to self.rename_options
    errlog = ''
    scripts = self.get_scripts()
    self.modules = [0] * len(scripts)
    systempath = list(sys.path)
    sys.path.insert(0, self.getpath(self.jabr_loc(), 'scripts'))
    for i in range (0, len(scripts)):
      try:
        script = self.split_filename(scripts[i])[0]
        self.modules[i] = __import__(script)
      except (TypeError, ImportError):
        errlog += "{0}\n".format(traceback.format_exc())
        self.err = "Unable to load all scripts.\n" + \
                   "See Error.log for more information."
        scripts.pop(i)
        i -= 1
    if errlog:
      self.log_error(errlog)
    sys.path[:] = systempath
    
    for script in scripts:
      script = self.split_filename(script)[0]
      script = self.format_script(script)
      self.rename_options.append(script)
    
  def capitalize(self, match):
    return match.group().upper()
    
  def format_script(self, script):
    # Formats filename of script for readability
    if re.search("[_-]", script):
      script = re.sub("([_-])", ' ', script)
    elif re.search("^[a-z]", script):
      script = re.sub("(^[a-z])", self.capitalize, script)
    elif re.search("[' '][a-z]", script):
      script = re.sub("([' '][a-z])", self.capitalize, script)
    elif re.search("[a-z][A-Z]", script):
      script = re.sub("([a-z])([A-Z])", "\g<1> \g<2>", script)
    elif re.search("[A-Z][A-Z]", script):
      script = re.sub("([A-Z])([A-Z])", "\g<1> \g<2>", script)
    else:
      script = ' '.join(script.split())
      return script
    script = self.format_script(script)
    return script
    
  def delduplicates(self, oldlist, newlist):
    # Checks for duplicates and removes them from files to be added
    duplicates = set(oldlist).intersection(set(newlist))
    for item in newlist:
      if item in duplicates:
        del newlist[newlist.index(item)]
    
  def rename_status(self, duplicates):
    # Disables Rename button if the newname listbox is empty
    # or if there are duplicate outputs in the newname listbox
    if (self.newname_lstbx.size() == self.newname_blanks) or (duplicates):
      self.rename_btn.config(state='disabled')
    else:
      self.rename_btn.config(state='normal')
    
  def yscroll(self, *args):
    self.oldname_lstbx.yview(*args)
    self.newname_lstbx.yview(*args)
    
  def sync_selection(self, evt):
    # Gets the active Listbox selection,
    # clears the selected values in the other Listbox,
    # then finally adds the active selection to the other Listbox
    event = evt.widget
    curselection = event.curselection()
    if curselection == self.oldname_lstbx.curselection():
      for i in self.newname_lstbx.curselection():
        self.newname_lstbx.selection_clear(i)
    elif curselection == self.newname_lstbx.curselection():
      for i in self.oldname_lstbx.curselection():
        self.oldname_lstbx.selection_clear(i)
    for i in curselection:
      self.newname_lstbx.selection_set(i)
      self.oldname_lstbx.selection_set(i)
    
  def scrollsync_1(self, *args):
    if self.oldname_lstbx.yview() != self.newname_lstbx.yview():
      self.newname_lstbx.yview_moveto(args[0])
    self.y_scrollbar.set(*args)
    
  def scrollsync_2(self, *args):
    if self.newname_lstbx.yview() != self.oldname_lstbx.yview():
      self.oldname_lstbx.yview_moveto(args[0])
    self.y_scrollbar.set(*args)
    
  def default_rename_option(self):
    self.rename_var.set(self.rename_options[0])
    self.show_group(self.rename_options[0])
    
  def update_filename(self, ren_index, string):
    # Updates Filename through calling respective functions
    errlog = ''
    if ren_index == 0:
      # DEFAULT: Letter Case
      return self.changecase(string)
    else:
      try:
        return self.modules[ren_index-1].update_filename(string)
      except AttributeError:
        errlog += "{0}\n".format(traceback.format_exc())
        self.show_error("Error found in 'update_filename' attribute of '{0}' module.\n" \
                        "See Error.log for more information.".format(self.rename_var.get()))
        self.log_error(errlog)
        self.default_rename_option()
    
  def changecase(self, string):
    case_index = self.case_options.index(self.case_var.get())
    if case_index == 0:
      return string.title()
    elif case_index == 1:
      return string.lower()
    elif case_index == 2:
      return string.upper()
    
  def get_uniques(self, filenames):
    tmp = []
    for file in filenames:
      if file not in tmp:
        tmp.append(file)
      else:
        filenames = [val for val in filenames if val != file]
    return filenames
    
  def cleanup(self, module):
    index = self.rename_options.index(module)
    if index != 0:
      try:
        self.modules[index-1].cleanup()
      except AttributeError:
        pass
    
  def update_newname(self, *args):
    # Updates newname listbox based on selected rename option specification/s
    
    # Clears listbox selection and gets renaming configuration
    new_filenames = []
    duplicates = 0
    self.newname_blanks = 0
    self.oldname_lstbx.selection_clear(0, self.oldname_lstbx.size())
    self.newname_lstbx.selection_clear(0, self.newname_lstbx.size())
    ren_index = self.rename_options.index(self.rename_var.get())
    file_index = self.file_options.index(self.file_var.get())
    self.newname_lstbx.delete(0, self.newname_lstbx.size())
    
    # Gets specified part of filename then sends it out to be updated
    try:
      for file in self.file_list:
        if file_index == 0:
          # Filename Only
          prefix, suffix = self.split_filename(file[0])
          newfile = self.update_filename(ren_index, prefix) + suffix
        elif file_index == 1:
          # Extension Only
          prefix, suffix = self.split_filename(file[0])
          newfile = prefix + self.update_filename(ren_index, suffix)
        elif file_index == 2:
          # Filename & Extension
          newfile = self.update_filename(ren_index, file[0])
        new_filenames.append(newfile)
        
      # Adds updated filename to newName listbox, blank if no change
      uniques = self.get_uniques(new_filenames)
      for i in range (0, len(self.file_list)):
        if (self.file_list[i][0] != new_filenames[i]) or (new_filenames[i] not in uniques):
          self.newname_lstbx.insert(i, new_filenames[i])
          self.newname_blanks -= 1
          if new_filenames[i] not in uniques:
            self.newname_lstbx.itemconfig(i, fg='red')
            duplicates = 1
        else:
          self.newname_lstbx.insert(len(self.file_list), '')
          self.newname_blanks += 1
        
      if self.newname_blanks < 0:
        self.newname_blanks = 0
    except TypeError:
      pass
      
    self.oldname_lstbx.yview(self.oldname_lstbx.size())
    self.newname_lstbx.yview(self.newname_lstbx.size())
    self.cleanup(self.rename_var.get())
    self.rename_status(duplicates)
    
  def add_files(self):
    errlog = ''
    try:
      open = tkinter.Tk()
      open.withdraw()
      newfiles = filedialog.askopenfilenames()
      newfiles = self.tk.splitlist(newfiles)
    except Exception:
      errlog += "{0}\n".format(traceback.format_exc())
      self.err = "Unable to add all files.\n" + \
                 "See Error.log for more information."
      self.log_error(errlog)
    finally:
      filelistpaths = []
      for file in self.file_list:
        filelistpaths.append(file[1])
      newfiles = list(newfiles)
      self.delduplicates(filelistpaths, newfiles)
      
      for file in newfiles:
        self.oldname_lstbx.insert(len(self.file_list), os.path.basename(file))
        self.file_list.append([os.path.basename(file), file])
      self.update_newname()
      open.destroy()
    
  def remove_files(self):
    try:
      del self.file_list[int(self.oldname_lstbx.curselection()[0])]
      self.newname_lstbx.delete(self.newname_lstbx.curselection()[0])
      self.oldname_lstbx.delete(self.oldname_lstbx.curselection()[0])
      self.remove_files()
      self.update_newname()
    except IndexError:
      pass
    
  def clear_files(self):
    self.file_list = []
    self.newname_blanks = 0
    self.oldname_lstbx.delete(0, self.oldname_lstbx.size())
    self.newname_lstbx.delete(0, self.newname_lstbx.size())
    self.rename_btn.config(state='disabled')
    
  def show_group(self, grp_name):
    # Shows corresponding Rename Options group
    errlog = ''
    index = self.rename_options.index(grp_name)
    if index == 0:
      # DEFAULT: Letter Case
      self.module_grp.destroy()
      self.lettercase_grp.grid(column=0, row=3, columnspan=21, sticky='news', padx=5, pady=5)
    else:
      self.module_grp.destroy()
      self.module_grp = tkinter.LabelFrame(self, padx=5, pady=5)
      self.module_grp.grid(column=0, row=3, columnspan=21, sticky='news', padx=5, pady=5)
      try:
        self.modules[index-1].init(self.module_grp, self.update_newname)
      except AttributeError:
        errlog += "{0}\n".format(traceback.format_exc())
        self.show_error("Error found in 'init' attribute of '{0}' module.\n" \
                        "See Error.log for more information.".format(grp_name))
        self.log_error(errlog)
        self.default_rename_option()
    self.update_newname()
    
  def newname_availability(self, newname_lst):
    # Checks if candidate newname is an existing file
    errlog = ''
    for i in range (0, len(newname_lst)):
      newname = self.getpath(self.file_list[i][1], newname_lst[i])
      directory, filename = os.path.split(newname)
      if filename in os.listdir(directory):
        errlog += "'{0}' already exists.\n".format(newname)
        self.err = "All files were not renamed.\n" + \
                   "See Error.log for more information."
      
    if errlog:
      self.log_error(errlog)
      self.show_error()
      return 1
    
  def rename(self):
    errlog = ''
    newname_lst = list(self.newname_lstbx.get(0, self.newname_lstbx.size()))
    file_exists = self.newname_availability(newname_lst)
    if file_exists:
      return
    self.oldname_lstbx.delete(0, self.oldname_lstbx.size())
    self.newname_lstbx.delete(0, self.newname_lstbx.size())
    for i in range (0, len(newname_lst)):
      try:
        if newname_lst[i]:
          os.rename(self.file_list[i][1], self.getpath(self.file_list[i][1], newname_lst[i]))
          self.file_list[i][0] = newname_lst[i]
          self.file_list[i][1] = self.getpath(self.file_list[i][1], newname_lst[i])
          self.oldname_lstbx.insert(len(self.file_list), newname_lst[i])
        else:
          self.oldname_lstbx.insert(len(self.file_list), self.file_list[i][0])
      except OSError as error:
        errlog += "'{0}' was not renamed: {1}\n".format(self.file_list[i][1], str(error))
        self.err = "Not all files were renamed.\n" + \
                   "See Error.log for more information."
        self.newname_lstbx.delete(newname_lst.index(newname_lst[i]))
        self.file_list.pop(newname_lst.index(newname_lst[i]))
        newname_lst.pop(newname_lst.index(newname_lst[i]))
        i -= 1
    
    if errlog:
      self.log_error(errlog)
      self.show_error()
    self.update_newname()
    
  def about_show(self):
    self.about.geometry(
        "{0}x{1}+{2}+{3}".format(
            240,
            200,
            self.winfo_x() + int(self.winfo_width()/2) - 120,
            self.winfo_y() + int(self.winfo_height()/2) - 100
            )
        )
    self.about.deiconify()
    
  def about_hide(self):
    self.about.withdraw()
    
if __name__ == "__main__":
  app = Main(None)
  app.title("Just Another Bulk Renamer")
  app.minsize(480, 400)
  if app.err:
    app.show_error()
  app.mainloop()