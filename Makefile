SERVER=docker.io
OWNER=wizelinedevops
REPOSITORY=yasna
VERSION := $(shell cat version)
FULL_NAME=$(SERVER)/$(OWNER)/$(REPOSITORY):$(VERSION)

build:
	@docker build --no-cache -t $(FULL_NAME) .

push:
	@docker push $(FULL_NAME)
