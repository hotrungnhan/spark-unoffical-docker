export EXTENSION_ID=jlpniknnodfkbmbgkjelcailjljlecch
export WEB_URL=https://sparkchain.ai/dashboard
export GIT_USERNAME=sryze
export GIT_REPO=crx-dl
export PUBLIC_CONTAINER_PATH=hotrungnhan/spark

build: 
	docker buildx build -t $(PUBLIC_CONTAINER_PATH):${version} -t $(PUBLIC_CONTAINER_PATH):latest --push .

test:
  docker run -d \
  --name bless \
  -e EMAIL=${email} \
  -e PASSWORD=${password} \
  $(PUBLIC_CONTAINER_PATH):${version}
  
test_local:
	EXTENSION_ID=${EXTENSION_ID} \
	WEB_URL="${WEB_URL}" \
	EMAIL="${email}" \
	PASSWORD="${password}" \
	python3 main.py

download_ext:
	if [ ! -d "$(GIT_REPO)" ]; then	\
		git clone "https://github.com/$(GIT_USERNAME)/$(GIT_REPO).git"; \
	else \
		echo "$(GIT_REPO) already exists, skipping git clone."; \
	fi
	python3 ./$(GIT_REPO)/crx-dl.py "$(EXTENSION_ID)"
