FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-devel
MAINTAINER CHOMEII <meii11cao@gmail.com>

ENV MYPATH /workspace
WORKDIR $MYPATH

COPY test ./test

ENTRYPOINT ['python', 'test.py']