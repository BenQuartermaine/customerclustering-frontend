FROM python:3.8.12-buster 

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY raw_data/td.csv ./raw_data/td.csv
COPY customerclustering-frontend/ ./customerclustering-frontend/
COPY app.py .

CMD streamlit run app.py --server.port $PORT --server.address 0.0.0.0
