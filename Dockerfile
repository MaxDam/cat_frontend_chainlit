FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py /app/
COPY ./config/chainlit.md /app/chainlit.md
COPY ./config/.chainlit/config.toml /app/.chainlit/config.toml
CMD chainlit run cat_frontend.py -w
