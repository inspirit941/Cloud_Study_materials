# Deployment Manager & Managed Service
Automatically generate infrasturture by Calling Cloud API. 강력하기는 한데 몇 가지 걸리는 점이 있긴 함
* Maintainability… depends directly on the quality of SW.  여러 코드에서 API를 실행하고 있다면, 어느 코드에서 어떤 작업이 일어나는지 확인하기가 쉽지 않다. 관리하기도 까다로움.

그래서 Deployment manager 가 필요함. Highly structured templates and configuration files to document the infrastructure in an easily readable / understandable format.

API call을 conceal하기 때문에, 코드보다는 definition of infrastructure에 집중할 수 있다.

---
## Deployment Manager

지금까지 사용한 tools = GCP console, Cloud SDK, Cloud shell.

<img width="927" alt="스크린샷 2020-02-01 오후 2 31 57" src="https://user-images.githubusercontent.com/26548454/73591243-8972c100-452f-11ea-86bd-80ccf1f844c7.png">


얘는 일종의 infrastructure automation tool. 필요한 resource나 application을 declarative format으로 선언한다.

* repeatable
* declarative language
* can specify a set of resources which compose the application or service = allow you to focus on application.
* Deploy resource in parallel.
* templates, for other configurations.

얘 자체로 underlying API를 사용하기 때문에, 지금까지 만들었던 모든 것들을 그대로 만들어낼 수 있음. 인스턴스 / VPC network / firewall rules … 등등

Auto mode network template -> jinja2나 python원어 지원.

<img width="922" alt="스크린샷 2020-02-01 오후 2 37 37" src="https://user-images.githubusercontent.com/26548454/73591244-8972c100-452f-11ea-9f53-610621376fcc.png">


1. Resource에는 name, type, property 세 개의 인자가 필요함.
Type : Define API for a VPC network (compute.v1.network 라는 VPC 네트워크 가정)

기본적으로, auto mode network는 각 region당 하나의 subnetwork를 생성한다. Property 항목의 설정에 True값.

2. Firewall rule 생성
Property 부분에는 이 firewall rule을 적용할 source IP range, allowed protocol & ports 입력. sourceRange에 들어갈 ip range 자체를 template화하면 flexibility를 극대화할 수 있다.

3. config.yaml
이렇게 만든 jinja나 python 파일을 config.yaml 파일에서 import. Resource에는 이 설정으로 생성할 network와 firewall  rule을 각각 입력해준다. firewall의 경우 Reference network /ipprotocol / port까지 입력해줘야 한다.

여기서 ref.mynetwork.selfLink 형태로 firewall rule을 설정할 network을 지정했는데, selfLink의 의미는 ‘이 Network가 firewall rule보다 먼저 생성된다’는 뜻이다. 
이게 중요한 이유는, Deployment manager는 모든 Resouces를 병렬적으로 생성하기 때문. 레퍼런스를 이렇게 설정하지 않으면, firewall rule을 생성할 때 ‘적용할 network가 존재하지 않는다’는 에러메세지를 보게 됨.

이외에도 여러 개 tool을 쓸 수 있다. Terraform, puppet 등. infrastructure를 SW처럼 다룰 수 있게 해주는 Tool이라 보면 된다.

---
### Lab

Deployment Manager와 Terraform 사용법 둘 다 알려줌

#### Deployment Manager

1. Cloud shell 열고, config.yaml 파일 생성

```yaml
imports:
- path: instance-template.jinja
resources:
# Create the auto-mode network
- name: mynetwork
  type: compute.v1.network
  properties:
    #RESOURCE properties go here
    autoCreateSubnetworks: true
# Create the mynet-us-vm instance
- name: mynet-us-vm
  type: instance-template.jinja
  properties:
    zone: us-central1-a
    machineType: n1-standard-1
    network: $(ref.mynetwork.selfLink)
    subnetwork: regions/us-central1/subnetworks/mynetwork
# Create the mynet-eu-vm instance
- name: mynet-eu-vm
  type: instance-template.jinja
  properties:
    zone: europe-west1-d
    machineType: n1-standard-1
    network: $(ref.mynetwork.selfLink)  
    subnetwork: regions/europe-west1/subnetworks/mynetwork
    
# Create the firewall rule
- name: mynetwork-allow-http-ssh-rdp-icmp
  type: compute.v1.firewall
  properties:
    #RESOURCE properties go here
      network: $(ref.mynetwork.selfLink)
      sourceRanges: ["0.0.0.0/0"]
      allowed:
        - IPProtocol: TCP
          ports: [22, 80, 3389]
        - IPProtocol: ICMP
```

Instance template도 만들어준다.

