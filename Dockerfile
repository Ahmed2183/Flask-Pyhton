FROM python:3.10-slim
 
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
 
COPY . /flaskBlog
WORKDIR /flaskBlog
 
# Expose port 80
EXPOSE 80
 
# Specify the command to run the application
CMD ["python", "run.py"]
 