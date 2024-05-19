from tkinter import Tk, Button, Label, Entry, PhotoImage, Frame, Radiobutton, StringVar
from tkinter.filedialog import askopenfilename
from login_gui import LoginGUI
from exam_gui import ExamGUI
from file_handler import FileHandler

class MainApp:
    def __init__(self):
        self.bg_color = "#003f5c"  # Dark Blue
        self.fg_color = "#ffffff"  # White
        self.button_color = "#7a5195"
        self.login_gui = LoginGUI(self.bg_color, self.fg_color, self.button_color, self.center_window, self.create_gui)
        self.exam_gui = ExamGUI(self.bg_color, self.fg_color, self.button_color, self.center_window, self.is_cell_bold)
        self.file_handler = FileHandler()

    def center_window(self, window, width=500, height=400):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        center_x = int((screen_width - width) / 2)
        center_y = int((screen_height - height) / 2)
        window.geometry(f"{width}x{height}+{center_x}+{center_y}")

    def create_gui(self):
        root = Tk()
        root.title("Teacher's Tool: MCQ Randomizer")
        root.geometry("1000x700")
        root.configure(bg=self.bg_color)

        self.center_window(root, 1000, 700)

        file_path = [None]

        def select_file():
            file_path[0] = askopenfilename(filetypes=[("Excel files", "*.xlsx")])

        def upload_file():
            time_limit = time_limit_entry.get()
            if not time_limit:
                error_label.config(text="Time limit is required.")
                return

            if not file_path[0]:
                error_label.config(text="No file selected.")
                return

            ws = self.file_handler.read_excel(file_path[0])
            if ws:
                root.destroy()
                self.exam_gui.create(ws, int(time_limit))

        frame = Frame(root, bg=self.bg_color)
        frame.pack()

        instructions = Label(frame, text="EXCEL FILE MUST BE IN THIS FORMAT\n\n"
                                         "1. All Questions Must be in Column A.\n"
                                         "2. All Choices from A to D must be in column B to E.\n"
                                         "NOTE: The entire question and its choices must be on row 1.\n\n"
                                         "3. Cells with correct answers must be in BOLD Letters.\n"
                                         "Here's an example layout:\n", bg=self.bg_color, fg=self.fg_color)
        instructions.pack(pady=20)

        guide_image = PhotoImage(file="guide.PNG")
        image_label = Label(frame, image=guide_image, bg=self.bg_color)
        image_label.image = guide_image
        image_label.pack()

        Label(frame, text="Time Limit (in minutes):", bg=self.bg_color, fg=self.fg_color).pack()

        validate_command = root.register(lambda input: input.isdigit() or input == "")
        time_limit_entry = Entry(frame, validate="key", validatecommand=(validate_command, "%P"), bg=self.bg_color, fg=self.fg_color)
        time_limit_entry.pack()

        error_label = Label(frame, text="", bg=self.bg_color, fg=self.fg_color)
        error_label.pack()

        select_button = Button(frame, text="Select Excel File", command=select_file, bg=self.button_color, fg=self.fg_color)
        select_button.pack(pady=10)

        upload_button = Button(frame, text="Upload", command=upload_file, bg=self.button_color, fg=self.fg_color)
        upload_button.pack(pady=10)

        root.mainloop()

    def is_cell_bold(self, ws, row, col):
        cell = ws.cell(row=row, column=col)
        return cell.font.bold

    def run(self):
        self.login_gui.create()

if __name__ == "__main__":
    app = MainApp()
    app.run()