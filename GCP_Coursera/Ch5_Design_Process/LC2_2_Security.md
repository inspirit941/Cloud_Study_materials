# Design for Security
## Overview

구글 내에서 제공하는 security service는 크게 세 개. 
* transparent, automatic -> encryption of data that automatically occurs when data’s transported and when it’s at rest.
* offer methods for customization -> using own encryption key 라던가
* 다 구현되어 있지만, 원할 때만 security service를 제공받을 수 있도록 설정.


## Cloud Security

<img width="926" alt="스크린샷 2020-02-11 오후 2 51 21" src="https://user-images.githubusercontent.com/26548454/74232724-bc297000-4d0c-11ea-9848-63c483dbb65f.png">


구글이 제공하는 security 범위는 어디까지인지, 어디서부터 design해야 하는지 알기 위한 차원.


<img width="924" alt="스크린샷 2020-02-11 오후 2 52 36" src="https://user-images.githubusercontent.com/26548454/74232731-c0ee2400-4d0c-11ea-9e3c-ed15fa1457a0.png">


- VPC : get completely isolated network.
- cloud interconnect : VPN이나 private interconnection -> to 3rd party or your on-premisese. 여기서도 Everything in private.
- 3rd party Virtual Appliance : security audit appliance that you can install. 
- Google load balancer and google Network itself.

여튼 구글 안으로 들어오면 상당한 수준의 security를 보장한다.

### Network Access Control and Firewalls


Locking down network access to only what’s required. (Boston host 시스템으로 external IP주소를 줄인다던지)


<img width="923" alt="스크린샷 2020-02-11 오후 2 57 17" src="https://user-images.githubusercontent.com/26548454/74232735-c21f5100-4d0c-11ea-8ff4-6fa436cd305e.png">


보통 Firewall이 1차 방어 저지선이다. Ingress / egress 각각에 맞게 instance를 제어할 수 있음. Permit / deny, sort priorities that we want to take (and completely distributed)


<img width="924" alt="스크린샷 2020-02-11 오후 3 35 05" src="https://user-images.githubusercontent.com/26548454/74232738-c2b7e780-4d0c-11ea-89b9-516fb95f8358.png">

그래서, VM의 Security를 세팅할 때는 간단하다. 인터넷에 직접 expose 시키지만 않으면 됨. Baston host 형태로 만들고, google cloud shell로 vm에 접근하면 된다.


<img width="924" alt="스크린샷 2020-02-11 오후 3 37 24" src="https://user-images.githubusercontent.com/26548454/74232865-f2ff8600-4d0c-11ea-96a0-a2b99af64237.png">


또 다른 방법으로는 API access control이 있다. Expose sth to the web through a protected API endpoint. 
-> Who has access utilizing 확인 가능, validating every single call with a json web token + google API keys.



### Protection against Denial of Service


구글 레벨에서도 어느 정도는 DoS 방어 시스템을 갖추고 있다. 
- No physical Routers -> no actual HW that could be overloaded 같은 것

이게 아니어도 구글 측에서 제공하는 서비스들이 있고, 사용자가 design 과정에서 해당 서비스들을 사용할 수 있다.

<img width="924" alt="스크린샷 2020-02-11 오후 3 42 13" src="https://user-images.githubusercontent.com/26548454/74232874-f72ba380-4d0c-11ea-8012-2199997fc119.png">



<img width="921" alt="스크린샷 2020-02-11 오후 3 42 57" src="https://user-images.githubusercontent.com/26548454/74232881-f85cd080-4d0c-11ea-866f-b0d27c6e1456.png">


구글의 방어법
1. Cloud CDN
Bandwidth -> cache a lot of important content at the edge using Google Cloud CDN.
2. Load balancer
-> UDP나 SYN flood 전부 차단함.
	SYN Flood 
	basically when a TCP connection is being established, you have to send a synchronization and then usually there’s an acknowledgement saying, “OK, now we’re ready to talk.” Well, sometimes you can just say, “Hey, I want to synchronize.” It’s like somebody knocking on the door, but nobody ever answers. So you just keep pounding and pounding and pounding and no other services can actually connect.


<img width="922" alt="스크린샷 2020-02-11 오후 3 46 16" src="https://user-images.githubusercontent.com/26548454/74232883-f8f56700-4d0c-11ea-875d-689b21a61621.png">

