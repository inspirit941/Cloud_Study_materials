# Module 설명 - Compute Engine

## Module instruction
Compute Engine : VM을 Google infra에서 실행 가능하도록 하는 것. Google Virtual Networking 관점에서 Compute Engine을 다룰 예정.

cf. Full fledged : 완벽한, 심도깊은
Compute Engine의 장점이라면, 각각의 VM이 Full fledged OS, power and Generality를 제공한다는 점. 실제 서버 설정하듯이 CPU, 메모리, amounts and power 등을 설정할 수 있음. Network Worldwide Connectivity도 제공한다.

## Virtual Private Cloud (VPC) Network
GCP를 시작하는 대표적인 방법이 프로젝트 안에 자신만의 VPC를 만드는 것.
VPC는 GCP 자원이 인터넷 / 서로 다른 자원끼리 연결해 주는 핵심.  Segment your network, use firewall rules to restrict access to instance, create static routes to forward traffic to specific destinations.

VPC 네트워크는 Global scope를 가지고 있다.  (subnet은 regional Scope를 갖는다)
They can have subnets in any GCP region + subnets can span the zones that make up a region. (즉, 특정 Region (us-east1) 에 VPC를 등록해두면, 해당 region의 zones (us-east1-b, c 등)으로도 span이 가능하다.) 이 특성 때문에, define own network layout with global scope가 가능함.

또는, resources in different zones on the same subnet가 가능함. VPC에  subnet이 하나 등록되어 있으면, 해당 subnet이 등록된 region 안에서는 여러 zone에 걸쳐 resource를 받을 수 있다.

Subnet 사이즈는 동적으로 변화시킬 수 있다. By range of IP address allocated to it. 단, this doesn’t affect already configured VMs.

강의 예시
- VPC에서 one subnet is defined in GCP us-east1 region.
- It has 2 Compute Engine VMs attached to it. (Resource가 두 개) 얘네는 각각 different zone이다. (Us-east1-b, us-east1-c)  다른 Zone이어도, Same Subnet에 포함되어 있음
- 이 방식으로, Simple layout이면서도 resilient (탄력적인) solution을 구축할 수 있음

---
## Compute Engine
Create, run VM on Google infra.
- no upfront investment (초기투자 없음)
- fast, consistent performance 제공하는 CPU 원하는 만큼 만들 수 있다.

GCP console이나 Gcloud CLI로 생성 가능. 리눅스, 윈도우 서버 image, 또는 customized 형태나 physical Server에서 돌리던 image를 적용하는 것도 가능하다.

1. Pick Machine Type : how much memory, virtual CPUs.
만약 원하는 predefined setting이 없으면, custom setting도 가능. GPU도 가능.
2. Storage 선택. Standard or SSD.  
High performance with scratch space가 필요하면 local SSD. 대신 be sure to store data of permanent value somewhere else. (VM terminated되면 저장된 데이터도 다 날아가기 때문)
그래서 있는 게 Persistent disk. 이게 디폴트 설정이기도 하다.
3. Boot image. 리눅스 / 윈도우 / import own image
4. image에 certain configuration을 필요로 하는 경우도 많다. (Install SW package in first booting). 이 경우 define startup script도 지원한다.
5. 일단 한 번 실행되면, 이 디스크의 durable snapshot을 얻을 수 있다. 백업용으로 쓰던, migration으로 쓰던 상관없다.

그냥 서버 돌려놓는 용도로 필요한 경우 (사람이 들여다보는 일이 많이 필요치 않은 경우) -> preemptive VM 사용할 수 있다. 상술한 VM과 전부 동일하지만, compute engine permission to terminate if it’s resources are needed elsewhere. 
Saving Money로 유용함. 대신 여기서 돌려놓는 job은 stopped and restarted 가능하도록 설정해둬야 함.

GCP에서 지원할 수 있는 최대 CPU개수나 Memory가 있지만, 소비자는 일반적으로 scale up보다는 scale out을 더 선호한다. (처음부터 큰 서버 받고 시작하는 게 아니라, 필요한 경우 추가로 더 받아 사용한다는 의미로 보임)
* Load Metrics 정도에 따라 auto scaling 가능. (Add or remove VMs from applications.)
* balancing the incoming traffic across the VMs. VPC는 Load balancing 방법을 여러 가지 제공한다. 다음에 다룰 예정

---
## Important VPC capabilities

