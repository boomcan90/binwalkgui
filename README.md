# binwalkgui

## Getting prepped to work on this 

Install virtualenv to ensure that the dependencies don't clutter the global requirements. This can be done with 

```bash
sudo pip3 install virtualenv
```

Create and activate a virtualenv with the following commands: 

```bash
virtualenv -p python3 venv
source venv/bin/activate
```

After running these commands, the bash terminal should look like this: 

```sh
(venv) arjun@ubuntu:~/Desktop/binwalkgui$ 
```
Note the `(venv)` at the beginning of the prompt. This tells that the venv environment has been activated. 


## Installing binwalk 

To install binwalk, after activating the virtual environment, run the following commands: 

```bash
git clone git@github.com:ReFirmLabs/binwalk.git
cd binwalk 
python setup.py install 
```

This will install binwalk into the virtualenvironment for testing. 


## Installing tk

To instll tk, run the following commands: 

```bash
sudo apt install python3-tk
```

## Installing matplotlib (for entropy plotting)

To install matplotlib, run the following command:
```bash
python -m pip install -U matplotlib
```

## Using custom signatures

First, select the file you wish to scan (use [custom.zip](custom.zip) for demo)

Then from the 'Expert' option, select 'Search with custom magic file only'

Select the file that contains your custom signatures (use [magic.mgc](magic.mgc) for demo)
