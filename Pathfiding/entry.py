import tkinter as tk
import re


class EntryBox:
    def __init__(self, master, grid_length):
        self.frame = tk.Frame(master)
        self.master = master
        self.frame.pack()

        self.initiate_widgets()
        self.show_widgets()

        # all the variables that gets return to send signal
        self.showStep = False
        self.start = None
        self.end = None
        self.successInput = 0
        self.success = False
        self.coords = list()

        self.grid_length = grid_length

    def initiate_widgets(self):
        # all the buttons
        self.label1 = tk.Label(self.frame, text="start, Format:(int, int)")
        self.label2 = tk.Label(self.frame, text="end, Format:(int, int)")
        self.label3 = tk.Label(self.frame, text="x and y coordinate is < 40")
        self.entry1 = tk.Entry(self.frame)
        self.entry1.insert(0, "(0,0)")
        self.entry2 = tk.Entry(self.frame)
        self.entry2.insert(0, "(39,39)")
        self.check = tk.IntVar()
        self.check_button = tk.Checkbutton(
            self.frame, text="show step", variable=self.check)
        self.enter_button = tk.Button(
            self.frame, text="ENTER", command=self.get_coord_from_window)

    def show_widgets(self):
        self.label1.grid(row=0, sticky=tk.E)
        self.label2.grid(row=1, sticky=tk.E)
        self.entry1.grid(row=0, column=1)
        self.entry2.grid(row=1, column=1)
        self.label3.grid(row=2, columnspan=2)
        self.check_button.grid(row=3)
        self.enter_button.grid(row=3, column=1)

    def get_coord_from_window(self):
        def get_num_of_digit():
            num = 0
            for i in str(self.grid_length):
                num += 1
            return num

        self.checkCoords = [self.entry1.get(), self.entry2.get()]
        numOfDigit = get_num_of_digit()
        inputPattern = r"^[(]([0-9]{1," + str(numOfDigit) + \
            r"})[,]([0-9]{1," + str(numOfDigit) + r"})[)]$"

        self.newWindow = tk.Toplevel(self.master)
        self.append_coordinate = list()
        for coord in self.checkCoords:
            matched = re.match(inputPattern, coord)
            if matched is None:
                formatBox = ErrorBox(
                    self.newWindow, "Please follow the format!")
                self.successInput = 0
                self.coords.clear()
                self.checkCoords.clear()
                break

            for i in matched.groups():
                if int(i) >= self.grid_length or int(i) < 0:
                    boundBox = ErrorBox(
                        self.newWindow, "Out of Bound!")
                    self.successInput = 0
                    self.coords.clear()
                    self.checkCoords.clear()
                    break
                # successful
                self.successInput += 1
                self.append_coordinate.append(int(i))
                if len(self.append_coordinate) == 2:
                    self.coords.append(tuple(self.append_coordinate))
                    self.append_coordinate.clear()

        if self.successInput == 4:
            self.success = True
            self.master.destroy()

    def get_coords(self):
        return self.coords

    def get_check_state(self):
        return self.check.get()


class ErrorBox:
    def __init__(self, master=None, message=None):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.label = tk.Label(self.frame, text=message)
        self.frame.pack()
        self.closeButton = tk.Button(
            self.frame, text="OK, Let me check", command=self.close_window)
        self.label.pack()
        self.closeButton.pack()

    def close_window(self):
        self.master.destroy()


def main():
    # debugging purposes
    correctInput = False
    while not correctInput:
        def on_close():
            nonlocal correctInput
            correctInput = True
            root.destroy()
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW",  on_close)
        entry = EntryBox(root, 40)
        root.mainloop()
        if entry.success:
            correctInput = True
    print(entry.check.get())


if __name__ == "__main__":
    main()
