# GCP + VPC
GCP 개념설명

GCP를 포괄하는 거대한 Ecosystem 
-> consists of OpenSource SW, providers, partners, developers, 3rd party SW, other Cloud providers.

구글 클라우드만 놓고 보면 G Suite, Gmail, GA, Search 등 여러 개의 서비스의 집합체. GCP도 이 중 하나로, Infrastructure / Platform / Software 를 제공한다는 특징이 있는 셈이다.

제공하는 서비스는 크게 IaaS / PaaS / SaaS (SW as a Service) 로 나뉘어진다.

Infrastructure : basic underlying framework of fundamental facilities. Application의 생성과 구동을 가능하게 하는 모든 것들.

- Compute Engine : VM을 클라우드 내에서 구동하고 on demand flexibility를 제공
- Google Kubernetes Engine : run Containers as applications on a Cloud Environment
- App Engine : PaaS Framework. Infra 걱정 없이 running code in the Cloud. 
- Cloud Function : Serverless Execution Environment of Function as a Service. 이벤트 발생 시마다 execute code. 

이 강의에서는 Compute Engine이 메인.

## Using GCP
GCP 사용법
- GCP console : Web User interface. GUI. 
Cloud Shell 형태로 cmd 제공. (Browser-based interactive shell environment)  -> temporary VM (5GB disk storage + cloud SDK preinstalled.) 

* SDK = gsutil이나 bq, gcloud 등의 명령어 조합
* Client Library = 다양한 언어로 최적화.
* Admin API = Resource Management 기능 제공

- Cloud Mobile App : manage GCP service from your Android, iOS device. (Ssh 로 인스턴스 실행하거나 로그 보는 게 가능함)

Cloud Shell 특징
* gcloud: for working with Google Compute Engine and many GCP services
* gsutil: for working with Cloud Storage
* kubectl: for working with Google Container Engine and Kubernetes
* bq: for working with BigQuery
* Language support for Java, Go, Python, Node.js, PHP, and Ruby
* Web preview functionality
* Built-in authorization for access to resources and instances

After 1 hour of inactivity, the Cloud Shell instance is recycled. Only the /home directory persists. Any changes made to the system configuration, including environment variables, are lost between sessions.

---
### Lab Review : Console & Cloud Shell

Console can do things Shell Can’t and vice-versa.

Console = 일반적으로 repetitive or more leveraged activities 지원.
Ex) Console can keep track of the context of your configuration activities.

Shell = detailed & precise Control, script and automate activities.
cf. /.profile 파일에 source config 형태로 저장하면, 매번 실행될 때마다 환경변수가 지정된 변수로 세팅된다. Config 파일 안에 필요한 환경변수 정의를 지정해두면 됨.

---
### Lab Review : Infrastructure Preview

Marketplace에서 Jenkins certified by Bitnami로 Compute Engine 할당받기, Deployment Manager 활용하기, VM 접속해서 Jenkins 업데이트하기.

---
### Demo

Project = key organizer of infrastructure resources / relate these resources to billing accounts.

모든 형태의 resource는 project라는 단위 안에서만 consume. 즉 Project 단위로 사용 가능한 resource가 구분되는 것. 퀵랩에서의 실습환경으로는 프로젝트 생성이 restricted.

cf. 프로젝트를 생성할 때, 몇몇 서비스들은 처음에는 Not available할 수 있다.

console의 GUI에서는 프로젝트 생성 및 삭제가 그리 어렵지 않다. Cloud Shell의 경우 `gcloud config list` 로  현재 콘솔창에서 지정된 project의 설정을 확인 가능.

Shell 환경에서 프로젝트를 swapping하려면, 프로젝트 ID를 환경변수로 지정해두는 게 좋다. `export PROJECT_ID1="id"` 형태로 임시 환경변수 생성 후
 `gcloud config set proejct PROJECT_ID1`이라고 입력하면 됨. 즉, 반드시 환경변수 쓰지 않아도 set project “ID”입력하면 된다.

---
## Overview - VPC

VPC : google’s managed networking functionality for your Cloud platform resources.
-> 여기서 다시 네트워크를 fundamental components로 구분; projects, networks, subnetworks, IP address, routes, firewall rules, network price 등등 

