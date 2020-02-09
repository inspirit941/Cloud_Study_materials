# Presentation Layer
## Overview

<img width="926" alt="스크린샷 2020-02-09 오후 12 32 51" src="https://user-images.githubusercontent.com/26548454/74096795-d154a200-4b46-11ea-8116-9b1b9c4f0f84.png">

Presentation Layer : 사용자와 시스템 간, business logic, stored service 간 데이터 flow를 말한다. 간단히 말해 Networking.


## Presentation Layer : Network Configuration

Networking 에서 가장 중요시해야 할 건 Location. 이게 latency 차이를 만드는 핵심이기 때문. Distributed network일수록 outage tolerance가 강해지지만, round trip time is slower between distant elements 문제 때문에 performance limitation은 반드시 존재한다.

<img width="924" alt="스크린샷 2020-02-09 오후 12 41 45" src="https://user-images.githubusercontent.com/26548454/74096799-d6b1ec80-4b46-11ea-8a56-a5f30fb4167f.png">

미국 - 유럽 간 통신은 1초당 최대 6~7 round trip을 넘어갈 수 없다. 하지만 datacenter를 통해서는 2000 per sec. 사용자의 위치에 맞게 가장 적절한 network location of resource를 지정하는 게 land balancing.


<img width="926" alt="스크린샷 2020-02-09 오후 12 49 08" src="https://user-images.githubusercontent.com/26548454/74096800-d74a8300-4b46-11ea-9cf6-5ad878b7995c.png">

사용자를 application servers with capacity in the closest region과 매칭하는 게 Load balancer. Global Load balancer의 존재로, single external IP address로 사용자와 가장 가까운 location에 traffic을 보낼 수 있다.


<img width="927" alt="스크린샷 2020-02-09 오후 12 51 17" src="https://user-images.githubusercontent.com/26548454/74096801-d87bb000-4b46-11ea-81e8-7c584147d30b.png">


* Global load balancer.

- HTTP / HTTPS load balancer -> IPv4, v6 지원. 
로드밸런서 측에서 terminates certificates. 이 방식 때문에 allows entry from any location.
- SSL load balancer = proxy처럼 기능하지만, ssl certificates 제공
- TCP도 지원

DoS protection, 이외에도 monitor traffic for any type of unwanted traffic from internet.

* Network load balancer 

보통 layer 3에서 작동하며, session affinity / connection training 등. Load balancer 차원에서 health check 수행, start and shut down instance 작업도 같이 한다.

* Internal load balancer

Internal IP address로 통신.


<img width="927" alt="스크린샷 2020-02-09 오후 1 06 33" src="https://user-images.githubusercontent.com/26548454/74096815-fa753280-4b46-11ea-83b3-b135dc81bd56.png">

필요한 통신방법과 프로토콜에 맞는 거 고르면 된다.


---
## Presentation Layer : integration with other environments

<img width="924" alt="스크린샷 2020-02-09 오후 1 08 35" src="https://user-images.githubusercontent.com/26548454/74096816-fea15000-4b46-11ea-8d7d-93b600821d4b.png">

Now, we do offer external IPs that you can assign to virtual machines, but they really kind of goes against best practices. Since you’re only allowed seven static IP addresses per project, we recommend you put those on a load balancer. 

Now, if you’re doing a network or an internal load balancer, you’re going to get any external IP that you can use. But we have a reserve set of global IP addresses available to you. Now, these are available only for our global load balancers and that’s because we’ve configured BGP routes, so that way they’re announced at every single pop in the world.


<img width="924" alt="스크린샷 2020-02-09 오후 1 12 45" src="https://user-images.githubusercontent.com/26548454/74096817-ffd27d00-4b46-11ea-9e88-e1131e87acf2.png">

Cloud CDN : global edge point 사용. 전세계에 분포해 있는 edge point 덕분에 cloud service를 쓰지 않는 지역이어도 performance를 확보하고 latency를 줄일 수 있다.

Now, in order to use the CDN, you have to turn on HTTP(S) load balancing or other network load balancing. But in this case here, you can actually push and publish content directly from Google Cloud stores to the CDN. But if you want to use it from the network layer, we can automatically start to cache any data that goes through our HTTP(S) load balancer. So that’s a kind of a huge benefit.

Another one, it’s really affordable. And second, you can actually save 50 percent egress fees. So normally, we charge about nine, I believe it’s nine cents as of this recording, egress for every gigabyte of data that leaves our network. Now, if that data that leaves our network is coming from cloud CDN or even one of our cloud CDN providers, that drops down by 50 percent. So it’s a huge advantage to your users, to your apps, and to the bottom line.


<img width="924" alt="스크린샷 2020-02-09 오후 1 23 45" src="https://user-images.githubusercontent.com/26548454/74096818-ffd27d00-4b46-11ea-8f5d-3fb7bcf9f160.png">

클라우드와 다른 클라우드 간 통신.

1. 인터넷을 사용하는 경우
- Google Cloud Router를 GCP 쪽에 설치. 이게 있으면 other cloud 쪽에서도 GCP VM에 접근할 수 있음. 
- Dedicated interconnection 필요. (또는 partner interconnect)

<img width="927" alt="스크린샷 2020-02-09 오후 2 05 11" src="https://user-images.githubusercontent.com/26548454/74096819-0103aa00-4b47-11ea-9a52-590d3a10ae22.png">

2. VPN 사용
마찬가지로 cloud router 사용해야 함. 통신하는 양쪽의 network (GCP와 on-premises 또는 다른 cloud) 에서 한쪽에 변화가 있을 경우, 반대편에서 변화를 자동으로 인지하고 알아서 설정해주는 역할




<img width="925" alt="스크린샷 2020-02-09 오후 2 15 35" src="https://user-images.githubusercontent.com/26548454/74096820-019c4080-4b47-11ea-8c47-53c5236f2fbe.png">

성능

Dedicated network의 경우 unsaturated. Shared link가 아니기 때문에 10 ~ 100 GB link 제공.

VPN의 경우 multiple channel로 throughputs을 높일 수는 있지만, stream 양에 따라서 편차가 좀 나는 편이다. 대신  Changing encryption으로 성능에 변화를 줄 수 있음
	- ASE-GCM : highest throughput 제공.
	- iperf : measure throughputs

---