VPC의 routing tables -> forward traffic from one instance to another within same network, across sub-networks, btwn GCP zones without requiring external IP address.

= Built in.

Firewall instance -> VPC에서 global distributed firewall 제공. incoming / outgoing traffic의 Instance access 제어가 가능함.

How to define? -> Metadata tags on Compute Engine instance. Ex) web 태그 = port 80과 443에서 오는 요청을 web이라는 태그를 가진 VM에서 받도록 설정하는 식.

기본적으로 VPC는 GCP project에 포함된 하나의 구성원 개념이다. 만약 여러 개의 프로젝트가 있고, 각각의 VPC끼리 통신하거나 작업할 일이 있다면?
* VPC Peering -> simply peering relationship btwn 2 VPC (exchange traffic)
* Shared VPC -> IAM의 who controls and what in one project 기능을 can interact with a VPC in another.

앞서 auto-scale 기능을 설명했었다. Changing load에 맞춰 scale out할 수 있도록 하는 기능. 그러면, VM 개수가 유동적일 때 Customer는 Application에 어떻게 접근하는가?? -> Cloud Load Balancing으로 해결.

Cloud Load balancing = Fully distributed, SW-defined managed Service for all your traffic. 이 balancer는 구글 측에서 관리하고 작동하기 때문에, 사용자가 신경쓸 필요 없다. 그냥 traffic 들어오는 입구에 Cloud Load Balancing 기능을 넣으면 됨. http / https / other TCP & SSL / UDP 등 전부.
-> single anycast IP frontends all your backend instances in regions around the world.

(User get a single, global anycast IP address. -> Traffic goes over Google backbone from the closest point-of-presence to the user -> backends are selected based on load -> only healthy backends receive traffic. No pre-warning is required.  = 만약 어느 시점에 과부하가 걸릴 것 같은 경우라 해도, 구글에 미리 알려줄 필요 없다)
Cross region load balancing도 지원한다. (미국 사용자, 독일 사용자, 일본 사용자... 각각 다른 region의 resource 할당한다는 의미로 보임.)

1. Cross regional load balancing for Web Application = HTTPS load balancing 사용 추천 (7 layer = high level. Url 레벨에서 로드 밸런스 처리한다고 보면 됨. url에 따라서 다른 백엔드로 보낸다.)
2. SSL traffic (not http) = global SSL proxy load balancer 사용 (layer 4 = port level)
3. Other TCP (not use SSL) = global TCP proxy load balancer.
2와 3은 특정 port number에서만 작동하며, TCP에만 적용된다.
4. UDP / any other port에서 오는 요청 = load balance across GCP region with regional load balancer. 
5. 1~4까지는 인터넷에서 구글 network로 들어오는 트래픽을 대상으로 한 것들임. 만약 inside traffic을 load-balancing하고 싶은 경우? Internal load balancer 사용. GCP internal IP주소를 받아서 Compute Engine VMs 간 load balancing을 지원함.



구글의 Cloud DNS 서비스

Cloud CDN (content delivery Network) -> google globally distributed edge caches to cache content close to your users. 
Lower network latency + save money 가능.
HTTPS load balancing을 사용할 때 체크박스 형태로 선택 가능. 만약 이미 사용중인 CDN이 있고 그 CDN이 구글과 interconnect partner라면 그대로 사용 가능

Interconnect options.
GCP 사용자들 중 Own network (on-premises = 사내 or 직접설치 network / networks in other clouds.) 에서 google VPC로 연결하려는 경우가 있다.

1. VPN을 사용하는 경우… GCP feature 중 하나인 Cloud Router 사용 가능. 사용자의 network와 google VPC 간 route information을 VPN의 Border Gateway Protocol로 교환하는 것. 예컨대 VPC에서 새 subnet을 만들면, on-premises network에서도 자동으로 새 subnet의 라우트를 받아오는 것


2. Internet 사용을 원치 않는 경우 = Direct Peering. 구글과 직접 Peering하는 것. Peering = putting a router in the same public data center as a google point of presence and exchange traffic. 구글 통해서 통신한다고 보면 될 거 같음. 

3. Customers who are not already in a point of presence -> can contract with a partner in the Carrier peering program to get connected. 단점: it isn’t covered by a google service level agreement. 

4. Wants highest uptimes for the interconnection with Google = Dedicated interconnect 사용해야 함. 구글과 direct private connections을 맺는 것. If these connections have topologies that meets google’s specification, it can be covered by up to 99.99% SLA.


