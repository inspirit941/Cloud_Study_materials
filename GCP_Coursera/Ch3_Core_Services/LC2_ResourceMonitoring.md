# Resource Monitoring
사실상 stack driver 다루는 파트.
Monitoring / logging / diagnostics for your applications.

<img width="925" alt="스크린샷 2020-01-26 오후 1 32 06" src="https://user-images.githubusercontent.com/26548454/73131333-a77e8400-404c-11ea-89c6-ebf30b394ff5.png">

크게 monitoring, logging, error reporting, tracing, debugging 서비스를 제공하며, 사용한 만큼 돈 낸다. Free usage allotments도 존재함.

수많은 3rd party SW나 Open Source와 호환되는, growing Ecosystem of tech partners.

---
## Monitoring

<img width="927" alt="스크린샷 2020-01-26 오후 1 38 05" src="https://user-images.githubusercontent.com/26548454/73131334-a8171a80-404c-11ea-86f7-4fb666a85bad.png">


Site Reliability Engineering (SRE) 에서 가장 중요한 게 monitoring. SRE 자체가 build, deploy, maintain largest SW system에 매우 중요한 요소 (구글에서 중시한다고 함)

<img width="923" alt="스크린샷 2020-01-26 오후 1 41 15" src="https://user-images.githubusercontent.com/26548454/73131335-a8171a80-404c-11ea-9a70-dcacceb719df.png">


기본적으로 Dynamically configure monitoring after resources are deployed, create chart for basic monitoring activities.

여러 가지 데이터 형태로 Ingest가 가능 (metrics, events, metadata 등). 대시보드나 차트, alert 기능도 지원한다.


<img width="925" alt="스크린샷 2020-01-26 오후 1 43 20" src="https://user-images.githubusercontent.com/26548454/73131336-a8171a80-404c-11ea-855f-15b4a213a746.png">


Root Entity는 Workspace이며, 기본적인 configuration 설정이 가능한 단위. workspace 안에 최대 100개의 monitored project 설정이 가능하다. GCP와 AWS account 가능.

Monitored project의 metric data에 접근이 가능하다.

First monitor GCP project in a workspace == “hosting project”. Workspace를 생성할 때 반드시 지정해야 한다. 이 프로젝트의 이름이 곧 workspace의 이름이 된다.

AWS account에 연결하려면, GCP 프로젝트 내에서 aws connector를 연결해야 한다.

Workspace 자체가 ‘관리하는 모든 project’의 데이터를 토대로 하는 작업이라서, workspace 접근 권한이 있는 사용자는 각각의 프로젝트 데이터에도 전부 접근할 수 있다. 

다시말해 stackdriver role assigned to one person on 1 project -> applies equally to all projects monitored by that workspace. 따라서 권한 분리가 필요하면 여러 개의 workspace를 사용해야 한다.


차트 / Alert 기능 제공. (Alert policy 설정 가능) 특정 조건에 맞으면 알림 가는 것 (네트워크 부하가 기준을 넘으면 이메일이나 SMS를 전송하는 등)


Creating alert에서 권장사항
* alerting on symptoms, not necessarily causes.
* use multiple notification channels
* describing what actions need to be taken / what resources need to be examined.
* Avoid noise. (This will cause alerts to be dismissed overtime) 필요한 것만 alert 써라


Uptime check = test the availability of your service.


Stackdriver monitoring can access some metrics without the monitoring agent. (CPU 사용량, disk traffic metrics, network traffic, uptime information) 이외의 것들에 접근하려면 monitoring agent를 설치해야 한다.

<img width="924" alt="스크린샷 2020-01-26 오후 1 59 27" src="https://user-images.githubusercontent.com/26548454/73131337-aa797480-404c-11ea-890d-dd5e2c466588.png">

Compute Engine / EC2 instance를 지원함

각 instance의 startup script에 install monitoring agent 명령어를 입력하면 됨.


Custom Metrics
만약 stackdriver monitoring에서 제공하지 않는 형태의 metric을 원할 경우, custom metrics를 만들 수 있다. 강의 예시에서는 Python code를 보여줬고, 필요하면 links section 확인하라고 함

---
### Lab

---
## Logging, Error reporting, Tracing and Debugging

<img width="928" alt="스크린샷 2020-01-26 오후 2 17 19" src="https://user-images.githubusercontent.com/26548454/73131338-aa797480-404c-11ea-9a1b-15c9cc2f5b51.png">

Store, search, analyze, monitor, alert on logged data and events from GCP to AWS.

로그 저장, logs viewer 형태의 UI, API manage logs programmatically. 로그 저장 자체는 30일이고, Cloud Storage Buckets / BigQuery, Cloud Pub|Sub topics에 해당 로그데이터를 export 할 수 있다.

BigQuery에 export할 때 -> Analyze logs, visualize in DataStudio.

PubSub에 export할 때 -> stream logs to applications / endpoints.

Monitoring Agent와 마찬가지로, startsciprt에 logging agent를 설치해야 한다. Compute engine / EC2 instance에 설치할 수 있음.

---
### Error reporting

<img width="925" alt="스크린샷 2020-01-26 오후 2 25 40" src="https://user-images.githubusercontent.com/26548454/73131339-aa797480-404c-11ea-9555-cc93f66fdcf1.png">

Centralized Error management Interface -> sorting, filtering capabilities 제공, real time notification when new errors are detected.

App Engine Standard environment에서 generally available, Flexible environment나 Compute Engine, EC2에서도 활용된다.

여러 언어 지원. (Go java Nodejs python ruby php 등)

---
### Tracing

<img width="925" alt="스크린샷 2020-01-26 오후 2 29 12" src="https://user-images.githubusercontent.com/26548454/73131340-ab120b00-404c-11ea-8e6f-20410f4ece42.png">

Latency data from your application + display it on GCP console인 distributed tracing system. Near-real time 형태, Stackdriver traces to generate in-depth latency reports.

App Engine, HTTP load balancer, 기타 stackdriver trace API가 심어저 있는 Application에서 데이터 수집 및 활용 가능.

---
### Debugging

<img width="928" alt="스크린샷 2020-01-26 오후 2 32 37" src="https://user-images.githubusercontent.com/26548454/73131342-ab120b00-404c-11ea-90ed-39bbb972498a.png">

inspect the state of running Application in real time. (정확히는 10ms 정도의 latency 부하가 생긴다 (app state capture 과정에서). Production level에서의 코드 작동방식 / state 분석과 버그 확인 등에 쓰임. 다양한 언어 제공.

---
### Lab

App Engine에서 돌아가는 앱을 토대로 stackdriver 기능 활용해볼 예정

Lab 문제들
- logging Agent를 설치해야 하는 건 Compute Engine뿐이다. (App Engine / Kubernetes 등에는 해당사항 없음)
- Error reporting 서비스는 instances에 전부 제공됨 (compute engine, app engine, kubernetes 등)

---
## Quiz

Trace = latency 측정 및 제공하는 서비스

*Stackdriver integrates several technologies, including monitoring, logging, error reporting, and debugging that are commonly implemented in other environments as separate solutions using separate products. What are key benefits of integration of these services?*
-> Reduce overhead / noise, streamlines use, fixes problems faster.

Stackdriver integration streamlines and unifies these traditionally independent services, making it much easier to establish procedures around them and to use them in continuous ways.

