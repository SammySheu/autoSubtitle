FROM python

COPY . /home

WORKDIR /home

RUN pip3 install --upgrade -r ./requirements.txt

RUN apt update && apt install -y ffmpeg

RUN install -m 644 ./font_config/PingFang.ttc /usr/share/fonts/truetype/

CMD [ "python3", "main.py" ]