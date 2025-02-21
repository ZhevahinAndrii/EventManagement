FROM python:3.10-slim
LABEL authors="Андрій Жевагін"


WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app/
EXPOSE 80
CMD sh -c "./wait-for-it.sh ${DB_HOST}:${DB_PORT} -- \
    && python manage.py migrate \
    && if [ \"$DEBUG\" = \"False\" ]; then python manage.py collectstatic --no-input; fi \
    && if [ \"$DEBUG\" = \"False\" ]; then gunicorn -b 0.0.0.0:8000 --workers 4 EventManagement.wsgi:application; else python manage.py runserver 0.0.0.0:8000; fi"
