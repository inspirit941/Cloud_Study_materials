# Scaling & Automation
## Overview
Interconnecting Network에 초점. 각각의 App, workload마다 여러 종류의 network connection solution이 필요함.

## Cloud VPN

<img width="926" alt="스크린샷 2020-01-27 오후 3 27 12" src="https://user-images.githubusercontent.com/26548454/73426075-c6e01e80-4376-11ea-9db6-7e012b0cca86.png">

On-premises network와 GCP VPC network를 IPSec VPN tunnel로 연결하는 작업을 수행한다. 

두 개의 네트워크는 one VPN gateway에서 encrypted -> other VPN gateway에서 decrypted. 이 암호화 작업으로 public internet을 사용하면서도 security 확보가 가능하다.

* site to site VPN
* dynamic routes
* IKEv1, IKEv2 지원.

Cloud VPN doesn’t support new cases where a client computers need to dial in to a VPN using client VPN software. 즉 Cloud VPN 말고 다른 VPN 소프트웨어 쓰려는 건 지원하지 않는다

<img width="926" alt="스크린샷 2020-01-27 오후 3 33 31" src="https://user-images.githubusercontent.com/26548454/73426041-b5971200-4376-11ea-8da7-65692c65ef65.png">

예시.
현재 on-premises와 GCP가 있고, GCP 내에는 subnets in US-east and US-West. 각각의 region에는 resource가 있다. 여기서 두 resource는 internal IP로 통신이 가능하다. Routing within a network is automatically configured이기 때문.

On-premise network와 Cloud VPN을 연결하려 configure VPN gateway, on-premise VPN gateway, VPN tunnel 설정을 해줘야 한다.

- Cloud VPN gateway : regional resources that uses a regional external IP address. 
- on-premise VPN gateway는 physical device in your data center / physical | software based VPN offering in another Cloud providers network. (External IP address 존재)
- VPN tunnel : connects your VPN gateways and serves as the virtual medium through which encrypted traffic is passed.

즉 두 개의 gateway는 각각 internet과 연결된 VPN tunnel이 존재해야 함. 인터넷으로 두 개의 gateway가 통신하기 위해서는 각각의 VPN tunnel이 있어야 함.

*Maximum transaction unit (MTU) for your on-premises VPN gateway는 1460byte를 넘을 수 없다.* 암호화 + 캡슐화 과정에서의 packet 때문.

<img width="928" alt="스크린샷 2020-01-28 오후 12 29 31" src="https://user-images.githubusercontent.com/26548454/73426042-b5971200-4376-11ea-8ff9-37526b85c7e9.png">

Cloud VPN은 Static / dynamic routes 둘 다 지원한다. Dynamic routes를 사용하려면 Cloud Router 설정이 필요함.

- Cloud Router : Cloud VPN tunnel에서 manage routes를 담당함. Border gateway protocol (BGP) 사용. Routes update / exchange without changing tunnel configuration을 가능하게 함.

Ex) 위 슬라이드에서 GCP에는 tests / prod라는 서로 다른 regional subnet이 있다. On-premise는 29개의 subnet이 있고, 두 개의 네트워크 자체는 Cloud VPN tunnel로 연결되어 있음.
-> 여기서 만약 GCP network 내에 또 다른 subnet을 만들고, on-premise의 /24 subnet이 traffic을 Handle하게 설정하고 싶다면?

이런 식의 network configuration change가 발생할 때, VPN tunnel은 Cloud Router를 써서 BGP session을 만든다. (On-premises VPN도 BGP를 지원해야 한다) 이렇게 되면, new network seamlessly advertised. new subnet을 사용하고, 트래픽 주고받는 데 전혀 문제없이 작동하는 걸 볼 수 있다. (Lab)

BGP setup을 위해서는 additional IP address가 양측 VPN tunnel에 반드시 할당되어 있어야 한다. 
-> 각각의 assigned IP address는 link-local 이어야 한다.
-> 169.254.0.0/16 범위. 얘네는 network 내에서의 IP address space에 포함되는 게 아니고, BGP session을 위해서만 사용되는 애들임

(Link-local: 단일 네트워크로 범위가 제한되는 주소체계. 특정 사이트 내에서만 사용할 수 있는 주소를 site-local address라고 하는데, 그것보다 더 작은 개념. 링크 안에서만 통용되는 주소라고 보면 된다)  


