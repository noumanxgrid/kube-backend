from flask_cors import CORS
from flask import Flask, request
from api_callscheduler import ApiCallSchedular
from models import DB_Connection
import validators


app = Flask(__name__)
CORS(app)


# Defining Home Route


@app.route("/", methods=["GET", "POST"])
def home():
    """
    home function for the default home route

    :return: A string that will be displayed at the home route
    """
    return "This application is created by Faheem Khan - S201"

# Defining activity route where requests will be POST from Front-End


@app.route(
    "/activity",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def process_request():
    """
    This function is used to process the API requests coming from React App
    :param request_data: When Flask app will be called at this route, a response from the
    front-end will be posted here in the following format:

    request format = [{ id: uuidv4(),  api: 'a valid url', freq: 'frequency' , duration: 'duration'}]

    This is an Array, each entity having api endpoint, frequency, and
    duration for which api will be called and data will be published
    """
    db = DB_Connection()
    db.create_record_table()
    request_data = request.json
    for api_request in request_data:
        api = api_request["api"]
        freq = int(api_request["freq"])
        duration = int(api_request["duration"])

        # If API endpoint is valid, It schedules the api calls for each request
        if validators.url(api) == True:
            if (freq > 0 and duration > 0):
                db.create_job(api, freq, duration)
                job_id = db.total_jobs()
                db.create_job_table(job_id)
                print('Job Added')
                api_schedular = ApiCallSchedular(
                    frequency=freq, duration=duration, api_endpoint=api, job_id=job_id
                )
            else:
                return {"response": "Your request can't be processed, Please enter frequency and duration greater than zero!"}
        else:
            return {"response": f"\nPlease enter a valid API-EndPoint. Given API Endpoint({api}) is not valid!"}

    # Returning this response to the Front-End
    return {"response": 'Your Job is successfully Added'}


@app.route("/results",
           methods=["GET", "POST"],
           strict_slashes=False,
           )
def results():
    """
    This function is used to process the requests at results route.
    :returns : All the Running Jobs
    """
    db = DB_Connection()
    jobs = db.show_jobs()
    print(jobs)
    return{'response': jobs}


@app.route("/results/id",
           methods=["GET", "POST"],
           strict_slashes=False,
           )
def process_Id_requests():
    """
    This function is used to process the requests of a certain job
    : returns : All the entries of the Table of a certain job
    """
    request_data = request.json
    db = DB_Connection()
    records = db.get_id_table(request_data['taskId'])
    return{'response': records}


if __name__ == "__main__":
    app.run(debug=True, port=8080)
