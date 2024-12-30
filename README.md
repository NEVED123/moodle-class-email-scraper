# Get Email List From Moodle Class

There is no easy way on Moodle to get a list of all students emails in a class. This script solves that issue. This script will output a text file with all student emails (filtering out the teacher), so that you can easily copy and paste all of them at once into an email message.

## Prerequisites

This guide assumes you have pulled the code from GitHub, and have Python 3.12 and Pip installed.

## Usage

### Create config.json

In the same file as moodle-emails.py, create a file `config.json`, and paste this code:

```
{
    "courseId" : 123456,
    "cookie": "your-cookie"
}
```

The values are place holders right now.

### Get Your Cookies

Navigate to the page of the course you are interested in, then open up Developer Tools (The "Inspect Element" thing). Click the "Console" tab on the top, and type in the console `document.cookie`. This will output a string of text. Right click and select 'Copy string contents'. Now, in `config.json`, replace "your-cookie" with the copied value. Ensure that the value is surrounded in "double quotes", not 'single quotes'.

### Course Id

In the full URL of your class page, you will see something like:

`https://moodle.oakland.edu/course/view.php?id=298318`

Grad the value after `id=`, and paste that in place of `123456` in `config.json`

### Run the script

(Optionally) Create a virtual environment for dependencies:

`python3.12 -m venv .env && source .env/bin/activate`

Install dependencies:

`pip install -r requirements.txt`

Run the script:

`python3.12 moodle-emails.py`



