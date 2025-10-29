FROM ubuntu:latest
LABEL authors="laris"

ENTRYPOINT ["top", "-b"]