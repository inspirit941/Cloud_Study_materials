# Cloud IAM
Email-like address names, job-type role in granular permission.

## Cloud IAM

Who can do What, on which resources를 정의한 것.
- Who : Person, Group, Application 전부 해당한다.
- What : Privilege / Action
- Resource는 모든 종류의 GCP 서비스.

Cloud IAM Resource의 계층구조를 토대로 IAM 적용가능한 객체를 파악할 수 있다.

상위 -> 하위 순으로 각각
Organization Node -> Folders -> Projects -> Resources 순서.
각각의 Resource는 하나의 Parent만을 갖는다.

모든 계층 Level에서 policy 지정이 가능하며, policy란 set of roles + role members를 지칭한다. Resource inherits policies from their parents.


1. Organization Resource == your Company. 
2. Folder == your Department. 
3. Projects == trust boundary within your company. Services within same project은 default level of trust.

Policy hierarchy는 resource hierarchy를 따른다. 리소스 구조가 달라지만 policy 구조도 변경된다. 만약 특정 프로젝트의 Organization을 변경하면, 변경된 Organization의 Cloud IAM을 따른다.

*child policies cannot restrict access granted at the parent level.* 만약 Folder Level에서 editor role을 주고 해당 폴더의 하위 프로젝트에는 viewer role을 부여했다면, 이 사람은 프로젝트의 edit 권한을 갖고 있다.

따라서 웬만하면 follow the principle of least privilege. (Identities, roles, resources 전부 해당되는 내용) 가능하면 select the smallest scope that’s necessary for the task.

---
### Organization 

1. Organization : Root Node in the GCP resource hierarchy.

- Organization Admin : Control over all cloud, resources. (예컨대 모든 프로젝트의 관리자 권한을 부여할 수 있음. Auditing에 유용함)
- Project Creator Role. Organization level에서 이 역할이 부여되면, 해당 Organization 내 모든 프로젝트에도 inherited된다.

Organization Resource -> Created and provisioned when a G suite, Cloud Identity account creates GCP projects. G suites / Cloud Identity 계정은 Super Admin 권한을 부여받는다.

Super Admin / Organization admin = setup process와 lifecycle control for the Organization resources에서 핵심적인 기능.

* Super Admin
-> Super Admin을 가진 계정이 Organization admin role을 특정 사용자에게 부여할 수 있음.
-> Be the point of contact in case of recovery issues.
-> Control the lifecycle of G suite / Cloud Identity account and Organization resources. 

* Organization Admin
-> defines IAM role.
-> determine structure of resource hierarchy.
-> delegate responsibility over critical components (networking, billing, resource hierarchy through IAM roles.)

“Least privilege” 원칙상, 다른 종류의 permission (creating Folders같은)은 없다. 다른 종류의 권한을 얻기 위해서는 additional role을 해당 account에 부여해야 함.


2. Folders : viewed as sub organization within the Organization.

Additional grouping / isolation boundary btwn projects 역할을 담당한다. 회사 구조나 특징에 따라 세분화하거나 계층구조를 추가로 생성할 수 있음.

Delegation of administration Rights도 담당한다. Department 폴더가 있고 그 아래 Team 1, 2, 3… 등의 subfolders가 존재한다면,  department는 하위 Team Folders가 가지고 있는 모든 GCP resource의 통제권한을 받을 수도 있는 셈. 
반대로, 특정 Folder와 그 하위 folders에만 resource 접근권한을 부여하는 식의 limit access도 가능하다.

* Other Resource Manager Roles
[image:16A837D2-FDD2-4007-BBF2-64346C3A5911-491-0000772825CD991A/스크린샷 2020-01-23 오후 12.48.45.png]


---
### Roles

3 Types of Roles in Cloud IAM.

