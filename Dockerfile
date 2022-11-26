# 
FROM python:3.10.0

# 
WORKDIR /

# 
COPY ./requirements.txt /requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# 
COPY . /
EXPOSE 8000
# 
CMD ["uvicorn", "app.main:app","--host", "0.0.0.0", "--port", "80"]
