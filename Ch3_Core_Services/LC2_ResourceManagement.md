# Resource Management
Resource management = controlling cost.

Quota / limit consumption 두 가지 방식이 있음. Default quota는 요청할 경우 증가시킬 수 있다.

---
## Cloud Resource management

<img width="925" alt="스크린샷 2020-01-26 오전 11 45 55" src="https://user-images.githubusercontent.com/26548454/73130469-333be480-403c-11ea-9b44-7bfe96914f48.png">


기본적으로는, IAM을 다룰 때 상정했던 계층구조를 그대로 따른다.
- Policy -> roles + members, set on resources. Resources inherit policies from their parents. 즉, union of parent & resource. 또한 parent policy가 less restrictive할 경우, more restrict한 resource policy를 자동으로 기각한다.

Billing은 bottom up 방식으로 책정된다. 한 프로젝트 내에 부여된 수많은 resource는 각각의 방식 (use rate, number of items, feature use 등) 으로 요금이 걸리고, 이 요금은 프로젝트 단위로 통합된다.

한 프로젝트는 하나의 billing Account와 연동되어 있다. 즉 Organization level에서는 여러 개의 billing acounts를 관리할 수 있다는 뜻.

<img width="926" alt="스크린샷 2020-01-26 오전 11 49 37" src="https://user-images.githubusercontent.com/26548454/73130470-333be480-403c-11ea-807d-4853a719ff68.png">


한 프로젝트가 여러 개의 resource consumption 사용량을 누적해 저장하기 때문에, 프로젝트 그 자체가 Track resources / quota usage 관리에 적합한 편이다. Enable Billing, Manage permissions and credentials, Enable services and APIs.

프로젝트의 uniqueness를 담당하는 3개의 identifier;
- Project 이름 : human readable, not used by any Google APIs.
- Project number : 서버 측에서 생성 -> 부여하는 고유 넘버
- Project ID : unique ID generated from your project name.
- 
GCP console이나 Resource manager API에서 최소 셋 중 하나는 필요함

<img width="921" alt="스크린샷 2020-01-26 오전 11 56 26" src="https://user-images.githubusercontent.com/26548454/73130471-33d47b00-403c-11ea-9003-e2c6a527610a.png">


Resource는 크게 global, regional, zonal로 분류된다.
- Global : image, snapshots, networks.
- Regional : External IP address
- Zonal : instances, disks

이 분류와 무관하게, 어쨌든 전부 project 안에 들어감. 그래서 project 단위로 billing / reporting이 가능함.

---
### Quotas

<img width="923" alt="스크린샷 2020-01-26 오후 12 00 01" src="https://user-images.githubusercontent.com/26548454/73130464-32a34e00-403c-11ea-8309-14befb9eafb2.png">

모든 resource는 project quota / limit의 영향을 받는다.
- 프로젝트에서 얼마나 많은 리소스를 만들어낼 수 있는가.
- API request를 얼마나 많이 보낼 수 있는가 (rate limit)
- region별로 얼마나 많은 resource를 사용할 수 있는가.

GCP 사용이 확대될수록, quota 자체도 서서히 증가한다. 필요에 의해 많이 늘리고 싶을 경우 설정할 수 있음. (Proactively request is available.)


어차피 자동으로 조절도 되고 필요하면 늘려주는데도 Quota가 필요한 이유??

<img width="926" alt="스크린샷 2020-01-26 오후 12 06 40" src="https://user-images.githubusercontent.com/26548454/73130465-32a34e00-403c-11ea-9a41-6d4cd6b967ae.png">

- 에러든 외부공격이든, 필요 이상의 consumption 방지용
- billing spikes / surprise 방지
- size consideration / periodic review 강제하는 역할 (cheaper / smaller alternative가 존재하진 않을지 고민하게 만드는 것)

(quota의 존재 의미 자체가 ‘resources가 항상, 무한히 available한 게 아니라는 시그널이기도 함. 만약 해당 region에서 더 이상 SSD를 만들 수 있는 상태가 아니라면, quota가 남아 있어도 해당 region에서는 더 이상 자원을 할당받을 수 없음)

---
### Labels and Names

Project / folder 단위로 resource segregation이 이미 적용되어 있다. 만약 more granularity가 필요하다면? = label, name 사용 가능.

<img width="929" alt="스크린샷 2020-01-26 오후 12 22 47" src="https://user-images.githubusercontent.com/26548454/73130466-32a34e00-403c-11ea-9b2a-0274e2fc816c.png">


Label = key : value pair that you can attach to your resources. GCP console이나 manage API, gcloud 등으로 생성할 수 있다. 각각의 resource당 최대 64개의 label 생성이 가능함.

script에서 analyze costs / run bulk operations on multiple resource 용도로도 활용 가능.

사용 권장 예시들
<img width="924" alt="스크린샷 2020-01-26 오후 12 25 33" src="https://user-images.githubusercontent.com/26548454/73130467-333be480-403c-11ea-9626-07957a4fa62a.png">

팀이나 cost 관리 단위로 label을 설정하거나, components 구분 기준으로 사용할 수 있는 등등.

cf. Label과 tag를 혼동해서는 안 된다.

<img width="923" alt="스크린샷 2020-01-26 오후 12 27 19" src="https://user-images.githubusercontent.com/26548454/73130468-333be480-403c-11ea-9dac-c04a6914688c.png">

Label은 user-defined strings in key-value format. Organize resources across GCP 용도로 쓴다. 여러 resource에 전부 적용 가능하며, Billing 용도로 쓰임

tag은 user-defined strings -> instance only. 보통 networking (firewall rules 적용할 때 등) 용도로 쓴다. 


---
### Billing

budget을 설정할 수 있다. 얼마나 spending이 증가하고 있는지 확인 가능해짐.

Budget alert -> 특정 수준 이상으로 자원을 쓸 경우 알림. Email 같은 걸로. 또는 특정 기준 이상으로 사용량이 ‘넘어갈 것 같은’ 경우에도 알림 보내도록 설정할 수 있다.

Email 말고도 Cloud pub | sub notification을 사용할 수 있다. 여기에 cloud function을 더해서, pub | sub로 nofitication이 올 경우 automate cost management가 가능하도록 작업할 수도 있음.

또는, 직전에 설명한 Label을 활용해 GCP cost optimization이 가능함.
Ex) 여러 continent에 흩어져 있는 instances -> continent 다른 애들끼리 서로 발생시키는 traffic == cost다. 이 경우 instance의 relocation으로 비용을 낮추거나 caching service (Cloud CDN)로 network usage를 낮출 수 있을 것.

강의에서는 labeling resources / exporting your billing data를 BigQuery에 올려서 다루는 걸 추천함. 쿼리 만드는 것도 쉽고, visualization (DataStudio) 도 가능.

---
### Billing admin

보안문제로 lab은 없고 그냥 설명하고 넘어감

---
### Lab

BigQuery 접속 -> 프로젝트 선택 -> create dataset.

구글 cloud storage에 있는 데이터를 create table 형태로 불러온다.

그냥 storage에 있는 csv 파일 불러온 다음 bigQuery에서 SQL 명령어 날리는 게 전부.


---
### Quiz

유의점

Budgets in GCP are not a way to prevent spending or stop resources. They are a tool for raising awareness about the consumption of resources so that a business can implement its own consumption management processes.

---
