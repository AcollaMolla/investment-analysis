# investment-analysis
A collection of notebooks and source data that I use to analyze investment cases

# Installing
## Installing Python
### On Windows
The easiest way to install Python on Windows is to do it via Microsoft Store:
1. Open Powershell and type `python`
2. You should be redirected to Microsoft Store and follow the instructions there to install Python
3. Close Powershell and open it again and type `python --version` -- You should see a output similar to `Python 3.10.9` depending on what version of Python you installed.

## Installing Jupyter
Install Jupyter from the command-line by opening PowerShell and run:

```
pip install jupyterlab
```

The installation will take a few minutes.

Finally, install Jupyter Notebook with:

```
pip install notebook
```

You can now launch Jupyter Notebook with:

```
python -m notebook
```

> You might have to restart PowerShell before running `python -m notebook`!

If this is the first time you are running Jupyter Notebook you might have to set a token and password. The token can be found in the PowerShell session where you started Jupyter Notebooks using `python -m notebook`. It will look something like this:

```
[C 13:00:59.645 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///C:/Users/Dator%201/AppData/Roaming/jupyter/runtime/nbserver-9804-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/?token=<TOKEN>
     or http://127.0.0.1:8888/?token=<TOKEN>
```

Copy any one of these tokens and goto `localhost:8888` in you Web Browser and select to log in to Jupyter Notebook using Token.