---
### Lab
VPN tunnel btwn 2 networks in separate regions (VM끼리 internal IP address로 통신 가능하도록)

* 계정에 2개의 VPN network가 있고, 각각의 subnet이 서로 다른 region인 걸 확인.
* firewall rule에서 각각의 network가 allow icmp인지 확인. ssh와 icmp 트래픽을 받을 수 있도록 설정한 것.
* 두 개의 subnet이 VPN connect이 없는 경우 -> internal IP address 통신이 불가능하다. external은 인터넷 통한 통신이라서 작동함.

실습에서는 single tunnel (symmetric configuration)을 사용하지만, 실제로는 multiple tunnel / gateway를 사용하는 게 일반적이다. Single point of failure 방지용.


VPN gateway 생성을 위해서는
1. Reserve 2 static IP address. VPC network -> external IP address에서 할당받을 수 있다.
2.  Vpn1 gateway + tunnel1to2 생성. Hybrid connectivity -> VPN에서 VPN connection.
3. Gateway에는 vpn1 정보를, tunnel에 vpn2 관련정보 (static ip, remote network ip range 등)을 입력한다.
반대로도 마찬가지
4. 두 개 만들고 나면, tunnel 연결이 자동으로 진행된다. 설정에 문제 없으면 established.
5. 각각의 instance에서 ssh로 internet IP address 통신해도 잘 되는 걸 볼 수 있다.

---
## Cloud interconnect and Peering

<img width="929" alt="스크린샷 2020-01-28 오후 1 24 35" src="https://user-images.githubusercontent.com/26548454/73426044-b62fa880-4376-11ea-9a9b-4cc459372f53.png">

Connect Infrastructure to Google -> Cloud interconnect / peering 서비스는 여러 개가 있다. 크게 dedicated vs Shared connections, layer 2 vs layer 3 connection으로 나뉜다.

* Dedicated Connections : Google Network와 direct connection
* Shared Connection : connection to Google’s network via a partner.
* Layer2 connection은 pipes directly into your GCP network by VLAN. Connectivity to internal IP address in the RFC 1918 address space.
* Layer3의 경우 public IP address로 G suite services, Youtube, Google Cloud API를 통한 access를 지원한다.

직전에 설명한 Cloud VPN -> 인터넷을 사용하지만, 트래픽을 encrypt해서 internal IP address에 접근 가능하도록 하는 서비스. 따라서 이 서비스는 Direct peering / Carrier Peering과 특히 궁합이 좋다.

---
### Cloud Interconnect

<img width="927" alt="스크린샷 2020-01-29 오후 12 10 19" src="https://user-images.githubusercontent.com/26548454/73426242-28a08880-4377-11ea-9d30-93dc86b90095.png">


* Dedicated Interconnect
On-premise Network와 Google Network를 physical connection으로 연결하는 방법. 대량의 데이터 전송이 편하다는 점에서 cost-effective that purchasing additional bandwidth over public internet.

이 방법을 사용하려면 provision a cross-connect btwn the Google Network & own router in a common co-location facility. 즉 위 사진처럼 On-premise router와 Google Perring Edge가 colocation (동일장소 배치).

to Exchange routes btwn networks -> configure a BGP session over the interconnect btwn cloud router / on-premises router. (클라우드 라우터 & on-premise 라우터 둘 다 BGP session을 생성할 수 있어야 함) 이게 있으면 상호 네트워크간 통신이 원활하다.

99.99% uptime SLA.

physically colocation이 필요하다고 했다. Google 측에서 제공하는 colocation 위치가 있음. 지리적으로 접근하기 쉬우면 상관없는데, 구글의 colocation facility를 사용하기 어려운 경우가 있다. 그 때 사용할 수 있는 게 Partner interconnect


<img width="928" alt="스크린샷 2020-01-29 오후 12 26 55" src="https://user-images.githubusercontent.com/26548454/73426205-0f97d780-4377-11ea-9072-569431553a60.png">

* Partner interconnect
On-premise network와 VPC network를supported service provider로 연결하는 것. Physical data center가 Dedicated interconnect colocation 장소에서 멀리 떨어져있는 경우에 권장.

