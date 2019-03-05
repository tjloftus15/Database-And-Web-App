# Database-And-Web-App
Created a database which was located on AWS cloud services and accessed by a web application (Python Portion)


This repository showcases the Python portion of the database-web application. these files make up the server, which accesses the database.
The files under 'server' are the files which are of interest here. The database is relational, and uses MySQL. 
The '__init__.py' file handles all the HTTP routing from the interactions of the user with the UI. It then routes the request to the corresponding method in 'database.py', which then queries the database, and returns the results, which are displayed in graph or table form on the web page.

## About My Database

My database is on the AWS cloud. I have removed the URL and key for safety reasons. The schema is Bar-Beer-Drinker. There are 4 entity tables and 4 relational tables. There is the drinker, item, bar, and bill tables, which are the entity ones. Then, there are the Likes, Frequents, Sells, and Transaction tables, whihc are the relational tables. In summary, the database has a collection of people, where the people live, bars, where the bars are located, things the bar sells, bills at at the bars, what drinks people like, what bars people frequent, what items bars sell, and information about the bills, called transactions.
