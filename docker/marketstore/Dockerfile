FROM marketstore:bc

COPY ./mkts.yml /etc/mkts.yml

ENTRYPOINT ["marketstore"]
CMD ["start", "--config", "/etc/mkts.yml"]
