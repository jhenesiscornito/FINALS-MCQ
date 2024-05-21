from tkinter import Tk, Button, Label, Frame, Radiobutton, StringVar
import random

class ExamGUI:
    def __init__(self, bg_color, fg_color, button_color, center_window, is_cell_bold):
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.button_color = button_color
        self.center_window = center_window
        self.is_cell_bold = is_cell_bold

    def create(self, ws, time_limit, fname, lname, year, section, course):
        exam = Tk()
        exam.title("Teacher's Tool: MCQ Randomizer")
        exam.geometry("1000x700")
        exam.configure(bg=self.bg_color)

        self.center_window(exam, 1000, 700)

        frame = Frame(exam, bg=self.bg_color)
        frame.pack(expand=True)

        selected_choice = StringVar(value="")  # Initialize ang selected_choice to an empty string
        error_label = None

        questions = []
        options = []
        row_indices = []

        for idx, row in enumerate(ws.iter_rows(min_row=1, values_only=True), start=1):
            if row[0]:
                questions.append(row[0])
                options.append(row[1:5])
                row_indices.append(idx)

        combined = list(zip(questions, options, row_indices))
        random.shuffle(combined)
        questions, options, row_indices = zip(*combined)

        correct_answers = 0
        total_questions = len(questions)
        current_question_index = [0]

        # e define ang timer_label ug time_left
        timer_label = None
        time_left = [0]

        # e convert ang time_limit sa seconds
        if time_limit is not None:
            time_left = [time_limit * 60]
            timer_label = Label(exam, text=f"Time left: {time_left[0]} seconds")
            timer_label.pack(anchor='center', expand=True)

        def update_timer():
            if current_question_index[0] >= total_questions:  # e check kung na answeran na ang tanan nga questions
                return  # og mao, i return ang function

            time_left[0] -= 1
            hours, remainder = divmod(time_left[0], 3600)
            minutes, seconds = divmod(remainder, 60)
            timer_label.config(text=f"Time left: {hours} hours, {minutes} minutes, {seconds} seconds", 
                               bg=self.bg_color, 
                               fg=self.fg_color,
                               font=("Helvetica", 12))

            if time_left[0] <= 0:
                for widget in frame.winfo_children():
                    widget.destroy()

                name_label = Label(frame, text=f"NAME: {fname} {lname}\n"
                                   f"COURSE: {course}\n"
                                   f"YEAR LEVEL: {year}\n"
                                   f"SECTION: {section}\n", 
                                   font=("Helvetica", 12), 
                                   bg=self.bg_color, 
                                   fg=self.fg_color)
                name_label.pack(pady=10)

                score_label = Label(frame, text=f"Final Score: {correct_answers} / {total_questions}", 
                                    bg=self.bg_color, 
                                    fg=self.fg_color, 
                                    font=("Helvetica", 12, "bold"))
                score_label.pack(pady=20)

                # Hide the timer label
                timer_label.pack_forget()

                # Display the remaining time
                hours, remainder = divmod(time_left[0], 3600)
                minutes, seconds = divmod(remainder, 60)
                remaining_time_label = Label(frame, text=f"Remaining time: {hours} hours, {minutes} minutes, {seconds} seconds", 
                                             bg=self.bg_color, 
                                             fg=self.fg_color,
                                             font=("Helvetica", 12))
                remaining_time_label.pack(pady=10)

                submit_button.pack_forget()
                return

            # If time is not yet up, schedule the next call to update_timer
            exam.after(1000, update_timer)

        def check_answers(event=None):
            nonlocal correct_answers, error_label, timer_label  # Add timer_label here
            user_answer = selected_choice.get()

            # Check if an answer is selected
            if not user_answer:
                if error_label is None:
                    error_label = Label(frame, text="Please select an answer before submitting.", 
                                        bg=self.bg_color, 
                                        fg=self.fg_color,
                                        font=("Helvetica", 12, "bold"))
                    error_label.pack(pady=10)
                return
            else:
                if error_label is not None:
                    error_label.destroy()
                    error_label = None

            correct_answer = None
            for j, option in enumerate(options[current_question_index[0]]):
                if self.is_cell_bold(ws, row_indices[current_question_index[0]], j + 2):
                    correct_answer = chr(65 + j)
                    break

            if user_answer == correct_answer:
                correct_answers += 1

            current_question_index[0] += 1
            if current_question_index[0] >= total_questions:
                for widget in frame.winfo_children():
                    widget.destroy()

                # Display the remaining time
                hours, remainder = divmod(time_left[0], 3600)
                minutes, seconds = divmod(remainder, 60)

                # Display the user's information
                # Label(frame, text=f"NAME: {fname} {lname} COURSE: {course}  YEAR LEVEL: {year} SECTION: {section}", 
                #       font=("Helvetica", 15, "bold"), 
                #       bg=self.bg_color, 
                #       fg=self.fg_color).pack()
                # Label(frame, text=f"Final Score: {correct_answers} / {total_questions}", font=("Helvetica", 12), bg=self.bg_color, fg=self.fg_color).pack()

                name_label1 = Label(frame, text=f"NAME: {fname} {lname}\n"
                                   f"COURSE: {course}\n"
                                   f"YEAR LEVEL: {year}\n"
                                   f"SECTION: {section}\n", 
                                   font=("Helvetica", 12), 
                                   bg=self.bg_color, 
                                   fg=self.fg_color)
                name_label1.pack(pady=10)

                score_label1 = Label(frame, text=f"Final Score: {correct_answers} / {total_questions}", 
                                    bg=self.bg_color, 
                                    fg=self.fg_color, 
                                    font=("Helvetica", 12, "bold"))
                score_label1.pack(pady=20)

                if time_limit is not None:
                    remaining_time_label = Label(frame, text=f"Remaining time: {hours} hours, {minutes} minutes, {seconds} seconds", 
                                                 bg=self.bg_color, 
                                                 fg=self.fg_color,
                                                 font=("Helvetica", 12))
                    remaining_time_label.pack(pady=10)

                if time_limit is not None and timer_label is not None:
                    timer_label.pack_forget()

                # Hide the submit button
                submit_button.pack_forget()

                # Add an exit button
                exit_button = Button(frame, text="EXIT", command=exam.destroy, 
                                     bg=self.fg_color, 
                                     fg=self.bg_color, 
                                     font=("Helvetica", 12, "bold"))
                exit_button.pack(pady=10)

            else:
                display_question()

        def display_question():
            for widget in frame.winfo_children():
                widget.destroy()

            question = questions[current_question_index[0]]
            question_label = Label(frame, text=f"Question {current_question_index[0] + 1}: {question}", 
                                   font=("Helvetica", 18, "bold"),
                                   bg=self.bg_color, 
                                   fg=self.fg_color)
            question_label.pack()

            selected_choice.set(None)  # Reset the selected choice
            submit_button.config(state="disabled")  # Disable the submit button
            exam.unbind('<Return>')  # Unbind the <Return> key event

            choices = options[current_question_index[0]]
            for idx, choice in enumerate(choices):
                choice_text = str(choice).strip()
                choice_button = Radiobutton(frame, text=choice_text, variable=selected_choice, value=chr(65 + idx),
                                            command=enable_submit,
                                            font=("Helvetica", 12, "bold"),
                                            selectcolor=self.bg_color,
                                            bg=self.bg_color,
                                            fg=self.fg_color)
                choice_button.pack()

        def enable_submit():
            submit_button.config(state="normal")  # Enable the submit button when a choice is selected
            # Bind the ENTER key to the check_answers function
            exam.bind('<Return>', check_answers)

        # Initially disable the submit button
        submit_button = Button(exam, text="SUBMIT", command=check_answers, state="disabled", 
                               fg=self.fg_color, 
                               bg=self.bg_color, 
                               font=("Helvetica", 12, "bold"))
        submit_button.pack(anchor='center', expand=True)


        # Start the timer only if time limit is not None
        if time_limit is not None:
            update_timer()

        display_question()

        exam.mainloop()