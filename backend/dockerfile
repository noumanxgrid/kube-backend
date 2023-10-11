FROM python:3

# setting working dir inside container
WORKDIR /app

ENV FLASK_APP=app.py 

# Copying the required files
COPY . .

# installing requirements
RUN pip install -r requirements.txt

# Exposing port 3001
EXPOSE 3001

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080" ]