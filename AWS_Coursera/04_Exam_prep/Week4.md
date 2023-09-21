## Design Cost-Optimized Architecture

### Cost-Optimized Storage Solutions

![스크린샷 2023-09-18 오후 9 10 53](https://github.com/inspirit941/inspirit941/assets/26548454/c0bcc7c4-905c-47c7-92d5-e2593fff5ee9)
<br>

이전까지 배웠던 services를 토대로, 요구사항에 적합한 service를 선택했을 때 cost-optimizing하는 방법.
- EBS volume이라면, 적절한 크기의 storage 선택해야 함. not over-provisioning

![스크린샷 2023-09-18 오후 9 22 50](https://github.com/inspirit941/inspirit941/assets/26548454/0f051969-23fa-4329-8c84-89f6b730b2d2)
<br>

- locally attached ephemeral storage: lowest compute-related cost storage options
  - EC2 instance에 붙어 있음. hourly rate.
- EBS with EC2 instance: block-level persistent storage
  - backup / migration을 위한 snapshot 기능.
  - GP2 instance: IOPS bursting 특화
  - 안쓰는 EBS volume은 삭제해야 비용 절감됨
- S3: low cost, accessible globally, durability, no limit, lifecycle policy / different storage class 제공

![스크린샷 2023-09-19 오후 7 46 48](https://github.com/inspirit941/inspirit941/assets/26548454/25e2479e-f023-4997-aecc-664b065c89d7)
<br>

cost optimization을 위한 visibility. 사용량과 비용 측정하기.
- CloudWatch -> track your metrics, turn on alarms to immediate take actions
- Trusted Advisor -> AWS Well-Architected Framework tools
- Cost Explorer...

핵심은 Define your metrics, Set Target Goals, Define & Enforce your tagging strategy, Use Cost Allocation tools.
- how do you use cost allocation tags? 사용예시?
  - filter views in Cost Explorer

AWS Cost management tools for high-level usage? cost explorer / cost and usage reports?
- Cost Explorer로 high-level view, drill down specific.
- Cost and Usage Reports는 과금 기준과 단위를 세분화해서 보여줌. hour, day, month, product, resource tags, etc.
- billing alarm, free tier alarms, alarms with AWS budget 등의 기능도 활용할 수 있다.

AWS Organization / Control Tower: centrally manage billing, control access, compliance, security, shared resources.

![스크린샷 2023-09-20 오전 11 05 17](https://github.com/inspirit941/inspirit941/assets/26548454/aed1774f-7f00-4811-af40-df1522db34ad)
<BR>

AWS Autoscaling, 특히 EC2 autoscaling 활용한 cost optimization.
- Trusted Advisor가 underutilized EBS Volume 를 찾아서 최적화를 도와준다.

EBS cost optimization
- how many IOPS you're using / how many IOPS you're paying for 비교하기.
- type은 용도에 맞지만, 사용량보다 capacity가 높은 volume을 쓰고 있다면 초과비용 발생 중임

lifecycle rule: 필요없는 데이터는 일정 기간이 지난 후 자동 삭제
- AWS Data Lifecycle Manager / Backup: old EBS volume 또는 백업본 삭제하는 기능.

S3 Optimization: different storage class 사용하기. 가격차이를 알 것까지는 없지만, storage tier class별 차이는 알아야 함 (retriveal cost)
- S3 Lifecycle Configuration: automatically transit all objects in a bucket, based on a period of time.
- Intelligent Tiering: access pattern에 따라, 각각의 object를 most efficient cost-effective access tier로 변경.
- 만약 Requester pays bucket 설정하면, S3에서 데이터 request / download 하려는 사용자가 비용을 지불하도록 만들 수 있다. (보통은 S3 bucket owner가 pay for it.)
  - requester pays bucket for storage, transfer, usage 설정하면 됨.

Data Migration Cost Optimization for hybrid Environments
- DataSync, SnowFamily, Transfer Family, Storage Gateway
- 예컨대 250TB 데이터를 S3로 옮긴다면.. Snowball 사용을 권장.

Data transfer cost minimize의 경우 
- CD (cloudFront) 로 cache
- Dedicated network links from on-prem to AWS, with Direct Connect

### Walkthrough question 4.1

![스크린샷 2023-09-20 오후 12 18 14](https://github.com/inspirit941/inspirit941/assets/26548454/c3de2151-13f3-459e-9e99-8d45610a52f0)
<br>

Answer: B. FSx는 fully-managed Microsoft Windows file system. no upfront HW / SW costs.
- A: S3 File Gateway는 S3에 File interface를 지원하는 것. Authenticate with Active Directory on the on-prem side를 지원하지만, object가 S3에 저장된 이후에는 지원하지 못함.
- C: EFS는 Linux-based workload용. windows는 지원하지 않음
- D: S3는 object level storage. 굳이 쓴다면 backup storage. 그러나 S3 bucket을 EC2 instance에 마운트할 수는 없다.


### Design Cost-optimized Compute solutions

![스크린샷 2023-09-20 오후 8 28 55](https://github.com/inspirit941/inspirit941/assets/26548454/08bce922-c533-4ede-89ec-2cf33396ee6c)
<br>

EC2의 다양한 Pricing options / other compute service that meets requirements.
- EC2의 경우
  - spot instance: 서버 할당과 반납이 임의로 이루어져도 괜찮은 stateless web server, batch processing 또는 using HPC / big data
- data transfer cost 줄이는 cloudfront
- licensing cost 줄이기 위한 Aurora / RDS

![스크린샷 2023-09-20 오후 9 34 22](https://github.com/inspirit941/inspirit941/assets/26548454/877cdeff-9a80-49fb-9ec9-39cd6e732f11)
<br>

instance size, correct type 선택하는 게 출발점.
- compute optimized / memory optimized
- hybrid options - Outpost, Snowball Edge
  - 예컨대 AWS managed services on Outpost
    - charged based on usage by instance hour
    - excludes underlying EC2 instance / EBS storage charges
  - Edge computing combines geography / networking to bring computing closer to end user.
    - 예컨대 IoT로 business logic을 Remote로 실행할 때...  
    - 이 경우에는 data center나 server managing하면서 비용 절감하는 방향으로 가면 안 됨.

increase elasticity; only use resources when those resources are needed. (pay-for-what-we-use model)
- autoscaling
- CloudFormation template, managed by tags

choosing the right price model
- EC2의 different pricing models; On-demand, Saving plans, Reserved instances, Spot instances, Dedicated host, Dedicated instances, Scheduled instances, Capacity Reservations
  - interruption이 허용되는 batch processing이라면? -> spot instance
  - interruption은 불가능, lambda / Fargate / EC2 등의 flexibility 확보? -> Saving plans

match storage to usage
- compute environment에 적합한 크기의 storage 사용.

measuring / monitoring to optimize.
- cloudwatch, cost explorer...

![스크린샷 2023-09-21 오전 12 04 48](https://github.com/inspirit941/inspirit941/assets/26548454/1a7f8ffa-5724-4f8b-955f-21018dd048d3)
<br>

Elastic Load balancer를 앞단에 붙여서 horizontally scale to meet your demand. 각각의 LB를 어떤 상황에 써야 하는지.
- Application LB
- Network LB
- Gateway LB


LB를 autoscaling group에 붙이면
- LB metric을 사용할 수 있다. (ALB의 request count per target)
- health check를 붙일 수 있다. (EC2 autoscaling group에서 identify / replace unhealthy instances)

### Walkthrough question 4.2

![스크린샷 2023-09-21 오전 12 07 48](https://github.com/inspirit941/inspirit941/assets/26548454/94167e73-1913-4e4b-9546-5b12fd737155)
<br>

Answer: B. Lambda는 operational overhead 없이 간단한 Microservice 배포하는 데 최적화. api gateway를 붙이면 rapid scale change가 가능함. managed service이므로 DDoS로 무력화하기 쉽지 않고, api gateway에서 request method별로 throttle설정도 가능. api gateway의 경우 counterfeit request (L7) / SYN floods (L3) 다 방어됨
- A. Beanstalk로 빠르게 앱 빌드는 가능하지만, scaling 대응이 상대적으로 느림. EC2 bootup 물리적 시간. EC2라서 idle 상태일 때도 비용이 나가므로 not cost-effective
- C. A와 동일한 이유.
- D. A와 동일한 이유. container라서 scale 자체는 빠르지만, cluster 단위로 scale up 할 때는 시간이 걸림.

### Design cost-optimized Database Solution

![스크린샷 2023-09-21 오전 12 14 57](https://github.com/inspirit941/inspirit941/assets/26548454/1960ffa3-d452-4398-877f-9ccaaef0c5c2)
<br>

일단 Data Type별로. 보통 RDS가 일반적인 transactional processing system에서 핵심. 그러나 여기에 다 저장하는 건 performance issue / cost ineffective
- access pattern, expected scale / growth 토대로 판단한다.

Migrating data to AWS?
- 기존 RDB 일부를 EC2 또는 RDS로
- Large object from RDB to S3
- 기존 RDB 일부를 NoSQL data store로 (dynamoDB)

이외에도
- 특정 DB specific feature가 반드시 필요한가
- table schema / entity definition이 애플리케이션 커지면서 바뀔 여지는 없나?

![스크린샷 2023-09-21 오전 12 19 03](https://github.com/inspirit941/inspirit941/assets/26548454/3c15c256-a11a-4b98-a9d1-4ec9a0a01bbb)
<br>

DynamoDB 같은 NoSQL DBf로 migration 한다면?
- HW provisioning, setup / configuration, replication, SW patching 등 Operational overhead를 줄여줄 것이다

보다 cost-effective한 managed service 고려하기
- use Aurora Serverless over Aurora

<img width="683" alt="스크린샷 2023-09-21 오후 4 14 00" src="https://github.com/inspirit941/inspirit941/assets/26548454/ffb59e01-3148-47f8-9306-cf07ccc0d146">
<bR>

Select Appropriate scaling strategy.
- 예컨대 RDS에서 heavy read request가 들어올 때 high CPU 문제로 performance issues를 겪고 있다면?
  - vertical scale은 가능하지만 가격이 비쌈.
  - horizontal scale도 가능은 하지만, read replica나 cache 등의 방법을 쓰는 게 더 낫다.

backup plan에서는 RPO requirements with appropriate frequency를 맞추는 게 좋다. (RTO보다) <br>

point-in-time recovery, retention policy 지원하는 서비스는 무엇이 있고, 적절한 값은 무엇일지. <br>

가급적이면 managed service 권장.

### Design cost-optimized Network architecture

<img width="972" alt="스크린샷 2023-09-21 오후 4 19 28" src="https://github.com/inspirit941/inspirit941/assets/26548454/034888c0-a05c-4491-b737-2abad420a0b9">
<br>

AWS networking is Virtualized. AWS 자체가 managed networking service.
- switches, routers 등 network equipment을 사용자가 신경쓸 필요 없음
- CPU / Storage 쓰는 것처럼 Network도 사용한 만큼 비용을 내는 시스템.

<img width="681" alt="스크린샷 2023-09-21 오후 4 21 50" src="https://github.com/inspirit941/inspirit941/assets/26548454/65c79b8d-c2a4-40c7-a444-71ad921fb20f">
<BR>

Data Layer
- connections btwn AWS / on-prem... 상황에 맞는 solutions.
  - configuring network connectivity
  - 예컨대 private connection이 필요하다면 site-to-site VPN / Dedicated Direct Connect location 등의 서비스를 사용 가능.
  - 보통 Direct Connect가 VPN보다 가격이 비싸다. Direct Connect에서 제공하는 수준의 throughput / security가 필요하지 않다면 VPN이 좋은 선택지.
- how you connect AWS resources to manage?
  - EC2에 접근한다? - SSH / RDP, 또는 AWS system Manager Session Manager, AWS EC2 instance connect.

- Connection btwn VPCs within a Region / Cross Region
  - peering connection이 transit gateway보다 유용한 경우는?
  - data transfer 비용은 across AWS regions할 때 발생.
    - VPC peering이 transit gateway보다는 비용이 낮다.

<img width="971" alt="스크린샷 2023-09-21 오후 4 30 45" src="https://github.com/inspirit941/inspirit941/assets/26548454/9697c20b-56af-4b8f-9872-0183e9ec17c3">
<br>

VPC gateway Endpoints: data transfer cost 없이 S3 / DynamoDB within same region이 가능함.
- traffic that crosses AZ boundary... data transfer charge.
- 따라서 가급적이면 Local AZ를 활용해야 함.

NAT gateway 
- 보통 prod 환경에서는 public subnet for each AZs에 NAT gateway를 배포.
- Dev 환경이라면 shared NAT gateway 세팅할 수 있다.

transit gateway <br>

throttling strategy for your workload.
- API gateway에서 Usage plan과 api key 설정으로 defined limits / quotas 초과할 경우의 설정을 부여할 수 있음.

design with Appropriate Bandwidth.
- Direct Connect로 on-prem과 AWS가 연결되어 있다고 할 때, failover with minimal cost?
  - 또 하나의 Direct Connect 설정하면 비용과 configuration time이 추가로 든다. site-to-site VPN이 cost effective.

S3 cost?
- 사용하고 있는 storage / cost for api calls made to S3 / data transfer out of the bucket.
  - 따라서 비용 절감의 방법 중 하나는 api call 횟수 / data tranfer 횟수를 줄이는 것.
  - cloudFront (CDN) 사용.
    - origin (S3, EC2, ELB 등..)과 cloudfront 간 data transfer에는 비용이 들지 않는다.
    - provides regional Edge cache, at no additional cost


### Walkthrough question 4.4

<img width="948" alt="스크린샷 2023-09-21 오후 4 40 37" src="https://github.com/inspirit941/inspirit941/assets/26548454/c83aee63-7daf-48f4-99b7-c70ba25b50a9">
<br>

Answer: A. Session Manager를 사용하면 inbound port 설정 없이도 secure / audible instant management, maintain a bastion host, manage ssh keys 등이 가능하다. Session Manager로 EC2 통신하는 데에는 비용이 들지 않음. 따라서 private service인 경우 특히 유용하다.
- B: bastion host를 Public에 세팅하고 private subnet의 EC2에 로그인 - classic ways. 그러나 bastion host 띄우고 유지하는 비용이 필요함.
- C: 기술적으로 불가능. NAT gateway는 egress traffic만 취급하기 때문. inbound connection to the instance가 불가능하다.
- D: VPN connection으로 해도 되긴 하는데 additional cost가 들어가므로 정답이 아님.

### Wrap up

<img width="957" alt="스크린샷 2023-09-21 오후 4 46 10" src="https://github.com/inspirit941/inspirit941/assets/26548454/4e531f6e-1ba5-4bdd-a567-8ca63960be66">
<img width="682" alt="스크린샷 2023-09-21 오후 4 47 36" src="https://github.com/inspirit941/inspirit941/assets/26548454/8adb69dc-59ff-4f49-869d-6bbd53afece9">
<br>