Pops : Google Network가 나머지 internet과 연결된 지점. GCP can bring its traffic closer to his peers, bcz it operates an extensive global network of interconnection points.

---
## Virtual Private Cloud (VPC)

GCP에서는 provisioning GCP Resources, connect them to each other, and isolate them from each other in VPC. 또한 GCP 내부 or GCP - on-premise간  fine-grained network policy를 설정하는 것도 가능하다.

VPC 자체는 conprehensive set of Google Managed networking Object라고 볼 수 있다.
Projects : encompass every single service that you use, including networks.
Networks : 3 flavor ; default, auto mode, custom mode
Subnetworks : allows you to devide or segregate your environments.
Regions and Zones : represent google’s datacenter, they provide continuous data protection + high availability.
VPC provides IP address for internal / external use along with granular IP address range selection.

---
### Projects, Networks, Subnetworks

Project : objects, services with billing에 중요한 단위. It contains entire networks. 
디폴트로는 5개의 네트워크를 quota로 갖고 있고, 더 필요하면 설정에서 바꿀 수 있다. 

Network : 네트워크는 공유 or peered with 형태로 다른 프로젝트와 관계맺을 수 있다. 해당 네트워크들은 IP주소가 따로 있진 않고, 단지 construct of all of individual IP addresses and services within that network. GCP 네트워크는 global 기준이며, 가능한 모든 region에 접근할 수 있다. Subnetwork를 가지고 있으며, subnetwork는 해당 네트워크에서 resource를 segregate할 수 있는 단위.

3 VPC Network Type. 
기본적으로 Projects는 Default VPC with presets subnets + firewall rules 형태로 주어진다. Default Network == Auto Mode network.

정확히는, One subnet per region 형태로 subnet이 주어지며 non-overlapping sider blocks & firewall rules (allows ingress traffic from ICMP, RDP, SSH traffic from anywhere, default network 내의 모든 포트와 프로토콜 허용)
Subnet은 predefined IP range with /20 mask (fixed /20 subnetworks per region. Expandable up to /16). 전부 fit within 10.128.0.0/9 cider block.

Custom Mode network
subnet을 자동으로 세팅해주지 않는다. 사용자에게 subnet / IP range 권한이 전부 주어짐. 어느 region에 어느 subnet을 생성할지 스스로 정할 수 있고, RFC 1918 address space 내에서 IP Range도 정할 수 있다. 단, range can’t overlap btwn subnets of same networks.
Auto -> Custom으로 설정 변경도 가능하다. 사용자에게 모든 통제권을 줌, 단, one way로만.  Custom을 다시 Auto로 돌리는 건 불가능하다.


Project 안에 5개의 네트워크가 있고, 각 네트워크마다 multiple regions across the world. 즉 하나의 네트워크 내에서 us-east1 region으로 인스턴스를 만들고, 다시 Europe-east1으로 인스턴스를 만들어도 무방하다.

서로 region이 달라도 같은 Network에 속해 있는 VM끼리는 internal IP address로 통신이 가능하다. 물리적 거리와 상관없이, 구글 통신망 내의 configuration protocol로 들어올 경우 same rack로 보기 때문.

반면, 같은 region이라고 해도 VM끼리 소속된 Network가 다르면 통신은 External IP address를 토대로 통신해야 한다. 같은 region / 다른 VM인 경우, public internet을 사용하는 대신 Google edge router를 사용한다. 대신, different billing / security ramification (파문)이 있음.


앞서 말했듯 동일한 VPC 네트워크 안에 있는 VM instance는 global scale로 private 통신이 가능하기 때문에, Single VPN만으로도 on-premise 와 GCP 간 connection이 가능하다. 즉 on-premise -> Cloud VPC Network의 VPN gateway로 접근하면 gateway에서 필요한 VM으로 연결해주는 식.
-> 다른 region에 있어도 private 통신이 가능 + on-premise Network와는 Single VPN gateway로 통신 가능 = reduce cost + management complexity.