1. Primitive Roles : 기본적으로 GCP console에서 제공되는 role.  상당히 포괄적인 권한을 가지고 있음. GCP 프로젝트에 적용할 경우, 해당 프로젝트의 모든 resources에 영향을 미친다. 때문에 fixed, coarse-grained level of access에서 주로 필요함.

크게 Owner, Editor, Viewer가 있고, Billing Admin이 따로 존재함.
- Owner = Full admin access. Add / Remove Members & delete project 가능
- Editor = Modify / delete access. 개발자가 deploy / modify / configure resources할 수 있는 용도
- Viewer = read only.

Concentric한 특성. 즉 Owner는 editor 권한이 포함되어 있고, editor는 viewer 권한이 포함되어 있다.

- Billing Admin : manage billing / add or remove admin (without the right to change the resource in the projects.)

2. Predefined Roles : granular access to specific GCP resources & prevent unwanted access to other resources.

Collections of Permission이라고 봐도 된다.

[image:AED6303C-3076-4430-8729-4590A581E477-491-000078678B8BCD2C/스크린샷 2020-01-23 오후 1.11.19.png]

IAM으로 특정 프로젝트에 InstanceAdmin Role을 부여했다고 할 때, 이 role은 결국 compute engine을 다룰 수 있는 여러 가지 permission의 집합이 된다. 이 permission은 API 형태.

Compute Engine에서 제공하는 몇 가지 predefined Role.
	
	1. Compute Admin : Full Control of Compute Engine resources.
	2. Network Admin : Permission to CRUD networking resources Except for Firewalls, SSL certificates. (Firewall, SSL, ephemeral IP address는 read-only)
	3. Storage Admin : Permission to CRUD disk, images, snapshots. (Project의 editor Role은 부여하고 싶지 않지만 project image 관리 권한은 필요한 경우 등)


3. Custom Role : Finer-grain Role. 
Ex) Compute Engine을 CRD하는 건 가능하지만, re-configure 작업은 허용하고 싶지 않을 경우

---
### Demo : Custom roles.

Start / Stop Compute Engine, not reconfiguring it.

GCP console에서 roles 파트 -> create role 클릭. 이름 정하고 Add permission 클릭해서 필요한 role만 부여하는 게 가능하다.


---
### Members

5 types of members; Google Account, Service Accounts, Google Groups, G suite Domains, Cloud Identity Domains.

- Google Account : Developer, administrator or any other person who interacts with GCP. 구글 계정과 연동된 이메일만 있으면 Identity 취급을 받을 수 있다.
- Service Account : Belongs to your application, instead of to an individual end user. 예컨대 GCP host인 code를 실행하려면, 어떤 service account로 코드를 실행할 건지 지정해야 한다. 
Application의 logical component 구분을 위해 Service Account를 여러 개 생성하는 것도 가능하다.
- Google Group : named Collection of Google Account + Service Account. 그룹마다 대응되는 unique email address가 필요하다. Access policy를 여러 명의 사용자에게 동시에 적용해야 할 때 특히 유용하다.
- G suite Domains : organization의 internet domain name 지정.  (example.com 같은 형태). 사용자를 G suite domain에 추가할 경우, new Google Account가 가상의 group에 등록된다 (ex) username@example.com 형태)
- GCP 사용자 중에 G suite 사용자가 아닌 경우는 Cloud Identity를 써서 동일한 결과를 얻을 수 있다. Lets you manage users in group using Google Admin Console.  (대신 G suite에서 제공하는 products - Gmail, docs, Drive, Calender는 사용 불가능.)

Cloud Identity는 Free / Premium 두 가지가 있음. Premium의 경우 Mobile device Management 기능이 있다.

*You cannot use Cloud IAM to create or manage your users or groups.* Cloud Identity나 G suite를 사용해야 한다.

-> 그럼, 만약 다른 형태의 corporate directory가 이미 있는 경우엔? GCP에 그대로 적용할 방법은 없는가?

