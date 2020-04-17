import binwalk 
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import matplotlib
import os

# Initial Setup
window = Tk()
window.title("BinwalkGUI")

# Generating labels
label_name_title = Label(window, text="Filename:", anchor=W, justify=LEFT)
label_name_title.grid(column=0, row=0)

label_name = Label(window, text="", anchor=W)
label_name.grid(sticky=W+E+N+S,column=1, row=0)

label_results_title = Label(window, text="Results:", anchor=W, justify=LEFT)
label_results_title.grid(column=0, row=2)

label_results_data_header = Label(window, text='Offset', font=("TkFixedFont"), anchor=W)
label_results_data_header.grid(sticky=W+E+N+S,column=1, row=2)
label_results_data_description = Label(window, text='Description', font=("TkFixedFont"), anchor=W)
label_results_data_description.grid(sticky=W+E+N+S,column=2, row=2)

label_results_data_offset = Label(window, text="", anchor=W, justify=LEFT, font=("TkFixedFont"))
label_results_data_offset.grid(sticky=W+E+N+S,column=1, row=3)

label_results_data_description = Label(window, text="", anchor=W, justify=LEFT, font=("TkFixedFont"))
label_results_data_description.grid(sticky=W+E+N+S,column=2, row=3)



menubar = Menu(window)
window.config(menu=menubar)
subMenu = Menu(menubar, tearoff=0)
subMenu2 = Menu(menubar, tearoff=0)

filename_path = ""
magic_path = ""

def browse_file():
	global filename_path
	filename_path = filedialog.askopenfilename()
	#print(os.path.basename(filename_path))
	label_name.configure(text=os.path.basename(filename_path))

def choose_magic():
	global magic_path
	magic_path = filedialog.askopenfilename()
	#print(os.path.basename(magic_path))
	label_name.configure(text="%s (Magic file: %s)" % (os.path.basename(filename_path), os.path.basename(magic_path)))

def show_entropy():
	if filename_path is not "":
		binwalk.scan(filename_path, quiet=True, signature=True, entropy=True)
	else:
		messagebox.showerror("Error", "Please choose a file before plotting entropy")

quiet_mode=BooleanVar()
menubar.add_cascade(label="File", menu=subMenu)
menubar.add_cascade(label="Expert", menu=subMenu2)
subMenu.add_command(label="Open", command=browse_file)
subMenu2.add_checkbutton(label="Toggle quiet mode", onvalue=1, offvalue=0, variable=quiet_mode)
subMenu2.add_command(label="Plot entropy", command=show_entropy)

def magic():
	# label_name.configure(text="firmware.zip")
	if filename_path is not "":
		# binwalk execution
		#print(quiet_mode.get())
		choose_magic()
		if magic_path is "":
			messagebox.showerror("Error", "No file selected")
			return
		results_string_offset = '' 
		results_string_description = ''

		for module in binwalk.scan(filename_path, signature=False, magic='magic.mgc',quiet=quiet_mode.get()):
			for result in module.results: 
				results_string_offset += "0x%.8X\n" % (result.offset)
				results_string_description += "%s\n" % (result.description)
		label_results_data_offset.configure(text=results_string_offset)
		label_results_data_description.configure(text=results_string_description)
	else: 
		messagebox.showerror("Error", "Please choose a file before analyzing")

subMenu2.add_command(label="Search with custom magic file only", command=magic)
# Helper functions
def analyze():
	# label_name.configure(text="firmware.zip")
	if filename_path is not "":
		label_name.configure(text=os.path.basename(filename_path))
		# binwalk execution
		#print(quiet_mode.get())

		results_string_offset = '' 
		results_string_description = ''

		for module in binwalk.scan(filename_path, signature=True ,quiet=quiet_mode.get()):
			for result in module.results: 
				results_string_offset += "0x%.8X\n" % (result.offset)
				results_string_description += "%s\n" % (result.description)
		label_results_data_offset.configure(text=results_string_offset)
		label_results_data_description.configure(text=results_string_description)
	else: 
		messagebox.showerror("Error", "Please choose a file before analyzing")

def extract():
	files_extracted = ""
	if filename_path is not "":
		for module in binwalk.scan(filename_path, signature=True, extract=True):
			for result in module.results:
				if result.file.path in module.extractor.output:
					# These are files that binwalk carved out of the original firmware image, a la dd
					if result.offset in module.extractor.output[result.file.path].carved:
						print ("Carved data from offset 0x%X to %s" % (result.offset, module.extractor.output[result.file.path].carved[result.offset]))
						files_extracted += module.extractor.output[result.file.path].carved[result.offset]
						files_extracted += "\n"
					# These are files/directories created by extraction utilities (gunzip, tar, unsquashfs, etc)
					if result.offset in module.extractor.output[result.file.path].extracted:
						print ("Extracted %d files from offset 0x%X to '%s' using '%s'" % (len(module.extractor.output[result.file.path].extracted[result.offset].files),result.offset,module.extractor.output[result.file.path].extracted[result.offset].files[0],module.extractor.output[result.file.path].extracted[result.offset].command))

		messagebox.showinfo("Files carved", "The following files have been carved: \n" + files_extracted)


# Generating buttons
execute_button = Button(window, text="Analyze File", command=analyze)
execute_button.grid(column=1, row=5)

extract_button = Button(window, text="Extract File", command=extract)
extract_button.grid(column=2, row=5)

window.mainloop()
