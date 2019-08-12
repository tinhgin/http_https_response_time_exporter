FROM python

COPY --chown=nobody:nogroup resptime_exporter.py /start.py

RUN set -x  \
    && rm /etc/localtime	\
	&& ln -s /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime	\
    && pip install prometheus_client requests numpy

USER nobody

CMD python /start.py