이런 경우 
- Google Cloud Directory Sync를 사용할 수 있다. 
Admin can log in & manage GCP resources with same username & password. 
From existing Active Directory or LDAP system -> users / groups in your Cloud Identity Domain. 
Scheduled one-way Sync이므로,  Google Cloud Identity에 적용될 때 no information in your Active Directory / LDAP map is modified. Synchronization이 끝난 후에야 rules are set up.

- Single Sign-on Authentication. 
이미 사용하는 identity system이 있으면, SSL configure만 맞추면 구글에서도 계속 사용 가능하다. authentication이 필요하면 구글에서 identity system 쪽으로 redirect되며, 해당 시스템에서 authenticate 완료되면 구글 시스템에도 접근이 가능하다.

기존 시스템이 SAML2, SSO configuration을 사용한다면 링크 세 개로 작업이 가능할 만큼 쉽고, 그렇지 않을 경우 3rd Party System (ADFS, Ping, Okta)를 쓰면 된다.

GCP account를 생성하지만 gmail 말고 다른 계정을 메일알림을 받는 것도 가능하다.

---
### Service Account

Service Account : account belongs to your application instead of to an individual end user.

Server - to - Server interaction in a project without supplying user credentials. User account에 담긴 credential을 application 어딘가에 저장하는 게 아니라, 필요한 credential을 주고받기 위한 계정을 Service Account에 걸어놓는 것.

Account 자체는 이메일 형식으로, 3 types 존재.
- User-created or Custom
- Built-in
- Google API service Account

All projects come with the built-in Compute Engine default service Account. 

Default service Account를 제외하면, GCP API service Account를 사용한다. 보통 (project-number@cloudservice.gserviceaccount.com) 이메일 형태로 되어 있음. 얘는 internal Google processes on your behalf을 위해 만들어진 계정이고, 보통 editor role을 받을 경우 주어진다.

Custom Account는 flexibilty가 좀 더 높다. 원하는 만큼 만들 수 있고, Access scopes나 Cloud IAM role을 지정하고, 필요한 instance에 부여하면 된다.

*Default Compute Engine Service Account*

- project-number@developer.gserviceaccount.com 형태. Editor role을 부여받을 경우 자동으로 제공된다.
- 새 instance를 실행할 경우 service account가 자동으로 enabled된다. 필요하면 이 account를 override by another service account / disable service account for the instance. 


Authorization is the process of determining what permission an authenticated identity has a set of specified resources.
(어떤 identity가 어떤 resource에 permission을 가지고 있는지 호확인하는 작업)

[image:1CC7C596-DD5B-4A69-BDB0-F2D40F70E726-491-00007DB7A4E88925/스크린샷 2020-01-23 오후 2.54.15.png]

- Scopes = whether an authenticated identity is authorized. 보통 authenticated Identities / service account를 가지고 있으면 된다.

예컨대 application A, B 둘 다 Cloud storage buckets를 사용하려 한다고 가정하면
- 각각 Google authorization Server에 요청을 보내고, access token을 받는다. A는 read-only scope를, B는 read-write scope를 받게 된다.

Default service account를 사용하면서 scope를 customized하는 것도 가능하다. Default Service Account에는 Scope를 사용하지만, user-created service Account라면 Cloud IAM role 사용하는 걸 권장한다.
또한, default service Account는 primitive / predefined role 기능을 제공하는 반면, user-created service Account는 predefined role만 가능하다.

Roles for service Account -> assigned to groups or users 형태로도 사용 가능하다.
뭔 소리냐면
1. Service Account를 생성하고, instaneAdmin Role을 부여했다고 가정하자. Permission to CRUD VM or disk가 가능함.
2. 이 Service Account 자체를 하나의 resource처럼 취급하는 거다. decide who can use it by providing users or a group with the service account user role.
3. 이걸 부여받은 사용자는 사용자이지만 Service Account계정을 활용해서 작업을 수행하는 것.

Service Account 계정을 받은 User는 Service Account가 접근할 수 있는 모든 resource를 그대로 부여받는다. 권한 부여에 조심해야 함. 

