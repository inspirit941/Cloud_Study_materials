## Computing & Networking

### Computing

#### EC2 

<img width="1049" alt="스크린샷 2023-04-08 오후 1 18 47" src="https://user-images.githubusercontent.com/26548454/230702896-0a53b7df-ddee-41ad-bad7-48d565731eb4.png">
<br>

EC2 : Elastic Compute as a Service.
- AMI (Amazon Machine Image) : how you want your image to be configured.
  - OS, pre-installed application
  - launch permission
  - block device mapping 등등
- 하나의 AMI 설정을 활용해서 같은 종류의 EC2 Instance를 여러 개 발급받아서 사용할 수 있다.
- AMI preDefined Spec은 AWS 외에도 Community에서 지정한 것들이 있으며, AWS Marketplace에서 확인할 수 있다.

<br>

| Instance Family | Description | Use Cases |
| --- | --- | --- |
| General purpose | Provides a balance of compute, memory, and networking resources, and can be used for a variety of workloads. | Scale-out workloads such as web servers, containerized microservices, caching fleets, distributed data stores, and development environments. |
| Compute optimized | Ideal for compute-bound applications that benefit from high-performance processors. | High-performance web servers, scientific modeling, batch processing, distributed analytics, high-performance computing (HPC), machine/deep learning, ad serving, highly scalable multiplayer gaming. |
| Memory optimized | Designed to deliver fast performance for workloads that process large data sets in memory. | Memory-intensive applications such as high-performance databases, distributed web-scale in-memory caches, mid-size in-memory databases, real-time big-data analytics, and other enterprise applications. |
| Accelerated computing | Use hardware accelerators or co-processors to perform functions such as floating-point number calculations, graphics processing, or data pattern matching more efficiently than is possible with conventional CPUs. | 3D visualizations, graphics-intensive remote workstations, 3D rendering, application streaming, video encoding, and other server-side graphics workloads. |
| Storage optimized | Designed for workloads that require high, sequential read and write access to large data sets on local storage. They are optimized to deliver tens of thousands of low-latency random I/O operations per second (IOPS) to applications that replicate their data across different instances. | NoSQL databases, such as Cassandra, MongoDB, and Redis, in-memory databases, scale-out transactional databases, data warehousing, Elasticsearch, and analytics. |


AMI에서 정의한 설정 외에도 하드웨어나 네트워크 리소스 관련한 선택지도 있다. 애플리케이션 종류에 따라 적절한 타입을 선택할 수 있음. 공식문서에서 확인할 수 있다.
- Compute-optimized / Memory-optimized / Storage-optimized 등
- i.e. G instance는 Graphic intensive application을 위한 서버.
- M5 General instance는 balanced resource 제공. Web server처럼 리소스 사용비율이 비슷한 경우 적합

<img width="1043" alt="스크린샷 2023-04-08 오후 1 26 20" src="https://user-images.githubusercontent.com/26548454/230703055-3a9b461a-eb34-4428-997a-390e3cd1c100.png">

- Instance Type: Hardware capability
- Instance size: 해당 인스턴트의 리소스 양.

instance type을 선택하고, 성능을 확인한 뒤 필요하다면 다른 타입의 인스턴스로 교체하는 식으로 운용할 수 있다.
- instance Resize도 Web UI / API 방식으로 지원하고 있다.

##### Lifecycle


<img width="1048" alt="스크린샷 2023-04-08 오후 1 38 43" src="https://user-images.githubusercontent.com/26548454/230703402-5a6fa620-0f3a-4cd7-aa2b-11b2c384e42a.png">
<br>

사용자가 AMI configuration으로 EC2 생성을 요청하면
- Pending: VM booting up. boot 끝나면 Running으로 변경
- Running: 비용 청구가 시작되는 지점. 
  - rebooting: 서버 재시작.
  - stopped: 서버 정지. powering down laptop과 비슷한 개념. 서버를 start하면 pending 상태로 돌아간다.
  - stop-hibernate: stop 상태와 일치하지만, boot up sequence 없이 바로 Running으로 전환될 수 있는 상태. 현재 상태가 메모리에 그대로 남아 있기 때문.
  - Terminated: 할당받은 서버를 제거함. 모든 리소스가 할당 해제됨.
    - 실수로 terminate 요청을 보냈을 때를 대비해서, AWS Console에서 잠시 동안은 visible 상태를 유지한다.


