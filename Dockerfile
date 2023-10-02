FROM python:3.11

WORKDIR /agent

RUN apt-get update -y
RUN apt install libgl1-mesa-glx wget libglib2.0-0 -y

COPY ./requirements.txt /agent/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /agent/requirements.txt

# COPY ./assets /code/assets
# COPY ./assets /usr/local/lib/python3.11/site-packages/streamlit/static/assets
# this is for making sure the assets are available to the index.html file

COPY ./.streamlit /agent/.streamlit
# COPY index.html /usr/local/lib/python3.11/site-packages/streamlit/static/index.html

EXPOSE 8501

ENTRYPOINT [ "streamlit", "run" ]
CMD [ "agent_with_ui.py", "--server.headless", "true", "--server.fileWatcherType", "none", "--browser.gatherUsageStats", "false"]