# Python Atlassian Accounts
A python implementation for a simple http client to send api calls and receive json responses from Jira and confluence api endpoints

## Prerequisites
- Python 3.10 or later
- Python's requests library

## Installation & Usage
To run the program, simply carry out the following:
Linux:
```bash
git clone https://github.com/Ocinom/py-atlassian-accounts.git
cd py_atlassian_accounts/py_atlassian_accounts
cp constants.py.example constants.py
```
Windows:
```bash
git clone https://github.com/Ocinom/py-atlassian-accounts.git
cd py_atlassian_accounts/py_atlassian_accounts
copy constants.py.example constants.py
```
After which, edit constants.py using a text editor like vim or notepad++
After configuring `constants.py`, run stay in the directory with `main.py` and run the following:
```bash
python main.py
```

## Modules
This program consists of the following modules, each containing their own `README.md` file to detail its functionality:
- api - Http client functionality to communicate with Atlassian servers
- io - ==WIP==  Read and parse files into data structure implementations to be used by the http module
- logs - The directory to contain log files


## TODO:
[] Create a simple implementation in the io module to read csv data and process it into data structures
[] Configure logging for the io module
[] Update main.py to read csv files to be parsed in the io module
[] Update main.py to pass csv data to http calls in the api module
