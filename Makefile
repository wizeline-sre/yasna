SERVER=docker.pkg.github.com
OWNER=wizeline-sre
REPOSITORY=yasna
IMAGE_NAME=yasna
VERSION := $(shell cat version)
FULL_NAME=$(SERVER)/$(OWNER)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION)

build:
	@docker build -t $(FULL_NAME) .

push:
	@docker push $(FULL_NAME)