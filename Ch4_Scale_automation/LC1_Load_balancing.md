# Load Balancing and Autoscaling
High availability 확보를 위해. Serve content as close as possible to your users on a system. (1M queries per sec)

Cloud Load Balancing = Fully distributed SW defined managed system. 완벽한 SW이므로 HW infrastructure나 physical 장비가 필요없다.

<img width="807" alt="스크린샷 2020-01-31 오전 11 40 15" src="https://user-images.githubusercontent.com/26548454/73587307-d5a50d80-44fd-11ea-93d1-873bb5ba2cd4.png">

크게 두 가지의 load balancer. Global vs Regional. 서비스의 사용자나 인스턴스가 Global 분포라면 Global 사용. (전세계 단위의 사용자에게 single anycast IP address로 provide할 경우)

Regional은 Same GCP region에 있는 instances의 load balancing 지원. Internal Load balancer로는 Andromeda라는 GCP SW defined network virtualization stack을 사용하고, network load balancer로는 Maglev라는 large distributed SW system을 사용한다.


그 외에도 Proxy based regional layer 7 load balancer가 있다. It is accessible only in the load balancers’ region in your VPC network.

---
## Managed Instance Group


<img width="922" alt="스크린샷 2020-01-31 오전 11 54 28" src="https://user-images.githubusercontent.com/26548454/73587308-d5a50d80-44fd-11ea-8251-4cd84998d900.png">


Identical VM instances that you control as a single entity using an instance template. 여러 개 인스턴스를 한번에 업데이트하는 등의 작업이 가능하다. 만약 Application에서 추가 Compute Resoures가 필요하면 automatically scale the number of instances in the group.

Load balancer와 합쳐져서 수행하는 기능이 몇 가지 있음. 만약 instances in the group crashes, stops, or are deleted by an action other than the instance group command -> managed instance group측에서 자동으로 recreate the instances to resume processing tasks. 새로 만들어진 인스턴스는 삭제된 인스턴스와 동일한 이름, template을 갖게 된다.

Automatically identify and recreate unhealthy instances in a group, to ensure that all instances are running optimally.

Regional managed instance group 시스템 형태를 zonal managed instance group보다 권장하는 편. Regional 적용을 해야 spread the application load across multiple zones이 가능하기 때문.
-> entire zone 자체가 박살이 나도 해결이 가능하기 때문 (zonal failure / unforeseen senarios 대응이 쉽다) Regional일 경우, 같은 region의 다른 zone에서 동일한 기능을 수행하도록 세팅해줄 수 있다.


<img width="925" alt="스크린샷 2020-01-31 오후 12 01 57" src="https://user-images.githubusercontent.com/26548454/73587309-d5a50d80-44fd-11ea-8a5c-a1979c73885b.png">

1. Instance template 생성
2. Managed instance group of end specific instances을 생성.
3. Instance group manager가 자동으로 populates the instance group based on internal templates.

GCP console 사용 가능. 인스턴스 생성하는 것과 거의 똑같다.

<img width="921" alt="스크린샷 2020-01-31 오후 12 11 38" src="https://user-images.githubusercontent.com/26548454/73587310-d5a50d80-44fd-11ea-995a-3c23a36b5227.png">

생성 과정에서 Specific rule Define이 필요함.
1. Decide whether the instance group is going to be single / multi zoned + where those locations will be.
2. Choose the ports that you are going to allow / load balance across.
3. Select instance template you want to use.
4. Whether you want to auto-scale, under what circumstances.
5. Consider creating health check to determine which instances are healthy and should reserve traffic.

---
### AutoScale / health Check

<img width="928" alt="스크린샷 2020-01-31 오후 12 14 32" src="https://user-images.githubusercontent.com/26548454/73587333-f3727280-44fd-11ea-8a3a-7773f2f5653c.png">


상술했듯, managed instance group은 autoscale 작업으로 load량에 따라 instance add / remove을 자동으로 수행 가능하다. 비용절감 + 유연한 대처가 가능함

Autoscaling Policy만 잘 지정해주면 된다. CPU 사용량 / Load balancing Capacity / monitoring metrics / queue-based workload (like Pub/Sub) 등등의 기준이 있음.

사진 예시
-> target cpu 사용량이 75%고 현재 100, 80%라면 -> cpu 사용량이 75 아래로 내려가도록 인스턴스 생성. 반대의 경우라면 인스턴스 삭제.

<img width="924" alt="스크린샷 2020-01-31 오후 12 18 13" src="https://user-images.githubusercontent.com/26548454/73587334-f3727280-44fd-11ea-9209-ace6d3d2e119.png">

