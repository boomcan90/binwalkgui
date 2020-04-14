import binwalk 
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# Initial Setup
window = Tk()
window.title("BinwalkGUI")

# Generating labels
label_name_title = Label(window, text="Filename:")
label_name_title.grid(column=0, row=0)

label_name = Label(window, text="", anchor=W)
label_name.grid(sticky=W+E+N+S,column=1, row=0)

label_results_title = Label(window, text="Results:")
label_results_title.grid(column=0, row=2)

label_results_data_header = Label(window, text='Offset        Description', font=("TkFixedFont"), anchor=W)
label_results_data_header.grid(sticky=W+E+N+S,column=1, row=2)

label_results_data = Label(window, text="", justify=LEFT, font=("TkFixedFont"))
label_results_data.grid(column=1, row=3)

# Helper functions
def analyze():
	# label_name.configure(text="firmware.zip")
	if label_name.cget("text") is not "":
		# binwalk execution

		results_string = '' 
		for module in binwalk.scan(label_name.cget("text"), signature=True, quiet=True):
			for result in module.results: 
				results_string += "0x%.8X    %s \n" % (result.offset, result.description)

		label_results_data.configure(text=results_string)
	else: 
		messagebox.showerror("Error", "Please choose a file before analyzing")

def extract():
	files_extracted = ""
	if label_name.cget("text") is not "":
		for module in binwalk.scan(label_name.cget("text"), signature=True, extract=True):
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

def choose_file(): 
	label_results_data.configure(text='')
	file_name = filedialog.askopenfilename()
	label_name.configure(text=file_name)


# Generating buttons
execute_button = Button(window, text="Analyze File", command=analyze)
execute_button.grid(column=1, row=5)

extract_button = Button(window, text="Extract File", command=extract)
extract_button.grid(column=2, row=5)

choose_file_button = Button(window, text="Choose file to analyze", command=choose_file)
choose_file_button.grid(column=2, row=0)

window.mainloop()
