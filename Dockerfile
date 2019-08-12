FROM python

COPY --chown=nobody:nogroup resptime_exporter.py /start.py

RUN pip install prometheus_client requests numpy

USER nobody

CMD python /start.py