즉 네트워크 레벨에서 DDoS 등의 공격을 상당부분 막아낼 수 있음. Load balancer와 Firewall을 전방에 배치하면 됨. 오히려 까다로운 건 한 번에 몰아치는 공격이 아니라, 서서히 늘어나는 식의 공격이다. 진짜 사용자 트래픽인지 헷갈리기 때문


<img width="919" alt="스크린샷 2020-02-11 오후 3 48 27" src="https://user-images.githubusercontent.com/26548454/74232885-f98dfd80-4d0c-11ea-87c7-b9d386703632.png">


Infra level에서의 방어법. 이 모든 방어를 뚫었다면, autoscaling으로 대응한다. Add more resources, split it btwn different regions. 예컨대 미국에 서버를 뒀는데 아시아에서 공격이 온다? -> spin up a region in Asia로 absorb the traffic.


### Resource sharing and isolation

구글이 제공하는 Network topology는 여러 종류가 있음. The least secure design은 everything is in a single failure domain, all parts communicate and depend directly on one another. 이외에도 separating the parts, providing more private 할 수 있는 기능을 제공.


* Sharing : enable collaboration between parts.
* Isolation : prevents the compromise of one part from spreading to the other.


<img width="924" alt="스크린샷 2020-02-11 오후 7 28 50" src="https://user-images.githubusercontent.com/26548454/74232888-fa269400-4d0c-11ea-8ee4-21a71866275c.png">


1. Isolating through VPC.

통신해야만 하는 두 project가 있을 때, isolate two networks from each other. 두 개의 네트워크는 완전히 독립이며, 따라서 own IAM, Private IP space, private security Mechanism을 가지고 있음. 상대방의 네트워크에 접근하거나 통신할 수는 있지만, authentication이 있어야 함.



<img width="925" alt="스크린샷 2020-02-11 오후 7 31 50" src="https://user-images.githubusercontent.com/26548454/74232979-2fcb7d00-4d0d-11ea-8039-c622078c176a.png">


2. Isolation using VPN tunneling

이 경우, 두 개의 네트워크 사이에 encrypted link를 만들어둔다. Cloud건 on-premises건 상관없음. Project 간 통신을 하려면, they can use another private IP address subnet space to increase the privacy, and the encrypted communication btwn the two.

물론 encrypted communication은 기본적으로 제공되는 기능이지만, 여기서는 more granular control over encryption이 가능하다는 점 정도?


<img width="924" alt="스크린샷 2020-02-11 오후 7 38 03" src="https://user-images.githubusercontent.com/26548454/74232987-34903100-4d0d-11ea-8a49-1463d19e5526.png">


3. Cross-Project VPC network peering.

Directly connect 2 projects together using a private IP address. 


<img width="925" alt="스크린샷 2020-02-11 오후 7 39 11" src="https://user-images.githubusercontent.com/26548454/74232990-3528c780-4d0d-11ea-8990-8fb36b65a578.png">

예시. Contracting with an outsourcing firm who’s developing itself, but you don’t want to give their users access to your project.

Organization 끼리 통신할 수 있도록 만들어놓고, IAM으로 detailed control 작업을 하는 것.



<img width="925" alt="스크린샷 2020-02-11 오후 7 41 41" src="https://user-images.githubusercontent.com/26548454/74232995-35c15e00-4d0d-11ea-8c7e-71bc9ae2d9b1.png">


4. Shared Private Cloud

하나의 Organization 안에 여러 개의 VPC를 만들어놓는 것. 각각의 VPC는 cross-project networking으로 통신하는 구조. Shared VPC에 해당하는 프로젝트를 하나 만들고, 해당 프로젝트는 VPC 간 통신을 전담하게 하는 구조라고 보면 된다.

-> single server provider that need to provide access to different projects. 인터넷 통하지 않고 통신하는 방법으로 사용.




<img width="923" alt="스크린샷 2020-02-11 오후 7 49 13" src="https://user-images.githubusercontent.com/26548454/74232999-36f28b00-4d0d-11ea-9fba-68b4714bc022.png">

