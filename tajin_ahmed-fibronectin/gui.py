from tkinter import *
import sys
from datetime import time
from tkinter.font import BOLD
from turtle import clear


'''
GUI features
- file name box (later maybe window to search for file)
- checkbox for each frequency being plotted
    - checkbox for raw and clean data
        - raw data plots are individual for overtone of each freq/dis
- abs base time t0, tf

WIP
- input for scale of time (seconds, minues, hours)
- alternate plot options:
    - plot dF and dD together
    - normalize F

- look into:
    - interactive plots (plotly)
    - open explorer to search for file
'''


### INPUT DEFINITIONS ###
#file_name = "08102022_n=2_Fn at 500 ug per ml and full SF on func gold at 37C"
#file_ext = '.csv'
#abs_base_t0 = time(8, 35, 52)
#abs_base_tf = time(9, 9, 19)
# column names



'''Variable Initializations'''
file_info = ['','']
will_plot_raw_data = False
will_plot_clean_data = False
will_overwrite_file = False
abs_base_t0 = time(0, 0, 0)
abs_base_tf = time(0, 0, 0)
x_timescale = 's'
which_plot = {'raw': {'fundamental_freq': False, 'fundamental_dis': False, '3rd_freq': False, '3rd_dis': False,
                    '5th_freq': False, '5th_dis': False, '7th_freq': False, '7th_dis': False,
                    '9th_freq': False, '9th_dis': False},

            'clean': {'fundamental_freq': False, 'fundamental_dis': False, '3rd_freq': False, '3rd_dis': False,
                    '5th_freq': False, '5th_dis': False, '7th_freq': False, '7th_dis': False,
                    '9th_freq': False, '9th_dis': False}}


'''Function Defintions for UI events'''
def col_names_submit():
    file_info[0] = file_name_entry.get()
    file_info[1] = file_path_entry.get()
    global will_overwrite_file
    if file_overwrite_var.get() == 1:
        will_overwrite_file = True
    else:
        will_overwrite_file = False

    global abs_base_t0
    global abs_base_tf
    h0 = hours_entry_t0.get()
    m0 = minutes_entry_t0.get()
    s0 = seconds_entry_t0.get()
    hf = hours_entry_tf.get()
    mf = minutes_entry_tf.get()
    sf = seconds_entry_tf.get()
    if(h0 == '' and m0 == '' and s0 == ''):
        h0 = 0
        m0 = 0
        s0 = 0
    if(hf == '' and mf == '' and sf == ''):
        hf = 0
        mf = 0
        sf = 0
    try:
        abs_base_t0 = time(int(h0),int(m0),int(s0))
        abs_base_tf = time(int(hf),int(mf),int(sf))
    except ValueError as exc:
        err_label.grid(row=20, column=0)
        print(f"Please enter integer values for time: {exc}")
    submitted_label.grid(row=13, column=0)

def clear_file_data():
    global file_info
    global abs_base_t0
    global abs_base_tf
    file_info = []
    abs_base_t0 = time(0, 0, 0)
    abs_base_tf = time(0, 0, 0)
    cleared_label.grid(row=12, column=0)
    file_name_entry.delete(0, END)
    file_path_entry.delete(0, END)
    hours_entry_t0.delete(0, END)
    minutes_entry_t0.delete(0, END)
    seconds_entry_t0.delete(0, END)
    hours_entry_tf.delete(0, END)
    minutes_entry_tf.delete(0, END)
    seconds_entry_tf.delete(0, END)
    file_overwrite_var.set(0)

def handle_fn_focus_in(_):
    if file_name_entry.get() == "File name here":
        file_name_entry.delete(0, END)
        file_name_entry.config(fg='black')

def handle_fn_focus_out(_):
    if file_name_entry.get() == "":
        file_name_entry.delete(0, END)
        file_name_entry.config(fg='gray')
        file_name_entry.insert(0, "File name here")

def handle_fp_focus_in(_):
    if file_path_entry.get() == "Enter path to file (leave blank if in same dir)":
        file_path_entry.delete(0, END)
        file_path_entry.config(fg='black')