```jinja
resources:
- name: {{ env["name"] }}
  type: compute.v1.instance  
  properties:
     machineType: zones/{{ properties["zone"] }}/machineTypes/{{ properties["machineType"] }}
     zone: {{ properties["zone"] }}
     networkInterfaces:
      - network: {{ properties["network"] }}
        subnetwork: {{ properties["subnetwork"] }}
        accessConfigs:
        - name: External NAT
          type: ONE_TO_ONE_NAT
     disks:
      - deviceName: {{ env["name"] }}
        type: PERSISTENT
        boot: true
        autoDelete: true
        initializeParams:
          sourceImage: https://www.googleapis.com/compute/v1/projects/debian-cloud/global/images/family/debian-9
```

sourceImage : OS version 설정.

이렇게 설정하고, config.yaml 파일이 있는 디렉토리에서 
`gcloud deployment-manager deployments create dminfra --config=config.yaml --preview`

입력하면 config대로 실행했을 때 어떤 결과가 나오는지 preview로 알려준다.

`gcloud deployment-manager deployments update dminfra` -> 실행. dminfra는 config.yaml과 jinja 파일이 있는 경로 이름이다.
`gcloud deployment-manager deployments create dminfra --config=config.yaml` 처럼 써도 됨.

#### Terraform

Cloud shell로 디렉토리 하나 만들고, 그 안에 provider.tf 파일 생성한 뒤 첫 줄에 `provider “google” {}` 입력.
cmd창에서 `terraform init ` 로 terraform initialize.

1. My network.tf를 만들고 아래 내용을 입력한다.

```tf
# Create the mynetwork network
resource "google_compute_network" "mynetwork" {
name = "mynetwork"
#RESOURCE properties go here
auto_create_subnetworks = "true"
}

# Add a firewall rule to allow HTTP, SSH, RDP and ICMP traffic on mynetwork
resource "google_compute_firewall" "mynetwork-allow-http-ssh-rdp-icmp" {
name = "mynetwork-allow-http-ssh-rdp-icmp"
#RESOURCE properties go here
network = google_compute_network.mynetwork.self_link
allow {
    protocol = "tcp"
    ports    = ["22", "80", "3389"]
    }
allow {
    protocol = "icmp"
    }
}

```

네트워크 설정 + firewall 설정.

2. 디렉토리 안에 하위폴더 instance를 만들고, main.tf 파일을 생성한 뒤 아래 내용을 입력한다.

```tf
variable "instance_name" {}
variable "instance_zone" {}
variable "instance_type" {
  default = "n1-standard-1"
  }
variable "instance_subnetwork" {}

resource "google_compute_instance" "vm_instance" {
  name         = "${var.instance_name}"
  zone         = "${var.instance_zone}"
  machine_type = "${var.instance_type}"
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
      }
  }
  network_interface {
    subnetwork = "${var.instance_subnetwork}"
    access_config {
      # Allocate a one-to-one NAT IP to the instance
    }
  }
}

```

3. Instance 설정이 완료됐으면, mynetwork.tf에 생성할 instance 설정을 추가해준다

```tf
# Create the mynet-us-vm instance
module "mynet-us-vm" {
  source           = "./instance"
  instance_name    = "mynet-us-vm"
  instance_zone    = "us-central1-a"
  instance_subnetwork = google_compute_network.mynetwork.self_link
}

# Create the mynet-eu-vm" instance
module "mynet-eu-vm" {
  source           = "./instance"
  instance_name    = "mynet-eu-vm"
  instance_zone    = "europe-west1-d"
  instance_subnetwork = google_compute_network.mynetwork.self_link
}
```

이제 cmd창에서


```
terraform fmt
terraform init
```
Terraform fmt -> To rewrite the Terraform configuration files to a canonical format and style, run the following command

다시 Init 실행하면, 인스턴스 두 개가 추가된다.

Terraform의 execution plan을 확인하려면 
`terraform plan`
실행하려면 `terraform apply` 입력하면 된다.


---
## GCP MarketPlace

<img width="921" alt="스크린샷 2020-02-01 오후 7 15 52" src="https://user-images.githubusercontent.com/26548454/73591245-8a0b5780-452f-11ea-8fe3-ad6a12fb2263.png">

it lets you quickly deploy functional SW packages that run on GCP. 3rd party vendor가 제공하는 SW도 어느 정도 지원해준다는 의미인듯. Solutions are built together with all of your projects GCP services. 만약 3rd party 라이센스를 보유하고 있으면, 구글에 Deploy하고, 필요할 때만 scale later하면서 사용할 수 있다는 것.

단, 이 경우 구글이 fix critical issues / vulnerability 체크는 해주지만 deploy한 이후에는 책임지지 않는다.

예시의 경우 Lamp Stack 검색 -> configuration 세팅 -> deploy. deploy할 때 구글 서비스들 (stackdriver 같은) 사용여부 선택이 가능.

