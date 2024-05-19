# MCQ Randomizer

This project is a Multiple Choice Questions (MCQ) randomizer tool built with Python and Tkinter. It allows teachers to create a quiz from an Excel file where questions, choices, and the correct answer (in bold) are defined.

## Features

- User-friendly GUI
- Time-limited quizzes
- Score calculation

## Installation

This project requires Python and pip installed. Clone the repository and install the dependencies with the following commands:

```bash
git clone https://github.com/arceeluceno13/mcq-randomizer.git
cd mcq-randomizer
pip install -r requirements.txt
```

## Usage
  If the guide.PNG file is in the same directory as your main_app.py file, you should use the following command:

```bash 
pyinstaller --onefile --windowed --add-data "guide.PNG;." --add-data "exam_gui.py;." --add-data "file_handler.py;." --add-data "login_gui.py;." main_app.py
  ```

If the guide.PNG file is inside an img directory which is in the same directory as your main_app.py file, you should use the following command:

```bash
pyinstaller --onefile --windowed --add-data "img/guide.PNG;img" --add-data "exam_gui.py;." --add-data "file_handler.py;." --add-data "login_gui.py;." main_app.py
```

## Known Issues
There's a bug when changing icon via PyInstaller. As a workaround, you can use Resource Hacker to change the icon of the exe file. You can download Resource Hacker from 
[here](https://www.angusj.com/resourcehacker/).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 