Instance group을 보면, 위 사진처럼 utilization monitoring이 가능하다. Policy 만들 때 참고.

Stackdriver monitoring 기능을 사용하면, set up alerts through several notification channels.


<img width="927" alt="스크린샷 2020-01-31 오후 12 20 04" src="https://user-images.githubusercontent.com/26548454/73587335-f40b0900-44fd-11ea-86e4-cf3a2ac693b8.png">


Health check은 stackdriver의 uptime check와 거의 유사한 기능. 프로토콜, 포트, health criteria만 설정해주면 된다. 이 설정에 맞게 GCP 쪽에서 health 정도를 계산한다. 
- ‘얼마나 자주 health check 할 건지’ = check interval
- How long to wait for a response = timeout
- how many successful attempts are decisive = healthy threshold
- how many failed attempts are decisive = unhealthy threshold

위 사진예시는 15초 간 두 번의 health check 수행해서 health여부를 판단하는 설정.


---
## HTTP(S) Load Balancing

Acts at layer 7 of OSI model. Layer 7 = application layer, which deals with the actual content of each message allowing for routing decision based on URL.

<img width="813" alt="스크린샷 2020-01-31 오후 12 30 35" src="https://user-images.githubusercontent.com/26548454/73587336-f40b0900-44fd-11ea-8260-c07507e64210.png">


구글에서는 Global HTTP(S) load balancer 지원. 어느 application이든 single anycast IP address로 사용자에게 접근할 수 있다는 것. Multiple backend instances / across multiple regions.

Http는 load balanced on 80, 8080포트, https는 443에서. IPv4와 IPv6 지원. Enable content-based, cross-regional load balancing 가능하다. URL -> set of instances로 route mapping도 가능함.

기본적으로 접근하려는 사용자에게 가장 가까운 거리의 instance group이 자동 할당되며, 해당 그룹이 여유가 없을 경우 그 다음으로 가까운 거리의 group을 찾는 식이다.

<img width="924" alt="스크린샷 2020-01-31 오후 12 35 06" src="https://user-images.githubusercontent.com/26548454/73587337-f40b0900-44fd-11ea-8552-09cc37d611fb.png">

1. 인터넷에서 들어오는 Request는 global Forwarding Rule에 의해 target HTTP proxy로 넘어간다.
2. Target Http proxy에서 request를 URL map과 대조해서, appropriate backend Service로 요청을 보낸다. Ex) www.example/audio -> audio service backend로 보내고, video면 video service backend로 보내는 식.
3. Backend service는 들어온 요청을 solving capacity zone & instance held of its attached backends.


<img width="925" alt="스크린샷 2020-01-31 오후 4 55 32" src="https://user-images.githubusercontent.com/26548454/73587338-f40b0900-44fd-11ea-8b53-2371565bece0.png">


백엔드 서비스에서는 health check, session affinity, timeout setting 등도 진행함.

Health check은 configured interval로 진행되며,  check를 통과한 instance만 request를 받을 수 있다. unhealthy로 분류된 애들은 다시 정상화될 때까지 request 처리 불가능.

보통 HTTPS load balancing은 round robin 알고리즘으로 request distribution 진행. Session affinity에 의해 overridden 가능. 
- Session affinity =  attempts to send all requests from the same client to the same VM instances. (한놈만 팬다 느낌)
- timeout setting = 30 sec by default. Backend service가 request Fail 여부를 판별하기 위해 기다리는 시간이라고 보면 된다.

Backends themselves contains an instance group, balancing mode, and a capacity scalar. 
* instance group : managed instance group with / without autoscaling 또는 unmanaged instance group.
* Balancing mode : load balancing system에게 how to determine when the backend is at full usage인지를 알려주는 것.
만약 full usage라는 진단이 서면, new request는 자동으로 routed to the nearest region that can still handle request.
-> based on CPU 사용량 or request per sec.
* Capacity Setting : additional control that interacts with balancing mode setting. 
Ex) 만약 인스턴스의 CPU 최대 사용량을 80%로 하고 싶으면, balancing mode에 cpu 사용량을 최대 80%로 설정한 다음 capacity를 100%로 설정하면 된다. 여기서 만약 사용량을 절반으로 줄이고 싶으면, balancing mode는 그대로 두고 capacity만 50%로 낮추면 된다.

모든 Backend 설정은 즉각적으로 반영되는 게 아니다. 설정한 다음 몇 분 정도 기다려야 함.

---
### Example : HTTP load balancer

<img width="923" alt="스크린샷 2020-01-31 오후 5 08 51" src="https://user-images.githubusercontent.com/26548454/73587365-24eb3e00-44fe-11ea-84b5-ff9b45a9bce0.png">