Service provider network 쪽에 Google VPC와 on-premise network 연결을 요청한다. 연결이 되면 can request partner interconnect connection -> establish BGP session btwn Cloud Router & on-premises Router. BGP session이 연결되면 통신 가능.


<img width="926" alt="스크린샷 2020-01-29 오후 12 46 20" src="https://user-images.githubusercontent.com/26548454/73426206-0f97d780-4377-11ea-8919-433c74cd507c.png">

Connection 3가지 요약정리. 세 가지 모두 on-premise network와 VPC network에서 Internal IP address Access를 지원한다. 
*셋의 차이점은 Capacity / requirements for using a service*

1. IPsec VPN tunnel : Public Internet을 사용하되, 그 안에서 encrypted된 traffic을 생성해 통신하려는 시스템. 양쪽 다 VPN gateway + tunnel 세팅이 되어 있어야 함. 
1.5GBps는 Public internet 사용할 경우, 3GBps는 Direct peering 사용할 때의 capacity. Capacity를 키우기 위해서는 Multiple tunnel을 세팅하는 경우가 많다.
2. Dedicated Interconnection : 10GBps. Google-supported colocation facility가 필요하다. 최대 8개 link까지 만들 수 있음.
3. Partner interconnection : 50MBps에서 10GBps까지 가능. Requirements depends on Service Provider.

권장사항: 처음에는 VPN tunnel 설치. Enterprise-grade로 필요할 경우 Dedicated / Partner interconnection 사용하는 걸 추천한다고 함.

---
### Peering

<img width="924" alt="스크린샷 2020-01-29 오후 1 10 39" src="https://user-images.githubusercontent.com/26548454/73426207-0f97d780-4377-11ea-8c0b-efdb188a6d7e.png">

구글 / Google Cloud property 접근하려 할 때 유용한 방법. Business network과 google 사이의 connection 연결방법 중 하나로, 구글의 broad-reaching Edge network location을 활용해 internet traffic exchange가 가능하다.

구글과 peering entity 간 BGP route exchanging을 하는 것. 연결되기만 하면, 구글에서 제공하는 모든 형태의 서비스 이용이 가능하다. 단, SLA 개념은 없음. Direct peering을 하기 위한 requirement는 link 보라고 하고 넘어감


구글의 Edge Point를 사용하는 거라고 했다. Colocation facility와 마찬가지로 Edge point도 전세계에 분포해 있음. (Points of Presence - PoPs) 근처에 PoPs가 없으면, Carrier Peering을 선택할 수 있다.

<img width="928" alt="스크린샷 2020-01-29 오후 1 42 48" src="https://user-images.githubusercontent.com/26548454/73426208-0f97d780-4377-11ea-8c00-fe7e659aaacc.png">

Carrier Peering의 경우, Partner interconnect와 비슷하게 구글과 접촉할 수 있는 Service Provider를 끼고 작업하는 것. Partner requirement를 맞추는 게 중요하다. 자세한 내용은 link로 다룬다고 하고 넘어감

마찬가지로, SLA 없다.


<img width="924" alt="스크린샷 2020-01-29 오후 1 45 57" src="https://user-images.githubusercontent.com/26548454/73426332-5be31780-4377-11ea-9070-94ef0a6762e1.png">


요약. Peering은 Public IP address로 Access하고 싶은 경우에 활용할 수 있다. 두 서비스의 차이는 Requirement / Capacity. 구글과 직접 Peering하는 경우 링크당 10GBps까지 보장하며, GCP Edge point와 연결되어 있어야 한다. Carrier peering은 Partner의 요구사항에 따라 다르고, Capacity도 파트너마다 다름.

---
### Choosing a Connection

Dedicated / Sharing, Layer2 / Layer3 방식으로도 Hybrid Connection을 구분했지만, interconnect / Peering 방식으로도 구분 가능하다.

<img width="925" alt="스크린샷 2020-01-29 오후 1 49 18" src="https://user-images.githubusercontent.com/26548454/73426333-5be31780-4377-11ea-9e37-b86e5938feec.png">

InterConnect : Direct access to Internal IP address (RFC1918 IP address in your VPC, with an SLA).

