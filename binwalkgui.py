import binwalk 
from tkinter import *

#test

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
	label_name.configure(text="firmware.zip")

	# binwalk execution

	results_string = '' 
	for module in binwalk.scan("firmware.zip", signature=True, quiet=True):
		for result in module.results: 
			results_string += "0x%.8X    %s \n" % (result.offset, result.description)

	label_results_data.configure(text=results_string)

# Generating buttons
execute_button = Button(window, text="Analyze File", command=analyze)
execute_button.grid(column=1, row=5)

window.mainloop()