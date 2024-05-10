# load the python image needed for the app
FROM python:3.9

# create an app folder in the root folder
WORKDIR /app

# copy the app files to the app folder in the root
COPY . /app/

# run the installion command to install the packages from the requirements file.
RUN pip install -r /app/requirements.txt

# run the main python file of the app
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080"]