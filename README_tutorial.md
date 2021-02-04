# CAETÊ

**Disclaimer: This is a heavly altered for of jpdarela/CAETE-DVM, do not merge it with the original one**

This is the implementation of the Dynamic version of CAETÊ - including Nitrogen and Phosphorus cycling

The code in this repository is based on an earlier version of CAETÊ that was not dynamic and did not have the N and P cycling implemented.

THis is part of my ongoing PhD research project.

# For me to run

If you have just coloned this project you should:

- Install pyhthon poetry

The `project.toml` is a file describing the python dependencies for the project.
The `poetry.lock` defines the exact versioning of each lib to avoid collisions.

To install the dependencies just run.
`poetry install`

To start a python virtual environment with the libs you have just installed, simple run on the vscode terminal:
`poetry shell`

To exist the (.venv) shell just type `exit` on the terminal.

While inside the `(.venv)` shell you can run python commands using `poetry run python _python_file_.py`

# Configuring Fortran Debug

To debug fortran code in fscode, with breakpoint you will need `gdb`, the `Modern Fortran` vscode extension,the `Fortran Breakpoint` vscode extension, and `C/C++` vscode extintion.
You can find all of them in the vscode extention marketplace

Make sure to install them all before continuing.

After that you need to create a vscode task to compile your fortran code, you can use this as an example:
Create a file named `tasks.json` insede your `.vscode` folder:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "make debug",
      "type": "shell",
      "command": "make debug",
      "options": {
        "cwd": "${workspaceRoot}/src"
      }
    }
  ]
}
```

This task simply runs the `make debug` inside the Makefile when it is called. The `make debug` compiles all fortran files, creates a

Then, you need to configure how the vscode debugger will be lounched.
For that open you `launch.json` inside you `.vscode` folder and add the following:

```json
{
  "name": "Debug Fortran",
  "type": "cppdbg",
  "request": "launch",
  "program": "${workspaceRoot}/src/run_debug",
  "args": [],
  "stopAtEntry": false,
  "cwd": "${workspaceRoot}",
  "externalConsole": false,
  //If you are using linux you are probably already have gdb
  "MIMode": "gdb",

  //If you are using macOS you probably have lldb, which is worst than gdb
  //"MIMode": "lldb",
  //"miDebuggerPath": "/usr/bin/lldb",

  "preLaunchTask": "make debug"
  // "logging": {
  //   "trace": true,
  //   "traceResponse": true,
  //   "engineLogging": true
  // }
}
```

If you are using linux, you have `gdb` so you don need to change anything in the code above.
What this configuration does is: it run the `make debug` task we have previously in our `tasks.json` file runs the `run_debug` file, that is inside the `/src` folder, in the vscode debugger interface.

With that you can set breakpoints in your fortran code, check stacktraces and variables values.

Since `caete_module` is compiled as a library and not a program, you will need to make a program that calls specific subroutines in the `caete_module` file. For an example of how to do it check them check the `debug_caete.f90` file, inside the `/src` folder.

# Debugging Mixed Python and Fortran code

I am still working on a mixing debuggin solutiion. I haven't managed to make it work in anyway and I don't think it has any simple solution. Solutions I have found use paid debugger aplication or a paid IDE, such as the Microsoft Visual Studio or the ARM debugger.

I think it is probably an f2py limitation.
I tried to run the model_drive.py using the Python debugger and while it is on pause I attached `lldb` to the python process running the `model_driver.py`. I added a breakpoint to the `budget.f90`it does not pause on it. I am not sure if there is a reasonable solution to that.

If anyone has an idea, please tell me.
This is the best post I found about it:
(https://nadiah.org/2020/03/01/example-debug-mixed-python-c-in-visual-studio-code/)[https://nadiah.org/2020/03/01/example-debug-mixed-python-c-in-visual-studio-code/]

# A very minimun git cheatsheet

These are some very basic git command in case you have forgotten them.

To clone a repository to your computer:
`git clone link_to_the_repository_`

To link all your branches:
`git branch`

The `*` will show which branch you are currently on.

To create a new branch: (avoid using spaces, git does not deal well with it, so use - or \_ between words)
`git branch my_branch`

After you crate a branch you probably want to move to it, to do it just type:
`git checkout my_branch`

Now you are in your new branch.

Then you changes some lines, to see what files have been changed:

`git status`

You realised you did not liked the changes you made to one specific, and you want to go back to the original file. You can just do: (Pay attention to the double slashes before the name of the file!!!)
`git checkout --the_file_you_messed_up`

I another file, you have changed some stuff and you liked it! and now you want to commit it. Simply do:

`git add the_name_of_the_file_that_you_changed`

To all all the files you have changes you can simply:

`git add .`

This is dangerous, try to avoid it. It is much better to add file by file.

Now you have added all your amazing changes and you can commit them to your branch.
Before commiting it is always useful to double check the branch you are in with `git branch`, you don't want to commit stuff in the wrong branch.

Now that you are sure you are in the right branch, you can commit by doing:
`git commit -m "you message"`
It is good practice to write a good short description of you change, and remember that the text must be inside the double quotes " ".

You realized you commits were great and you want to add it to you master. The best way to do it is to make a pull request. For that you just need to push your personal branch to github. Simply do it like:
`git push origin my_branch`

Now you can go to your gihub and open a pull request

While you were working on you branch you realized that the master branch has been updated.
I you want to update you master you must, move to the master branch and pull all the up updates from the remote master. You can do this by:
`git checkout master` -> to move to the master branch
`git pull origin master` -> this will get the most updated version of the master branch in add it to your local master branch.

If you want to add the changes you just received on you master to your personal branch, you need to move back to your branch and merge your local master to your branch. This is a bit dangerous, so be careful:
`git checkout my_branch` -> to move to the branch you created earlier
`git merge master` -> this will apply the updated master branch to your branch

To check the url of you `origin` you can simply:
`git remote -v`

An that is basically it.

# Keeping your fork up to date

First you need to add the original repository into your remotes. We usually call the original repository upstream.
To add to that in your terminal:
`git remote add upstream https://github.com/jpdarela/CAETE-DVM.git`