def handle_fp_focus_out(_):
    if file_path_entry.get() == "":
        file_path_entry.delete(0, END)
        file_path_entry.config(fg='gray')
        file_path_entry.insert(0, "Enter path to file (leave blank if in same dir)")    

def clear_raw_checks():
    raw_ch1_freq_var.set(0)
    raw_ch1_dis_var.set(0)
    raw_ch2_freq_var.set(0)
    raw_ch2_dis_var.set(0)
    raw_ch3_freq_var.set(0)
    raw_ch3_dis_var.set(0)
    raw_ch4_freq_var.set(0)
    raw_ch4_dis_var.set(0)
    raw_ch5_freq_var.set(0)
    raw_ch5_dis_var.set(0)
    for channel in which_plot['raw']:
        which_plot['raw'][channel] = False
        

def select_all_raw_checks():
    raw_ch1_freq_var.set(1)
    raw_ch1_dis_var.set(1)
    raw_ch2_freq_var.set(1)
    raw_ch2_dis_var.set(1)
    raw_ch3_freq_var.set(1)
    raw_ch3_dis_var.set(1)
    raw_ch4_freq_var.set(1)
    raw_ch4_dis_var.set(1)
    raw_ch5_freq_var.set(1)
    raw_ch5_dis_var.set(1)
    for channel in which_plot['raw']:
        which_plot['raw'][channel] = True

def clear_clean_checks():
    clean_ch1_freq_var.set(0)
    clean_ch1_dis_var.set(0)
    clean_ch2_freq_var.set(0)
    clean_ch2_dis_var.set(0)
    clean_ch3_freq_var.set(0)
    clean_ch3_dis_var.set(0)
    clean_ch4_freq_var.set(0)
    clean_ch4_dis_var.set(0)
    clean_ch5_freq_var.set(0)
    clean_ch5_dis_var.set(0)
    for channel in which_plot['clean']:
        which_plot['clean'][channel] = False

def select_all_clean_checks():
    clean_ch1_freq_var.set(1)
    clean_ch1_dis_var.set(1)
    clean_ch2_freq_var.set(1)
    clean_ch2_dis_var.set(1)
    clean_ch3_freq_var.set(1)
    clean_ch3_dis_var.set(1)
    clean_ch4_freq_var.set(1)
    clean_ch4_dis_var.set(1)
    clean_ch5_freq_var.set(1)
    clean_ch5_dis_var.set(1)
    for channel in which_plot['clean']:
        which_plot['clean'][channel] = True

