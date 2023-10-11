from threading import Thread
import requests
from models import DB_Connection
from time import ctime





class ApiCallProcessor():

    def __init__(self, api_endpoint, job_id):
        """
        Constructor for APICallProcessor creates a thread for calling the 
        api endpoint and publishing the data to the database.

        :param api_endpoint: A valid url, which is to be called
        :var thread: A thread which executes a function without blocking the main program  
        :return: Starts the thread and returns Nothing
        """
        self.api_endpoint = api_endpoint
        self.db = DB_Connection()
        # Starting a new thread
        self.job_id = job_id
        self.thread = Thread(target=self.call_processor, args=())
        # Daemon thread will be running in the backend with blocking the main program
        self.thread.daemon = True
        self.thread.start()

    def call_processor(self):
        """
        This function calls the API endpoint and publishes the response to the database.

        :param api_endpoint: A valid url
        """
        try:
            res = requests.get(self.api_endpoint)
            if res.status_code == 200:
                data = str(res.content)
                TimeStamp = ctime()
                self.db.execute_job(self.job_id, TimeStamp, data)
                print('Data inserted:', data)
            else:
                print("Invalid Status Code")

        except requests.exceptions.ConnectionError:
            print(
                requests.exceptions.ConnectionError)