Q. Google Account도 있고, Google Account 자체도 그룹핑이 가능한데 왜 굳이 User에게 service account를 그룹핑해서 주는 건가. 이득이 뭐지

[image:A0F08ECD-0B78-4D26-BFB1-7E696B8A1C3E-491-00008012E886921B/스크린샷 2020-01-23 오후 3.36.34.png]


Service Account 1 : project A 소속, project B의 resource에 editor 권한이 있음
Service Account 2 : project A 소속, viewer 권한.

이 경우 굳이 scope를 조정하기 위해 VM을 다시 만들 필요 없음. Cloud IAM에서 project를 microservice 단위로 구별했기 때문. 서로 다른 resource에 접근하려면, 각각 다른 service account를 만들고 권한을 부여하면 된다. credential은 GCP 측에서 이미 관리하고 있는 중.

users는 username + password를 사용하지만, Service Account는 authenticate를 Key로 한다. 이 key에도 두 가지 방식이 있음. GCP-managed, User-managed. 

GCP-managed key는 GCP service에서 사용하는 key. Compute engine / app engine 등등.

[image:14F630A2-8E70-4E02-ABF3-3CB5200CE21B-491-0000806558A8A189/스크린샷 2020-01-23 오후 3.42.30.png]

---

### Cloud IAM best practices


---
### Lab : Cloud IAM

Console에서 IAM 파트 -> 현재 어떤 계정들이 어떤 permission을 가지고 있는지 확인 가능.

cf. project Viewer role이 없으면 콘솔에서 해당 프로젝트에 걸려 있는 resource를 볼 권한이 없다. 하지만 storage object viewer라는 제한된 권한을 가지고 있으면, gcloud창에서 gsutil ls gs:// 형태로 storage 자체는 볼 수 있다.

처음에 add members를 할 때, 프로젝트 단위로 new member를 집어넣기 때문. 프로젝트 자체에 접근권한이 없는 건 아니다.


Service Account 계정 생성 = IAM 창에서 service account 클릭. 계정이름 생성하고 permissions 설정 후 생성.
이 계정에 들어갈 user 입력.

You will grant the user the role of Service Account User, which allows that person to use a service account on a VM, if they have access to the VM.
You could perform this activity for a specific user, group, or domain.

Service Account에 적용될 user명 (예시에서는 Altostrat.com)을 add member로 추가한 뒤, IAM에 add member로 Altostrat.com에 compute instance Admin 권한을 준다.

그 후 VM을 만들 때 service account 부분에 default 말고, service account 생성할 때 만든 계정이름을 선택한 뒤 생성한다.

인스턴스를 생성한 뒤 ssh로 로그인한다. (나는 여기서 ssh connection error로 cmd창 접근이 안됐다. 뭐가 문젠지 모름)

여튼 ssh로 접근할 때, 인스턴스 생성 시 정의한 service account로 들어가는 것. 따라서 이 cmd창에서 `gcloud compute instance list`, `gsutil cp gs://yourbucketname/sample.txt .` 같은 “storage Viewer role”을 넘어선 명령어는 허용되지 않는다.

Because you connected via SSH to the instance, you can “act as the service account,” essentially assuming the same permissions.The service account the instance was started with had the Storage Viewer role, which permits downloading objects from GCS buckets in the project.To list instances in a project, you need to grant the compute.instance.list permission. Because the service account did not have this permission, you could not list instances running in the project. Because the service account/did/have permission to download objects, it could download an object from the bucket. It did not have permission to write objects, so you got a “403 access denied” message.

---
## Quiz

What abstraction is*primarily*used to administer user access in Cloud IAM?

-> Roles, an abstraction of job roles.

Cloud IAM administration uses pre-defined roles for administration of user access. The roles are defined by more granular permissions. But permissions are not applied to users directly, only through the roles that are assigned to them.