Subnetworks = works on regional Scale. 
region은 Zone의 상위 개념이기 때문에, subnetworks can cross zones. Region에 여러 개의 Zone이 있고, 각각의 Zone마다 VM이 하나씩 설치되어 있다고 할 때 Subnet은 Same Region에 있는 Zone끼리 연결할 수 있는 매개 역할을 한다.
간단히 말하면 Subnet은 IP address Range이고, 이 range 안에서 IP address로 여러 Zone의 VM에 접근하는 것.
단, first / second address (10.0.0.0 /10.0.0.1) 은 네트워크 / subnet gateway에 해당한다. 10.0.0.2, 10.0.0.3… 이런 식으로 각각 VM instance 지정되는 것. 그리고, 가장 마지막 range address는 broadcast address로 지정된다.
-> 4개의 IP주소는 GCP가 기본적으로 가져간다고 함.


서로 다른 Zone 내에 있는 VM이지만, 자기들끼리의 통신에는 same subnet IP address를 사용한다. This means that a single firewall rule can be applied to both VM’s even though they are in different Zones.

Expand Subnets without re-creating instances. 하나의 region에 여러 subnet이 필요하거나, 여러 region별로 VM을 만들어야 해서 Subnet이 필요한 경우. 즉 allowing for more instances in some subnets than others.
단, 유의점
1. Subnets cannot overlap with other subnets in these same VPC network in any region.
2. New subnet must be inside the RFC 1918 address space.
3. New network range must be larger than original one. = prefix length value must be a smaller number (?) 한 번i 확장하면 되돌릴 수 없다.
4. Auto mode subnets start with /20 IP range. /16 IP range까지 확장될 수는 있지만, 그 이상은 안 된다. 더 확장하려면 Auto -> custom으로 변경해야 함.
5. 너무 큰 subnet을 만드는 건 좋지 않다. Site arrange collisions (when using multiple network interfaces + VPC network peering ) or when configuring (a VPN or other connections) to an on-premises network. 꼭 필요할 때만 늘리는 걸 추천한다.

---
### Demo : Expand a Subnet

/29 mask로 custom subnet을 미리 생성해 둔 상태. 이 경우 8개의 address를 지원하지만, 이 중 4개는 GCP에서 기본적으로 가져가는 주소. 따라서 4개의 VM을 추가로 만들 수 있는 상황. 강의에서는 미리 4개의 instance를 만들어둔 채, 또 하나의 VM을 생성하려고 시도함. -> IP range exhausted로 생성에 실패한다.

Subnet detail 부분에서 IP address range 설정만 바꿔주면 해결된다. (강의에선 /23으로 변경) -> 약 500개의 instance를 더 만들 수 있다고 함.
이 기능의 핵심은, 이미 running중인 instance에는 어떤 형태로도 영향을 미치지 않는 상태에서 instance를 추가로 만들어낼 수 있다는 점이다.

---
### IP address

GCP에서 VM은 2개의 IP주소를 갖고 있다.
1. Internal IP address : assigned via DHCP internally. 모든 형태의 Machine (App Engine, Kubernetes)이 ‘실행될 때’ 부여받는 것. 
VM을 만들 때, symbolic name is registered with an internal DNS service that translates the name to the internal IP Address. DNS is scoped to the network -> can translate web URLs and VM names of hosts in the same network. But it cannot translate host names from VMs in a different network.

2. External IP address (Optional). Device나 Machine의 external facing이 필요한 경우 만들면 된다. It can be assigned from a pool, making it ephemeral. 또는 reserved external IP address = static하게 만들 수 있음.
VM does not know external IP ; it is mapped to. He internal IP

---
### Demo : Internal / External IP

VM을 생성할 때 “Management, Security, disks, networking, sole tenancy” 부분에서 network interface 부분을 확인한다. Internal IP / External IP에 각각 ephemeral / reserve static IP address가 있음. External의 특징은 “None” 설정이 가능하다는 것.

그리고, 단순히 IP range가 많다고 해서 해당 range만큼의 IP주소를 전부 쓸 수 있는 게 아니다. Quota가 정해져 있기도 하고, 해당 region이나 zone에서의 physical limit이 존재하기도 한다. 예시의 설정은 internal, external 둘 다 ephemeral로 설정.

-> instance를 끄고, 다시 실행할 때마다 external IP address가 바뀐다. Internal address의 경우 stayed for the time being.

---
### Mapping IP addresses

External IP address는 OS나 VM에서 알 수 없도록 되어 있다. VPC가 internal address <- -> Exterenal address를 연결하고 있기 때문. 실제로 VM 내에서 ipconfig를 입력하면 internal IP만 나온다.