def receive_raw_checkboxes():
    global will_plot_raw_data
    global which_plot

    if plot_raw_data_var.get() == 1:
        will_plot_raw_data = True
        which_raw_channels_label.grid(row=1, column=2)
        select_all_raw_checks_button.grid(row=19, column=2)
        clear_raw_checks_button.grid(row=20, column=2)
        raw_ch1_freq_check.grid(row=2, column=2)
        raw_ch1_dis_check.grid(row=3, column=2)
        raw_ch2_freq_check.grid(row=4, column=2)
        raw_ch2_dis_check.grid(row=5, column=2)
        raw_ch3_freq_check.grid(row=6, column=2)
        raw_ch3_dis_check.grid(row=7, column=2)
        raw_ch4_freq_check.grid(row=8, column=2)
        raw_ch4_dis_check.grid(row=9, column=2)
        raw_ch5_freq_check.grid(row=10, column=2)
        raw_ch5_dis_check.grid(row=11, column=2)

        if raw_ch1_freq_var.get() == 1:
            which_plot['raw']['fundamental_freq'] = True
        else:
            which_plot['raw']['fundamental_freq'] = False

        if raw_ch1_dis_var.get() == 1:
            which_plot['raw']['fundamental_dis'] = True
        else:
            which_plot['raw']['fundamental_dis'] = False

        if raw_ch2_freq_var.get() == 1:
            which_plot['raw']['3rd_freq'] = True
        else:
            which_plot['raw']['3rd_freq'] = False

        if raw_ch2_dis_var.get() == 1:
            which_plot['raw']['3rd_dis'] = True
        else:
            which_plot['raw']['3rd_dis'] = False

        if raw_ch3_freq_var.get() == 1:
            which_plot['raw']['5th_freq'] = True
        else:
            which_plot['raw']['5th_freq'] = False

        if raw_ch3_dis_var.get() == 1:
            which_plot['raw']['5th_dis'] = True
        else:
            which_plot['raw']['5th_dis'] = False

        if raw_ch4_freq_var.get() == 1:
            which_plot['raw']['7th_freq'] = True
        else:
            which_plot['raw']['7th_freq'] = False

        if raw_ch4_dis_var.get() == 1:
            which_plot['raw']['7th_dis'] = True
        else:
            which_plot['raw']['7th_dis'] = False

        if raw_ch5_freq_var.get() == 1:
            which_plot['raw']['9th_freq'] = True
        else:
            which_plot['raw']['9th_freq'] = False

        if raw_ch5_dis_var.get() == 1:
            which_plot['raw']['9th_dis'] = True
        else:
            which_plot['raw']['9th_dis'] = False

    else:
        will_plot_raw_data = False
        which_raw_channels_label.grid_forget()
        raw_ch1_freq_check.grid_forget()
        raw_ch1_dis_check.grid_forget()
        raw_ch2_freq_check.grid_forget()
        raw_ch2_dis_check.grid_forget()
        raw_ch3_freq_check.grid_forget()
        raw_ch3_dis_check.grid_forget()
        raw_ch4_freq_check.grid_forget()
        raw_ch4_dis_check.grid_forget()
        raw_ch5_freq_check.grid_forget()
        raw_ch5_dis_check.grid_forget()
        select_all_raw_checks_button.grid_forget()
        clear_raw_checks_button.grid_forget()
        


def receive_clean_checkboxes():
    global will_plot_clean_data
    global which_plot
    if plot_clean_data_var.get() == 1:
        will_plot_clean_data = True
        which_clean_channels_label.grid(row=1, column=3)
        select_all_clean_checks_button.grid(row=19, column=3)
        clear_clean_checks_button.grid(row=20, column=3)
        clean_ch1_freq_check.grid(row=2, column=3)
        clean_ch1_dis_check.grid(row=3, column=3)
        clean_ch2_freq_check.grid(row=4, column=3)
        clean_ch2_dis_check.grid(row=5, column=3)
        clean_ch3_freq_check.grid(row=6, column=3)
        clean_ch3_dis_check.grid(row=7, column=3)
        clean_ch4_freq_check.grid(row=8, column=3)
        clean_ch4_dis_check.grid(row=9, column=3)
        clean_ch5_freq_check.grid(row=10, column=3)
        clean_ch5_dis_check.grid(row=11, column=3)

        if clean_ch1_freq_var.get() == 1:
            which_plot['clean']['fundamental_freq'] = True
        else:
            which_plot['clean']['fundamental_freq'] = False

        if clean_ch1_dis_var.get() == 1:
            which_plot['clean']['fundamental_dis'] = True
        else:
            which_plot['clean']['fundamental_dis'] = False

        if clean_ch2_freq_var.get() == 1:
            which_plot['clean']['3rd_freq'] = True
        else:
            which_plot['clean']['3rd_freq'] = False

        if clean_ch2_dis_var.get() == 1:
            which_plot['clean']['3rd_dis'] = True
        else:
            which_plot['clean']['3rd_dis'] = False

        if clean_ch3_freq_var.get() == 1:
            which_plot['clean']['5th_freq'] = True
        else:
            which_plot['clean']['5th_freq'] = False

        if clean_ch3_dis_var.get() == 1:
            which_plot['clean']['5th_dis'] = True
        else:
            which_plot['clean']['5th_dis'] = False

        if clean_ch4_freq_var.get() == 1:
            which_plot['clean']['7th_freq'] = True
        else:
            which_plot['clean']['7th_freq'] = False

        if clean_ch4_dis_var.get() == 1:
            which_plot['clean']['7th_dis'] = True
        else:
            which_plot['clean']['7th_dis'] = False

        if clean_ch5_freq_var.get() == 1:
            which_plot['clean']['9th_freq'] = True
        else:
            which_plot['clean']['9th_freq'] = False

        if clean_ch5_dis_var.get() == 1:
            which_plot['clean']['9th_dis'] = True
        else:
            which_plot['clean']['9th_dis'] = False

    else:
        will_plot_clean_data = False
        which_clean_channels_label.grid_forget()
        clean_ch1_freq_check.grid_forget()
        clean_ch1_dis_check.grid_forget()
        clean_ch2_freq_check.grid_forget()
        clean_ch2_dis_check.grid_forget()
        clean_ch3_freq_check.grid_forget()
        clean_ch3_dis_check.grid_forget()
        clean_ch4_freq_check.grid_forget()
        clean_ch4_dis_check.grid_forget()
        clean_ch5_freq_check.grid_forget()
        clean_ch5_dis_check.grid_forget()
        select_all_clean_checks_button.grid_forget()
        clear_clean_checks_button.grid_forget()


