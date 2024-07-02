# Portsey

Portsey is my first complete Python3 script and is a little bit like the "netstat -tuln" command, showing the open ports on a machine but with the added benefit of tying this data to local services, binaries and processes just as the "lsof" or "ss" commands would. I recommend creating an alias to run this Python script for quicker access.

I've looked all over the internet for something similar, and I couldnt find anything to satisfy my requirements. You will find loads of people coming up with the most sophisticated methods in piping either netstat, ss, or lsof with each other, while utilizing obscure arguments to acheive a specific scenario but for my case, all I wanted was a simple yet complete way to qeury my local or remote servers IP ports. 

The only way I could get what I wanted was to learn basic Python and through aching trial and error, eventually write a script that does exactly what I wanted. This is Portsey.

Getting Started:

Portsey the script has some Python modules it requires to functions so as a rule of thumb, always manage installing new Python modules and libraries while in virtual environments so you dont accidentaly break your systems Python.

1) Create and/or activate your Python virtual environment because 
  Linux/MacOS: python -m venv /path/to/new/virtual/environment
  Windows: c:\>Python35\python -m venv c:\path\to\myenv

2) Activate your newly created virtual environment named "myenv".
  Linux/MacOS: source myenv/bin/activate
  Windows: C:\> myenv\Scripts\activate.bat

3) Install required Python module using pip3.
   pip3 install prettytable

4) Run the script with:
   Python3 portsey.py

That's it! If you're into experimentation with home or cloud computer labs, or even anywhere in between a beginner and expert hacker tinkerer, then I promise Portsey will benefit you loads.

 Optional: For quick launch of the script, i recommend creating an alias for the "Python3 portsey.py" command so you could call on the script only with its alias "ie: ports" no matter where you are in your shell.

