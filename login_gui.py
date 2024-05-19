from tkinter import Tk, Label, Entry, Button

class LoginGUI:
    def __init__(self, bg_color, fg_color, button_color, center_window, create_gui):
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.button_color = button_color
        self.center_window = center_window
        self.create_gui = create_gui

    def create(self):
        # Define the correct username and password here
        correct_username = "admin"
        correct_password = "123123"

        login = Tk()
        login.title("Login")
        self.center_window(login, 500, 400)
        login.configure(bg=self.bg_color)

        # Title label
        title_label = Label(login, text="TEACHER'S TOOL: MCQ RANDOMIZER", font=("Helvetica", 16, "bold"), bg=self.bg_color, fg=self.fg_color)
        title_label.place(relx=0.5, rely=0.2, anchor='center')

        Label(login, text="Username", bg=self.bg_color, fg=self.fg_color).place(relx=0.5, rely=0.3, anchor='center')
        username_entry = Entry(login, bg=self.bg_color, fg=self.fg_color)
        username_entry.place(relx=0.5, rely=0.4, anchor='center')

        Label(login, text="Password", bg=self.bg_color, fg=self.fg_color).place(relx=0.5, rely=0.5, anchor='center')
        password_entry = Entry(login, show="*", bg=self.bg_color, fg=self.fg_color)
        password_entry.place(relx=0.5, rely=0.6, anchor='center')

        error_label = Label(login, bg=self.bg_color, fg=self.fg_color)
        error_label.place(relx=0.5, rely=0.7, anchor='center')

        attempts = [0]

        def check_login(event=None):
            entered_username = username_entry.get()
            entered_password = password_entry.get()
            if not entered_username or not entered_password:
                error_label.config(text="Username and Password are required.")
                return

            if entered_username == correct_username and entered_password == correct_password:
                login.destroy()
                self.create_gui()
            else:
                attempts[0] += 1
                remaining_attempts = 3 - attempts[0]
                if attempts[0] < 3:
                    error_label.config(
                        text=f"Incorrect Username or Password. {remaining_attempts} attempts remaining. Please try again!")
                else:
                    error_label.config(text="Check with the Department Head for Account Details. Closing in 3 seconds...")
                    username_entry.config(state="disabled")
                    password_entry.config(state="disabled")
                    countdown(3)

        def countdown(time_left):
            if time_left > 0:
                login.after(1000, countdown, time_left - 1)
                error_label.config(
                    text=f"Check with the Department Head for Account Details. Closing in {time_left} seconds...")
            else:
                login.destroy()

        login_button = Button(login, text="Login", command=check_login, bg=self.button_color, fg=self.fg_color, font=("Helvetica", 9))
        login_button.place(relx=0.5, rely=0.8, anchor='center')

        login.bind('<Return>', check_login)

        login.mainloop()
