# Module introduction

GCP에서 workload를 돌릴 때, project organize를 위해서 Google Cloud Identity / Access Management (IM or IAM) 을 사용한다. 보통 who can do what을 control하기 위해 사용함.

보통 GCP 자원을 할당하고 정리하는 데 필요한 최소한의 단위는 project. 여기서 대부분 Group related Resource, because they have common business goals.
이런 경우, “Least privilege” is very important in managing any kind of compute infrastructure. (권한을 최소화하는 게 가장 중요하다)
대원칙은, ‘필요한 일에 관련된 권한만을 최소한으로 갖는다’ 

GCP는 IM (Identity management)를 사용해서 권한을 최소화한다. On-premise의 경우 보안을 책임지는 건 사업자 본인이지만, GCP로 들어오면 Lower level of Security는 구글에서 관리한다. 구글 자체의 스케일이 워낙 커서, 사업자 혼자 관리할 수 있는 것보다 리스크를 더 많이 관리할 수 있다. Upper layers of security stack만이 사용자 책임으로 남는다.

---
## GCP Resources hierarchy

GCP Resources는 기본적으로 organized into projects. 또는 folder라는 형태로도 organized된다. 폴더는 다른 폴더를 포함할 수도 있다. (일종의 container)

Resource hierarchy levels define trust boundaries. 계층구조는 Organization Node -> Folders -> Projects -> Resources 순서로 되어 있다. 즉 기본적으로 Folder나 projects는 organization node로 묶여 있다.  

Folder, projects, organization node에는 전부 Policy가 적용될 수 있다.  또한 Policy는 inherited downward 형태로 적용된다.

모든 Resources는 Project에 포함된 채로 존재한다. 즉 Projects는 GCP Service를 활용하기 위한 최소 단위라고 보면 된다. 모든 Project는 분리독립된 개체들이며, (Separate Compartment) 하나의 Resource는 하나의 Project에 소속되어 있다. 

Projects can have different owners / users. They’re built separately, managed separately.

GCP 프로젝트는 name / project ID가 존재한다.
- project id = 프로젝트를 refer할 때 많이 쓰는 human-readable Strings. Permanent, unchangeable identifiers. GCP에서 Unique한 값을 말한다. ‘어떤 프로젝트에 참여할 것인지’를 지정하기 위해 필요한 게 project ID.  (This is chosen by Customer. 코세라 퀴즈에서 언급)

cf. project name = 사용자의 필요에 따라 Assign할 수 있다.
- project number = GCP 측에서 각 프로젝트에 부여하는 번호. 이 수업에서는 다루지 않는 내용이라고 함.

Folders - Optional. 여러 프로젝트를 하나의 그룹으로 묶어야 하는 등의 효과를 낼 수 있다. 사업부서별, 기능별 등. 폴더별로 권한이나 policy를 부여하는 게 가능하다. 또한, 폴더별로 부여된 권한이나 IAM은 그대로 프로젝트에 inherit됨.

유의점: 만약 Folder를 사용할 거라면, Folder들을 그룹핑하는 Organization Node를 top of hierarchy에 두는 것을 권장한다.

일종의 Root node로, Project Creator와 비교하자
- Organization Policy Admin : Broad Control over all cloud resources. 이 권한을 받은 사람만 Policy Change가 가능하다.
- Project Creator : fine-grained control of project creation.

Org node를 어떻게 사용하는가?? -> G Suite를 쓰느냐 아니냐에 따라 좀 다름.
- G Suite 사용자라면, GCP 프로젝트는 자동으로 organization node에 포함된다.
- 그렇지 않을 경우 Google Cloud Identity를 써서 만들어야 함

Org Node를 만들었다면, 폴더를 생성하고 폴더 안에 프로젝트들을 넣는다.

*Less restrictive parent policy overrides a more restrictive resource policy.*

*Policies implemented at a higher level in the hierarchy can’t take away access that’s granted at lower level.* For example, suppose that a policy applied on a project gives user Jane the right to modify a Cloud Storage bucket. But a policy at the organization level says that she can only view Cloud Storage buckets, not change them. The more generous policy is the one that takes effect. Jane can modify the bucket.

