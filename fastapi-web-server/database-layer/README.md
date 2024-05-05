# Database Layer

The docker compose file within this directory will start the database and rabbitmq servce
for the server system to use.

The db-init-us has our specific database setup and so should not be available externally
from the project.  Specifically we should not commit the 03_uudex.sql to the repository.
I have added it to the .gitignore so that it is not accidentally committed.

## Starting database server and rabbitmq

docker compose up -d will start the system in the background.  The shell should be in
the current directory before running the docker compose command.
