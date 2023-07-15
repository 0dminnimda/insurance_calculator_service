FROM python:3.9

WORKDIR /app

COPY ./requirements/basic.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./insurance_calculator_service /app/insurance_calculator_service

EXPOSE 80
CMD ["python", "-m", "insurance_calculator_service", "--host", "0.0.0.0"]