Correct! Policies are a union of those applied on resource itself and those inherited from higher levels in the hierarchy. If a parent policy is*less*restrictive, it overrides a more restrictive policy applied on the resource. If a parent policy is*more*restrictive, it does not override a less restrictive policy applied on the resource. Therefore, access granted at a higher level in the hierarchy cannot be taken away by policies applied at a lower level in the hierarchy.


---
## Identity and Access Management (IAM)

IAM = administrators authorize who can take action on specific resources. 사용자에게 특정 리소스 관련 권한을 어디까지 지정할지 결정하는 것.

Who / Can do What / on Which Resources. 세 개로 나뉜다.

- Who : Can be defined either by a Google Account, Google Group, Service Account, G Suite, Cloud Identity domain.

- Can do What : Defined by IAM role. Collections of permission을 의미한다. 일반적으로, 최소 하나 이상의 Permission이 있어야 일할 수 있음. 프로젝트에서 instance 하나를 관리하려면 ‘생성, 삭제, 실행, 중단, 수정’ 등의 권한이 필요하기 때문
따라서, 보통 Permission 몇 개를 모아 하나의 Group으로 설정해, 편하게 관리할 수 있도록 하고 있다. 권한이 부여되는 범위는 who의 대상과 동일하다.

Cloud IAM의 Role은 크게 세 가지다.
- Primitive Role : Broad. *GCP 프로젝트 내 모든 서비스*에 적용 가능한 Role이다.  Affects all resources in GCP projects.
Owner, Editor, Viewer로 구성되어 있다. 
* Viewer : Can examine, but not change its state.
* Editor : Viewer + change its state
* Owner : Editor + manage roles and permissions on resources. Set up Billing도 가능하다.

프로젝트 Resource에는 권한이 없어도, 예산 설정권한은 필요한 사람이 있을 수 있다. 이 경우 Billing Admin Role을 제공할 수 있음.

다만, Primitive Role은 프로젝트가 복잡해질수록 Coarse하다. IAM에서는 fine-grain predefined Role을 제공한다.
Ex) compute Engine의 경우 predefined role을 특정 프로젝트, 폴더, entire organization에 적용 가능하다. *Apply to a particular services in a project.*

그리고, Cloud BigTable이라는 DB Service를 사용할 경우 Across Organization 레벨에서부터 특정 프로젝트에 이르기까지 Role offering이 가능하다.

---
### IAM Roles

직전에 예시를 들었던 Compute Engine에서, predefined fine-grained role 관련 추가설명.

Compute Engine instanceAdmin Role : 권한을 부여받은 machine에 한해서  “listing, reading, change configuration, starting and stopping” 권한이 있음.

여기서 더 finer한 권한이 필요한 경우가 있다. 예컨대 InstanceOperator Role이라는 권한을 정의하고, 이 권한에는 start, stop만을 부여하고 싶다. 이 경우 Custom Role을 사용해야 한다.

Custom Role을 사용할 때의 유의점
1. Need to Manage their Permissions. 
2. Custom Role은 project / organization Level에서만 사용되어야 한다. Folder에서는 사용 불가능. 

만약 사용자 대신 Compute Engine 자체에 권한을 부여하고 싶은 경우? -> Service Account를 사용하면 된다.

예컨대 Application을 GCP로 돌리고 있고 Storage에 데이터를 저장하려고 하는데, Application을 돌리는 Virtual Machine만이 데이터에 접근 가능하도록 설정하고 싶다.
-> Service Account를 만들어서, 해당 VM이 cloud Storage에 접근할 때 Authenticate할 수 있도록 설정한다. Service Account는 이메일 주소 형태로 정의됨. 비밀번호 대신 cryptographic keys를 사용한다.

Service Account도 일종의 Resource이므로, IAM Role의 적용을 받는다.   즉 Resource에 권한 설정하는 것과 동일함. 만약 Alice라는 사람은 관리를 해야 하고 Bob이라는 사람은 보는 것만 해야 하면, 해당 Service Account에 Alice는 editor, Bob은 viewer role을 등록하면 된다.

Different Groups of VMs in your project -> different identities 부여 가능. 권한 변경을 해야 할 경우에는 VM을 새로 만드는 일 없이 권한만 조절해주면 된다.

