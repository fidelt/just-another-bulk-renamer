### Just Another Bulk Renamer
***
A simple bulk-renaming tool inspired by Thunar's Bulk Renamer

### Creating Scripts
***
JABR is extensible. It works by first searching for `.py` and `.pyc` files from the `scripts` directory and importing them.
The script's functions will then be called by JABR whenever it is needed.

When creating a script for JABR, it **must** have the following functions:
- `init(jabr, update_newname)`
 - This is called whenever your script is selected. It's primary use is to provide JABR with the UI of your script.
 It takes two parameters. `jabr` and `update_newname`. Use `jabr` to place your UI elements on JABR,
 and `update_newname` to let your UI elements call on the `update_newname` function.
- `update_filename(string)`
 - This is called whenever JABR creates a preview of the output of your script in the list of new filenames.
 It takes the `string` parameter, which is the file's name. This function should contain the process of changing the filename.

There is another function that you may use on your script, although it is only optional:
- `cleanup()`
 - You may use this function to clean-up after `update_filename` is called.
 JABR will check if your script contains this function, but won't require it.

You may check the sample scripts that comes with JABR, as examples to creating your own script/s.