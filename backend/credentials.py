# Importing required libraries
import os

# please enter the Database Configurastion below.
ENDPOINT= os.getenv( "POSTGRES_ENDPOINT")
PORT = os.getenv("POSTGRES_PORT")
USER = os.getenv("POSTGRES_USER")
DBNAME = os.getenv( "POSTGRES_NAME") 
PASSWORD = os.getenv("POSTGRES_PASSWORD")