위 사진의 project는 single global IP address. 여기 접근하려는 사용자는 두 개의 region. (North America, EMEA)

1. Global Forwarding Rule이 들어오는 요청을 전부 target HTTP proxy로 보낸다.

2. proxy에서는 URL map을 체크하고, 들어온 요청 url에 맞게 appropriated Backend service로 요청을 보낸다. 위 사진의 경우 guestbook application with only one backend service.

3. 백엔드 서비스는 두 개 있다; US central 1-a, Europe west d. 각각의 region에 managed instance group 형태로 존재한다.
처음 요청이 들어오면, HTTPS load balancing service가 approximate origin of the request from the source IP address. (이 요청이 어디서 왔는지부터 파악한다)

4. Load balancing service는 백엔드 서비스의 instance group가 각각 어느 region인지, overall capacity / overall current usage를 알고 있다. 따라서 요청이 들어온 곳에서 가장 가까운 region이 available하면 그리로 요청을 보낸다.
예시에서는 미국 접속자는 미국 region, 유럽 접속자는 유럽 region으로 요청이 넘어갈 것.

5. Health instance가 없거나, 추가요청을 수용할 수 없는 상황이라면, 그 다음으로 가까운 region 측에 요청을 전달한다. 


-> 이걸 Cross-region Load balancing이라고 한다.

<img width="926" alt="스크린샷 2020-01-31 오후 5 20 54" src="https://user-images.githubusercontent.com/26548454/73587364-24eb3e00-44fe-11ea-8e41-fa6f62cb3082.png">

Load Balancing의 다른 경우는 Content-based load balancing. 예시의 경우 Web / video traffic에 따라 backend service를 분리해둔 상황.

트래픽은 URL header에 의해 분리되고, 요청하는 데이터가 video인지 web인지에 따라 상응하는 백엔드 시스템으로 요청을 보내는 식이다. 

이 모든 작업이 single global IP address로 처리됨.

---
### HTTP(S) Load balancing

HTTPS 로드밸런서도 상술한 HTTP 로드밸런서와 거의 동일하다. 후술할 몇 가지 차이점만 빼면

<img width="928" alt="스크린샷 2020-01-31 오후 5 24 50" src="https://user-images.githubusercontent.com/26548454/73587363-2452a780-44fe-11ea-9535-496cb3a9f023.png">

* Target HTTPS proxy 사용.
* 최소 한 개의 SSL certificate installed on the target HTTPS proxy for the Load balancer
* Client의 SSL session terminates at the load balancer
* Support QUIC transport layer protocol.
QUIC -> transport layer 프로토콜로, allow faster client connection initiation, eliminate head of line blocking in multiplexed streams, support connections migration when a client’s IP address changes. 


HTTPS 쓰려면 SSL certificate가 필요하다. Target proxy for the load balancer에 필요함. 최대 10개의 certificate 등록이 가능. SSL certificate는 로드 밸런싱 proxies에서만 쓰임.

---
### Lab

1. Firewall rule 체크. http 트래픽 to backend, TCP traffic from GCP health checker 허용해야 함.
-> firewall rule 두 개 만듬. 모든 http 트래픽 허용하는 거랑 health check용 (gcp용 특정 ip range, 모든 tcp 허용)
2. Apache2 웹서버 VM 생성. 매번 VM 만들 때마다 apache 설치 + 웹서버 실행되도록 VM설정.
3. VM 생성 시 disk를 keep alive 설정해주면, VM을 지워도 디스크는 남아 있다. 이걸 갖고 image를 만듦. 이 이미지가 일종의 template이고, managed instance group을 만들 때 사용할 예정이다.
4. Compute Engine -> Instance template 파트에서 instance template 생성
5. 만든 template으로 managed instance group 생성

Managed instance groups offer*autoscaling*capabilities that allow you to automatically add or remove instances from a managed instance group based on increases or decreases in load. Autoscaling helps your applications gracefully handle increases in traffic and reduces cost when the need for resources is lower. You just define the autoscaling policy, and the autoscaler performs automatic scaling based on the measured load.

6. 다 만들어지면, Compute Engine instance 부분을 들어가서 각각의 region별로 한 개씩 vm이 만들어졌는지 확인.
7. Http Load balancer 설정할 예정. Network service -> load balancing 선택. http load balancing 선택 후 Start configuration.

---
## SSL & TCP load balancing


<img width="806" alt="스크린샷 2020-01-31 오후 6 30 04" src="https://user-images.githubusercontent.com/26548454/73587366-24eb3e00-44fe-11ea-9b6d-e47aed5bb176.png">

