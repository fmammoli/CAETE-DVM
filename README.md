# CAETÊ
This is the implementation of the Dynamic version of CAETÊ - including Nitrogen and Phosphorus cycling

The code in this repository is based on an earlier version of CAETÊ that was not dynamic and did not have the N and P cycling implemented.

THis is part of my ongoing PhD research project.

# Development Environment
These are some general directions to install a sane `python` development environment so you can avoid multiple python version conflict.

## Installing Python
The solution here is to use a `python` version manager called `pyenv`
For a great tutorial follow: [Creating a sane Python Dev Env](https://pwal.ch/posts/2019-11-10-sane-python-environment-2020-part-1-isolation/)

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

A configuration so you can debug the model using vs code debug features.
First we should install some extensions, for that click in the extension tab, inside vscode and search for:
* Python, 
* Pylance, 
* Visual Studio Intellisense,
* Path IntelliSense,
* Modern Fortran*
* Fortran IntelliSense*

*Both Modern Fortran and Fortran IntelliSense depend on an already installed `gfortran` compiller, and Fortran IntelliSense needs the Fortran Language Server running, referer to their offical installation tutorial.

Now let's configure everything.

Inside you `/.vscode` folder add the following:

Let's start with `setting.json` file.

First check if if the project is using the correct `python` version, since we are using `poetry` to manage our virtual environemnta locally we can just point it to ou `.venv` folder. Check for the following line:
```
"python.pythonPath": ".venv/bin/python3.8",
```

Then, lets configure the new `pylance` language server. Add the following line:

```
"python.languageServer": "Pylance",
```

Now let's configure the Fortran IntelliSense extention, add
```
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
In the end, your `settings.json` should look like:
````
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
````
Now let's configure the `lunch.json`. This file will be used by the vscode debug session to lunch the `model_driver.py` automatically.

Create the `lunch.json` inside `.vscode` folder if it does not exist and add the following:

```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "cwd":"${workspaceFolder}/src",
            //"program": "${file}",
            "program": "${workspaceFolder}/src/model_driver.py",
            "console": "integratedTerminal"
        }
    ]
}
```

Now you run the model directly via the debug tag, use breakpoint, use the debug console inside vscode and watch variables.

## __AUTHORS__:

 - Bianca Rius
 - David Lapola
 - Helena Alves
 - João Paulo Darela Filho
 - Put you name here! (labterra@unicamp.br)
