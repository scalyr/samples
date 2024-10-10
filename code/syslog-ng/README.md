# **Syslog-ng with Docker**

This project provides a simple Docker configuration to run `syslog-ng`, forward logs using the HTTP Event Collector (HEC) to SentinelOne's ingestion endpoint, and configure multiple log sources.

## **Getting Started**

### **Prerequisites**

* Docker installed  (see bottom of page for instructions)
* Docker Compose installed



### **Installation**

1. Clone this repository or download the necessary files.  
2. Ensure that the following files exist in your project directory:  
   * `Dockerfile`  
   * `docker-compose.yaml`  
   * `syslog-ng.conf` (configuration for `syslog-ng`)  
   * Optional: Add additional `.conf` files in the `conf/` directory for more log sources if needed.

### **Steps to Run**

Build and start the Docker container:  

1.  `git clone https://github.com/scalyr/samples`
2.  `cd code/syslog-ng`
3.  `sudo docker-compose up --build -d`

1. This will:  
   * Build the syslog-ng Docker image based on the `Dockerfile`.  
   * Mount the `conf/` directory to `/etc/syslog-ng/conf.d/` in the container.  
   * Expose the required ports (514 for `fortigate` logs and 515 for other sources, such as Palo Alto).  
2. The syslog-ng server will now be running and will forward logs to SentinelOne.

---

## 

## **Configuring `syslog-ng.conf`**

The `syslog-ng.conf` file defines how `syslog-ng` works, including sources (log sources like UDP or TCP), and destinations (such as an HTTP endpoint like SentinelOne).

### **Adding HTTP Sources**

You can create as many HTTP destinations as needed in `syslog-ng.conf` to send logs to different endpoints. Here's an example configuration.

#### **Example `syslog-ng.conf`**

`@version: 3.36`  
`@include "scl.conf"`

`options {`  
    `# Customize options here`  
`};`

`source s_network_fortigate {`  
    `udp(port(514));`  
`};`

`source s_network_palo {`  
    `udp(port(515));`  
`};`

`destination d_sentinelone_fortigate {`  
    `http(`  
        `url("https://ingest.us1.sentinelone.net/services/collector/raw?sourcetype=marketplace-fortinetfortigate-latest")`  
        `headers("Authorization: Bearer YOUR_SENTINELONE_API_TOKEN", "Content-Type: text/plain")`  
        `body("${MESSAGE}")`  
        `method("POST")`  
        `content-compression("gzip")`  
        `batch-lines(5000)`  
        `batch-bytes(6000)`  
        `batch-timeout(10000)`  
        `retries(1)`  
        `workers(4)`  
    `);`  
`};`

`destination d_sentinelone_palo {`  
    `http(`  
        `url("https://ingest.us1.sentinelone.net/services/collector/raw?sourcetype=marketplace-paloaltofirewall-latest")`  
        `headers("Authorization: Bearer YOUR_SENTINELONE_API_TOKEN", "Content-Type: text/plain")`  
        `body("${MESSAGE}")`  
        `method("POST")`  
        `content-compression("gzip")`  
        `batch-lines(5000)`  
        `batch-bytes(6000)`  
        `batch-timeout(10000)`  
        `retries(1)`  
        `workers(4)`  
    `);`  
`};`

`log {`  
    `source(s_network_fortigate);`  
    `destination(d_sentinelone_fortigate);`  
`};`

`log {`  
    `source(s_network_palo);`  
    `destination(d_sentinelone_palo);`  
`};`

### **Key Points to Note**

1. **HTTP Headers**:  
   The headers use an API token for authentication with the SentinelOne API. Replace `YOUR_SENTINELONE_API_TOKEN` with your actual token.  
   * `Authorization`: This is your SentinelOne API token.  
   * `Content-Type`: Always set to `text/plain` for log data.

**HEC URL**:  
The URL follows this pattern:  
plaintext  
Copy code  
`https://ingest.us1.sentinelone.net/services/collector/raw?sourcetype=YOUR_SOURCETYPE`

2. The `sourcetype` in the URL is how SentinelOne identifies the log source. For example, `marketplace-fortinetfortigate-latest` for FortiGate logs or `marketplace-paloaltofirewall-latest` for Palo Alto logs.  
3. **Body**:  
   The `${MESSAGE}` variable captures the log message and sends it as the HTTP body. You can modify this based on how syslog-ng handles log messages.  
4. **Source Type**:  
   * The **sourcetype** in the URL corresponds to the parser on SentinelOne's side.  
   * The **host** maps to the `serverHost` field in SentinelOne.  
   * The **source** maps to the `logfile` field in SentinelOne, which shows the specific file or log source that sent the data.

### **Customizing Syslog Sources**

* Add new sources as needed in the `syslog-ng.conf` file, and configure them to listen on different ports.  
* Create corresponding `http` destinations to forward logs to SentinelOne's HEC.

---

### **Additional Notes**

* **Batching**: The configuration supports batching of log messages (5,000 lines or 6,000KB) before sending the data to SentinelOne.  
* **Retries**: The configuration attempts to resend data once if it fails (`retries(1)`).  
* **Compression**: Data is compressed using GZIP before sending (`content-compression("gzip")`).  
* **Workers**: The number of workers processing log data is set to 4 (`workers(4)`), which you can adjust based on performance requirements.

---


### **Installing Docker**
**RHEL 9**

```
sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine

sudo yum install -y yum-utils

sudo yum-config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo

sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


sudo systemctl start docker 
sudo systemctl enable docker
sudo mkdir ~/syslog-s1
sudo docker --version
```
**Ubuntu 22.04**
```
sudo apt update

sudo apt remove -y docker docker-engine docker.io containerd runc

sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl start docker 
sudo systemctl enable docker
sudo mkdir ~/syslog-s1
sudo docker --version
```

**Debian 11**
```
sudo apt update

sudo apt remove -y docker docker-engine docker.io containerd runc

sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list

sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl start docker 
sudo systemctl enable docker
sudo mkdir ~/syslog-s1
sudo docker --version
```

**CentOS 8**
```
sudo yum remove docker \
                docker-common \
                docker-snapshot \
                docker-engine

sudo yum install -y yum-utils

sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl start docker 
sudo systemctl enable docker
sudo mkdir ~/syslog-s1
sudo docker --version
```

**macOS**
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install --cask docker
open /Applications/Docker.app
docker --version
```

**Installing Docker on Windows**
Docker Desktop is the easiest way to get started with Docker on Windows. It requires Windows 10 or later (Pro, Enterprise, or Education versions).

1. **Download Docker Desktop**:
   - Go to the [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop) page.
   - Click on the **Get Docker** button to download the installer.

2. **Install Docker Desktop**:
   - Run the downloaded installer and follow the installation wizard.
   - During installation, make sure to enable the **WSL 2 feature** and install the WSL 2 kernel update (if prompted).
   - If you do not have WSL 2 installed, follow the [WSL installation instructions](https://docs.microsoft.com/en-us/windows/wsl/install).

3. **Start Docker Desktop**:
   - After installation, start Docker Desktop from the Start menu.
   - Wait for Docker to initialize (this may take a few minutes).

4. **Verify Installation**:
   Open a Command Prompt or PowerShell window and run:
   ```bash
   docker --version


## **Conclusion**

By following these steps, you can easily set up syslog-ng to forward FortiGate and Palo Alto logs (or any other sources) to SentinelOne. You can further customize the configuration based on your log source requirements and SentinelOne's data ingestion rules.

Let me know if you have any questions or need further assistance\!

