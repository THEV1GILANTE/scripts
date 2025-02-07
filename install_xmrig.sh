#!/bin/bash

ask_input() {
  local prompt=$1
  local default_value=$2
  echo -e "$prompt"
  read -p "$prompt [$default_value]: " input
  echo "${input:-$default_value}"
}

# Step 1: Update system and install dependencies
echo "Updating system and installing required dependencies..."

# Update package lists and install necessary dependencies
sudo apt update -y
sudo apt install -y build-essential cmake git libuv1-dev libssl-dev libhwloc-dev

# Check if git is installed, if not, install it
if ! command -v git &> /dev/null; then
  echo "Git is not installed. Installing Git..."
  sudo apt install -y git
fi

# Step 2: Clone XMRig repository if it doesn't exist
if [ ! -d "xmrig" ]; then
  echo "Cloning XMRig repository from GitHub..."
  git clone https://github.com/xmrig/xmrig.git
fi

cd xmrig

# Step 3: Create a build directory and navigate into it
echo "Creating build directory and navigating into it..."
mkdir -p build
cd build

# Step 4: Build XMRig using CMake
echo "Building XMRig..."
cmake ..
make -j$(nproc)

# Step 5: Ask the user for necessary inputs to configure XMRig
echo "Please provide the following details for your mining setup."

POOL_URL=$(ask_input "Enter the mining pool URL (the address where you will send your mining work)." "stratum+tcp://xmr.kryptex.network:7777")
USER=$(ask_input "Enter your wallet address (or user ID provided by the pool). This is where mined coins will be sent." "krxYMK8ZGD")
PASS=$(ask_input "Enter the password for the pool. Use 'worker' if unsure, or refer to your pool's instructions." "worker")
WORKER_ID=$(ask_input "Enter the worker ID to identify your mining machine on the pool. You can name it whatever you like." "worker")
MAX_CPU_USAGE=$(ask_input "Enter the maximum CPU usage percentage (Recommended: 75-90%)." "75")
THREADS=$(ask_input "Enter the number of threads you want to use for mining. Leave blank for auto-config based on your CPU." "")

# Step 6: Create the config.json file based on user input
echo "Configuring XMRig with the provided settings..."

cat <<EOF > config.json
{
  "autosave": true,
  "cpu": true,
  "pools": [
    {
      "url": "$POOL_URL",
      "user": "$USER",
      "pass": "$PASS",
      "rig-id": "$WORKER_ID",
      "nicehash": false,
      "enabled": true
    }
  ],
  "print-time": 60,
  "max-cpu-usage": $MAX_CPU_USAGE,
  "threads": $THREADS
}
EOF

# Step 7: Start mining with XMRig
echo "Starting the miner..."
./xmrig

# End of script
echo "XMRig setup is complete and the miner is running."
echo "To stop mining, press Ctrl + C."