그 외에도 Virtual NICs 기반으로 isolation하는 것도 가능하다. 각각의 VM instance는 최대 8개의 NICs를 handle할 수 있음. NIC가 있다는 건, have a private subnet that’s connected to them. 데이터는 one subnet에서 받고 통신은 another와 하는 등의 작업이 가능. “Kind of like a DMZ”



<img width="923" alt="스크린샷 2020-02-11 오후 7 52 21" src="https://user-images.githubusercontent.com/26548454/74233001-36f28b00-4d0d-11ea-8a97-26aa1ae99a0d.png">

GCP service를 internal IP로 접근하는 것도 가능함. With private networking, you can enable a private Google Cloud Access -> you never have to expose your services to the public internet.

VPC를 처음 생성할 때 private Google Access 설정을 활성화하면 된다.


### Data Encryption and Key Management


구글이 제공하는 bulit-in key management를 사용하거나, provide your own key. Sensitive Data라면 add your own encryption method 적용도 가능하다.


<img width="924" alt="스크린샷 2020-02-11 오후 7 56 58" src="https://user-images.githubusercontent.com/26548454/74233003-378b2180-4d0d-11ea-9a27-e55f67216f95.png">


Server side encryption은 이미 제공한다. Connection이 HTTPS로 이루어지고 HTTPS load balancer를 적용했다면, we’ve got encryption that’s communicating btwn any cloud services / any applications.

(key는 메모리에 저장되었기 때문에, nothing is actually being stored on the applications)

 
<img width="924" alt="스크린샷 2020-02-11 오후 8 01 14" src="https://user-images.githubusercontent.com/26548454/74233005-3823b800-4d0d-11ea-8cf9-2ba85555da0d.png">


구글이 key 관리하는 거 원하지 않는 사람들을 위한 기능.

<img width="919" alt="스크린샷 2020-02-11 오후 8 06 46" src="https://user-images.githubusercontent.com/26548454/74233097-673a2980-4d0d-11ea-9937-b00a83d1a147.png">


사용자가 제공하는 key는 GCP에서 메모리에 올려 사용할 뿐 저장하지 않는다.


<img width="924" alt="스크린샷 2020-02-11 오후 8 08 17" src="https://user-images.githubusercontent.com/26548454/74233094-66a19300-4d0d-11ea-8fe0-6d2bff12f612.png">

Persistent Disk, Client side encryption 등에도 지원한다.


### Identity Access and Auditing

구글은 IAM으로 access to resource를 관리한다.

<img width="923" alt="스크린샷 2020-02-11 오후 8 13 42" src="https://user-images.githubusercontent.com/26548454/74233091-6608fc80-4d0d-11ea-8c71-d8b49fadb719.png">

- Policy inheritance : organization level에서의 설정은 그 아래 모든 resource에 적용된다.

Who does what, to what resource를 규정할 수 있음.
* primitive roles : basically full access. Read, Write, View only, billing 네 개. Control everything이라는 점에서는 oversimplified.

custom rule을 만드는 걸 추천함.

Higher level에서 허용한 건 그 아래 level의 설정으로 override (기각) 할 수 없게 되어 있음.




<img width="930" alt="스크린샷 2020-02-11 오후 8 19 14" src="https://user-images.githubusercontent.com/26548454/74233090-64d7cf80-4d0d-11ea-9067-70ba0dbe4e82.png">


권한을 부여할 대상이 사람이 아닐 수 있음. 그 때 사용하는 게 Service Account. 가능하면 service account로 관리하는 걸 추천. Service Account도 마찬가지로 key 관리 (key rotation policy) 라던가, auditing for service account 등등. 특히 key는 주기적으로 rotation 해줘야 한다.



Auditing으로는 오픈소스인 Forseti도 사용 가능하고, Cloud Audit logging 도 사용 가능하다.


<img width="923" alt="스크린샷 2020-02-11 오후 8 23 08" src="https://user-images.githubusercontent.com/26548454/74233087-643f3900-4d0d-11ea-8323-7f0466638065.png">


read-only log that are unchangeable을 남겨놓는다. Track admin activity and data access 가능함. 최대 30일까지 로그 저장.



<img width="923" alt="스크린샷 2020-02-11 오후 8 25 23" src="https://user-images.githubusercontent.com/26548454/74233080-5f7a8500-4d0d-11ea-91c9-b4024a7fde20.png">

이런 것도 있다고 함.
