# 0x00. AirBnB clone - The console
[]()

## Concepts
* [Python packages]()
* [AirBnB clone]()

# Background Context
## Welcome to the AirBnB clone project!
Before starting, please read the [**AirBnB**]() concept page.

# First step: Writing a command interpreter to manage AirBnB objects.
This is the first step towards building a full web application: the **AirBnB clone**. This first step is very important because what is built during this project will be used with all other following projects: HTML/CSS templating, database storage, API, front-end integration…

Each task is linked and will help to:

* put in place a parent class (called ```BaseModel```) to take care of the initialization, serialization and deserialization of your future instances
* create a simple flow of serialization/deserialization: Instance <-> Dictionary <-> JSON string <-> file
* create all classes used for AirBnB (```User```, ```State```, ```City```, ```Place```…) that inherit from BaseModel
* create the first abstracted storage engine of the project: File storage.
* create all unittests to validate all our classes and storage engine

# What’s a command interpreter?
It's like the Shell but limited to a specific use-case. In this case, we want to be able to manage the objects of our project:

* Create a new object (ex: a new User or a new Place)
* Retrieve an object from a file, a database etc…
* Do operations on objects (count, compute stats, etc…)
* Update attributes of an object
* Destroy an object

## How to start the interpteter
## How to use the interpreter
## examples

# Resources
**Read or watch**:
* [cmd module](https://docs.python.org/3.8/library/cmd.html)
* [cmd module in depth](https://pymotw.com/3/cmd/)
* [packages concept page]()
* [uuid module](https://docs.python.org/3.8/library/uuid.html)
* [datetime](https://docs.python.org/3.8/library/datetime.html)
* [unittest module](https://docs.python.org/3.8/library/unittest.html#module-unittest)
* [args/kwargs](https://yasoob.me/2013/08/04/args-and-kwargs-in-python-explained/)
* [Python test cheatsheet](https://www.pythonsheets.com/notes/python-tests.html)
* [cmd module wiki page](https://wiki.python.org/moin/CmdModule)
* [python unittest](https://realpython.com/python-testing/)

Learning Objectives
At the end of this project, you are expected to be able to [explain to anyone](https://fs.blog/feynman-learning-technique/), **without the help of Google**:

General
* How to create a Python package
* How to create a command interpreter in Python using the ```cmd``` module
* What is Unit testing and how to implement it in a large project
* How to serialize and deserialize a Class
* How to write and read a JSON file
* How to manage ```datetime```
* What is an ```UUID```
* What is ```*args``` and how to use it
* What is ```**kwargs``` and how to use it
* How to handle named arguments in a function

# Requirements
## Python Scripts
* Allowed editors: ```vi```, ```vim```, ```emacs```
* All the files will be interpreted/compiled on Ubuntu 20.04 LTS * using python3 (version 3.8.5)
* All the files should end with a new line
* The first line of all the files should be exactly ```#!/usr/bin/* python3```
* A ```README.md``` file should be at the root of the folder of the project
* The code should use the pycodestyle (version ```2.8.*```)
* All the files must be executable
* The length of the files will be tested using ```wc```
* All the modules should have a documentation (```python3 -c 'print(\_\_import\_\_("my_module").\_\_doc\_\_)'```)
* All the classes should have a documentation (```python3 -c 'print(\_\_import\_\_("my_module").MyClass.\_\_doc\_\_)'```)
* All the functions (inside and outside a class) should have a documentation (```python3 -c 'print(\_\_import\_\_("my_module").my_function.\_\_doc\_\_)'``` and ```python3 -c 'print(\_\_import\_\_("my_module").MyClass.my_function.\_\_doc\_\_)'```)

# Python Unit Tests
* Allowed editors: ```vi```, ```vim```, ```emacs```
* All the files should end with a new line
* All the test files should be inside a folder ```tests```
* Use the [unittest module](https://docs.python.org/3.4/library/unittest.html#module-unittest)
* All the test files should be python files (extension: ```.py```)
* All the test files and folders should start by ```test_```
* The file organization in the tests folder should be the same as your project
* e.g., For ```models/base_model.py```, unit tests must be in: ```tests/test_models/test_base_model.py```
* e.g., For ```models/user.py```, unit tests must be in: ```tests/test_models/test_user.py```
* All the tests should be executed by using this command: ```python3 -m unittest discover tests```
* Test file by file by using the command: ```python3 -m unittest tests/test_models/test_base_model.py```
* All your modules should have a documentation (```python3 -c 'print(__import__("my_module").__doc__)'```)
* All the classes should have a documentation (```python3 -c 'print(__import__("my_module").MyClass.__doc__)'```)
* All the functions (inside and outside a class) should have a documentation (```python3 -c 'print(__import__("my_module").my_function.__doc__)'``` and ```python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'```)
* Work thoroughly on test cases, so that you don’t miss any edge case

# More Info
## Execution
The shell should work like this in interactive mode:
```
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb) 
(hbnb) 
(hbnb) quit
$
```

But also in non-interactive mode: (like the Shell project in C)
```
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
```

All tests should also pass in non-interactive mode: ```$ echo "python3 -m unittest discover tests" | bash```

[]()

# Tasks
### 0. README, AUTHORS
* Write a ```README.md```:
    * description of the project
    * description of the command interpreter:
        * how to start it
        * how to use it
        * examples
* You should have an ```AUTHORS``` file at the root of your repository, listing all individuals having contributed content to the repository. For format, reference [Docker’s AUTHORS page](https://github.com/moby/moby/blob/master/AUTHORS)
* You should use branches and pull requests on GitHub - it will help you as team to organize your work