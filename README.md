# Database-And-Web-App
Created a database which was located on AWS cloud services and accessed by a web application (Python Portion)


This repository showcases the Python portion of the database-web application. these files make up the server, which accesses the database.
The files under 'server' are the files which are of interest here. The database is relational, and uses MySQL. 
The '__init__.py' file handles all the HTTP routing from the interactions of the user with the UI. It then routes the request to the corresponding method in 'database.py', which then queries the database, and returns the results, which are displayed in graph or table form on the web page.

