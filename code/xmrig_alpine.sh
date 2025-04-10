#!/bin/sh

# Update package lists
apk update

# Install required packages
apk add --no-cache curl build-base

# Install XMRig miner
curl -L https://github.com/xmrig/xmrig/releases/download/v6.18.1/xmrig-6.18.1-linux-x64.tar.gz -o xmrig.tar.gz
tar -xvzf xmrig.tar.gz
cd xmrig-6.18.1
chmod +x xmrig

# Configure the miner (using the user's provided wallet and pool settings)
POOL="gulf.moneroocean.stream"
PORT="10128"
WALLET="45nqWWu8CV6WuNpEhbNAu4DWTmfUQBxRCWdND6iQVXyAL3cNNTeQoUWCmMzcaScdnJXJY3ttWxwJy9boywbN2XCn8Ejig1s"

# Run the miner
./xmrig -o $POOL:$PORT -u $WALLET -p x
