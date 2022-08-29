FROM python:3.8.12-buster 

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY raw_data/ ./raw_data/
COPY customerclustering_frontend/ ./customerclustering_frontend/
COPY app.py .

CMD streamlit run app.py --server.port $PORT --server.address 0.0.0.0
