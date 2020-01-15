# Module 설명 - Containers / Kubernetes
## Containers, Kubernetes (and Engine)
Compute Engine은 IaaS다. VM을 제공하고 persistent storage / networking을 지원하는 식이었음. App Engine은 GCP의 PaaS, Platform as a Service.

Kubernetes Engine은 불필요한 infra chore를 줄여준다는 점에서는 IaaS특징을 가지고 있고, Developers에게 필요한 일들을 처리하도록 build되어 있다는 점에서 PaaS 특성도 있다.

IaaS let you share compute resources by Virtualizing HW. 각각 instance마다 OS가 다르고, 이 위에 application을 올릴 거다. 이 경우 VM의 computing cost는 VM의 os 등 사용자가 원하는 대로 세팅한 환경 + Application 구동 비용이 된다.
만약 하나의 App이 성공해서, 똑같은 걸 하나 더 만들어야 한다고 생각해보자. 동일한 OS를 다시 할당받고 동일한 App을 올려서 구동하면, resource consumption이 생각보다 빠르게 증가할 수 있다.

PaaS 환경 (App Engine)을 예로 들면,  Blank VM을 제공받는 대신 Application 구동에 필요한 service를 제공받고 시작한다. 필요한 로직을 만들고, dependency를 개발환경에서 불러오는 식으로 작업을 할 수 있다. 그런데 App의 Demand가 커지면, platform scales your application seamlessly and independently by workload and infra. 이 scale 증가속도가 빨라지면, give up control of underlying server architecture.

그래서 등장한 게 Container. 
Independent scalability workloads like you get in PaaS environment + abstraction layer of OS / HW, like you get in IaaS environment를 제공하기 위해.

하나의 OS에서 entirely new instance를 굴리는 대신, Container process를 지원하는 OS로 대신하는 것. 간단히 말하자면 Virtuallize OS rather than HW. PaaS 같은 environment scale을 제공하지만 flexiblity는 IaaS가 제공하던 편의 수준을 누릴 수 있는 것.

OS나 HW를 일종의 블랙박스처럼 생각하고 작업할 수 있다는 뜻. 

Units of Codes running in Containers can communicate with each other over a network fabric. -> Can make applications Modular.
== Deploy easily, scale independently across a group of hosts. Host can scale up and down, start and stop Containers as demand for you application changes (even as hosts fail and are replaced).
-> 이걸 가능하게 해 주는 게 kubernetes. Many containers on many hosts의 orchestrate를 지원한다.

container로 가장 잘 알려진 건 Docker.

Flask로 웹 Application을 만들었다고 하자. 
1. 이걸 deploy하는 일반적인 방법은 requirements.txt에 python version, flask version, uwsgi version을 지정해줘야 했다. 
2. 대신, Dockerfile에서 ‘운영체제 설정 / 파이선 설치 / requirements 설치 / 실행’ 까지 작업하도록 파일을 생성한다
3. Docker build -t 형태로 container를 생성하고, docker run으로 해당 container를 실행한다.

이 다음 managing updates, app configuration, service discovery, monitoring은?? -> kubernetes Engine이 처리하는 내용들이다.

---
### Intro to Kubernetes and GKE

Kubernetes : Open Source orchestrator for containers so you can better manage and scale your applications.  It offers API that lets the authorized people control its operations through several utilities. (Ex - kubectl cmd)

기본적으로 kubernets는 let you deploy containers on a set of Nodes. Called “Cluster”.
Cluster -> a set of master components that control the system as a whole, and a set of Nodes that run containers. Node 자체는 그냥 computing instance라고 생각하면 된다. 
(하나의 instance 안에 여러 개의 containers가 존재할 수 있다)

Kubernetes에게 ‘set of applications & how they should interact’을 알려주면, ‘how to’는  알아서 한다. 그러면, 이 kubernetes Cluster는 어떻게 얻어야 하나?? -> Own HW나 VM을 제공하는 다른 환경에 Kubernetes를 설치해야 한다. 대신, 설치했으면 운영도 스스로 해야 한다.

이거 세팅하는 노력을 구글에서 대신하는 게 GKE, Google Kubernetes Engine이다. Kubernetes as a managed service in the cloud. GCP console이나 gcloud command in SDK로 생성 가능.

Ex)
GKE로 container cluster k1을 만들었다고 하자. 필요한 사전 설정을 끝내고 생성도 완료됐으면, GCP console에서 status를 확인할 수 있다. Kubernetes에서 container or a set of related containers를 deploy할 때, 내부적으로 정의된 abstraction called a ‘pod’에서 작동한다. 
Pod -> smallest deployable unit in Kubernetes. 간단히 생각하면, running process on your cluster로 봐도 된다.

일반적으로 1 pod = 1 container다. But if you have multiple containers with a hard dependency -> can package them into a single pod. It automatically share networking and disk storage volumes. 

각각의 pod는 unique IP address / set of ports for you container를 가지고 있다. Pod 내부에 있는 container끼리는 Localhost network interface로 통신한다. 

Kubernetes pod에 있는 container를 실행하는 명령어가 kubectl run cmd. It starts deployment with a container running a pod. 예컨대 실행해야 하는 container nginx open source Web Server라고 하자. Kubectl 명령어로 실행하면, it fetches an image of nginx of the version we request from a container registry.

Deployment represents a group of replicas of same pod. 설령 노드 중 하나가 죽더라도 기능하도록 하는 것. You can use a deployment to contain a component of your application or entire application. 예시로 돌아가면, nginx web server가 여기 해당한다. Running nginx pod를 확인하려면 kubectl get pods 명령어를 쓰면 된다.