now if you run `git remote -v` on your terminal to list your remotes you should see something like:

```bash
origin https://github.com/fmammoli/CAETE-DVM.git (fetch)
origin https://github.com/fmammoli/CAETE-DVM.git (push)
upstream https://github.com/jpdarela/CAETE-DVM.git (fetch)
upstream https://github.com/jpdarela/CAETE-DVM.git (push)
```

Your `origin` is the master branch on your fork, and `upstream` is the original repository that your forked from.

Now we will pull the changes in the `upstream` to our master branch.
For that make sure your are in your master branch.
`git checkout master`

than you can just
`git pull upstream/master master`

that just mean you will take the code from the master branch on the `upstream` repository and apply the changes into your local master branch.

To send the this new updated master to your fork master, namely, your origin, just make a push
`git push origin master`

That means your as sending the contents of your master branch into the origin.

And you are done! :)

# Development Dependencies

CAETÊ depends on a few packages that must be installed beforehand.
You can installed them using your favorite package manager: `apt`, `brew`, `pip`, `poetry`, etc.

General Dependencies

- make (for building automation)

Python Dependencies

- numpy
- f2py (part of numpy)
- cftime
- pandas
- matplotlib
- ipython

Make sure you have them properly installed before running the code.

# Running and Developing CAETÊ

~This section suposses you have a working python environment and an installed fortran compiler.
If you need help setting up your invornment, check this link.~

CAETÊ uses both Python and Fortran and uses `f2py` module to create an interface between them. This means that the Fortran code must be compiled before you can run Python code.

The Makefile inside `/src` folder have useful automation to make it easier.

`make clean` - it clear your python cache, deletes the `/output` folder and deletes all compiled fortran files, including the `.pyf` file.

`make so` - compiles all fortran code and creates the `caete_module.pyf`, the interface between Fortran and Python code.

To run CAETÊ you can do the following:

```bash
# Clean you cache
make clean

# Build caete_module.pyf
make so

# Run the model
python model_driver.py
```

