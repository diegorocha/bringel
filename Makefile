VERSION=dev

lint:
	@flake8

test:
	@pytest src --cov=bringel --cov=store --cov-report html --cov-report term-missing:skip-covered


build-web:
	@docker build --build-arg="APP_MODE=web" --build-arg="APP_VERSION=$(VERSION)" -t bringel:web-$(VERSION) .


build-worker:
	@docker build --build-arg="APP_MODE=worker" --build-arg="APP_VERSION=$(VERSION)" -t bringel:worker-$(VERSION) .

build: build-web build-worker
