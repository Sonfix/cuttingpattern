
# Final Project  

The goal was creating a web application for the company i work in which displays the cuttingpatterns of our machines.

The company I work for produces machinery for glas handling www.hegla.com.  

To be able to cut glas it is necessary to have a sort of plan, which tells you how to do it. And this in particular is a cuttingplan. These can come in two different versions and both of them need to be supported by this apllication.

Both versions got a header which contains general information of the plate to cut. The older version has all this information stored in one line where each position has a particular meaning. In the new version the file is structured like an xml file. Where each information has its own node.  

The real cutting information for both version are the same. Within the old version is located right under the header information. In the new version it is located within the Value node of the cuttingcode part.

  

## Distinctiveness and Complexity
 

This project does not build up any other project before. It is being developed for a certain company to have central application for the cuttingplans.

The complexity for this comes by parsing and handling each file. The cutting is structured like a Tree, where each cut builds it's own node. Each cut can have n numbers of childs. As far as the size of the glas can handle those. The cutting data can be cutted in several parts. There are 5 cut levels, X,Y,Z,V,W. X Cuts can contains Y cut childern, Y cuts can have Z children and so on.

While parsing the cutting code value the programm creates a tree (TraverseTree in programm). Handling data structures like these adds the complexity to this project.

Not only the backend needs to handle a tree datastructure, so does the front end. The Javascript with in the brackpic.js analysis the JSON formatted string and creates the graphical display for the cutting plan. This graphical display is realised by translating every node to a div, which then gets the matching style class to be displayed correctly. 

The web application stores the cuttingplan information in two different variations, one is the original code and the other one is the cached JSON formatted string. The application also allows to create customers and also customer groups. A cuttingplan needs to be related to a certain customer to give it a better structure for human understanding.


## How to Use

### Getting started

1. In your terminal, cd into the mail directory.
2. Run python manage.py makemigrations to make migrations for the cuttingpattern app.
3. Run python manage.py migrate to apply migrations to your database.
4. Finally start the server by running python manage.py runserver

## Using the Application

If you're not logged in yet, you will be asked to login or register at this application. 
After logging in you will be redirected to the index page. Here you can see all cuttingpattern which are uploaded by your user.
Clicking on the "Explorer" button in the navigation bar will lead you to a list of all customers and their cuttingplans.

To add a new cuttingpattern you can just drag and drop the given example files, from the example folder. This will than open a from where you can upload the cuttingplans.
You can also get this form by pressing the "Add Cuttingpattern" button in the navigation bar.

If you don't have any customers yet, you can create those by pressing the green plus symbol right next to the select field. A text field and another select field for the customer group will appear. If there are also no groups available you can add them by pressing the next green plus symbol. You can cancel this by pressing the red minus symbol.
Clicking on "send" will add the cutting pattern to the system. If everything succeded the form will close by itself, and reloads the page.



## Specifications

  The following function are supported by this apllication:
  - Register and/or logging in
  - Seeing all created cuttingplans
	  - all cuttingplans created by the user
	  - Name, Description, Customer and the date uploaded
	  - delete a cuttingplan
  - See detailed information of a cuttingplan
	  - getting the layout displayed
	  - seeing the size of each plate
	  - seeing additional sheet infos
	  - would be good to see the used area of sheets
	  - seeing machine cutting code
	  - seeing header information
  - Be able to see each customer and its group
  - Upload new cuttingfiles
	  - uploading by filling a certain form
	  - drag and drop files to prefill the form
  - Editing each models information within the admin page

## Files Description
- views.py: all functions which are called when a certain page is requested
- urls.py: includes all urls used for this project
- models.py: includes all models used for this project
- api.py: This file contains a function for each API call of this application.
- templates folder: Within this foldes any used template can be found
- static folder: Within in this folder you can find all the stylesheets, svgs and javascript files which are in use
	-  breakpic.js: this files contains all functions which are needed for creating the cuttingplan display
	- breakpic.css: contains all stlye information for the cuttingplan display
	- main.js: this files handles all the other functionallity for this project, e.g. calling API functions
	- style.css: contains the common style information for elements
- EDI folder: this foldes contains all the files for handling edi files.
	- edi_body.py: this files contains the classes which are necessary to create the tree datastructure and parsing the given files
	- edi_defines.py: located in this file are small classes which are only containig some data for handling the graphical part
	- edi_header.py: this file stores all the data located in the header of each file
- Examples Folder: in this folder you can find the example files for testing the application
  

## Upcoming features

This is not the end of this little project. A few features will be added in the future:
- implementing the internal optimization tool, this recalculates and realigns cuts regarding some configuration
- adding cuts via the graphical user interface and also export these files to an edi formatted file
- support exporting to the old and new version
- calculating the time needed for cutting each plate
- support files with more than one layout in it
- managing customers
	- changing names
	- changing customer group