Ex) project(a)의 one component(1) of your application needs to have an editor role on other project(2), but another component(3) doesn’t.
이 경우, VM (1)은 project(2)에 editor 권한을 갖는다. Editor role까지는 필요없는 VM (3)의 경우 objectViewer access 권한을 부여한다. 여기서 (1)과 (3)은 Service Account를 사용해 권한을 받은 것임. 1과 3이 포함된 project a는 project 2에 privilege가 있는 것.

---
## Interacting with GCP

GCP 사용 방법은 크게 네 가지. Console, SDK & Cloud Shell, Mobile App, APIs.

* 콘솔 : Web-Based administrative interface. App building에서는 사용 가능하고, End user는 접근할 수 없다. View / Manage All Resources  & projects. GCP의 API 서비스 Enable / Disable, Explore도 가능함. 
Cloud Shell도 접근 가능함. 이 경우 GCP의 SDK도 설치 없이 사용 가능.
* SDK : set of tools to manage resources and application on GCP.
	- gcloud tool : main CLI interface for GCP products & Services.
	- gsutil : Google Cloud Storage
	- bq : BigQuery
GCP 콘솔에서 Cloud Shell 버튼을 클릭하면 접근할 수 있다. 웹 브라우저에 모든 커맨드가 설치된 상태로 제공된다. 아니면 로컬 컴퓨터에 SDK 설치해서 쓸 수도 있음. Docker image 형태로도 제공된다.

Restful API도 제공함. (Representational state transfer paradigm). 간단히 말해 웹 브라우저가 서버에 요청하는 것처럼 GCP Service를 사용할 수 있다는 것. json 형태로 데이터 전송.

Console에서 이 API 설정을 on/off할 수 있다. 대부분은 Off 설정이며, quotas, limits가 걸려 있음. 필요할 경우에만 limit을 낮추거나 quotas를 높여 필요한 만큼 사용할 수 있음.

GCP Console에서 API Explorer도 제공. API를 interactively 사용할 수 있도록 하는 Tool. 어떤 API가 사용 가능하며 어떤 파라미터를 필요로 하는지 등등을 Document로 볼 수 있다.

User Code에서 GCP API를 불러오는 일이 번거롭고 귀찮지 않도록 Google에서는 API마다 라이브러리가 있다. 라이브러리는 크게 두 가지.
- Cloud Library : Latest and recommended Library for its API. 각 언어별 Native style과 idiom을 지원한다.
- Client의 Library가 호환이 되지 않는 경우 “Google API Client Library”를 필요한 언어로 제공한다.

모바일 앱 (OS무관) -> examine / manage the resource in GCP. 대시보드 형태로 정보 제공.

---
### Cloud MarketPlace (formerly Cloud Launcher)

GCP를 최소한의 노력으로 시작하려고 할 때 유용한 Tool. 사용자가 직접 Configure할 게 없음. 물론 필요한 경우 세팅을 변경하거나 수정할 수 있다. Cloud Launcher를 사용한다 해도, normal usage를 넘어서지 않는 한 Resource 사용 시 추가비용이 나오지는 않는다. 

users fee를 요구하는 경우는 Launcher에서 사용하는 프로그램이 3rd party with commercially licensed SW일 때. 대신 이 경우 실행하기 전에 예상 비용을 미리 알려준다. (cf. Networking Cost는 사용자가 얼마나 App을 쓰느냐에 따라 달라지기 때문에 따로 예상값을 알려주지 않는다)

GCP는 기본적으로 base image의 SW package에서 발생할 수 있는 critical issue, vulnerability를 해결하기 위한 업데이트를 진행한다. 단, Deploy 이후에는 자동 update를 제공하지 않음. 사용자가 deployed system에 접근할 수 있으므로, 사용자가 직접 maintain해야 한다.

---
## Demonstration, Lab, Activity, Quiz
시연 영상들.

LAMP stack 사용. 웹 개발을 위한 환경을 제공한다고 함.
(AWS EC2 할당받는 것과 유사해 보이는데, 설정을 스스로 할 필요가 없다는 차이점)

시크릿 모드를 사용하는 이유는, 혹시라도 진짜 구글 계정으로 GCP를 사용하는 걸 막기 위해서라고 함.
