## Designing a solution following across governance & management best practices

### Customer #4 - requirements
- 모든 서비스가 하나의 AWS Account (prod account) 내에 구성돼 있음.
- divide big single account into smaller pieces of infrastructure.
- 서비스 규모가 커지면서, 초기에 가볍개 환경 구축하고 관리할 수 있는 범위를 넘어선 상태.
  - 어떤 관리방식이 최적인지 알 수 없는데 billing도 신경 쓰임.
- personal email 기반 root user 로그인 방식 사용중.

The need for multiple accounts, with automatic account provisioning. <br>
Shared Services Account taht people will initially log in. <br>
Single Sign-On among the accounts.

#### Requirement DrillDown

AWS에 익숙하지 않은 회사나 팀에서 처음 사용할 때 자주 있는 일임. 보통 이런 경우 customer는 자기가 뭘 모르는지도 모르는 상태이기에 requirement가 명확하지 않을 때가 많다. Solution Architect는 이런 경우 requirement specification하는 역할.

- Devise a plan for 'how to manage multiple AWS Accounts'.
  - per workload / client / environment 등 여러 단위로 separate 가능. 도입 가능한 전략이 여러 개 있으므로, 상황에 따라 가장 맞는 걸 선택하면 된다
- Create an Account that users will initially sign in to.
- Configure single sign-on & Centralized credentialing.
- Enforce Configuration rules across AWS Accounts.
- Centralized Logging in a dedicated Account.

### Why Multi-Account Strategies?

선요약
- Have Group Workload, based on business purpose or ownership
- Centralized logging
- Constraint Access to Sensitive Data
- Limit blast radius from adverse Event
- Manage Cost better
- Distribute API request rate


Resource Grouping의 권장사항 (원칙?)
<br>

**Group Workloads based on Business purpose & Ownership.**
- 비즈니스 로직이나 팀별로 작업 process가 다름. 따라서 business unit 단위로 isolated group을 할당하는 것.
- security guardrail은 지키되 decentralized operational control을 부여할 수 있다.
- 위 예시의 경우, Marketing Agency에서 'Running Workloads for other customer' 중이라고 언급했음. 이 원칙을 적용하기 좋은 예시라고 판단.

<br>

Segmentation per Business Unit 기반 구조에 **Workload Segmentation Model** 을 추가한다.
- Each Environment from each separate customers 각각 organization unit (OU)를 갖게 된다.

<img width="977" alt="스크린샷 2023-07-28 오후 2 28 52" src="https://github.com/inspirit941/inspirit941/assets/26548454/0f927ed2-bd06-4bcb-bab1-37a4dcf5add2">
<br>

예컨대 Root OU 하위에 Customer OU를 생성하고, Customer 상황에 맞게 Phase별로 OU를 구조화할 수 있다.
- 예시의 경우 Dev, Testing, Production.
- Dev OU에서 아래와 같은 것들을 정의할 수 있다.
  - Dev환경에서 사용할 Dedicated Account
  - Configured Cloud IDE
  - AWS Organization의 SCP (Service Control Policies)를 적용하면, 개발자가 unauthorized resource를 생성하는 것을 막을 수 있다.
    - 예컨대 Dev존인데 엄청 큰 리소스를 발급받는 등의 행동을 차단한다던가.

AWS Account별로 권한을 분리함으로써 Governance & Access 관리를 쉽게 할 수 있음. <br>
또한 AWS의 billing 기준은 Account 단위. 따라서 billing bottleneck 확인하기도 용이하다.

<br>

Multiple AWS Account를 도입한다면, 두 가지 요인은 반드시 관리해야 한다. 안 그러면 오히려 managing 난이도만 올라감
- Automation
- Centralize Credentialing

<br>

