## Domain 1. Design Secure Architecture

Security 관련 서비스 이해하기 + security concepts, how they affect your decisions regarding the services and solutions you will end up evaluating.

Outline
- Design secure access to AWS Resources
- Design secure workloads and applications
- Determine appropriate data security controls

### Design Secure Access to AWS Resources

Defining how people, tools, applications you build will access the necessary AWS Services and your data.
- who or what can launch / terminate your resources
- how and when access is given along with operational permissions

![스크린샷 2023-09-07 오후 1 44 31](https://github.com/inspirit941/inspirit941/assets/26548454/93ff77f1-c24d-4a56-94f3-945879ca202d)
<br>

특히
- public / private / hybrid / multi-cloud 개념
- AWS Accounts: what they are, how they work to ensure you have secure accesss.
  - account root user security.
  - applying the principle of least privilege
  - MFA (multi-factor authentication) 
- IAM. **Global** AWS services; secure any data in the AWS IAM databases in all regions.

![스크린샷 2023-09-07 오후 7 10 20](https://github.com/inspirit941/inspirit941/assets/26548454/61866521-218d-4980-bd71-f0db58066644)
<br>

IAM identities start with no permissions. should be granted.
- how do you create IAM users, groups, and roles?
- what are their strengths and limitations?
- what scenarios would dictate possibly switching btwn various user groups / role-based permissions?

how IAM / other AWS Services give you the ability to secure credentials, best practices for handling those credentials.
- assigning various roles to AWS Services
- understand how to use AWS Security Token Service within / across accounts.
- how roles are used with federations. (on-prem이나 third party identity provider)
  - design / configure active directory to federation access to AWS IAM roles or users.

Policy: Identity나 resource에 붙어서 permission을 결정하는 AWS Object.
- **Identity-based policy**: Attached to IAM groups / users. specify 'what that identity can do - what resources that identity can access (permissions)'
- Resources policy: Attached to Resource. control 'who can access the resource / what actions they can perform on it'
  - S3 bucket, SQS queues, VPC endpoints, AWS KMS encryption keys
  - bucket policy의 경우 Identity policy와 Principle Policy가 다르다. 'which principles are affected by this resource policy'
- policy를 직접 생성할 필요는 없지만, read / interpret policy document 할 줄 알아야 한다.
  - policy statement 확인 - what is required, how it provides granularity with permissions. 
  - IAM decision logic - how it affect an identity with multiple policies attached.
  - appropriate use of resource policies for AWS Services


![스크린샷 2023-09-08 오전 11 15 43](https://github.com/inspirit941/inspirit941/assets/26548454/88507bbd-087a-4422-9433-43ba1bdbc45b)
<br>

Understand the methods, services, tools for **Traceability** when access to AWS resources.
- helps monitor, alert, audit actions & changes environments in real time.
- integrate log / metric collections

AWS Control Tower, AWS Organizations / Service control policies 이해해야 한다.
- Designing / Implementation 둘 다 중요함

### Walkthrough question 1.1

![스크린샷 2023-09-08 오후 2 13 39](https://github.com/inspirit941/inspirit941/assets/26548454/c96223a1-5695-4b03-a452-22e3cdd187dd)
<br>

Answer: B / D. 둘다 additional security for the root user of their AWS account.
- A의 access key, secret access key는 programmatic request to AWS 용도임. 이걸 root user가 쓰게 되면 full access to all resources하게 되므로 적절하지 못하다.
- C는 root user cannot assume a role to its own account라서 불가능. role은 services within the account / 3rd party access to other AWS accounts.


### Design Secure workloads and applications

how the people, tools, applications you build will securely access to AWS Services.
- who or what can launch / terminate your resources.
- managing how / when access is given.

![스크린샷 2023-09-08 오후 3 20 36](https://github.com/inspirit941/inspirit941/assets/26548454/c8060fba-58d3-4b91-a9f8-e47f851375d7)
<br>

Design, build, secure Amazon VPC. 종류는 두 가지.
- default
- custom

기본적으로 VPC는 one Region, one service Account 으로 만들어진다. (Regional service)
- Design Secure VPC;
  - 일반적으로 application은 multi-tiered. 
  - 각 tier별 application에 적용하기 위한 security groups, network access control lists, route tables, and NAT gateway 설정을 알아야 한다
  - provides granularity in rules, restrictions, allowances that you need.
  - 각각은 어떻게 동작하는지, 묶이면 어떻게 동작하는지.
- how to build the rules, pitfalls to avoid, rule processing logic, methods to employ them for better combined functionality.

Networking Fundamentals; protocol, CIDR, subnetting, routing, security filters, gateways...
- networking strategy: public / private subnet이 각각 어느 때 쓰여야 하는지. 차이는 뭔지. common practices.

Subnet: where our services sit and run inside our AWS VPCs.
- add structure / functionality to our VPC
- resiliency: Availability Zone resilient feature of AWS.

Routing: route table.
- 예컨대 on-prem 서버와의 통신이 필요하다면 traversing a VPN, in a private subnets.
- public internet access에 영향을 받지 않으려면?
  - AWS service Endpoints 서비스 활용이 필요함 (PrivateLink)
  - peering, transit gateways, VPN connections, Direct Connect 등 network connection tools / methods 등을 사용할 수 있음.

Endpoints: gateway objects that we can create inside our VPCs. AWS public service와 통신할 수 있는 internet gateway / NAT gateway와 비슷한 역할.
- good way to add secure access.
- 애플리케이션은 Public으로 열어둔 상태일 때 security 확보하기?
  - VPC peering을 사용할 수 있지만, managing overhead가 증가 / exposes other applications in the VPCs to the other VPCs that are peered.
  - PrivateLink 라는 서비스를 활용하면 exposing applications in adding secure access for other VPCs in other AWS accounts.
    - secure / scalable way to expose your application or service to a lot of VPCs
    - with no peering, internet gateway, NAT gateway
- External Connections to / from AWS resources using private connections with AWS Site-to-Site VPNs, AWS Client VPNs, and Direct Connect.

![스크린샷 2023-09-09 오후 4 39 10](https://github.com/inspirit941/inspirit941/assets/26548454/9cff1dce-f037-4893-9141-4d04bd53c791)
<br>

Security at Every Layer
- How do you build in security to your networking tiers?
- How do you secure application use across these tiers?
- what does the management of those security components looks like?
- PII 핸들링하기 위한 AWS Service는 무엇인가? - **AWS Macie**
  - use ML to discover, classify, protect sensitive data stored in S3.
  - 이외에도 AWS Cognito, GuardDuty 등이 있음.
  - cognito를 쓴다면 user pools, identity pools / how cognito brokers the SSO or ID federations.

Integrate security services: firewalls / proxy servers.
- AWS Shields, AWS WAF, AWS IAM identity Center, AWS Secrets Manager, AWS System Manager Parameter Store 등등..
  - shield standard와 shield advance 차이점 이해하기
  - 각 용도에 따른 security service 적용방법. i.e. external DDoS나 SQL injection 방어
    - **AWS Secrets Manager**: store a secret, need high volume access with automatic credential rotations
    - **AWS WAF**: can only deployed on certain AWS services (application LB, API gateway, Amazon CloudFront)



### Walkthrough question 1.2

![스크린샷 2023-09-09 오후 4 39 10](https://github.com/inspirit941/inspirit941/assets/26548454/9cff1dce-f037-4893-9141-4d04bd53c791)
<br>

Answer: B. Configure the access with Security Groups.
- Security Group은 일종의 virutal firewall for your instance to control inbound / outbound traffic.
  - matching rule이 없을 경우 blocking all other traffic 가능.
  - instance 단위로 설정할 수 있음. 따라서 same subnet이더라도 인스턴스별로 다르게 적용할 수 있다.

- A: network access control list의 경우 subnet boundary로 설정할 수 있다. 위 문제의 경우 두 개의 인스턴스가 같은 subnet에 위치해 있고 요구사항이 서로 다르므로 쓸 수 없다.
- C: VPC Peering의 경우 VPC 간 통신을 지원할 뿐 traffic-blocking 기능이 없다.
- D: route table의 경우 determine where network traffic from your subnet / gateway is directed. block traffic 기능이 없다.


### Determine appropriate data security controls

<img width="940" alt="스크린샷 2023-09-10 오후 12 49 03" src="https://github.com/inspirit941/inspirit941/assets/26548454/4e9dcd67-697b-4e48-81bf-a668b1020021">
<br>

what is Cloud Storage?
- cloud computing model that stores data through a cloud computing provider, whoi manages and operates data storage as a service.

Benefits?
- no HW to purchase, no storage to provision, no capital spending.
- time to deployment is faster. storage lifecycle management policies add automations, savings, and lock data in support of compliance requirements.

Requirements?
- ensure your data is safe, secure, available when needed.

어떤 storage 쓸 건지 결정?
- durability, availability, security, regulatory and governance requirements, functions requirements 확인
- 저장할 데이터의 타입; object? file? block?
- 크게 5가지 형태의 사용법
  - backup / recovery -> disaster recovery. 시험 나오고, resilient architecture design에 반드시 포함되어야 할 항목
  - SW test and development
  - data migrations
  - compliance
  - bigdata / data lakes


<img width="955" alt="스크린샷 2023-09-10 오후 12 52 24" src="https://github.com/inspirit941/inspirit941/assets/26548454/9cbd1d73-501f-4da0-9764-35300420946d">
<br>

backup / recovery는 cost와 complexity 기준으로 4가지 선택지.
- Active-passive strategy: region별로 active / passive workload 배포.
- disaster의 정의가 region 하나 데이터센터 날라가는 것보다 큰 경우라면 pilot light, warm standby, multi-site active-active 도입을 권장.

backup strategy; periodically / continously?. 자주 수행할수록 복구할 수 있는 지점이 많아짐
- EBS snapshot, DynamoDB backup, RDS / Aurora Snapshot, EFS backup using AWS Backup, AWS Redshift / Neptune snapshot, DocumentDB, S3 Cross-Region replication
  - S3 CRR의 경우 continous. asyn하게 object 백업. provide versioning for the storage object으로 restore point 가능..

<img width="953" alt="스크린샷 2023-09-10 오후 12 56 26" src="https://github.com/inspirit941/inspirit941/assets/26548454/63a92f5b-e73f-42e4-981c-b778db9f122e">
<br>

AWS Backup은 Centralized location to configure, schedule, monitor. 위와 같은 서비스들의 backup을 지원함
- supports copying backups across regions (disaster recovery across regions)


만약 hybrid environment 환경이라면 어떤 서비스를 써야 하나? AWS Storage Gateway?

---

data in transit / data in rest에 무관하게 security needs to be evaluated.
- principle of least privilege 적용.

Encrytion at rest: designed to protect against unauthorized access and theft

Encryption in rest: 보통 only one party is involved 일 때 사용. <BR>
Encryption in transit: protect data as it's being transferred btwn two places, and 2 or more parties are involved.
<BR>

encryption adds a tunnel around that data, so no one from the outside can read the data. <br>

<img width="680" alt="스크린샷 2023-09-10 오후 12 00 07" src="https://github.com/inspirit941/inspirit941/assets/26548454/4720498c-0648-4ee7-89ed-97adedd7cc3a">
<br>

이 분야에서 이해가 필요한 용어들
- plainText: unencrypted data를 뜻한다. text data라는 format에 국한된 게 아님. docs / images / applications 등등..
- algorithm: plainText와 encryption key를 받아서 암호화된 데이터를 생성하는 로직
- key: password used in algorithms, and produces cipherText
- cipherText: Encrypted Data를 말함.

encryptions / keys 사용하는 두 가지 types
- Symmetric
- Asymmetric

---

<img width="685" alt="스크린샷 2023-09-10 오후 12 12 31" src="https://github.com/inspirit941/inspirit941/assets/26548454/64700411-1fb0-4b35-99ba-3823334eb98a">
<br>

secure data at rest하려면?
- 예컨대, data encryption key의 management를 위해 AWS KMS를 쓰는 이유? (vs AWS Cloud HSM) / 두 서비스를 같이 쓰려면?
- how do you manage encryption keys across regions?
- what types of keys / what are the differences in capability?
- how often can you rotate each type of key?
- how to implement access policies for encryption keys

> 각 서비스 비교하고, 특정 요구사항에서 어떤 서비스를 사용해야 하는지.
> AWS Certificate Manager로 encrypt data in transit하기 / certificate renew 방법


<img width="684" alt="스크린샷 2023-09-10 오후 12 12 45" src="https://github.com/inspirit941/inspirit941/assets/26548454/958d1855-4cf4-468a-bc8b-355893b61968">
<br>

S3의 data in rest, data in transit 방식 - client-side / server-side.
- client-side: S3로 업로드하기 전에 먼저 encryption 처리
- server-side: 데이터 전송 자체는 https의 default encryption 사용. S3에 도착한 뒤 encrypted. 방식은 크게 세 가지.
  - customer-provided key 사용하기
  - S3 managed key 사용하기
  - customer master key stored in AWS KMS 사용하기

<img width="948" alt="스크린샷 2023-09-10 오후 12 16 58" src="https://github.com/inspirit941/inspirit941/assets/26548454/60811c69-70e2-4833-8325-8ada71d66a35">
<br>

Compliance / compliance requirements. security와 compliance는 shared responsiblity btwn AWS / customer.
- AWS provides best practices for securing sensitive data in AWS Data stores.
  - general data security patterns / clear mapping of patterns to cloud security controls.
- AWS의 cloud adoption framework with a specific security perspective to help. 
  - 5 capabilites; IAM, detective controls ,infrastructure security, data protection, incident response. 어떤 데이터를 어떻게 저장하고, 누가 접근권한이 있는지 설정.
  - classify properly. 보안 적용할 데이터와 아닌 데이터 구분.
  - add security controls or defense in depth. 
    - 보통 여기서 layering multiple security controls to provide redundancy along with 2 categories; preventative / detective


architecture / requirment에 따라 적합한 data protection 적용.
- 예컨대 VPN over the internet / private connection through AWS Direct Connect일 경우
- Connections btwn VPCs
- transfer of your data btwn services (i.e. S3 - VPC)
- public internet으로 사용자가 접근할 수 있을 때 data in transit 방법은?

<img width="675" alt="스크린샷 2023-09-10 오후 12 35 13" src="https://github.com/inspirit941/inspirit941/assets/26548454/2afb3786-6f30-4ec5-955f-cfab4199da51">
<br>

각 서비스별로 제공하는 security aspect 파악.
- S3와 AWS EBS의 data management / storage가 어떻게 다른지
- protection 적용이 performance of service에 영향을 미치는지

EBS volume에서 데이터가 생성되는 경우를 예시로 들면
- data needs to be protected while maintaining durability.
- Encrypted EBS volume -> least effort
- Encrypted S3 bucket으로 transit

how to handle root keys / how that method differs from your data keys
- S3와 KMS 중 managed service that secure, evaluate, audit the security of data? -> KMS

Protecting based on access patterns: 이 기능을 제공하는 서비스에는 어떤 것들이 있는지, how evaluated by service backends.
- S3의 경우 bucket 단위의 security 설정 + add controls based on specific paths or objects
- S3의 intelligent tiering 대신 data lifecycle management 사용해야 하는 경우는?

### Walkthrough question 1.3

<img width="682" alt="스크린샷 2023-09-10 오후 12 59 28" src="https://github.com/inspirit941/inspirit941/assets/26548454/bc125d2d-6f4f-492d-9e0e-786ee4495073">
<br>

KMS는 protect / validate your KMS keys를 위해 HW security modules을 사용함. manages the SW for the encryption.

Answer: A. KMS로 generate / control access to keys. it provides a secure way to generate, store, control the data keys / key durability.

- B: AWS Certificate Manager는 storing SSL keys 용도. not data keys.
- C: instance store volume은 ephemeral storage. durability 충족 안 됨.
- D: S3는 key management 기능이 없음. KMS policy only work for keys stored in KMS.


### Wrap up

<img width="682" alt="스크린샷 2023-09-10 오후 1 06 51" src="https://github.com/inspirit941/inspirit941/assets/26548454/27e27155-c912-4938-9f6f-44aa82c6a59b">
<br>

핵심은 Least privilege 원칙.
- multi account 환경에서 원칙을 지키려면 어떤 서비스를 써야 하는가? AWS Control Tower? AWS Service Catalog? AWS Organization?
- IAM 이해. IAM role과 IAM user는 각각 어떨 때 써야 하는가
- identity policy, resource policy, permissions policy, service control policy
  - overlapping allow / deny rule 상태일 때 어떻게 동작하는가
- different way to federate into AWS
  - AWS SSO / AWS Directory Service의 usecase
- monitoring services; CloudTrail, CloudWatch, VPC Flow logs
- Security control 설정해서 VPC 세팅하기
- AWS Shelds, AWS WAF, AWS Secrets Manager, AWS Systems Manager Parameter Store 각각의 특징과 사용처
- Data in transit / Data in rest
- 목적에 맞게 AWS KMS / AWS CloudHSM 선택