<br>
<img width="1044" alt="스크린샷 2023-04-08 오후 1 57 56" src="https://user-images.githubusercontent.com/26548454/230703944-262d23ae-fa01-46ef-911d-422e988bffb0.png">
<br>

데이터 유실 때문에 Termination 기능을 너무 두려워할 필요 없다.
- 기존에 할당받은 instance가 OS update / application dependency patch 등의 작업이 필요할 경우, 서버에 접근해서 inplace update 작업을 수행할 수도 있지만
- '문제가 해결된 새 인스턴스를 받고, 에플리케이션을 설치해서 구동한 뒤 old instance를 삭제' 로도 해결할 수 있다.

<br>

비용: EC2가 Running state인 것 / hibernate를 위한 stopping 상태일 때.
- 즉, 안 쓰는 인스턴스를 stop 처리하면 비용이 나가지 않는다.


#### Container Service on AWS


<img width="1051" alt="스크린샷 2023-04-08 오후 2 09 09" src="https://user-images.githubusercontent.com/26548454/230704387-76b5a2b2-4822-4dce-b012-d2e473e963e7.png">
<br>

Container image를 scalable하게 운영하고 싶을 경우
- AWS ECS (Elastic Container Service)
- AWS EKS (Elastic Kubernetes Service)

둘 다 Container Orchestration Tool. managing your own container service.

<br>