---
## Managed Service

Automate the creation of infrastructure -> 굳이 infrastructure를 만드는 대신, 아예 managed Service를 이용하는 방법도 있다. 이 서비스들은 보통 Continuum btwn PaaS, SaaS 형태. 구글 측에 운영이나 유지보수 관련 overhead를 맡기는 방식이라고 보면 된다.

얘네는 대부분 Data Analysis를 위한 것들. 따라서 굳이 Lab을 제공하진 않고, 특징이 뭔지만 간략히 소개할 예정


### BigQuery


<img width="929" alt="스크린샷 2020-02-01 오후 7 30 57" src="https://user-images.githubusercontent.com/26548454/73591246-8a0b5780-452f-11ea-9719-d2558a9a3edb.png">


Serverless, cost effective Cloud Data Warehouse. 페타바이트 단위 지원, Fast Query연산 지원. Free usage Tier 존재.

Query 연산에 상당한 강점이 있음. Serial Execution이면 오래 걸리는 작업이지만 BigQuery는 빠르게 작업할 수 있다고.

---

### Cloud DataFlow


<img width="810" alt="스크린샷 2020-02-01 오후 7 49 29" src="https://user-images.githubusercontent.com/26548454/73591261-b58e4200-452f-11ea-8020-91fd2cb1ddb3.png">

For transforming & enriching data in stream / batch mode. Fast & simplified development via expressive SQL, Java, Python API in the Apache Beam SDK.

Stackdriver 같은 애들과도 호환이 잘 된다.

<img width="927" alt="스크린샷 2020-02-01 오후 7 53 09" src="https://user-images.githubusercontent.com/26548454/73591262-b58e4200-452f-11ea-8e2f-a6f5f794dbd6.png">

상술했듯 stream / batch 데이터 둘 다 처리할 수 있음. 여러 다른 데이터 소스에서부터 데이터를 받아와서 transform -> 데이터 분석을 위한 BigQuery나 AI platform, BigTable 등에 적용할 수 있다.

---
### Cloud Dataprep

<img width="924" alt="스크린샷 2020-02-01 오후 8 00 12" src="https://user-images.githubusercontent.com/26548454/73591263-b58e4200-452f-11ea-90b6-5ce7c30338da.png">

데이터 visual exploring, cleaning, preparing structured / unstructured data for analysis reporting & ML.

next Ideal data transformation 제안을 진행하며, 코드 작업할 필요 없다는 장점. 데이터 프로파일링에 들어가는 시간 절약 가능.

Partner Service operated by Trifacta. 간단히 말해 data preparation 쪽 특화된 서비스. Pub/sub이나 storage 등에서 받은 raw 데이터를 Dataprep에 넣어 전처리하고, 그 후 DataFlow를 활용해 필요한 형태로 정제된 데이터를 bigTable / BigQuery에 넣는 식이다.

---
### Cloud Dataproc

<img width="919" alt="스크린샷 2020-02-01 오후 8 04 25" src="https://user-images.githubusercontent.com/26548454/73591264-b58e4200-452f-11ea-922d-cfecb0d9df29.png">

Apache Hadoop이나 Spark Cluster를 쉽게 사용할 수 있도록 해주는 서비스라고 보면 됨. 이 서비스들 자체가 on-prem일 경우 실행 활성화까지 5분 ~ 30분은 걸리는 작업속도를 늘려준다. Start, scale, shut down이 매우 쉬움. 다른 GCP 서비스와의 연동도 잘 되어 있는 편이며, data platform으로는 Hadoop과 Spark보다 통합된 편의 제공함.

이미 사용하는 Tool - 하둡, 스파크, 하이브 등 - 이 있으면, 별다른 redevelopment 없이 그대로 옮겨서 사용할 수 있다.


<img width="923" alt="스크린샷 2020-02-01 오후 8 07 21" src="https://user-images.githubusercontent.com/26548454/73591265-b626d880-452f-11ea-8a16-12893d81420d.png">

둘 다 데이터 처리 프로세싱이며, Batch / stream 지원함.
-> 하둡이나 스파크 같은 시스템을 이미 쓰고 있다면 dataproc이 맞는 선택지.
-> 아니라면, Hands-on DevOps 개념으로 사용할 건지 hands-off Serverless 개념으로 사용할 건지. DevOps라면 Dataproc, Serverless에 초점을 맞췄다면 DataFlow 쓰면 된다.


---

Serverless가 진짜로 서버나 Compute Engine이 없다는 소리는 아니다. 사용자 입장에서 서버를 고려할 필요가 없도록 Obfuscated 해뒀다는 뜻. Dataproc은 master / worker instance를 view and manage하는 시스템이므로 Serverless도 아님.