- Internal IP Address
Each in instance has a host name that can be resolved to an internal IP address. 이 hostname == instance name이라고 보면 된다.
Internal Fully Qualified Domain name (FQDN) for an instance. FQDN 이름은[hostname].[zone].c.[project-id].internal 형태로 존재함.

기본적으로 delete + recreate instance는 internal IP address를 바꾼다. 따라서 이것만 보면 other compute engine resource와의 연결이 끊어지게 된다. 매번 connection을 하기 전에 new IP address를 알아야만 하는 것처럼 보임

DNS name은 internal IP address에 상관없이 points to specific instance. 모든 인스턴스는 metadata server that also acts as a DNS resolver for that instance. 이 서버가 local network resource 에서 오는 모든 형태의 DNS queries를 관리하고, routes all other queries to Google’s public DNS servers for public name resolution. 즉 인스턴스 내부의 DNS resolver가 internal IP address의 변동에서 오는 문제점을 해결한다.

VM은 external IP address 주소를 모른다. 대신, network stores a lookup table dat matches external IP with internal IP (relevant instances)

- External IP address
External IP주소가 있으면 allow connections from hosts outside the project. Public DNS records (pointing to instances) are not published automatically. But, Admins can publish these using DNS servers. Domain and Servers can be hosted on GCP using Cloud DNS.

-> Cloud DNS 자체를 좀 더 보자.
= scalable, reliable, managed authoritative domain name system (DNS service) 간단히 말해 Domain name (url주소같은) -> IP address로 바꿔주는 것.
DNS record creation / update를 쉽게 해 주는 툴. 

GCP networking의 또 다른 특징 : alias IP range.
= you assign a range of internal addresses as an alias to VM network interface. 여러 개의 services running on a VM + 각각의 service마다 IP주소를 다르게 부여하고 싶을 때 유용한 기능. 즉 containers / running application hosted in a VM 마다 IP주소를 부여하는 식.


---
### Routes and Firewall Rules

How GCP routes Traffic.

기본적으로 
- every network has routes that let instance in a network send traffic directly to each other, even across subnets. (네트워크 내부의 인스턴스끼리 통신할 수 있도록, 서로 다른 subnet끼리도 통신 가능한 라우팅 제공)
- default routes that directs packets to destinations that are outside the network. 

일반적으로는 이 정도 라우터로도 normal routing needs는 충분하지만, special routes that overwrites these routes도 가능하다. 

또한, routes를 통해 나가는 packet은 Firewall rules를 통과해야만 밖으로 나갈 수 있다. 기본 세팅은 네트워크 내부의 모든 인스턴스끼리 서로 통신 가능하도록 설정되어 있지만, Manually created networks는 이런 predefined setting이 없다. 따라서 이건 설정을 해줘야 하는 부분이다.

Routes match packets by destination IP address, and packets also match a firewall rule.  그래야 외부로 트래픽이 나갈 수 있다.
routes는 네트워크가 생성될 때 만들어지며, enabling traffic delivery from anywhere. Subnet이 생성될 때도 만들어지며, VM이 Same Network 내에서 communicate가 가능해지게 한다.

Each Route in the routes collections -> apply to one or more instances. Network과 instance tag matching이 되면 routes가 적용된다. 만약 network은 match되는데 specified instance tag가 없으면, 네트워크 내 모든 instace에 route가 적용된다.

Compute Engine은 이 routes collection으로 individual read-only routing tables for each instance를 만들어낸다. 모든 VM instance in the network -> directly connected to this router, and all packets leaving a VM instance are first handled at this layer before they are forwarded to the next step. Virtual Network router selects the next hop for a packet by consulting the routing table for that instance.

GCP Firewall rules to protect VM instance from unapproved connection both inbound / outbound (ingress / egress) VPC 네트워크 자체가 일종의 distributed Firewall로 작동한다. Firewall rules are applied to the network as a whole, 최종적으로 connection의 승인 / 거절은 instance 레벨에서 결정됨.

Instance - other network뿐만 아니라 instance btwn same network에도 firewall 존재.

StateFul 특성을 갖고 있다. If a connection is allowed btwn a source / target or a target at a destination -> all subsequent traffic in either direction will be allowed. 다시 말해, 한 번 연결되어 세션이 만들어지면 bidirectional communication을 지원한다.

