# The Dunk Detector 

Welcome to our CS3200 - Dtabase Design semester project! Our team decided to build a data-driven basketball scouting and analytics application. The Dunk Detector serves as the all-in-one platform for coaches, general managers, data scientists, and scouts to find all the data they need to make informed decisions about their team, players, and game strategies. 

For example, coaches will be able to pull and compare their players' statistics against up and coming rivals or potential recruits to better understand how to develop a solid game startegy and where to best spend their scouting efforts. Similarly, data nalaysts are able to pull information from the statistics table and any other relevant tables to identify team and individual player performance trends and key team statistics. General managers will have access to players contract information and other essential financial data to ensure that the team's budget is being efficiently spent. Lastly, scouts will be able to keep track of highlight players to then generate and upload scout reports that the coaches and GMs can access.  

# How to Run this Application
1. Clone the repository with your favorite git integration (`HTTP`, `SSH`, `CLI`). 
2. Create a virtual environment by running the following commands:
```
pip install virtualenv
python<version> -m venv <virtual-environment-name>
```
If you wish, you can directly install all the requirements onto the `venv` by running `pip install -r requirements.txt` 

3. If you do not have it already install Docker on your computer. Then run the following commands to create the `api`, `app`, and `db` containers with `docker-compose`: `docker compose -f docker-compose.yaml up -d`. If you wish to shutdown and delete all the containers run the following command: `docker compose -f docker-compose.yaml down`. To start a specific container, like the `db` container, run the following command: `docker compose -f docker-compose-testing.yaml up db -d` only start the database container (replace `db` with `api` or `app` for the other two services as needed). To stop the containers from running when not needed but not deleting them, run: `docker compose -f docker-compose-testing.yaml stop`.

4. Note: The repository also contains `-testing.yaml` `docker-compose` files. Use these for testing purposes once you clone the repo if you wish to modify it. Once your changes are working and have them pushed to main, delete and re-create the containers and try running the app again!

5. Now, you should be able to access the application at `localhost:85001`

# Further Reading
For more specific information, read `INSTRUCTIONS.md` or check out any of the other `README.md` files throughout the repo.  