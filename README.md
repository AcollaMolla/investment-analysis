# investment-analysis
A collection of notebooks and source data that I use to analyze investment cases

# Running the Jupyter Notebook
Clone this repo and start a Jupyter Notebook session on your PC:

```
python -m notebook
```

Go to `localhost:8888` in your preffered Web Browser and navigate to the directory where you cloned this repo.
Open the notebook.

## Mute changes in Git
If you want to use Git and commit your own changes to the source code it is a good idea to tell Git to ignore each Notebook cell run as a change:

```
git config filter.strip-notebook-output.clean 'jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to=notebook --stdin --stdout --log-level=ERROR'  
```

# Prerequisites
This Jupyter Notebook requires that you have the following installed on your PC:

- Python
- Jupyter Lab
- Jupyter Notebook

And the following packages need to be installed in Python:
- `pandas`
- `matplotlib`
- `scipy`

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

## Installing required Python packages
Open a PowerShell window and install the required Python packages needed to run the Notebook in this repo:

```
python -m pip install pandas
python -m pip install matplotlib
python -m pip install scipy
```