Peering : Access to Google Public IP address, without SLA

<img width="929" alt="스크린샷 2020-01-29 오후 2 07 39" src="https://user-images.githubusercontent.com/26548454/73426334-5be31780-4377-11ea-982e-681248a467de.png">


1. G suite나 youtube, 기타 API 형태 서비스를 사용할 거라면 Peering 추천, 네트워크를 GCP에 연결하는 게 목적이라면 InterConnect 방식 추천
2. 구글의 colocation 위치조건에 맞는 게 없으면 Cloud VPN이나 Partner Interconnect 권장.
여기서, Short duration & trials + encrypted channel이 필요할 경우 Cloud VPN을, 그게 아니면 Partner interconnect.
3. Dedicated lnterconnect 조건에 부합한다고 해도 “can’t provide your own encryption mechanism for sensitive traffic”, “10 Gbps가 너무 크거나 multiple cloud access가 필요없을 경우”는 Cloud VPN이나 partner interconnect가 더 낫다.

---
### Shard VPC, VPC peering

Single project라면 1개의 VPC만 가지고 있는 경우가 일반적이다. 이 네트워크 안에 여러 Region + instance가 존재하는 식. 하지만 보통은 Multiple Project + Multiple VPC Network + subnets 형태로 운영하기 마련.

GCP project끼리 VPC network을 공유하는 방법을 다룸
* Shared VPC : share Network across several projects in your GCP organization.
* VPC network peering : configure private communication across projects in same / different organizations.

<img width="919" alt="스크린샷 2020-01-29 오후 2 28 35" src="https://user-images.githubusercontent.com/26548454/73426335-5c7bae00-4377-11ea-9eeb-40d2e6053fed.png">

-> resources can communicate each other securely & efficiently using internal IPs from their networks.

사진 예시.
One Network = Web Application Servers project. 이 네트워크는 다른 3개의 프로젝트와 sharing중. 총 4개의 프로젝트는 전부 same network에 instance를 두고 있고, private communication to the server using internal IP address 상태다. 외부 Client / on-premises와는 External IP address로 통신하고 있음. 클라이언트나 on-premises에서 백엔드 프로젝트에 직접 접근하는 건 불가능한 구조로 되어 있다.

Shared VPC를 쓸 경우, 위 구조처럼 ‘host project’가 존재하고, 여러 개의 service가 attached된 형태. 이런 형태의 VPC network를 Shared VPC network라고 부른다.

 
<img width="922" alt="스크린샷 2020-01-29 오후 6 23 55" src="https://user-images.githubusercontent.com/26548454/73426336-5c7bae00-4377-11ea-8a1a-cecda7ea2115.png">

-> VPC Peering은 서로 다른 두 개의 VPC network를 private RFC 1918 connectivity로 연결한 걸 말한다. 두 개의 네트워크가 같은 프로젝트건 아니건, 같은 organization 내에 있건 말건 상관없음. 

각각의 VPC network는 고유의 firewall rule을 가지고 있다고 설명한 적이 있다. 위 사진을 예시로 들면, VPC Peering을 위해서는 각각의 network (consumer / producer) 에서 서로를 peer설정해야 한다. 두 개 모두 서로를 peer등록할 경우 VPC Network Peering이 활성화되며, routes are exchanged.

활성화가 완료되면, 각각의 VM이 상대 VPC network와 private communication이 가능해진다. (Interval IP address 사용 가능)

일종의 decentralized, distributed approach to multiproject networking. 각 VPC마다 자기 firewall rules, routing table을 각각 그대로 유지하고, separate administrator group을 유지하고 있기 때문.

External IP address로 통신하는 게 아니기 때문에 not incur network latency, no security / cost drawbacks.


<img width="926" alt="스크린샷 2020-01-29 오후 6 47 46" src="https://user-images.githubusercontent.com/26548454/73426337-5d144480-4377-11ea-8a30-bc020bb8b949.png">

두 가지 방식의 가장 큰 차이점은 ‘Network administration Model’. 
* Shared VPC는 일종의 Centralized multi-project model. (Security / network policy 자체는 single designated VPC network에서 결정하기 때문)
* VPC Peering의 경우 각각의 VPC network has separate administrator, maintains its own global firewall, routing table.

---