cf. 만약 모든 형태의 firewall이 삭제되는 등의 문제가 생기면, deny all ingress rule, allow all egress rule for the network.

Firewall configuration도 set of firewall rules 형태로 설정할 수 있다. 
- Parameters
1. The direction of rules : inbound connection은 ingress rule only, outbound connection은 egress rule only.
2. Source of destination : ingress의 경우 source : IP address, source tag or source service account 형태, egress의 경우 destination; one or more range of IP
3. Protocol and port : 프로토콜이나 포트별로 아예 restricted rule 설정을 지정할 수 있음.
4. Action of the rule : allow or deny packets that matches the direction, protocol port and source / destination of rules. 그래서 결국 통과시킬 거냐 말 거냐
5. Rule assignment : rule -> instance 형태로만 지정할 수 있다. 기본 설정은 All rules are assigned to all instances. 특정 rule -> 특정 instance로만 설정하도록 바꿀 수 있다.

GCP firewall Use case - Egress

“Egress firewall rules” ctrl Outgoing connection originated inside your GCP network.
- Egree allow rules -> allow outbound connections that matches specific protocol ports / IP address.
- Egree Deny rules -> prevent instances from initiating connections that match non-permitted port protocol and IP range combinations.

여기 적용되는 rule에서의 destination -> should be specified using IP CIDR ranges. 즉, external host가 IP CIDR range를 지키지 않는 방식이면 connection 시도가 불가능하다. 따라서 VM에서 initiated된 undesired connection을 방지할 수 있다.
Internal VM에서도 specific GCP CIDR ranges 규칙을 적용할 수 있다. 보통 특정 Subnet의 VM이 same network의 another VM에 inappropriate 접근을 하는 경우 차단할 목적으로 씀.

GCP firewall Use case - Ingress

Incoming connections to the instance from any source를 관리한다.
- ingress allow rules -> allow specific protocol ports / IP ranges to connecting.
Firewall prevents instance from receiving connections on non-permitted ports and protocols. 위와 마찬가지로 특정 source에만 rule이 적용되도록 조정할 수 있고, Source의 CIDR ranges 확인 과정을 통해 undesired connection from external network / from GCP IP range를 차단할 수 있다.

---
### Pricing

- Ingress : No charge. Ingress traffic 관리 과정에서 load balancer가 일하는 걸 제외하면.
- egress의 경우 조건에 따라 좀 다름
	* Same Zone 내의 통신 (internal IP 사용하는 경우)
	* to Google Product (유튜브, maps, Drive)  / 또는 traffic to a different GCP service within the same region
-> Not Charged.
	* between zones in the same region -> internal IP를 안 쓰는 경우에 해당함.
	* to the same zone (External IP address 사용하는 경우). External ip를 사용할 경우 egress btwn zones in the same region 취급됨. (External IP로는 VM의 zone 구분을 못하기 때문)
	* egress Btwn regions within US / Canada
-> per GB $0.01
Egress btwn regions, not including traffic btwn US의 경우 varies by region.

Price calculator 써라. Web based.

---
### Lab

Routes tell VM instances and the VPC network how to send traffic from an instance to a destination, either inside the network or outside GCP. Each VPC network comes with some default routes to route traffic among its subnets and send traffic from eligible instances to the internet.

In the left pane, click*Routes*. Notice that there is a route for each subnet and one for the*Default internet gateway*(0.0.0.0/0). These routes are managed for you, but you can create custom static routes to direct some packets to specific destinations.


Each VPC network implements a distributed virtual firewall that you can configure. Firewall rules allow you to control which packets are allowed to travel to which destinations. Every VPC network has two implied firewall rules that block all incoming connections and allow all outgoing connections.

In the left pane, click*Firewall rules*. Notice that there are 4*Ingress*firewall rules for the*default*network:
	* default-allow-icmp
	* default-allow-rdp
	* default-allow-ssh
	* default-allow-internal

Without a VPC network, there are no routes. VPC Default network를 전부 삭제하면, routes도 전부 비어 있는 걸 확인할 수 있다.

VPC network에서 region -> subnet 별로 range가 있다. 새 인스턴스를 해당 region에 만드는 경우, 인스턴스의 internal IP는 subnet에서의 IP address range에 포함되는 걸 확인할 수 있다.