Global load balancing for Encrypted, non-http traffic. It terminates user SSL connections at the load balancing layer, then balances the connections across your instances using SSL / TCP protocol.

Multiple region에 적용 가능하며, load balancer automatically directs traffic to the closest region that has capacity. IPv4, IPv6 둘 다 지원하며, intelligent routing, certificate management, security patching, SSL policy 다 지원한다.

* intelligent routing -> capacity 여유가 있는 백엔드 서비스로 request 자동 할당
* certificate management -> only need to update your customer-facing certificate in one place when you need to switch those certificates.
Self-signed certificate로 management overhead for your VM을 줄일 수 있다.
* SSL이나 TCP에서 취약점이 발견될 경우, GCP에서 apply patches ah the load balancer automatically. (To keep your instance safe)

<img width="923" alt="스크린샷 2020-01-31 오후 6 38 27" src="https://user-images.githubusercontent.com/26548454/73587367-24eb3e00-44fe-11ea-8e24-8e64485df85d.png">

위 사진의 경우, traffic from lowa와 Boston 두 개가 있지만, Global load balancing layer에서 SSL connection은 terminated된다.
새로운 connection이 closest backend service로 연결됨. 즉 boston은 us east region으로, lowa는 us central region으로 backend service를 연결받는 것.

TCP와 SSL 둘 다 proxy 사이의 연결에서 사용할 수 있지만, SSL을 추천하는 편이라고 함

---
### TCP proxy load balancing


<img width="929" alt="스크린샷 2020-01-31 오후 6 41 52" src="https://user-images.githubusercontent.com/26548454/73587368-2583d480-44fe-11ea-8c7e-e50c9d750bf5.png">

Unencrypted, non-http traffic인 TCP에 사용되는 로드밸런싱 시스템. SSL과 마찬가지로, Load Balancing Layer에서 TCP session 자체는 terminated된다. Then forwards the traffic to your VM instances using TCP / SSO.

마찬가지로 multiple region에 적용 가능하며, load balancer automatically directs traffic to the closest region that has capacity.

IPv4 / v6 둘 다 지원하고, intelligent routing과 security patching 제공한다.

예시 설명은 그림까지 SSL과 거의 동일하다. 마찬가지로 client의 TCP session은 load balancing layer에서 terminated되고, 내부에서 새로운 connection이 closest backend instance로 연결된다는 내용. Proxy와 backends는 SSL, TCP 둘 다 가능하지만 SSL 추천한다는 내용까지 동일


---
## Network Load balancing

<img width="920" alt="스크린샷 2020-01-31 오후 6 47 39" src="https://user-images.githubusercontent.com/26548454/73587369-2583d480-44fe-11ea-8cd2-1a4fef90d297.png">

Regional, non-proxy Load Balancing System. 다시말해 All traffic is passed through the load balancer, instead of being proxied. + traffic can only be balanced btwn VM instances that are in same region. (Global은 region 단위로 밸런싱을 수행하지만, 얘는 그렇지 않다)

Forwarding rule로 ‘incoming IP protocol data (address, port, protocol type 등)’ 을 사용한다. Load balance UDP traffic, TCP NSSL traffic on ports that are not supported by TCP proxy / SSL proxy Load balancer.

Backends of network load balancer -> template based instance group이나 target pooled resources.

<img width="919" alt="스크린샷 2020-01-31 오후 6 52 04" src="https://user-images.githubusercontent.com/26548454/73587383-5bc15400-44fe-11ea-8353-f71dc86c4436.png">

-> Target pooled resources : defined a group of instances that receives incoming traffic from forwarding rules. Forwarding rule에 따라 트래픽이 target pooled resource에 도착하면, load balancer가 target pool안의 instance 중 하나를 선택한다. (Based on source IP, port, destination IP and port 기준에 맞게)

얘는 forwarding rules that handles TCP / UDP traffic일 경우에만 사용 가능한 개념. 각각의 프로젝트마다 최대 50개의 pool이 존재하며, 각 target pool마다 단 하나의 health check 기능을 탑재할 수 있다.

Regional Load balancer에 딸려나온 기능이니만큼, target pool 안의 모든 인스턴스는 같은 region 안에 있어야 한다.

---
## Internal Load Balancing

<img width="810" alt="스크린샷 2020-02-01 오후 12 52 39" src="https://user-images.githubusercontent.com/26548454/73587384-5bc15400-44fe-11ea-82c1-0e1e51d2f6de.png">

Regional, private load balancing (TCP / UDP based traffic.) 즉 private load balancing IP address를 사용해서 run / scale service가 가능하다. This is only accessible through internal IP address of VM instances in same region.

