from tkinter import Tk, Button, Label, Frame, Radiobutton, StringVar
import random

class ExamGUI:
    def __init__(self, bg_color, fg_color, button_color, center_window, is_cell_bold):
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.button_color = button_color
        self.center_window = center_window
        self.is_cell_bold = is_cell_bold

    def create(self, ws, time_limit):
        exam = Tk()
        exam.title("Student's Exam")
        exam.geometry("1000x700")

        self.center_window(exam, 1000, 700)

        frame = Frame(exam)
        frame.pack(expand=True)

        selected_choice = StringVar(value="")  # Initialize with an empty string
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

        # Convert time limit to seconds and create a label to display it
        time_left = [time_limit * 60]
        timer_label = Label(exam, text=f"Time left: {time_left[0]} seconds")
        timer_label.pack(anchor='center', expand=True)

        def update_timer():
            if current_question_index[0] >= total_questions:  # Check if all questions have been answered
                return  # If they have, return without scheduling the next call to update_timer

            time_left[0] -= 1
            hours, remainder = divmod(time_left[0], 3600)
            minutes, seconds = divmod(remainder, 60)
            timer_label.config(text=f"Time left: {hours} hours, {minutes} minutes, {seconds} seconds")
            
            if time_left[0] <= 0:
                for widget in frame.winfo_children():
                    widget.destroy()

                score_label = Label(frame, text=f"Final Score: {correct_answers} / {total_questions}")
                score_label.pack()

                # Hide the timer label
                timer_label.pack_forget()

                # Display the remaining time
                hours, remainder = divmod(time_left[0], 3600)
                minutes, seconds = divmod(remainder, 60)
                remaining_time_label = Label(frame, text=f"Remaining time: {hours} hours, {minutes} minutes, {seconds} seconds")
                remaining_time_label.pack()

                submit_button.pack_forget()
                return
            
            # If time is not yet up, schedule the next call to update_timer
            exam.after(1000, update_timer)

        def check_answers():
            nonlocal correct_answers, error_label
            user_answer = selected_choice.get()

            # Check if an answer is selected
            if not user_answer:
                if error_label is None:
                    error_label = Label(frame, text="Please select an answer before submitting.")
                    error_label.pack()
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

                score_label = Label(frame, text=f"Final Score: {correct_answers} / {total_questions}")
                score_label.pack()

                # Hide the timer label
                timer_label.pack_forget()

                # Display the remaining time
                hours, remainder = divmod(time_left[0], 3600)
                minutes, seconds = divmod(remainder, 60)
                remaining_time_label = Label(frame,
                                             text=f"Remaining time: {hours} hours, {minutes} minutes, {seconds} seconds")
                remaining_time_label.pack()

                submit_button.pack_forget()
            else:
                display_question()

        def display_question():
            for widget in frame.winfo_children():
                widget.destroy()

            question = questions[current_question_index[0]]
            question_label = Label(frame, text=question,
                                   font=("Helvetica", 12, "bold"),
                                   bg="lightblue",
                                   fg="darkblue",
                                   )
            question_label.pack()

            selected_choice.set(None)  # Reset the selected choice
            submit_button.config(state="disabled")  # Disable the submit button

            choices = options[current_question_index[0]]
            for idx, choice in enumerate(choices):
                choice_text = str(choice).strip()
                choice_button = Radiobutton(frame, text=choice_text, variable=selected_choice, value=chr(65 + idx),
                                            command=enable_submit,
                                            font=("Helvetica", 12, "bold"),
                                            bg="lightblue",
                                            fg="darkblue",
                                            )
                choice_button.pack()

        def enable_submit():
            submit_button.config(state="normal")  # Enable the submit button when a choice is selected

        submit_button = Button(exam, text="Submit", command=check_answers,
                               state="disabled")  # Initially disable the submit button
        submit_button.pack(anchor='center', expand=True)

        # Start the timer
        update_timer()

        display_question()

        exam.mainloop()