The*External IP addresses*for both VM instances are ephemeral. If an instance is stopped, any ephemeral external IP addresses assigned to the instance are released back into the general Compute Engine pool and become available for use by other projects. When a stopped instance is started again, a new ephemeral external IP address is assigned to the instance. Alternatively, you can reserve a static external IP address, which assigns the address to your project indefinitely until you explicitly release it.

같은 VPC 내에서 다른 region을 기반으로 만들어진 두 개의 VM은 ssh에서 ping -c 3 “internal IP address” (또는 internal ip주소 대신 vm 이름을 입력할 수도 있다.) 으로 통신이 가능하다. 이름으로 가능한 이유는 VPC 내의 DNS service가 address instance로 이름을 지정해두었기 때문.  Internal IP주소가 매번 바뀌는 걸 고려하면 꽤 효율적이다.

You can SSH because of the*allow-ssh*firewall rule, which allows incoming traffic from anywhere (0.0.0.0/0) for*tcp:22*. The SSH connection works seamlessly because Compute Engine generates an SSH key for you and stores it in one of the following locations:
* By default, Compute Engine adds the generated key to project or instance metadata.
* If your account is configured to use OS Login, Compute Engine stores the generated key with your user account.
Alternatively, you can control access to Linux instances by creating SSH keys and editing public SSH key metadata.

Which firewall rule allows the ping to mynet-eu-vm’s external IP address?
-> “mynetwork-allow-icmp”


IP CIDR ranges of these networks do not overlap. This allows you to set up mechanisms such as VPC peering between the networks. If you specify IP CIDR ranges that are different from your on-premises network, you could even configure hybrid connectivity using VPN or Cloud Interconnect.


VPC Network Custom으로 네트워크를 만들면, 필요한 region에만 Subnet을 생성하는 게 가능하다.

해당 VPC 안에서 instance를 만들기 위해서는 *Management, security, disks, networking, sole tenancy*. 설정에서 networking interface를 특정 VPC이름으로 지정하면 된다.


You can ping the external IP address of all VM instances, even though they are in either a different zone or VPC network. This confirms that public access to those instances is only controlled by the*ICMP*firewall rules that you established earlier.

---
## Common network Design

Handful of designs best related to this module 위주로 설명.

1. availability.
-> Application의 availability를 높이려면, place 2 VM into multiple zones “within same subnets”. Single Subnet을 사용할 경우 firewall rule against the subnetwork가 만들어지는데, it can improve availability without additional security complexity.
하나의 region에 multiple Zone을 사용하는 방법은 availability를 향상시키는 방법이다.

2. Globalization
Resource in different Zones (single Region) -> isolation from many types of infra, hardware, SW failures. Different Region 안에 resource를 활용할 경우 isolation 정도가 더 강해진다. 
-> Robust system with resources spread across different failure domains.
Global Load Balancer를 사용하면 route traffic to the region that is closest to Users. -> better latency / lower network traffic cost

3. Baston host isolation
External facing point of entry into a network containing private network instance. 즉 외부와 연결되는 창은 하나고, 외부에서 접근할 수 없는 인스턴스들을 그 창과 연결하는 식. Fortification point가 하나로 줄어들고, audit은 inbound ssh communication from internet을 조절하는 걸로 쉽게 해결 가능하다.

---
### Lab : Bastion Host.

일종의 maintenance Server를 만들고, 필요한 기능은 internal IP를 통해서만 접근할 수 있도록 하는 방식.

The default setting for a default or auto-type network is to allow SSH access from any source IP address. Restrict access to just your source IP address to see what happens when you try to connect from the GCP Console.
-> default ssh firewall setting을 내 컴퓨터 ip주소만 접근가능하게 설정하면, console로 ssh 접근 불가능. (인스턴스를 브라우저에서 접근하려면 Google’s IP address range에서 ssh로 접근할 수 있어야 하기 때문)

When instances do not have external IP addresses, they can only be reached by other instances on the network or via a managed VPN gateway.
In this case, the bastion VM serves as a management and maintenance interface to the webserver VM.

---
### Quiz에서
Minimum # of IP address that VM need = 1. (VM 자체는 internal IP만 있으면 된다.)




#컴퓨터공학쪽지식/Coursera/GCP/ch2_Foundation/Introduction