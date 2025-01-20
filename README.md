# [Bless Unoffical Docker](https://github.com/hotrungnhan/Bless) 

## [Support me by register account with REF, thanks you !!!](https://bless.network/dashboard?ref=NZ7IIO)
# Setup
1. [Download Docker Desktop](https://www.docker.com/products/docker-desktop).
2. Login to [Bless](https://bless.network/dashboard).
3. Download Extensions and start a node.
4. Open [chrome-extension://pljbjcehnhcnofmkdbjolghdcjnmekia/index.html](chrome-extension://pljbjcehnhcnofmkdbjolghdcjnmekia/index.html)
5. Inspect to get javascript console.
6. Retrive key by type this javascript command.
```javascript
await chrome.storage.local.get()

/*

{
    "authToken": "sample text",
    "nodeData": {
        "peerEncryptedPrivKey": "sample text",
        "peerPubKey": "sample text"
    }
}

*/
```
7. Replace `AUTH_JWT` with authToken, `NODE_PRIVATE_KEY` with peerEncryptedPrivKey, `NODE_PRIVATE_KEY`  with peerPubKey.
8. Open CMD and use the Docker Run command of the built image from Docker Hub.
9. Check and Manage the app from Docker Desktop > Containers.
10. If you're container stuck at any step, please verify your credential.
# Usage Options
## A) Use built image from [Docker Hub](https://hub.docker.com/r/kellphy/nodepay)
#### Docker Compose
```
services:
  nodepay:
    image: hotrungnhan/bless
    restart: unless-stopped
    pull_policy: always
    environment:
      - AUTH_JWT=your_key
      - NODE_PRIVATE_KEY=your_key
      - NODE_PUBLIC_KEY=your_key
```
## B) Docker Run
```
docker run -d \
  --restart unless-stopped \
  --pull always \
  -e AUTH_JWT="your_key" \
  -e NODE_PRIVATE_KEY="your_key" \
  -e NODE_PUBLIC_KEY="your_key" \
  hotrungnhan/bless
```

# Credit 
* [Kellphy](https://github.com/Kellphy)
* * [MRColorR](https://github.com/MRColorR)