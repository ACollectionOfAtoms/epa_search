# Facilitated Access to Public EPA Records
This program should provide a broad overview of EPA violations occuring in the USA at the city, state, and nation wide level. 
## !-----------This projects server is no longer accesible! I plan to redo this as a webapp interfacing with EPA data directly ---------!
### The following are required:
  * Python 2.7.9 + 
    * cx_Oracle
    * wxPython
    * rpy2

## Installing the modules:

Use these terminal commands to install the required Python modules:
```
    pip install cx_Oracle
    pip install rpy2
```

#### Installing wxPython:
If on OSX it is recommended to use Homebrew (http://brew.sh/)
and the following commands:
```
    brew install wxmac
    brew install wxpython
```
#####Alternately:
http://www.wxpython.org/download.php


## Using the program:

While in the folder which contains epa_search.py, simply enter:
```   
     python epa_search.py
```
The rest is intuitive! Take note that any graphs generated will be saved as .pdf's in the current directory!


## An Example:

#### First we run the program: 

![alt text](http://i.imgur.com/WF0yAD0.png "Just type python epa_search.py in your terminal!")

#### Now we select the level of analysis. Here we choose "City wide":

![alt text](http://i.imgur.com/IJYgofm.png "Lets inspect this city!")

#### I'm going to go ahead and choose Rhode Island:

![alt text](http://i.imgur.com/GOqUBzQ.png "I've never been there myself...")

#### Now we type the city name... The capital should do:

![alt text](http://i.imgur.com/2VSV3Yr.png "The capital of Rhode Island")

#### Finally we can inspect the facilities with the largest amount of cumulative EPA violations (These include violations of the Clean Air Act, Clean Water Act, and the Resource Conservation and Recovery Act):

![alt text](http://i.imgur.com/QhgMCpd.png "Energy Companies tend to be high on the list...")

#### After generating the graph, we open it:

![alt text](http://i.imgur.com/tXPPKdt.png "The lovely terminal...")

#### And voilà:

![alt text](http://i.imgur.com/EZq6XHB.png "A wonderful graph")