Default: pods are only accessible inside your cluster. 하지만 nginx web server는 인터넷을 통해 외부인이 접속할 수 있도록 해야 함. Pods in your deployment publicly available, you can connect a load balancer to it by running the kubectl expose command.
-> it creates a service with a fixed IP address for your pods. (A Service is the fundamental way Kubernetes represents load-balancing.)
정확히는, Kubernetes Attach on external load balancer with a public IP address to your service, so that others outside the cluster can access to it.

GKE에서는 Network load balancer를 사용한다. Compute Engine makes available to VM에 사용하던 Managed Load balancing service 그거 맞다. GKE는 이걸 containers에서 사용할 수 있게 지원해주는 것.

따라서, 외부에서 IP 주소를 받아 들어오면 routes to the pod behind the service. 예시의 경우는 pod가 nginx 1개뿐이다.  + “Service”의 의미란, groups a set of pods together and provides a stable endpoint for them을 말한다. 예시로 다시 돌아가면, IP address가 Network Load Balancer를 거쳐 들어오도록 하는 걸 Service라고 한다.

왜 굳이 Service라는 개념을 사용해야 하나? 여러 pods를 그룹핑해서 운영하는 대신, 그냥 pods’ IP주소에 직접 접근하면 안 되나?
-> deployment 과정에서 pods는 만들어지기도 하고 없어지기도 한다. 즉 pods가 받는 IP주소 자체는 not stable. 즉 Service는 stable endpoint를 위한 기능인 셈이다.

Kubernetes에서 제공하는 다른 종류의 services도 있다. Suitable for internal application backends. Kubectl get services cmd는 사용할 수 있는 service IP주소를 반환한다. 외부 사용자는, 단지 이 service IP주소만 알고 있으면 container를 사용할 수 있는 것. 

To scale a deployment (= need more power 상황), kubectl scale cmd를 쓰면 된다. 예시로 돌아가면, 아까 1개였던 nginx server pod을 3개까지 늘리는 경우가 이에 해당한다. 대신, 이 3개의 pods에 접근하는 건 Service IP주소고, 이건 변하지 않는다. 

여러 useful parameter를 활용하면 auto scale이 가능함.

Kubernetes의 진짜 강점은 Declarative way. command를 입력하는 대신 configuration file 안에 what you want your desired state to look like, and kubernetes figures out how to do it. 이 configuration 파일이 곧 management tool로 작동한다. Config 파일만 바꾸고 present the changed version to Kubernetes = Edit.

나중에 Version Control System처럼 사용하기도 용이하다. Kubectl apply -f  파일이름.yaml 형태로 사용.

일반적으로, 내부적으로 update를 진행할 때, endpoint 너머에 있는 clientr가 불편함을 느껴서는 안 된다. 여러 프로그램이 얽혀 있다면, 손대기도 어렵고. Deployment의 중요한 속성 중 하나가 update strategy다. 
Ex) rolling update = kubernetes가 새로운 version의 pod을 하나씩 만들어낸다. 새 버전의 pod가 사용 가능해질 때까지 기다리는 것.

Kubernetes Pod : a group of containers. Containers in a pod are deployed together.
Kubernetes cluster : a group of machines where kubernetes can schedule containers in pods. (안에 services도 있고, deploy 담당하는 master도 있고, 여러 개의 node 안에 pods가 들어 있다.)
Kubernetes Engine workloads -> runs in clusters built from Compute  Engine VM.

---
### intro to Hybrid and Multi-Cloud computing (Anthos)

On-premise distributed system architecture부터 확인해보자. Cloud computing이 자리잡기 전에 기업이 사용하던 방식.

일반적으로 기업 레벨의 소프트웨어들은 분산처리가 기본이다. 따라서 최소 두 개 이상의 서버가 필요함. container의 등장으로, workload를 microservice 단위로 쪼개서 maintainability / expandability를 확보할 수 있었다.

예전에는 모든 분산처리 시스템 + 하드웨어 장치를 모든 기업이 보유하고 있었다. (Housed) 회사가 보유한 수준의 computing resource를 넘어서게 되면, procure more powerful servers. 새로 산 서버에 ‘필요한 모든 network changes / expansions’ 를 해놓아야 하고, configuration settings / load applications and dependencies / resource bottleneck도 처리해야 한다. 이러다보니 보통 on-premise upgrade에는 몇 달 ~ 몇 년까지도 소요되는 게 일반적이었음. 이런 서버의 수명이 3~4년인 걸 생각하면, 비용도 비싼 편.

그래서, 회사 입장에서 당장 computing power가 필요하다면? Relocate some workloads away form on-premises to the Cloud하려는데, unwilling or unable to move the enterprise application from on-premise to Cloud?
-> Modern Hybrid / Multi-cloud architecture can help.

간단히 말해, 몇몇 기능은 on-premise에서 작동하도록 유지한 채 몇몇 기능을 클라우드에 올리는 것. 클라우드의 서버는 사내 서버와 호환될 수 있는 형태로 구성한다. 클라우드로 올리는 pace나 workloads는 사측에서 필요한 대로 정할 수 있는 형태로 운영된다.

Anthos : 구글이 제시하는 modern hybrid / multi-cloud distributed systems and service management. 
- Kubernetes와 Google Kubernetes Engine on-prem 을 사용함. (on-premises / Cloud environments stay in sync)
- It provides rich set of tools for monitoring / maintaining the consistency of your applications across all networks (on-premises or clouds)

예시 설명하는데 뭔소린지 모르겠음
??????

---

