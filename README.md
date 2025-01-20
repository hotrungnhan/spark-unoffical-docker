# [Spark Unoffical Docker](https://github.com/hotrungnhan/spark-unoffical-docker) 

## [Support me by register account with REF, thanks you !!!](https://sparkchain.ai/register/?r=46694143)
# Setup
1. [Download Docker Desktop](https://www.docker.com/products/docker-desktop).
2. Login to [Sparkchain](https://sparkchain.ai/dashboard).
3. Download Extensions and start a node.
7. Replace `EMAIL` with your email, `PASSWORD` with your password.
8. Open CMD and use the Docker Run command of the built image from Docker Hub.
9. Check and Manage the app from Docker Desktop > Containers.
10. If you're container stuck at any step, please verify your credential.
# Usage Options
## A) Use built image from [Docker Hub](https://hub.docker.com/r/hotrungnhan/sparkchain)
#### Docker Compose
```
services:
  sparkchain:
    image: hotrungnhan/sparkchain
    restart: unless-stopped
    pull_policy: always
    environment:
      - EMAIL=your_key
      - PASSWORD=your_key
```
## B) Docker Run
```
docker run -d \
  --restart unless-stopped \
  --pull always \
  -e EMAIL="your_key" \
  -e PASSWORD="your_key" \
  hotrungnhan/sparkchain
```

# Credit 
* [Kellphy](https://github.com/Kellphy)
* [MRColorR](https://github.com/MRColorR)
