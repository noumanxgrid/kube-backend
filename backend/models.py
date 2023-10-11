import psycopg2
from credentials import *
from time import ctime


class DB_Connection():

    def __init__(self):
        """
        Creates connection with AWS Aurora Database
        """
        self.conn = psycopg2.connect(host=ENDPOINT, port=PORT,
                                     database=DBNAME, user=USER, password=PASSWORD)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def create_record_table(self):
        """
        Creates a table for all the jobs initialized by the User
        """
        try:
            table = self.cur.execute(
                "CREATE TABLE Jobs (id serial PRIMARY KEY, TimeStamp TEXT, ApiEndpoint TEXT, Frequency INT, Duration INT);"
            )
        except psycopg2.errors.DuplicateTable:
            print(psycopg2.errors.DuplicateTable)

    def create_job(self, api_endpoint, frequency, duration):
        """
        Inserts the data from the Front-End Application into Jobs Table

        :param api_endpoint: A valid url
        :param frequency: The frequency at which API Endpoint will be called
        :param duration: The duration for which API Endpoint will be called
        """
        self.cur.execute(
            "Insert into Jobs (TimeStamp, ApiEndpoint, Frequency, Duration) VALUES (%s, %s, %s, %s)", (ctime(), api_endpoint, frequency, duration))

    def show_jobs(self):
        """
        retuns: All the current Jobs
        """
        self.cur.execute("Select * from Jobs")
        return self.cur.fetchall()

    def create_job_table(self, job_id):
        """
        Creates a table for each Job to store the API data

        :param job_id: The ID of the Job
        """
        try:
            self.cur.execute(
                f"CREATE TABLE table{job_id} (id serial PRIMARY KEY, TimeStamp TEXT, Data TEXT);"
            )
        except psycopg2.errors.DuplicateTable:
            print(psycopg2.errors.DuplicateTable)

    def execute_job(self, job_id, current_time, data):
        """
        Inserts the data from the api_endpoint into the respective job table

        :param job_id: The Id of the Job
        :param current_time: Time at which API is invoked
        :param data: The data which is returned by the api_endpoint
        """
        self.cur.execute(
            f"INSERT into table{job_id} (TimeStamp, Data) VALUES ( %s, %s);", (
                current_time, data)
        )

    def total_jobs(self):
        """
        :returns total_jobs(str): total number of jobs
        """
        self.cur.execute("Select count(*) from Jobs")
        id = self.cur.fetchall()
        return str(id[0][0])

    def get_id_table(self, job_id):
        """
        :param job_id: The id of the Job
        :returns all the records in a job table
        """
        self.cur.execute(f"SELECT * from table{job_id}")
        return self.cur.fetchall()
