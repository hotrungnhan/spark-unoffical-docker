build: 
	docker buildx build -t hotrungnhan:${version} -t hotrungnhan:latest --push .

test:
  docker run -d \     
  --name bless \
  --cpus="0.1" \
  --memory="250M" \
  -e AUTH_JWT="your_key" \ 
  -e NODE_PRIVATE_KEY="your_key" \
  -e NODE_PUBLIC_KEY="your_key" \
  hotrungnhan/bless:${version}