'''Enter event loop for UI'''
root = Tk()
fr = Frame(root)
fr.grid(row=7, column=0, rowspan=2)


# define and place file info labels and buttons
# FIRST COLUMN ELEMENTS (file data)
file_name_label = Label(root, text="Enter data file information", padx=50)
spacing = Label(root, text="         ")
file_name_label.grid(row=0, column=0)
spacing.grid(row=1, column=0)
cleared_label = Label(root, text="Cleared!")
submitted_label = Label(root, text="Submitted!")
err_label = Label(root, text="Error occured,\nplease see terminal for details", font=("Arial",14))

file_name_entry = Entry(root, width=40, bg='white', fg='gray')
file_name_entry.grid(row=2, column=0, columnspan=1, padx=8, pady=4)
file_name_entry.insert(0, "File name here")
file_name_entry.bind("<FocusIn>", handle_fn_focus_in)
file_name_entry.bind("<FocusOut>", handle_fn_focus_out)

file_path_entry = Entry(root, width=40, bg='white', fg='gray')
file_path_entry.grid(row=3, column=0, columnspan=1, padx=8, pady=4)
file_path_entry.insert(0, "Enter path to file (leave blank if in same dir)")
file_path_entry.bind("<FocusIn>", handle_fp_focus_in)
file_path_entry.bind("<FocusOut>", handle_fp_focus_out)

file_overwrite_var = IntVar()
file_overwrite_check = Checkbutton(root, text='Overwrite file with cleaned data?', variable=file_overwrite_var, onvalue=1, offvalue=0, pady=10)
file_overwrite_check.grid(row=5, column=0)

baseline_frame = Frame(fr)
baseline_time_label = Label(root, text="Enter absolute baseline time")
baseline_time_label.grid(row=6, column=0)

baseline_frame.grid(row=7, column=0, columnspan=1)
hours_label_t0 = Label(baseline_frame, text="H0: ")
hours_label_t0.grid(row=0, column=0)
hours_entry_t0 = Entry(baseline_frame, width=5, bg='white', fg='gray')
hours_entry_t0.grid(row=0, column=1)
minutes_label_t0 = Label(baseline_frame, text="M0: ")
minutes_label_t0.grid(row=0, column=2)
minutes_entry_t0 = Entry(baseline_frame, width=5, bg='white', fg='gray')
minutes_entry_t0.grid(row=0, column=3)
seconds_label_t0 = Label(baseline_frame, text="S0: ")
seconds_label_t0.grid(row=0, column=4)
seconds_entry_t0 = Entry(baseline_frame, width=5, bg='white', fg='gray')
seconds_entry_t0.grid(row=0, column=5)

hours_label_tf = Label(baseline_frame, text="Hf: ")
hours_label_tf.grid(row=1, column=0)
hours_entry_tf = Entry(baseline_frame, width=5, bg='white', fg='gray')
hours_entry_tf.grid(row=1, column=1)
minutes_label_tf = Label(baseline_frame, text="Mf: ")
minutes_label_tf.grid(row=1, column=2)
minutes_entry_tf = Entry(baseline_frame, width=5, bg='white', fg='gray')
minutes_entry_tf.grid(row=1, column=3)
seconds_label_tf = Label(baseline_frame, text="Sf: ")
seconds_label_tf.grid(row=1, column=4)
seconds_entry_tf = Entry(baseline_frame, width=5, bg='white', fg='gray')
seconds_entry_tf.grid(row=1, column=5)
spacing.grid(row=9, column=0)