![_ihG6qHQT-yZDxIWFNrDSg_0173e688f8524deaafdbb3530d7018f1_image](https://user-images.githubusercontent.com/26548454/230704955-ca2a7a75-82cc-4f1f-90aa-4e4f43a184ba.png)
<br>

ECS: End-to-end container orchestration service
- quickly spin up new container
- manage them across a cluster of EC2 instances.

AWS ECS container agent를 EC2 instance에 설치.
- agent: cluster management를 위해 ECS service와 통신할 수 있는 오픈소스.
- EC2에 ECS agent가 설치된 인스턴스를 Container instance라고도 한다.
<br>


Underlying OS나 Container가 떠 있는 instance 관리조차도 필요 없다면 
- AWS Fargate. serverless compute platform for ECS & EKS.

<br>

Container는 VM보다 bootup time이 짧다.
- increasing service Demand에 보다 빠르게 반응하기 위해서는 EC2보다 적합한 솔루션일 수 있음.


#### Serverless

<img width="1043" alt="스크린샷 2023-04-08 오후 2 57 42" src="https://user-images.githubusercontent.com/26548454/230705978-f5d7572e-96d6-4b1f-bdd7-859236040af6.png">
<br>

EC2를 사용한 ECS나 EKS를 사용할 경우, EC2 인스턴스를 관리하는 건 서비스를 쓰는 사용자가 담당해야 한다.
- Application SW / Security Patch 작업
- Scale of instances
- Architecting to be hosted in HA manner.
  - Deploying instances across at least 2 AZs.
  - 등등..

자유도가 높긴 한데, 모든 애플리케이션이 이 정도의 인프라 자유도가 필요한 건 아님. 비즈니스 로직에 집중하고 underlying heavy things는 managed solution으로 처리하고 싶은 사용자가 있다.
- 이들을 위한 용어가 **serverless**. 사용자가 underlying infrastructure에 접근할 수 없음.
- provisioning, scaling, fault tolerance, maintenance를 service provider가 해주는 것.


##### AWS Fargate

<img width="1055" alt="스크린샷 2023-04-08 오후 3 01 01" src="https://user-images.githubusercontent.com/26548454/230706098-45665884-8754-4c73-912d-99bea34333f0.png">

<img width="1047" alt="스크린샷 2023-04-08 오후 3 01 12" src="https://user-images.githubusercontent.com/26548454/230706099-7a09a36c-acf2-4f00-a254-6f95cbc8481b.png">

Fargate: Managed Serverless compute platform for containers.
- ECS와 EKS 자체는 underlying EC2 instance managing까지 제공하는 서비스.
- Containerized Application을 배포할 수 있는 선택지로 EC2 instance 대신 Fargate service를 사용할 수 있음.
  - scaling / fault tolerance 기능이 내장되어 있음. 
  - underlying OS / Environment 사용할 필요 없음.
  - Application content, networking, storage, scaling requirement만 정의하면 된다.

<br>
<img width="1053" alt="스크린샷 2023-04-08 오후 3 14 12" src="https://user-images.githubusercontent.com/26548454/230706536-5c5f8b04-f440-4d1e-aac4-d5a8dc65ebde.png">
<br>

1. Build your Container Images / Push into Registry.
2. 해당 이미지를 배포할 때 사용할 CPU / Memory 리소스를 정의한다. ECS면 instance 리소스이고, EKS면 pod resource.
3. 컨테이너가 사용한 vCPU, Memory, Storage에만 비용이 청구된다.
   - Spot instance / compute savings plan 옵션 제공

Fargate는 일반적인 Container Usecase에 활용 가능
- MSA architecture Application
- batch processing
- ML Applications
- Migrating on-prem application to the cloud


##### Lambda

<img width="1045" alt="스크린샷 2023-04-08 오후 3 20 18" src="https://user-images.githubusercontent.com/26548454/230706734-3d7cb79e-d87a-4193-87f4-32014ef580bf.png">
<br>

- package / upload your code to the lambda
- lambda functions
- create a trigger that controls when the lambda functions invoke.

함수는 managed environment에서 실행되며
- Autoscale - trigger로 들어오는 request amount에 맞게 functions scale out 
- High Available
- maintenance of environment is done by AWS
- timeout: 15 min

사용자는 
- CPU / Memory 요구사항
- 함수가 실행되기 위한 permissions / dependencies 설정.

Long batch Job이나 Deep Learning에는 부합하지 않음.
- Web Backend handling request 
- backend report processing service
- microservice hosting

함수가 실행될 때만 1ms interval 단위로 측정해서 비용을 산정.


## Networking

<img width="1041" alt="스크린샷 2023-04-08 오후 3 52 06" src="https://user-images.githubusercontent.com/26548454/230707813-65746db6-095c-49e8-91e9-617113cbc284.png">
<br>

예시로 소개한 간단한 서비스 구조에서, EC2 instance를 배포하려면 해당 서버가 어느 네트워크에서 동작할지를 선택해야 한다.
- 어떤 네트워크를 선택하고 어떤 설정을 부여하는지에 따라 incoming internet traffic을 받을 수 있게 됨.
- AWS는 각 region별로 default VPC를 생성해준다.
  - default VPC는 인터넷 접근이 가능하므로, 외부 노출하면 안 되는 민감한 서비스일 경우 사용자가 좀더 신중해야 한다.
- VPC 관련 설정은 EC2-Related Service에만 해당함. Lambda 같은 경우는 Network 관련 고민이 아예 필요없다.
  - 하지만 VPC는 Architecture 설계할 때 근간이 되는 개념이므로, 알고 가는 게 좋다.

### AWS VPC

<br>
<img width="1040" alt="스크린샷 2023-04-08 오후 4 01 40" src="https://user-images.githubusercontent.com/26548454/230708178-f8c20249-13bd-49dc-8ff1-c74d475bab0d.png">
<br>

VPC는 application과 underlying resource를 외부로부터 격리하는 역할.
- 사용자의 허가 없이는 incoming / outgoing traffic 둘 다 불가능하다.

<img width="1057" alt="스크린샷 2023-04-08 오후 4 03 58" src="https://user-images.githubusercontent.com/26548454/230708242-d8e5c8af-e25f-46a6-8375-212a9a303e9e.png">

VPC를 생성할 때 필요한 두 가지 input
- Region : AWS Console의 global navBar 오른쪽 상단에서 선택 가능
- IP Range (CIDR format) : Create VPC 화면에서 input으로 추가할 수 있음.

<br>

![스크린샷 2023-04-08 오후 6 20 33](https://user-images.githubusercontent.com/26548454/230713919-15d5e71c-c88c-484c-b791-a9d7ae0f5ab6.png)
<br>

subnet: VPC 안에 resource (i.e. EC2 instance)를 할당할 segment
- granular control over access to your resources.
  - 예컨대 외부 인터넷에 연결되어야 하는 애플리케이션이 있다면, internet connectivity를 활성화한 subnet에 EC2 instance를 추가하는 식.
  - DB처럼 외부와 직접 연결될 필요가 없는 서비스는 private subnet에 생성하는 식.
- subnet 생성에는 세 가지 input이 필요하다.
  - VPC: subnet을 생성할 공간
  - AZ: Availability Zone. 예시의 경우 A zone (us-west-2a)
  - CIDR range : 할당할 ip 대역

<br>

![스크린샷 2023-04-08 오후 6 28 20](https://user-images.githubusercontent.com/26548454/230714181-d15c95c5-cf24-46f2-b063-3f8e794a6813.png)
<br>

기본적으로, 같은 VPC에 포함되어 있는 리소스만 서로 통신이 가능하다.
- 인터넷 통신을 하려면 Internet Gateway와 VPC를 연결해야 함.
- Internet Gateway를 생성하고, VPC에 attach해야 적용된다.

![스크린샷 2023-04-08 오후 6 27 06](https://user-images.githubusercontent.com/26548454/230714154-5a2c3366-d9f3-45e7-9291-7ed7c7a83556.png)
![스크린샷 2023-04-08 오후 6 27 36](https://user-images.githubusercontent.com/26548454/230714158-60c1725a-d13c-47f8-aa4f-1f932605c688.png)
<br>

- AWS Web Console로 붙일 수 있음.

<br>

![스크린샷 2023-04-08 오후 6 31 17](https://user-images.githubusercontent.com/26548454/230714321-8fe5374e-ed69-4c1b-bb43-0fa9b4996fa1.png)
<br>

Virtual Private Gateway (VGW): AWS에 올라간 리소스가 public internet 말고 on-prem에서만 접근 가능하도록 만들 때 사용하는 컴포넌트.
- 암호화된 VPN Connection을 제공함.

![스크린샷 2023-04-08 오후 6 33 09](https://user-images.githubusercontent.com/26548454/230714401-b098a394-fcc4-4af6-b6ed-ce1644543f3b.png)
<br>

High Availability를 위해서는 최소 두 개의 AZ zone에 동일한 subnet 설정을 해두는 것이 좋다.
<br>

![fC4DaI4uRuCRtkolNtRUSA_2ceb6c8eeddf4ffba7175739502a34f1_image](https://user-images.githubusercontent.com/26548454/230714454-959e25da-f0f0-4ab4-82e6-d94e555d37f9.png)
<br>

Reserved IP: 각각의 subnet에서 AWS가 특정 목적을 위해 사용하는 고유 ip.
- 예컨대 10.0.0.0/22 -> 총 1024개의 ip주소.
  - subnet 4개를 구성하면, 각각의 subnet에는 256개의 ip가 할당된다.
  - 이 중 5개는 AWS에서 기본으로 사용함. 
  - 따라서, 하나의 subnet에서 사용자가 쓸 수 있는 ip주소는 총 251개.



#### VPC Routing

![스크린샷 2023-04-08 오후 6 45 15](https://user-images.githubusercontent.com/26548454/230714765-09948de3-64b2-4d77-8180-71f1ab2d908b.png)
<br>

VPC에 multiple Subnet 구축하고 internet gateway 붙인 뒤 애플리케이션까지 띄웠다. 
- 사용자가 애플리케이션에 접근하면, 인터넷으로 접근할 수 있는 subnet 중 사용자 애플리케이션에 정확히 도달하도록 설정해야 함.
- AWS는 Route table을 제공함.
  - Route table: set of routes (rules) where the network traffic is directed.
  - Subnet level / VPC level 설정 가능.
<br>

![스크린샷 2023-04-08 오후 9 03 33](https://user-images.githubusercontent.com/26548454/230720062-4fdb9a38-8c68-4a09-9d85-eeb63c172b1a.png)
<bR>

VPC를 최초로 생성하면, AWS에서 main Route table을 자동으로 만들어준다.
- VPC 간 통신은 Local로 정의됨. = 외부 통신이 불가능하고 Subnet 간 통신이 가능한 이유. Subnet 간 통신은 local 통신과 동일하게 간주한다.

<br>

![스크린샷 2023-04-08 오후 9 04 04](https://user-images.githubusercontent.com/26548454/230720105-ed7eca02-772d-47fe-b08c-340e7f3942c3.png)
![스크린샷 2023-04-08 오후 9 04 17](https://user-images.githubusercontent.com/26548454/230720108-df0c63c3-69c2-4d40-beb9-f3cb153894a0.png)
<br>

AWS Console로 확인해보면, table을 선택했을 때 routes에 Target: Local로 정의된 필드 하나만 확인된다.

<br>

![스크린샷 2023-04-08 오후 9 31 11](https://user-images.githubusercontent.com/26548454/230721199-6ef48017-6f46-4098-95ea-7f67ec446c8e.png)
<br>

subnet이 public internet 접근이 가능한지 아닌지는 route table에 internet gateway <-> subnet 연결이 있느냐 없느냐로 결정된다.
- 따라서 custom route table을 생성하고
  - subnet 간 통신을 허용하는 local은 자동 생성되며
  - public subnet과 internet gateway를 연결하는 Routing table 필드가 필요하다 (igw-id)

![스크린샷 2023-04-08 오후 9 32 14](https://user-images.githubusercontent.com/26548454/230721265-d8fba815-a0f9-419a-a06d-dbb89776494b.png)
![스크린샷 2023-04-08 오후 9 32 27](https://user-images.githubusercontent.com/26548454/230721266-b108a768-5a85-4d91-bd6c-7df71c57094a.png)
![스크린샷 2023-04-08 오후 9 32 56](https://user-images.githubusercontent.com/26548454/230721267-755e504d-3e71-409a-83c7-221ce2441c40.png)

- 새로운 route table을 생성하고
- Edit table에서 internet gateway를 추가한다.
  - Destination의 0.0.0.0/0 은 어디서든 트래픽을 받겠다는 뜻
  - internet gateway 선택

route table은 적용되었고, 이 중 특정 subnet에만 internet access를 허용하고 싶으면

![스크린샷 2023-04-08 오후 9 38 22](https://user-images.githubusercontent.com/26548454/230721503-56faad5f-d3ee-4c71-abea-eb48d78f8f1b.png)
![스크린샷 2023-04-08 오후 9 38 36](https://user-images.githubusercontent.com/26548454/230721506-744e6383-1185-4d78-a4f3-7d2341dceb54.png)

<br>

- Association을 선택하고
- Public subnet이라고 명명한 subnet에 association 추가하면 된다

설정 최종 결과본은 아래와 같다.

![스크린샷 2023-04-08 오후 9 40 17](https://user-images.githubusercontent.com/26548454/230721574-62a12c56-37e7-43ff-b25d-9289d49c5096.png)

<Br>

#### VPC Security


서비스를 internet에 연결해서 트래픽을 받게 되면, 외부로부터 들어올 수 있는 risk에 대비해야 한다. 
<br>

AWS에서 VPC Security를 제공하는 방법은 크게 두 가지.
- Network Access Control List (Network ACLs)
- Security Groups

<br>

![스크린샷 2023-04-08 오후 9 51 11](https://user-images.githubusercontent.com/26548454/230722159-b1e90187-d415-4337-b70a-46e281be7c75.png)
<br>

##### Network ACL

Subnet 단위의 firewall로 이해하면 됨.
- inbound / outbound로 구분되며, 인터넷에 연결되었을 경우 보통 inbound / outbound 둘 다 설정해줘야 한다.
- stateless
- Everything is allowed by default. 


![스크린샷 2023-04-08 오후 9 51 25](https://user-images.githubusercontent.com/26548454/230722216-f0d8910a-999d-41ab-a85f-0cb866c07918.png)
![스크린샷 2023-04-08 오후 9 51 35](https://user-images.githubusercontent.com/26548454/230722220-514819d0-1ed1-429b-9249-2cce58ec2597.png)
![스크린샷 2023-04-08 오후 9 52 02](https://user-images.githubusercontent.com/26548454/230722222-7faeb0ad-bd0e-4cc9-9165-43cc9cf858b4.png)

<br>

##### Security Group

![스크린샷 2023-04-08 오후 9 55 00](https://user-images.githubusercontent.com/26548454/230722291-73f0de48-9018-4b62-a83b-47f7b1f920ca.png)
<br>

EC2 instance 단위의 firewall로 이해하면 됨.
- Not Optional. 즉 EC2 instance를 생성할 때 security group을 반드시 지정해주게 되어 있음.
- VPC에서 security group을 새로 생성하면, inbound traffic는 전부 Deny, outbound traffic은 전부 allow.
- Security Group의 경우 inbound만 정하면 outbound는 따로 지정하지 않아도 자동 적용된다.
- stateful. connection이 외부로부터 요청이 와서 맺어진 건지 / EC2가 외부로 요청을 보내서 맺어진 건지 알고 있기 때문. 따라서 incoming traffic이 들어오면, 그에 대응하는 outbound traffic은 허용하는 방식으로 되어 있다.

![스크린샷 2023-04-08 오후 9 55 39](https://user-images.githubusercontent.com/26548454/230722330-110449bf-ea0e-44a1-8dd7-ac324d0a85ff.png)
![스크린샷 2023-04-09 오전 12 40 04](https://user-images.githubusercontent.com/26548454/230730269-7b3eb9c6-fc2d-46c8-85f4-78bc9522a31c.png)


- network acl은 default allow이므로, 보통은 security group을 사용해서 특정 애플리케이션이나 인스턴스의 access restrict를 구성하는 편.
- fine-grained control을 적용하려면 ACL에 layer를 추가하는 식으로 사용한다.


##### Hybrid Connectivity with AWS


지금까지의 설명은 모든 리소스가 전부 AWS 내부에 있을 때 적용되는 것. on-prem과 AWS Cloud 간 통신이 필요하면?
- AWS VPN: 많이 쓰이는 방법. 크게 두 가지 방식이 있다.
  - Site-to-Site VPN: DataCenter를 AWS VPC에 연결하려 할 때 쓰임.
  - AWS Client VPN: Administer를 AWS / Data Center에 연결할 때 쓰임. 개발자 개인 노트북에 VPN 연결해서 회사 리소스에 접근할 수 있는 것과 비슷한 원리
- AWS VPN을 사용해서 virutal private gateway와 통신. 

Virtual Private Gateway: on-prem DataCenter와 VPN or AWS Direct Connect라는 서비스를 통해 통신할 수 있도록 하는 DoorWay

<br>
<img width="1076" alt="스크린샷 2023-04-09 오후 12 36 24" src="https://user-images.githubusercontent.com/26548454/230752803-99f2507d-e1cd-4da3-b69e-78eff91cf32a.png">
<br>

AWS Direct Connect: hosted private connection to AWS through a Direct Connect Delivery partner or AWS
- on-prem DataCenter와 AWS 사이에 private, Dedicated Connection을 제공함.
- Regular Open (Public) internet 방식이 아님. traffic이 AWS Global Network을 타고 전달됨.
  - 인터넷 사용 시 발생할 수 있는 병목현상이나 latency 변동성을 낮춤.
  - public internet 대비 Larger / Reliable Throughput 제공. 따라서 트래픽 규모가 크거나 전송할 데이터양이 많을 경우 권장