그 때문에, internal load balancing으로 configure internal load balancing IP address, act as the frontend to your private backend instance 형태로 많이 활용한다. 전부 internal IP address 형태 통신이라서 low latency.

Load balancing Service를 위한 public IP가 필요하지 않으므로, internal requests to stay internal to your VPC network & the region이 가능하다.


<img width="925" alt="스크린샷 2020-02-01 오후 1 00 20" src="https://user-images.githubusercontent.com/26548454/73587385-5c59ea80-44fe-11ea-9d74-344664f39f6e.png">

SW-defined, fully distributed load balancing 방식. VM이나 physical sth이 필요없다. 

Internal load balancing의 traditional proxy model이 왼쪽 방식. 
1. load balancing 작업을 수행하는 IP address가 있고, 클라이언트는 이 IP주소로 요청을 보낸다. 
2. 클라이언트의 request는 load balancer에서 terminated되고, load balancer가 backend service와의 connection을 새로 생성하는 식. 
즉 Connection이 클라이언트 - 로드밸런서, 로드밸런서 - 백엔드서비스로 총 두 개.

GCP의 internal load balancing model은 오른쪽 방식을 사용한다. 
Lightweight load balancing built on top of Andromeda (Google’s network virtualization stack)를 사용해서 directly delivers the traffic from the client instances to a backend instances. (클라이언트 인스턴스와 백엔드 인스턴스 둘 다 Google network 안에 있다)


<img width="927" alt="스크린샷 2020-02-01 오후 1 07 35" src="https://user-images.githubusercontent.com/26548454/73587386-5c59ea80-44fe-11ea-907c-24b4ef39e88d.png">

이 방식으로 internal load balancing supports 3 tier webService.
1. 외부 사용자와 연결하는 Global load balancer가 존재. 여기서 일단 모든 트래픽을 흡수한 뒤 사용자 지역에 맞는 region의 백엔드 서비스로 요청을 보낸다.
2. Backend region 내에 internal load balancer가 존재한다. (Application / internal tier)
3. last tier는 Database Tier (each of zones).

이런 시스템의 장점: database / application 둘 다 not exposed externally. Simplified security, network pricing

---
## Lab
2개의 managed instance group in same region을 만들고, instance group을 backend로 사용해서 internal load balancer를 작동시킬 예

VPC 네트워크에 subnet 2개인 네트워크 하나가 미리 생성되어 있음. Firewall rule에서 app-allow-http, app-allow-health-check 두 개를 만들어준다.

Instance template 먼저 생성해주고, 그 후에 instance group을 만들어준다.

cf. health check는 network service의 load balancing에서 생성하고 작업해줘야 한다


---
## Choosing a load balancer

<img width="927" alt="스크린샷 2020-02-01 오후 2 03 52" src="https://user-images.githubusercontent.com/26548454/73587388-5c59ea80-44fe-11ea-85cd-aed61ddeaba7.png">

1. IPv6 지원 여부.
HTTPS, SSL & TCP proxy load balancing services support IPv6 clients. 얘네만이 IPv6 사용하는 user의 request를 load balancer가 terminate한 뒤, proxy them over IPv4 to your backends. 

사진의 예시 : DNS에서 웹 도메인 주소가 각각 IPv4, IPv6로 대응되도록 만들어뒀다. 따라서 클라이언트가 어떤 주소를 쓰던 접속이 가능. 클라이언트가 v6를 쓰면 Load balancing 쪽에서 내부 백엔드 통신은 IPv4로 진행하고, 클라이언트에게 돌려줄 때는 IPv6로 통신할 수 있게 지원해준다.

2. Global vs Regional, External vs Internal, traffic type에 따른 구분.

<img width="924" alt="스크린샷 2020-02-01 오후 2 08 35" src="https://user-images.githubusercontent.com/26548454/73587398-7f849a00-44fe-11ea-8135-46bdfe399cf9.png">


외부 인터넷과의 통신 목적이면 왼쪽 상단에서부터 출발.
	- 트래픽 종류에 따라 구분한다. (HTTP(S), TCP, UDP)
	- TCP 사용  -> SSL / TCP proxy? Network load balancing service?
Regional 통신 목적이면 오른쪽 상단에서부터 출발.

<img width="923" alt="스크린샷 2020-02-01 오후 2 13 23" src="https://user-images.githubusercontent.com/26548454/73587399-7f849a00-44fe-11ea-8b0a-096e040270fe.png">


---
## Quiz
*Which of the following are applicable autoscaling policies for managed instance groups?*
- CPU 사용량
- Monitoring metrics
- Queue-based workload
- Load balancing Capacity
