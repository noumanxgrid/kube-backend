from threading import Thread
from api_callprocessor import ApiCallProcessor
import time


class ApiCallSchedular():
    def __init__(self, frequency, duration, api_endpoint, job_id):
        """
        Constructor for ApiCallScheduler that Starts a thread for scheduling the calls of api endpoint

        :param frequency: Frequency at which the endpoint will be called
        :param duration: Duration for which to run the REST calls and then publishes the output to the database
        :param api_endpoint: A valid url
        """
        self.frequency = frequency
        self.duration = duration
        self.api_endpoint = api_endpoint
        self.start_time = time.time()
        self.current_time = 0
        self.frequency_in_seconds = (
            3600 / self.frequency
        )
        self.job_id = job_id

        # Starting new thread to schedule the api calls
        self.thread = Thread(target=self.apicall_scheduler, args=())
        # Daemon thread will be running in the backend with blocking the main program
        self.thread.daemon = True
        self.thread.start()

    def apicall_scheduler(self):
        """
        apicall_scheduler function schedules the calls for api endpoint and 
        calls ApiCallProcessor to process the requests

        :param duration: Duration for which to run the REST calls
        :var current_time: time when this function was called
        """
        while self.current_time <= (self.duration * 3600):
            backend_processor = ApiCallProcessor(
                api_endpoint=self.api_endpoint, job_id=self.job_id)
            time.sleep(self.frequency_in_seconds)
            self.current_time = time.time() - self.start_time