file_data_submit_button = Button(root, text="Submit file information", padx=12, pady=8, command=col_names_submit)
file_data_submit_button.grid(row=10, column=0)
file_data_clear_button = Button(root, text="Clear Entries", padx=12, pady=8, command=clear_file_data)
file_data_clear_button.grid(row=11, column=0)


# SECOND COLUMN ENTRIES (define and place checkboxes for raw data)
plot_raw_data_var = IntVar()
plot_raw_data_check = Checkbutton(root, text="Plot raw data?", variable=plot_raw_data_var, onvalue=1, offvalue=2, command=receive_raw_checkboxes, padx=60, pady=10)
plot_raw_data_check.grid(row=0, column=2)
which_raw_channels_label = Label(root, text="which channels for full raw data?")

# a lot of checkboxes for selecting which channels to plot for clean and raw data
raw_ch1_freq_var = IntVar()
raw_ch1_freq_check = Checkbutton(root, text="Ch 1 frequency", variable=raw_ch1_freq_var, onvalue=1, offvalue=0, command=receive_raw_checkboxes)
raw_ch1_dis_var = IntVar()
raw_ch1_dis_check = Checkbutton(root, text="Ch 1 dissipation", variable=raw_ch1_dis_var, onvalue=1, offvalue=0, command=receive_raw_checkboxes)
raw_ch2_freq_var = IntVar()
raw_ch2_freq_check = Checkbutton(root, text="Ch 2 frequency", variable=raw_ch2_freq_var, onvalue=1, offvalue=0, command=receive_raw_checkboxes)
raw_ch2_dis_var = IntVar()
raw_ch2_dis_check = Checkbutton(root, text="Ch 2 dissipation", variable=raw_ch2_dis_var, onvalue=1, offvalue=0, command=receive_raw_checkboxes)
raw_ch3_freq_var = IntVar()
raw_ch3_freq_check = Checkbutton(root, text="Ch 3 frequency", variable=raw_ch3_freq_var, onvalue=1, offvalue=0, command=receive_raw_checkboxes)
raw_ch3_dis_var = IntVar()
raw_ch3_dis_check = Checkbutton(root, text="Ch 3 dissipation", variable=raw_ch3_dis_var, onvalue=1, offvalue=0, command=receive_raw_checkboxes)
raw_ch4_freq_var = IntVar()
raw_ch4_freq_check = Checkbutton(root, text="Ch 4 frequency", variable=raw_ch4_freq_var, onvalue=1, offvalue=0, command=receive_raw_checkboxes)
raw_ch4_dis_var = IntVar()
raw_ch4_dis_check = Checkbutton(root, text="Ch 4 dissipation", variable=raw_ch4_dis_var, onvalue=1, offvalue=0, command=receive_raw_checkboxes)
raw_ch5_freq_var = IntVar()
raw_ch5_freq_check = Checkbutton(root, text="Ch 5 frequency", variable=raw_ch5_freq_var, onvalue=1, offvalue=0, command=receive_raw_checkboxes)
raw_ch5_dis_var = IntVar()
raw_ch5_dis_check = Checkbutton(root, text="Ch 5 dissipation", variable=raw_ch5_dis_var, onvalue=1, offvalue=0, command=receive_raw_checkboxes)

clear_raw_checks_button = Button(root, text='clear all', command=clear_raw_checks)
select_all_raw_checks_button = Button(root, text='select all', command=select_all_raw_checks)


# THIRD COLUMN ENTRIES (define and place checkboxes for clean data)
plot_clean_data_var = IntVar()
plot_clean_data_check = Checkbutton(root, text="Plot clean data?", variable=plot_clean_data_var, onvalue=1, offvalue=0, command=receive_clean_checkboxes, padx=60, pady=10)
plot_clean_data_check.grid(row=0, column=3)
which_clean_channels_label = Label(root, text="which channels for full clean data?")

