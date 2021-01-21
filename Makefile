SERVER=quay.io
OWNER=wizeline-sre
REPOSITORY=yasna
VERSION := $(shell cat version)
FULL_NAME=$(SERVER)/$(OWNER)/$(REPOSITORY):$(VERSION)

build:
	@docker build --no-cache -t $(FULL_NAME) .

push:
	@docker push $(FULL_NAME)
