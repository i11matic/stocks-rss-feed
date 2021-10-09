FROM python:3.10.0

RUN mkdir /app

RUN mkdir /root/.streamlit
# we need to add an empty cred file to bypass streamlit email prompt
ADD credentials.toml /root/.streamlit

WORKDIR /app

ADD app.py .

ADD dist/stocks_rss_feed-0.1.0-py3-none-any.whl .

RUN pip install stocks_rss_feed-0.1.0-py3-none-any.whl && \
    rm -rf stocks_rss_feed-0.1.0-py3-none-any.whl

ENTRYPOINT streamlit run ./app.py