You can also run it interactively inside `ipython` to have direct access to the variables or you can also run it directly from the vscode debug environment. To run using vscode debug environment follow this little guide (Running CAETÊ from vscode debug environment)[#Development-Environment]

# Development Environment

These are some general directions to install a sane `python` development environment so you can avoid multiple python version conflict. This will avoid a lot of `sudo` problems for example or running a library with the wrong `python` version.

In this guide you will install:

- pyenv to manage python version.
- Python
- (Optionally) Poetry to manage the project dependencies.
- Vscode extensions for debuging python and fortran90.

## Installing Python

The solution here is to use a `python` version manager called `pyenv`. It will enable you to configure a python environment without breaking the python environment of your operating system.
This is largely based on this great tutorial: [Creating a sane Python Dev Env](https://pwal.ch/posts/2019-11-10-sane-python-environment-2020-part-1-isolation/)

## Pre-requesits

**For MacOS**

For MacOs you need to install Xcode, Xcode Command Line Tools and Homebrew.
XCode:
To install Xcode, go to the App Store and download it. It is a large download ~(12GB) so it can take a while.
Then, open Xcode and install any additional component if it requires any.
After installing Xcode, restart your Mac.

Xcode Command Line Tools
Open your terminal and paste the following:

```
xcode-select --install
```

It may open you update center or say you already have command line tools installed.
Close your terminal and open it again so changes can have effect.

Homebrew
Homebrew is a packege manager for MacOs, it works much like `apt` in linux systems. To install it, just paste the code in your terminal:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

Close your terminal and open it again so changes can have effect.

Support Libraries
Now you can install the dependencies for `pyenv`, for that just run on your terminal:

```
brew install openssl readline xz
```

Close your terminal and open it again so changes can have effect.
And now you are ready to install `pyenv`.

**For Linux (Ubuntu)**

To install the required dependencies on Ubuntu you can simply use `apt-get`. Just run the following:

```
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
```

Close your terminal and open it again so changes can have effect.
And now you are ready to install `pyenv`.

## Installing and configuring pyenv

`pyenv` can be installed by a simple command line, just open your terminal and paste:

```
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

Close your terminal and open it again so changes can have effect.

Now you need to add some initialization configuration.

If you are on MacOs, open your `~/.zshrc` file. You can open it in vscode using your terminal, just paste:

```
code ~/.zshrc
```

If you are on Ubuntu, open your `~/.bashrc` file. You can open it in vscode using your terminal, just paste:

```
code ~/.bashrc
```

At the end of the file, paste the following:

```bash
## Setting up shims for pyenv
# ref https://pwal.ch/posts/2019-11-10-sane-python-environment-2020-part-2-pyenv/
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Close your terminal and open it again so changes can have effect.

to check if `pyenv` is working, just type on your terminal:

```
pyenv versions
```

You should see something like that:

```
➜ pyenv versions
* system (set by /home/fmammoli/.pyenv/version)
```

This is your system pyton, the one that comes installed by default by your MacOS or your Linux.

## Using Pyenv to install Python

Now we can finally install `Python` using `pyenv`.

For that, open your terminal and type:

```
pyenv install --list | grep 3.8
```

This will list all available 3.8 python versions, to look for other versions just change the 3.8 to 2.7, for example, if you need to install python 2 for some reason.

The version I want is 3.8.6, but find which version you need and then type:

```
pyenv install 3.8.6
```

This can take a while, so don't panic. If nothing changes in 10min or so, you may have a problem.

You should see something like that on your terminal, but with different filepaths:

```
Downloading Python-3.8.6.tar.xz...
-> https://www.python.org/ftp/python/3.8.6/Python-3.8.6.tar.xz
Installing Python-3.8.6...
Installed Python-3.8.6 to /User/fmammoli/.pyenv/versions/3.8.1
```

Update your configurantions by typing:

```
pyenv rehash
```

To check if your new python version was installed correctly, just type:

```
pyenv version
```

And you should see:

```
* system (set by /User/fmammoli/.pyenv/version)
  3.8.6
```

The \* indicates your active Python.

### Changing your default python version

You can change your python version using the `global` command, like the following:

```
pyenv global 3.8.6
```

This will set the python 3.8.6 (the one you just installed previously) as your global pyton version.
To guarantee the changes have effect, close your terminal and open it again.

Now you can run `pyenv versions` on your terminal and you should see something like:

```
 system
* 3.8.6 (set by /User/fmammoli/.pyenv/version)
```

The \* indicates your active python version.

To run `python` on your terminal, you just type:
`python`
And the intercative prompt should start with your active python version. You should see something like:

```bash
Python 3.8.6 (default, Oct 20 2020, 15:15:44)
[Clang 12.0.0 (clang-1200.0.32.2)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
```

You can change your global python to other versions you can use the same syntax, say you want to use the original system version:

```
pyenv global system
```

And that is it! Now you have a

## Installing Poetry

`Poetry` works as a virtual environment manager and as a dependence manager for `python` projects. By using `poetry` we can guarantee that everyone that cloned the repository is using the same `python` version and the same version for every library. This reduces inconsistencies among different environments making bugs easier to track.

To install `poetry` you just need to run a simple script on your terminal.
So open a new terminal and just paste the following:

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

To check if the installation was successful, open a new terminal and run:

```
poetry --version
```

You should see something like `Poetry version 1.1.4`. If not refer to the `poetry` installation guide.

By default, `poetry` install the virtual environment (venvs) in the user folder, which is quite obscure, but we can change it so it installas everything inside the project folder in a new `.venv` folder. For that just run on your terminal:

```
poetry config settings.virtualenvs.in-project true
```

Now you can use `poetry` to stop suffering from weird environment problems.

## Configuring CAETE-DVM to run on poetry

To use

## Installing Dependencies for the CAETE-DVM

Dependencies for the python project are described in the `pyproject.toml`.
Once you clone the repository you have to install all its dependencies.

Since we are using `poetry`, this sted is very simple. First open the terminal insde vscode and `cd` to the root folder of the CAETE-DVM if you are not in it.

Now we have to start the `poetry` virtual environment, for that just run:

```
poetry shell
```

This will create a new shell with the python described in `pyproject.toml` and tell vscode to use the virtual env interpreter.

Now, to install the dependencies, just run:

```
poetry install
```

This will download and install all the required dependencies locally, this can take some time, about 5 to 10min depending on your internet connection. Is it is hanged for more then 3min in the same step, you probably have a problem. Just `ctrl + c` to stop the process and then run it again.

If you have no `error` on your terminal you have successfully installed all CAETE-DVM dependecies!

## Developing and Running the Model

## VS_Code Configuration

A configuration so you can debug the model code using vscode debug features and use both Python and Fortran Intellisense.

### Pre-requisites

This assumes you already have a fortran compiler installed, specially gfortran and a working python environment. If you don't, please read the tutorial from the start.

If you are running a Linux you problably already have gcc.

If you are running MacOS, gcc is installed when you install Xcode and the command-line-tool. (To see how to install both of these, refer to the start of the tutorial).

To check if you have gcc install on any platform, open your terminal and type:

```
gcc --version
```

You should see something like:

```bash
Apple clang version 12.0.0 (clang-1200.0.32.21)
Target: x86_64-apple-darwin20.1.0
Thread model: posix
InstalledDir: /Library/Developer/CommandLineTools/usr/bi
```

If nothing appears, you may have a problem.

### Installing vscode extensions

First, we need to install the fortran-language-server. For that, open your terminal and run the following:

```
pip install fortran-language-server
```

Now open the CAETE project with vscode.

Now we can start installing some useful vscode extensions
For that click in the extension tab, inside vscode and install the following:

- Python,
- Pylance,
- Visual Studio Intellisense,
- Path IntelliSense,
- Modern Fortran\*
- Fortran IntelliSense\*

\*Both Modern Fortran and Fortran IntelliSense depend on an already installed `gfortran` compiller, and Fortran IntelliSense needs the Fortran Language Server running, referer to their offical installation tutorial in case of problems.

### Configuring your vscode environment

Now let's configure everything.

In the root folder of your project you will find the `/.vscode` folder, here is where all configurations will go.

Let's start with `setting.json` file.

First check if if the project is using the correct `python` version,

If you are using `poetry` to manage our virtual environemnts locally we can just point it to ou `.venv` folder. Add the following line:

```json
"python.pythonPath": ".venv/bin/python3.8",
```

If you are not using poetry, add the following:

```json
"python.pythonPath": "~/.pyenv/versions/3.8.6/bin/python",
```

This will inform vscode to use the python interpreter version 3.8.6, installed using pyenv. This line simply point to the python path.

Then, lets configure the new `pylance` language server. Add the following line:

```json
"python.languageServer": "Pylance",
```

Now let's configure the Fortran IntelliSense extention, add the following line:

```json
    "[fortran]": {
        "editor.acceptSuggestionOnEnter": "off"
    },
    "[fortran_fixed-form]": {
        "editor.acceptSuggestionOnEnter": "off"
    },
    "[FortranFreeForm]": {
        "editor.acceptSuggestionOnEnter": "off"
    }
```

In the end, your `settings.json` should look like this:

```json
{
  "python.pythonPath": ".venv/bin/python3.8",
  "python.languageServer": "Pylance",
  "[fortran]": {
    "editor.acceptSuggestionOnEnter": "off"
  },
  "[fortran_fixed-form]": {
    "editor.acceptSuggestionOnEnter": "off"
  },
  "[FortranFreeForm]": {
    "editor.acceptSuggestionOnEnter": "off"
  }
}
```

This will give you code completition and highlight for both Python and Fortran code.

Now let's configure the `lunch.json`. This file will be used by the vscode debug session to lunch the `model_driver.py` automatically.

Create the `lunch.json` inside `.vscode` folder if it does not exist create it and add the following:

```json
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Model Driver",
      "type": "python",
      "request": "launch",
      "cwd": "${workspaceFolder}/src",
      //"program": "${file}",
      "program": "${workspaceFolder}/src/model_driver.py",
      "console": "integratedTerminal"
    }
  ]
}
```

What it does is to inform vscode debug to run `model_driver.py` using python.

Now you run the model directly via the debug tab, use breakpoint, use the debug console inside vscode and watch variables.
You can ever run the model line by line checking all changes in any variables!

## Installing CAETÊ dependencies

The model depends on a few packages to run:

- numpy = "^1.19.4"
- cftime = "^1.2.1"
- pandas = "^1.1.4"
- matplotlib = "^3.3.3"
- ipython = "^7.19.0"

If you are using `poetry` as your python dependency manager, you just need to open the terminal inside vscode and type:

```
poetry install
```

This will install all the dependencies with their correct version using the `poetry.lock` and `pyproject.toml` as the reference files.

If you are not using poetry, you can install them using `pip` directly to your active python. It is better to install them one by one, so you can have a more precisa error log if something goes wrong. To install them just run each `pip` command on your terminal:

```bash
# To install numpy
pip install numpy

# To install
pip install cftime

# To install pandas
pip install pandas

#To install matplotlib
pip install matplotpib

#To install ipython
pip install ipython
```

If you want to run the files inside the `/input` folder, you will need different dependencies that are more complicated to install. This will be covered in a different tutorial.

## Running and Developing CAETÊ

CAETE uses fortran code that must be compiled beforehand so it can be used by the Python code.
To create this interface, CAETE uses `f2py` module that is located inside `numpy`.
All procedures to compile and interface the fortran code is managed in the `Makefile` inside `/src`, there you can change how you call the f2py module and check the individual steps.

Makefile provides a useful set of feature:
`make clean` will delete the outputs and cleand the python cache.
`make so` will compile the fortran code and run f2py.

To run the model you can simply do the following.
In your terminal, navigate to the `/src` folder:

````
cd /src
```

Then clean your cache and the old outputs by running:
```
make clean
```

Then compile the fortran code and create the python interface:
```
make so
```

To run the model, simply run:
```
python model_driver.py
```
This will take a long to time to run and use a lot of your computer resources, but you can stop at any time by pressing ctrl+c on your terminal.

All outputs will be saved on the folder `/src/outputs`.
To run the model again make sure you cleaned your previous outups by running `make clean`.
If you make any changes to any fortran file, you will need to run `make so` again, before running `model_driver.py`.

You can also run it through vscode debug tab. Considering you have already configured `.vscode/launch.json`, just go to the debug tab and click the little green arrow or press F5.

You can also run it interactively by using `ipython`.


python

## __AUTHORS__:

 - Bianca Rius
 - David Lapola
 - Helena Alves
 - João Paulo Darela Filho
 - Put you name here! (labterra@unicamp.br)
````
