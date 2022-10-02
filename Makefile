export version=$(shell cat ./VERSION)
export registry=ghcr.io

# START CHANGE HERE
export fname=terminal
export image=codref/$(fname)-faas
# STOP CHANGE HERE

export extra_params=

build_dev:
	faas build -f $(fname).yml $(extra_params)

up:
	DEPLOY_ENV_NAME=production FAAS_GATEWAY=api.codref.org faas-cli up -f $(fname).yml $(extra_params)

serve:
	docker run --rm -it \
		--env-file $(shell pwd)/.env \
		-v $(shell pwd)/$(fname)/:/home/app/function/ \
		-p 8081:8080 $(registry)/$(image):latest sh -c 'fwatchdog'

shell:
	docker run --rm -it \
		--env-file $(shell pwd)/.env \
		-v $(shell pwd)/$(fname)/:/home/app/function/ \
		-p 8081:8080 $(registry)/$(image):latest sh
				