clean_ch1_freq_var = IntVar()
clean_ch1_freq_check = Checkbutton(root, text="Ch 1 frequency", variable=clean_ch1_freq_var, onvalue=1, offvalue=0, command=receive_clean_checkboxes)
clean_ch1_dis_var = IntVar()
clean_ch1_dis_check = Checkbutton(root, text="Ch 1 dissipation", variable=clean_ch1_dis_var, onvalue=1, offvalue=0, command=receive_clean_checkboxes)
clean_ch2_freq_var = IntVar()
clean_ch2_freq_check = Checkbutton(root, text="Ch 2 frequency", variable=clean_ch2_freq_var, onvalue=1, offvalue=0, command=receive_clean_checkboxes)
clean_ch2_dis_var = IntVar()
clean_ch2_dis_check = Checkbutton(root, text="Ch 2 dissipation", variable=clean_ch2_dis_var, onvalue=1, offvalue=0, command=receive_clean_checkboxes)
clean_ch3_freq_var = IntVar()
clean_ch3_freq_check = Checkbutton(root, text="Ch 3 frequency", variable=clean_ch3_freq_var, onvalue=1, offvalue=0, command=receive_clean_checkboxes)
clean_ch3_dis_var = IntVar()
clean_ch3_dis_check = Checkbutton(root, text="Ch 3 dissipation", variable=clean_ch3_dis_var, onvalue=1, offvalue=0, command=receive_clean_checkboxes)
clean_ch4_freq_var = IntVar()
clean_ch4_freq_check = Checkbutton(root, text="Ch 4 frequency", variable=clean_ch4_freq_var, onvalue=1, offvalue=0, command=receive_clean_checkboxes)
clean_ch4_dis_var = IntVar()
clean_ch4_dis_check = Checkbutton(root, text="Ch 4 dissipation", variable=clean_ch4_dis_var, onvalue=1, offvalue=0, command=receive_clean_checkboxes)
clean_ch5_freq_var = IntVar()
clean_ch5_freq_check = Checkbutton(root, text="Ch 5 frequency", variable=clean_ch5_freq_var, onvalue=1, offvalue=0, command=receive_clean_checkboxes)
clean_ch5_dis_var = IntVar()
clean_ch5_dis_check = Checkbutton(root, text="Ch 5 dissipation", variable=clean_ch5_dis_var, onvalue=1, offvalue=0, command=receive_clean_checkboxes)

clear_clean_checks_button = Button(root, text='clear all', command=clear_clean_checks)
select_all_clean_checks_button = Button(root, text='select all', command=select_all_clean_checks)


# conclude UI event loop
root.mainloop()

''' Grab data from UI temp into variables for data analysis'''


# assign file info data
print(which_plot)
print(f"{abs_base_t0}\n{abs_base_tf}")
raw_num_channels_tested = 0
clean_num_channels_tested = 0
for channel in which_plot['raw'].items():
    if channel[1] == True:
        raw_num_channels_tested += 1

for channel in which_plot['clean'].items():
    if channel[1] == True:
        clean_num_channels_tested += 1

total_num_channels_tested = raw_num_channels_tested + clean_num_channels_tested
print(total_num_channels_tested)

''' ERROR CHECKING '''
# verify file info
if len(file_info) == 0:
    print("please define file information!")
    sys.exit(1)
#elif (file_info[0] == '' or file_info[0] == 'File name here'):
#    print("File name not specified")
#    sys.exit(1)
else:
    file_name = file_info[0]
    if file_info[1] == 'Enter path to file (leave blank if in same dir)':
        file_path = ""

# verify baseline time entered
#do that

print(file_info)
print("\n\n")

'''TEMP ASSIGNMENTS to not have to enter into gui every time while debugging'''
file_name = "08102022_n=2_Fn at 500 ug per ml and full SF on func gold at 37C.csv"
file_path = ""
clean_num_channels_tested = 10
abs_base_t0 = time(8,29,48)
abs_base_tf = time(9,5,55)

