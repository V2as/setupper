import subprocess
import time

def run_command(command):
    """Run a shell command."""
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Executed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")

def main():
    # Step 1: Update, upgrade, and install necessary packages
    run_command("apt-get update; apt-get upgrade -y; apt-get install curl socat git -y")
    
    # Step 2: Install Docker
    run_command("curl -fsSL https://get.docker.com | sh")
    
    # Step 3: Clone the Marzban-node repository
    run_command("git clone https://github.com/Gozargah/Marzban-node")
    
    # Step 4: Create a directory for Marzban-node
    run_command("mkdir -p /var/lib/marzban-node")
    
    # Step 5: Navigate to the Marzban-node directory
    run_command("cd ~/Marzban-node")
    
    # Step 6: Replace the content of the docker-compose.yml file
    docker_compose_content = """
services:
  marzban-node:
    # build: .
    image: gozargah/marzban-node:latest
    restart: always
    network_mode: host

    environment:
      SSL_CLIENT_CERT_FILE: "/var/lib/marzban-node/ssl_client_cert.pem"

    volumes:
      - /var/lib/marzban-node:/var/lib/marzban-node
"""
    with open("docker-compose.yml", "w") as file:
        file.write(docker_compose_content)
        print("docker-compose.yml file updated.")

    # Step 7: Ask the user for the SSL client certificate content
    print("Please paste the content for ssl_client_cert.pem. The process will continue after detecting '-----END CERTIFICATE-----':")
    ssl_cert_content = ""
    while True:
        line = input()
        ssl_cert_content += line + "\n"
        if "-----END CERTIFICATE-----" in line:
            break
    
    # Step 8: Save the ssl_client_cert.pem content to the specified path
    with open("/var/lib/marzban-node/ssl_client_cert.pem", "w") as ssl_file:
        ssl_file.write(ssl_cert_content)
        print("ssl_client_cert.pem file created at /var/lib/marzban-node/")

    # Step 9: Wait for 3 seconds
    time.sleep(3)
    
    # Step 10: Bring up the Docker containers
    run_command("docker compose up -d")

if __name__ == "__main__":
    main()
  