![kV3NuU3lTJ2dzblN5fydcA_d6ce084a421f4b5589fab68c13354bf1_Reading4 1A](https://github.com/inspirit941/inspirit941/assets/26548454/c8ff5a48-df2d-47ff-ac17-f8baf276502c)
<br>

cf. Multiple IT Operating Models

**Tranditional Ops Model**
- custom / commercial off-the-shelf (COTS) 굴리는 팀에서 해당 applcation의 Engineering 관리. (operation은 관리하지 않음)
- underlying Infrastructure (platform) / application의 operation도 Cloud Platform Engineering 팀에서 전부 관리.

**CloudOps Model**
- Application 관리하는 팀에서 Engineering / Operations 관리.
- underlying platform 관련 Engineering / Operations는 Cloud Platform Engineering 팀에서 담당

**DevOps Model**
- Applcation 팀에서, 애플리케이션이 구동하기 위한 underlying platform 영역까지도 Engineering / Operations을 담당한다.
- Cloud Platform Engineering은 여러 애플리케이션이 동시에 구동되는 Shared Platform을 담당함.

### IAM Roles - AWS Authentication Core Mechanism


AWS Identity Access Management (IAM)
- Manage Credentials for access to an AWS Account.
- IAM Users, Groups, Roles로 구성됨.
  - users / roles: credentials / permission을 제공하는 IAM entities
  - groups: Collections of users.

Users는 Permenant Credential을 부여받는 반면, role은 temporary credential / sign-in 할 수 있는 URL을 받는다.
- **어떤 identity가 어떤 동작을 할 수 있는가** 를 정의하는 것은 동일함.
- 미리 정의해두고, 이 권한을 필요로 하는 anyone에게 부여하는 것.
  - Same Account -> IAM User
  - Different Account -> IAM User
  - AWS Service (EC2 등)
  - External User - SAML 2.0, OIDC 또는 custom-built identity broker로 authenticated된 대상.

cf. AWS Service Role
- user에게 role 부여한 것과 동일한 논리로, service에게 권한을 부여하는 것.
- 예컨대 다른 서비스와 통신해야 한다면, 해당 서비스와 통신할 수 있는 Permissions을 부여받은 Role이 있어야 한다.
  - EC2에서 lambda를 호출할 거라면, lambda를 호출할 Permissions이 포함된 Role을 EC2 service가 가지고 있어야 함.

<br>

multiple Account 생성하는 방식으로 갈 때, IAM Users를 복사하는 식으로 구현되어선 안 됨.
- 아래 Demo를 통해 Users 생성하는 대신 Role을 적용하는 방식을 설명함.
<br>

<img width="923" alt="스크린샷 2023-07-28 오후 3 25 02" src="https://github.com/inspirit941/inspirit941/assets/26548454/eaf56060-287a-4c42-b156-2ed1c2a5b09c">
<br>

Account A에 Role을 생성할 것임.
- 이 Role은 'Account B에 있는 user가 assume-role 이라는 API Call을 할 수 있도록 Allow하는 것'

Account A에 관련된 정보
- account는 IAM Role을 가지고 있다.
- account ID는 suffix가 8173. developer-account-a 라는 이름으로로도 불린다.
- **Who is Authorized to Assume this Role?**
  - (Role Trust Relationship이라고도 부른다)
  - 다른 Account에 있는 'rafael'이라는 IAM User.
- Role Permission: AdministratorAccess
- Role Name: AdminRole

<br>

Account B에 관련된 정보
- IAM Role을 부여받을 User 정보를 가지고 있다.
- IAM user로 rafael이 있고, user ID와 해당 user의 AWS Resource Name (ARN) 번호가 있다.

<br>

이제 AWS Account A로 로그인한 뒤 AdminRole이라는 이름의 Role을 생성한다. 이 Role은 AdministratorAccess라는 Permission 권한을 부여받았다.

<img width="933" alt="스크린샷 2023-07-28 오후 3 36 24" src="https://github.com/inspirit941/inspirit941/assets/26548454/8fcfcf24-387b-4135-8f39-d60ce0c4e726">
<br>

AWS IAM의 Role Create 옵션을 선택한다.

<br>
<img width="933" alt="스크린샷 2023-07-28 오후 3 37 33" src="https://github.com/inspirit941/inspirit941/assets/26548454/0615b835-ecfe-4701-89a9-dde4d3ac5a5b">
<br>

그럼 Role Trust Relationship을 선택하라고 나온다. 
- **Who is authorized to take this Role** 과 같은 의미.
- AWS Account 하위에 있는 User에게 부여할 것이므로, AWS Account를 선택한다.

<br>
<img width="930" alt="스크린샷 2023-07-28 오후 3 37 44" src="https://github.com/inspirit941/inspirit941/assets/26548454/da241749-ce20-4c3f-8e3e-fbbb74dd4e2a">
<br>

이 Role을 부여할 AWS Account ID를 입력한다. 
- AWS Account B의 ID를 입력한다.

<br>
<img width="930" alt="스크린샷 2023-07-28 오후 3 38 19" src="https://github.com/inspirit941/inspirit941/assets/26548454/7f644a26-1563-47b2-994c-4db7a54aeb2c">
<br>

다음으로, 이 Role에 어떤 Permission을 부여할 것인지 선택한다.
- AdministratorAccess를 부여하기로 했으므로, Permission에서 해당 permission을 검색해서 선택한다.

<br>
<img width="934" alt="스크린샷 2023-07-28 오후 3 38 33" src="https://github.com/inspirit941/inspirit941/assets/26548454/b10ecf3d-512a-4084-99e0-31650d6c2cf9">
<br>

이 Role에 부여할 Name / Description을 결정할 수 있다.
- Role Name으로 AdminRole을 쓰기로 정의했으니, 그대로 입력해준다.

---

<img width="936" alt="스크린샷 2023-07-28 오후 3 44 41" src="https://github.com/inspirit941/inspirit941/assets/26548454/437e8967-9d77-445a-ae91-d60dacf9696d">
<br>

생성한 AdminRole 정보를 확인해보면, Trust Relationship에서 account의 root에 role이 부여된 걸 볼 수 있다.
- rafael이라는 user에게만 적용되는 것이 원래 의도이므로, ARN값의 root을 user/rafael로 바꿔준다.

---

<img width="930" alt="스크린샷 2023-07-28 오후 3 48 38" src="https://github.com/inspirit941/inspirit941/assets/26548454/9d8c4072-f712-44f9-a426-6f2500280587">
<br>

이제 rafael이라는 user로 AWS Console에 로그인해서 Role을 사용해본다. 콘솔에서 switch role 선택해본다.

<img width="939" alt="스크린샷 2023-07-28 오후 3 49 42" src="https://github.com/inspirit941/inspirit941/assets/26548454/5166117f-5a05-4c65-950d-b91c1896522e">
<br>

role을 선택할 수 있다.
- 해당 Role은 Account A에서 만들었으므로, Account A의 ID값을 입력한다.
- Role 이름으로 AdminRole 입력하고 Switch Role 클릭한다.

<img width="941" alt="스크린샷 2023-07-28 오후 3 51 07" src="https://github.com/inspirit941/inspirit941/assets/26548454/fda2874a-c021-4626-8b65-23ae2c9466b4">
<br>

콘솔 로그인창이 rafael이라는 user가 아니라, AdminRole이 된 것을 확인할 수 있다.
- 해당 Role이 부여받은 permission 내에서만 동작이 가능함.
- 예컨대 View 권한만 받은 role로 접근한다면, resource의 create / update / delete는 불가능하게 만들 수 있다.

**IAM Role 기능이 Across-Authentication 로직의 핵심이므로 매우 중요함**
- 특정 IAM user나 group, 또는 other account에서 정의한 role을 선택해서 역할을 부여할 수 있다.
- Can Avoid Replicating same users across accounts.
  - **Essential for Centralized Credentialing**

### Organizing Accounts together using OUs (Organization Units)


![organizations-HIW 1870c83be9fdfc55680172a1861080a91b700fff](https://github.com/inspirit941/inspirit941/assets/26548454/92e04d7f-8ac7-4bb5-a3d7-aa78c839c790)
<BR>

AWS Organization: Managed service that helps you organize your accounts. (https://aws.amazon.com/ko/organizations/)
- centralize / govern your environment.
- AWS Associate 자격증 범위로만 다루므로 깊게 들어가지는 않음.

제공하는 기능
- create / add existing accounts
- create groups (organization units)
- apply policies (Service Control Policies)
- enable / disable AWS service in the child accounts inside your organizations.

최초로 Create Organization을 실행하면, 로그인한 계정을 management account로 정의한 base Organization(root)이 생성된다.
- base 하위에 Organization Unit (OU) 생성이 가능하다.

SCP (Service Control Policies)는 Console에서 Policies 하위 항목에서 Enable / Disable할 수 있다.
- Permission Mechanisms that governs the entire OU / Account boundary.

아래 예시는 t2.micro를 제외한 EC2 Instance 생성을 막는 Policy의 생성 과정.

<img width="934" alt="스크린샷 2023-07-30 오후 3 17 22" src="https://github.com/inspirit941/inspirit941/assets/26548454/03f2dade-88e3-485a-b838-c7828566ca88">
<img width="933" alt="스크린샷 2023-07-30 오후 3 37 19" src="https://github.com/inspirit941/inspirit941/assets/26548454/b555c55f-675b-494b-858c-95244d4a0e55">
<br>

Create New Policy에서 Json Document를 위와 같이 추가한다.
- Statement에서 ec2 resource의 접근을 allow 한다.
- ec2의 RunInstance Action의 경우, 인스턴스 종류가 t2.micro가 아닐 경우 (stringsNotEquals) Deny한다.

<img width="935" alt="스크린샷 2023-07-30 오후 3 37 36" src="https://github.com/inspirit941/inspirit941/assets/26548454/8cef3a2e-f4ad-4b75-b612-c0cbf962568c">
<img width="917" alt="스크린샷 2023-07-30 오후 3 37 54" src="https://github.com/inspirit941/inspirit941/assets/26548454/d30f4eac-e33a-467f-8674-79341a3d8513">
<img width="936" alt="스크린샷 2023-07-30 오후 3 38 02" src="https://github.com/inspirit941/inspirit941/assets/26548454/da906218-cfe8-4a6f-b14b-c8beef1dff01">
<br>

SCP를 OU에 적용하기
- 적용할 Organization Unit을 선택한다
- 상세 페이지에서 Policies > Attach Policy 선택한다
- 직전에 만들어둔 SCP를 선택한다.

이렇게 되면, Dev Environment라는 OU에 속한 모든 AWS Account에는 ec2에서 t2.micro 이외의 리소스 생성이 불가능해진다.
<br>

<img width="937" alt="스크린샷 2023-07-30 오후 3 41 33" src="https://github.com/inspirit941/inspirit941/assets/26548454/69395c39-9360-4a07-9eeb-f8adbc83fcf1">
<br>

OU에서 'Add an AWS Account'로 aws account를 OU에 추가할 수 있다.

### Moving from One Account to Another

AWS Organization과 SCP 방식으로 Account 생성 / Permission을 자동화할 경우, Account 개수가 많아진다. 그럼 보통 아래와 같은 요구사항이 생김.
- Move Between Accounts
- Single Sign On

IAM Identity Center (AWS Single Sign On 서비스)를 활용할 수 있다. 핵심 기능은 아래와 같다.
- Workforce identities
  - Human User에 대응되는 identity를 workforce identity라고 한다. 직접 만들거나, user's own identity source를 AWS에 매핑할 수 있음. 지원되는 Identiy Sources는 아래와 같다
    - MS Active Directory Domain Services
    - External Service Identity Providers (Okta, Azure AD)
- Application assignments for SAML applications
  - SSO access를 SAML 2.0 application에 적용할 수 있다. (salesforce / MS 365)
  - access to applications in a single place, without setting up federation separately
- Identity Center Enabled applications
  - AWS의 서비스 - Managed Grafana, Monitron, Sagemaker Studio Notebook - 에서는 Identity Center의 sign-in & user discovery services와 자동으로 연동됨.
- Multi-Account Permission: 여러 account에 IAM permission을 한 번에 설정할 수 있다.

<Br>
<img width="938" alt="스크린샷 2023-07-30 오후 3 58 41" src="https://github.com/inspirit941/inspirit941/assets/26548454/92477a33-3b77-447a-b7b0-35df9bd5501d">
<img width="922" alt="스크린샷 2023-07-30 오후 4 01 46" src="https://github.com/inspirit941/inspirit941/assets/26548454/0f95dfb8-d5af-4de5-bc02-cfc0123d13e7">
<br>

서비스에셔 Create User를 수행한다.
- user 생성할 때 Generate a one-time password를 선택하면, 생성 완료했을 때 위처럼 팝업창이 뜬다.

<img width="936" alt="스크린샷 2023-07-30 오후 4 02 37" src="https://github.com/inspirit941/inspirit941/assets/26548454/08e0bafd-8cd1-46ba-b190-e55f848a2ef0">
<br>

Permission Sets를 생성한다.

<img width="941" alt="스크린샷 2023-07-30 오후 4 02 53" src="https://github.com/inspirit941/inspirit941/assets/26548454/84029940-5dd1-407a-bfd5-e13d91594e2a">
<img width="940" alt="스크린샷 2023-07-30 오후 4 04 01" src="https://github.com/inspirit941/inspirit941/assets/26548454/b2c2b065-2ca7-4003-b555-b455f83dbb3a">
<img width="931" alt="스크린샷 2023-07-30 오후 4 04 17" src="https://github.com/inspirit941/inspirit941/assets/26548454/57247a3a-86eb-482c-8403-8c9168365995">
<br>

AWS Account를 보면, 이전에 AWS Organization으로 생성한 AWS Account를 조회할 수 있다. AWS Account에 접근할 수 있는 user 정보를 매핑한다.
- Assign users and groups로 user를 등록한다. 이 User는 AWS Identity Center에서 생성한 user

<img width="938" alt="스크린샷 2023-07-30 오후 4 08 10" src="https://github.com/inspirit941/inspirit941/assets/26548454/efea98a5-cb9a-4867-9e88-d1e28829336e">
<br>

이 매핑의 의미는
- raf 라는 사용자가
- Administer Access라는 PermissionSet으로
- Dev Environment A 라는 AWS Account를 사용할 수 있다.

<img width="929" alt="스크린샷 2023-07-30 오후 4 10 52" src="https://github.com/inspirit941/inspirit941/assets/26548454/7c800621-9815-4246-b052-b2b84dd7b76f">
<bR>

요렇게 정의하면, AWS Account에서 Single Sign On 세팅을 해준다. Dashboard에서 확인할 수 있다. 
- Access Portal URL을 들어가보면 아래와 같은 화면을 볼 수 있다.

<img width="942" alt="스크린샷 2023-07-30 오후 4 11 26" src="https://github.com/inspirit941/inspirit941/assets/26548454/6975e84f-e2ae-4a0b-bb9f-a329bf9c9d1b">
<img width="941" alt="스크린샷 2023-07-30 오후 4 12 07" src="https://github.com/inspirit941/inspirit941/assets/26548454/483dabbe-b910-47e2-bd70-2a3f2d51d5eb">
<br>

로그인을 위한 ID로 AWS User에 등록한 raf를, password에 one-time generated password를 입력한다.
- 최초 로그인할 경우 new password를 설정하는 프로세스가 있다.

로그인이 완료되면, 해당 User가 접근할 수 있는 AWS Account 정보를 볼 수 있다.
- AdministratorAccess 라는 PermissionSet으로 console 로그인 / Cli 로그인을 선택할 수 있다.
- 이런 방식으로 여러 user 정보를 single sign on 방식으로 navigate할 수 있다.

AWS Organization으로 Account를 생성하면, IAM Identity Center로 User / Account 

### Choosing Services for Logging

Logging은 크게 두 가지로 나뉨.
- Application log
  - 일반적으로 web server access log, error log, database log, 기타 exception logs by source code
  - 목적: Troubleshooting application issues.
  - Lambda / Gateway / ELB / S3 website hosting / CloudFront 등.. app logging integration with S3 or CloudWacth
  - CloudWatch Alarm / Metric / ML (anomaly detection) 등으로 활용 가능.
- Infrastructure log
  - infra change events (IAM calls made to an AWS account, api call 전후의 infra 상태 관련한 이벤트 로그)
  - AWS CloudTrail, AWS Config, VPC Flow logs, AWS GuardDuty 등에서 지원.
  - CloudTrail을 사용하면 Shared Services Account에서 발생하는 infra log를 집중화해서 관리할 수 있다.

#### CloudTrail

- monitors / records account activity across your AWS infrastructure, like storage / analysis / remediation.
  - 이벤트는 AWS Console, AWS CLI, AWS SDK, API 전부 포함됨
  - EC2에서 호스팅되는 애플리케이션이 호출하는 api 같은 정보는 포함하지 않는다.
- 보통 api 호출 이후 15분 정도 시차를 두고 반영됨
- Organization trail을 설정하면, 해당 org에 소속된 모든 account의 trail 정보가 자동으로 기록된다.
  - member는 trail 정보를 조회할 수는 있으나, 변경하거나 삭제할 수 없다.
  - by default, member account do not have access to the log files for the organization trail in S3 bucket.

#### AWS Config

AWS Resource를 관리하기 위한 용도의 서비스. 
- provides a detailed view of how AWS resources are configured in your AWS account.
- how resources are related to one another, how they were configured in the past (changes over time)
- can apply rules for how those resources are configured.

Resource Administration
- 어떤 리소스가 create, modified, deleted 되었는지를 api polling 없이도 모니터링할 수 있다.
- rule에 맞지 않는 AWS resource 요청을 보낼 경우, noncompliant 처리하고 notification 전송

auditing and compliance
- 관련 정보 제공 가능.

Managing and troubleshooting configuration changes
- 특정 Resource의 변경이 다른 서비스나 리소스에 어떤 영향을 미치는지 확인 가능.
- 변경 이력이 남아 있으므로 troubleshooting / last-known good configuration of a problem resource.

Security analysis
- historical information이 전부 남기 때문에 보안 관련한 이슈도 체크 가능.
  - user에게 부여된 IAM identity / Access Management permission 정보 혹은 EC2 Security group rules 등
- user, group, role 에 할당된 IAM policy 체크 가능.
  - 예시: 특정 user가 특정 시점에 AWS VPC setting 변경 권한을 가지고 있는지 확인 가능.
- security group configuration
  - 예시: 특정 group에서 block incoming TCP traffic to a specific port

#### VPC flow logs

capture information about IP traffic that goes to / from network interfaces in your VPC.
- CloudWatch log 또는 S3에 저장 가능
- 예컨대 아래와 같은 내용을 확인할 수 있다.
  - Diagnosing overly restrictive security group rules
  - Monitoring the traffic that reaches your instance
  - Determining the direction of the traffic to and from the network interfaces
- collected outside the path of your network traffic. 따라서 사용자의 network performance에 영향을 주지 않음.

#### AWS GuardDuty

near-continuous security monitoring service that analyzes and processes data sources.
- CloudTrail data events for Amazon S3 logs
- CloudTrail management event logs, DNS logs 
- Amazon EBS volume data, Amazon Elastic Kubernetes Service (Amazon EKS) audit logs, Amazon VPC flow logs.

intelligence feed / Machine learning으로 AWS 환경에서의 unauthorized, malicious activity 확인 가능.
- 예시. EC2에서 malware serving / mining bitcoin하는 것들 탐지
- 예시. 특이한 AWS access behavior 탐지 (쓴 적 없는 region에 올라간 instance라거나, unusal API call)

<br>

CloudTrail 사용 예시. S3 bucket에 management event를 저장한다.
<br>

![스크린샷 2023-08-02 오전 11 02 32](https://github.com/inspirit941/inspirit941/assets/26548454/bda46d04-62f1-49b7-ab9d-3c5b6dc144c2)
![스크린샷 2023-08-02 오전 11 02 57](https://github.com/inspirit941/inspirit941/assets/26548454/c6af9fee-bc14-4bfd-a5ea-74ecffb1ab6e)
![스크린샷 2023-08-02 오전 11 03 12](https://github.com/inspirit941/inspirit941/assets/26548454/8e844a7d-0c9c-403e-81ca-e2d1cbb608ae)


완성된 S3 Bucket. 이렇게 되면, 모든 Account에서 발생하는 이벤트가 하나의 S3 bucket에 저장된다.
<br>

![스크린샷 2023-08-02 오전 11 03 32](https://github.com/inspirit941/inspirit941/assets/26548454/24dec7a2-e321-44dd-a3e3-7a6b59967a4d)
<br>

cf. SCP를 적용할 때 권장하는 원칙
- SCP는 Root Organization에 적용. 
- SCP에서 사용자가 CloudTrail이나 계정 로그가 저장되는 S3 Bucket을 삭제할 수 없도록 Deny 설정한다.

<br>

### Automating Account Provisioning and Maintenance

<img width="949" alt="스크린샷 2023-08-05 오후 12 58 00" src="https://github.com/inspirit941/inspirit941/assets/26548454/27f94de4-9d1d-468d-b7ad-aeb86f95b1fe">
<br>

지금까지 소개한 서비스들의 간단한 기능과 역할 정리
- AWS Organization: account creation / deletion, SCP(Service Control Policies), control security guardrails
- AWS Identity Center: Single Sign On
- AWS CloudTrails: Centralized Logging - sending logs to a single account.

<br>

What about custom environment provisioning?
- i.e. entire Dev Environment for a new account

> 예컨대 팀에 새로운 개발자가 입사했다고 하자. 팀에는 cloud Dev Environment가 구축돼 있다. 새로 들어온 개발자에게 
> - Dev Environment에 접근할 수 있고
> - Cloud9 IDE를 포함한, 기타 AWS Service에 접근할 수 있는 AWS Account를 자동으로 할당해줄 수는 없을까?

위 요구사항을 나눠보면 크게 두 가지.
1. 생성된 Account에, 필요한 AWS 리소스를 매핑할 수 있게 한다.
2. AWS Account를 자동으로 생성해준다

---

#### AWS Service Catalog

비유하자면 일종의 AWS Resource Vending Machines.

- create / manage per-approved portfolios / products 담당.
- portfolio admin은 CloudFormation template으로 AWS Resource provisioning을 요청할 수 있다. 
  - 이걸 Catalog에서는 'product'라고 부른다.
- Portfolio에는 Product가 포함될 수 있다.
- users can browse the portfolios, and launch products on their accounts.

다시, 위의 Dev Environment를 예시로 들면
- Dev Environment 라는 Portfolio를 정의한다. portfolio에는 다양한 dev environment에 필요한 구성이 product 형태로 정의돼 있다.
  - 예컨대 'Single instance SQS Queue and API Gateway for Project A'
    - launch t2.micro / SQS Queue / API Gateway endpoints, pointing to pre-configured mock lambda functions.
  - 이외에도 CloudFormation이 제공하는 모든 기능을 사용할 수 있다.
    - instance type
    - service configuration
    - proper tagging strategies
    - security guardrails... 등 
- 이렇게 되면, standardized architecture 구성 가능한 building block Recipe가 생가는 셈.

---

#### AWS Control Tower

Automates Accounts Deployment. 비유하자면 AWS Account Vending Machine.
- AWS Service Catalog는 runs within one account.
- AWS Control Tower는 account creation / deploy Service Catalog + 기타 account에 필요한 것들을 account 생성 시점에 세팅.
  - Landing Zone을 설정하면, new account가 생성될 때 자동으로 실행할 CloudFormation을 지정할 수 있다.
  - Manual setting이 필요 없도록 전부 자동화하는 것. = **계정의 접근 권한이나 설정을 Standardize할 수 있다.**


### Customer #4, Solution Overview

<img width="945" alt="스크린샷 2023-08-05 오후 1 31 20" src="https://github.com/inspirit941/inspirit941/assets/26548454/421aa4f1-adfd-4c18-a8ab-0bff2d5f724c">
<br>

최종 구조는 위와 같다.
- Shared Service Account를 생성한다. 일종의 시스템 / Admin 계정인 셈
  - AWS Organization: Configure new Accounts, Security guardrails through SCPs.
  - IAM Identity Center: Single Sign On 기능 제공.
  - AWS CloudTrails: Centralized Logging
  - AWS Control Tower / Service Catalogs: Orchestrate the configuration of new Accounts / Environments
- Service catalog를 사용해서, 생성될 developer account의 infrastructure workload 관련 로그를 CloudWatch Log stream로 전송한다.

위 구조를 적용하기 위한 단계는 크게 세 가지.
- create infrastructure stacks. (IaC)
- workload migration to a new account.
  - IaC와 account deployment 관련한 숙련도 학습이 필요함. 
- database migration to these new accounts.

#### Taking the Architecture to the Next Level

읽기자료
- https://aws.amazon.com/blogs/industries/best-practices-for-aws-organizations-service-control-policies-in-a-multi-account-environment/
- https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html
- https://aws.amazon.com/organizations/getting-started/best-practices/

**SCP 관련**
<br>

사용자가 root 계정으로 모든 걸 처리하고 있었으므로, AWS Organization으로 restrict the use of the root user, across the member accounts. (using SCPs.)
- developer account를 생성했는데 그게 root user 권한이 있으면, 권한 분리 기능이 무력화된다.

Developer Account가 Cloudtrail같은 Shared Service Account에서 정의한 기능을 disable할 수 없도록 한다. (using SCPs)
- Member Account can't disable things like cloudtrail.
- root Organization Unit (OU)에 SCP 지정하면 됨.

Rejecting Console login from IP addresses that are not from office / corporate VPN. (using SCPs' Condition logic)

**Tag Policy: another type of policy**
- Shared Service Account뿐만 아니라, 모든 Member Account에 올바른 Tagging을 붙이는 것. uniformly.
- Enforce tagging schemas / requirements across accounts.
- Tag policy를 SCP에 포함하면, account가 tagging 관련해서 임의로 수정할 수 없도록 막을 수 있다.
  - 유의할 점: tag는 Case-sensitive.

**Enable Billing alarm**
- Shared Service Account로 로그인해서 CloudWatch의 billing 정보를 확인하면 billing per account인 걸 확인할 수 있음.
  - billing alarm per account가 가능하다.

**IAM Identity Center**
- Enable MFA (multi-factor Authentication). username / password 기반 로그인 외에도 authentication 방식을 추가해서 Security 향상하는 것.

서비스가 커지고 복잡해질수록 더 많은 Organization Unit이 생길 거고, 각 OU마다 적용하게 될 SCP가 있을 것임.
- 예컨대 회계를 위한 Account와 개발을 위한 Account는 서로 다른 OU에 속할 것이고, 따라서 적용되는 SCP도 다를 것. 또는 같은 개발자 계정이라 해도 Dev와 Prod OU별로 SCP가 다를 것이다.
- 이 때, Developer Account가 본인이 속한 OU에서 다른 OU로 넘어가는 것을 기본적으로는 제한해야 한다.
  - account의 OU 변경은 진짜 authorized user만 접근할 수 있도록.

### Assessment

