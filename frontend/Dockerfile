FROM grafana/grafana:11.1.0-ubuntu

COPY ./grafana_cfg /frontend
WORKDIR /frontend
USER root
RUN cat grafana.ini >> /etc/grafana/grafana.ini
USER 472
RUN grafana-cli --pluginUrl https://github.com/grafana/grafana-infinity-datasource/releases/download/v2.9.2/yesoreyeram-infinity-datasource-2.9.2.zip plugins install yesoreyeram-infinity-datasource
RUN cp grafana.db /var/lib/grafana/grafana.db
RUN chmod 640 /var/lib/grafana/grafana.db

ENTRYPOINT ["/run.sh"]
