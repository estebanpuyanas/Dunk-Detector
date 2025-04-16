# `database-files` Folder

The database for this project is created at the `DunkDetector.sql` file. From reading the file, you will notice that it first does `DROP DATABASE IF EXISTS` followed by `CREATE DATABASE IF NOT EXISTS`, this is done so if there are ny changes made into the DB, the file will delete the existing version and update it with the new version.

From there the file creates all the tables. Do not change the order of table creation, as they are linked in a way to avoid errors to dependencies that do not exist (e.g. the table coaches has an `FK` to `teamId` but teams has not been created yet). If you do choose to change the table creation run it in a database server or connection through a program like datagrip. Lastly, the file adds sample data to all the tables. 

Make sure you also re-start the `db` container as stated in the `./README.md` to ensure changes to the database are reflected server-side. 