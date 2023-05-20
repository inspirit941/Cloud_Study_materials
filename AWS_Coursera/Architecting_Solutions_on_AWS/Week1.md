## Designing a serverless web backend on AWS

Solution Architect가 되었다고 가정하고, customer의 요구사항에 맞게 어떤 AWS Service를 어떻게 조합하면 되는지를 소개하는 방식으로 강의가 구성됨.

<br>
<img width="1066" alt="스크린샷 2023-05-06 오후 4 08 42" src="https://user-images.githubusercontent.com/26548454/236608990-7538d00f-053d-48a9-8c80-84759eb8e7c6.png">
<br>

Overall Solution을 제공하기 위해 여러 AWS Service는 building block이 됨. 이걸 잘 구성해서 사용자의 요구사항에 맞게 제공하는 게 목표.
- 그래서 실제로 block을 앞에 두고 설명함
- Building Correct Solution이 아니라, Designing one of the Potential Solutions.

AWS Architecture Center: https://aws.amazon.com/architecture/?cards-all.sort-by=item.additionalFields.sortDate&cards-all.sort-order=desc&awsf.content-type=*all&awsf.methodology=*all&awsf.tech-category=*all&awsf.industries=*all <br>
AWS Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html

### Customer 예시 1. ECommerce 회사, migrate some workload to AWS

- 이전까지는 lift-and-shift 정도의 migration 방식으로 AWS 사용.
- Cloud-native way로 Rewrite할 생각이 있는 상태. 왜 lift-and-shift 대신 Rewrite?
  - Operation Overhead를 낮추고 싶어함.
  - business logic이 전부 하나의 order Service에 tied up된 상태. - slow / overwhelmed fail이 발생하는 상태.
    - on-prem에서 scaling하기 힘들어서 automate scaling 기능을 쓰고 싶음.
  - 서비스 간 tied up이 심해서, 하나 fail나면 다른 것도 영향을 받음
    - orders data의 Inconsistency 유발.
  - cloud-native하게 변경하기 위한 code rewrite 용의 있음
- 서비스 자체의 특성
  - spiky demand 있음 (promotion launch같은 이벤트)
- 기타 요구사항
  - monitoring / logging to be easy to put in place.
  - 모든 서비스가 same logging system을 사용했으면 좋겠음.
  - cost / performance optimize as much as possible.

#### Requirement Specification

<img width="1073" alt="스크린샷 2023-05-06 오후 4 28 07" src="https://user-images.githubusercontent.com/26548454/236609844-de38c4f5-3dea-4464-a2a5-ecaee15e4946.png">
<br>

Application hosted on-prem -> service-oriented Application hosted on AWS.
- 몇몇 서비스는 이미 Migrate완료, Order Service 부분의 migration 요청. Order Service는 multiple functions이 하나의 Monolitic codebase처럼 동작함.

요구사항
- Reliable / Resilient. 서비스 하나가 Fail나더라도 다른 곳에는 영향을 주지 않도록.
  - downstream call이 one code package에서 호출됨... SPOF. loosly coupled 되도록 변경 필요
- Managed Scaling -> Serverless 방식이 유용함.
- Decouple solution components to maximize resilience (SPOF 방지)
  - Event-Driven 방식을 적용하면 좋을 듯.
  - order processing / acceptance... 와 같은 downstream call을 Independent하게 만드는 것.
- Centralized Monitoring & Logging - serverless 서비스는 Cloudwatch로 통합되어 있어서 별 문제 아님.
- Optimize for cost, performance, efficiency, operational overhead.

### Architecting the Solution

<img width="1076" alt="스크린샷 2023-05-07 오후 2 06 10" src="https://user-images.githubusercontent.com/26548454/236658788-8e9229e2-a71b-4f49-9481-eef980be708a.png">
<br>

on-prem에서 동작하는 Web Server는 Customer DataCenter에서 VM으로 동작중.
- AWS에서 제공하는 Compute Service 종류를 확인 https://aws.amazon.com/ko/products/compute/
  - instance (VM) 서비스는 Serverless 종류가 아님.
    - VM 발급받고 lift-and-shift하면 간단하지만, best fit solution인지는 고민해야 한다.
  - Containers
  - Serverless
  - ...

<img width="1081" alt="스크린샷 2023-05-07 오후 2 10 42" src="https://user-images.githubusercontent.com/26548454/236658942-cf8fb65a-f292-484e-ac9c-bcda3de1d576.png">
<br>

Container 서비스에서 Fargate도 요구사항에 부합하는 옵션이다. 대신, Container 기술을 사용자가 도입할 의사가 있는지는 체크해봐야 함
<br>

Lambda는 cloud-native solution으로, operational overhead가 EC2 대비 매우 적다.
- Request / Event가 들어오면 Spins up its own instance of a lambda function.
  - lambda function runs in a microVM, powered by "FireCracker"
  - microVM will be shut down after a period of time.
  - 즉 only runs when it needs to run.

강의 예시에서는 Customer쪽에서 container 기술에 익숙하지 않은 상태이고, DynamoDB나 Lambda 같은 cloud-native serverless는 migration 과정에서 조금씩 익숙해지고 있다고 함. 따라서 lambda 사용하기로.
<br>

#### Computing service

<img width="1082" alt="스크린샷 2023-05-07 오후 2 18 48" src="https://user-images.githubusercontent.com/26548454/236659228-26fe2648-a8aa-4225-bdea-3dd3b1890c4a.png">
<img width="1077" alt="스크린샷 2023-05-07 오후 2 19 09" src="https://user-images.githubusercontent.com/26548454/236659229-cfb6158b-88bd-447c-9edb-0264f60a7076.png">
<br>

Lambda를 사용할 경우, 함수를 호출할 trigger(event)가 정의되어 있어야 한다.
- API Gateway가 이 경우 적절함. 어떤 http path / method로 요청이 들어왔을 때 함수를 실행할 것인지 결정할 수 있다.
- API Gateway에서 Authentication / Authorization 적용 가능. 소스코드로 직접 구현할 필요가 없어진다.
- API Gateway / Lambda 둘다 cloudwatch로 metric, log 전달이 가능하다.
- 둘다 managed scaling 가능.

<img width="1068" alt="스크린샷 2023-05-07 오후 2 47 25" src="https://user-images.githubusercontent.com/26548454/236660051-bb873bf2-89b4-44a1-84cf-54cc16cb5f74.png">
<br>

Lambda에 trigger를 추가하는 화면.
- AWS 사내 프로덕트는 프로덕트명으로 연결 가능.
- EventBridge는 AWS의 Event bus로, 클라우드 외부 3rd party 서비스에서 발생하는 이벤트를 받을 수 있도록 지원하고 있음.

<br>
<img width="1075" alt="스크린샷 2023-05-07 오후 2 59 41" src="https://user-images.githubusercontent.com/26548454/236660481-20081c37-c0c9-4da9-8312-7a3cd336732e.png">
<br>

Lambda 설정화면의 Tag
- key-value pair
- billing / filtering resources / tracking costs 등에 활용 가능

<br>
<img width="1037" alt="스크린샷 2023-05-07 오후 3 01 04" src="https://user-images.githubusercontent.com/26548454/236660545-67f1efef-beab-4f59-a387-ce2870f95d5e.png">
<br>

logs 항목은 기본적으로 enabled되어 있다. 
- cloudwatch로 다양한 종류의 로그를 전송함
  - runtime logs (invoke)
  - application logs


#### Database

customer는 mysql DB를 쓰고 있으며, managed scaling & reducing operation cost가 요구사항.
- https://aws.amazon.com/ko/products/databases/ 로 서비스중인 DB 서비스 목록을 확인해보자

<img width="1006" alt="스크린샷 2023-05-07 오후 3 07 27" src="https://user-images.githubusercontent.com/26548454/236660760-2d700b72-2ad5-46fb-b6f1-9277545caaeb.png">
<br>

- Relational DB : RDS, Aurora (Serverless option 제공하는 RDB), RedShift (Data Warehousing)
- key-value : DynamoDB (serverless)
- in-Memory: caching용 서비스
- Graph 같은 특수목적용 DB도 있다.

Serverless 제공하는 Aurora / DynamoDB를 비교하면
- Aurora: RDS based. Massive Scaling / high Performance 지원. Large Workload for Enterprise. MySQL / PostgreSQL과 호환됨.
  - RDS는 사용자가 DB instance 관련 옵션을 설정할 수 있음. Aurora는 Serverless 방식.
  - Elastic in Nature. pay only for capacity consumed -> spiky workload에서 유용함

- DynamoDB: non-Relational DB. Massive Scaling / high Performance 지원.
  - key-value store이며, high level of Conccurrent users 지원.
  - Managed scaling (Under the hood에서 전부 해결됨), Low operational Overhead


<br>
<img width="1078" alt="스크린샷 2023-05-07 오후 3 48 55" src="https://user-images.githubusercontent.com/26548454/236662380-8665bbc2-0cfe-4f31-8e05-fe6c06e79fd0.png">
<br>

요런 경우는, user application의 usage pattern / throughput needs을 보고 결정하는 게 효율적이다.

- Provisioned mode: how much data you read/write per sec.
- On-Demand mode: demand 변화에 따라 Scale changes.

spiky demand에 부합하는 건 on-demand. 이 경우, query pattern을 생각해봐야 한다. 서비스에서 사용가능한 Query 종류가 다르기 때문.

<br>
<img width="1080" alt="스크린샷 2023-05-07 오후 3 57 25" src="https://user-images.githubusercontent.com/26548454/236662714-234a4898-0ed6-4dde-9a05-b424a5067cb9.png">
<br>

DynamoDB
- multiple table로 생성할 수 없음. (standalone table)
- built-in Join query across multiple table은 제공되지 않음.
  - index 써서 조회 성능을 높이는 방식
- Data modeling should be done before table creation

customer 예시로는 order stash 용도로 DB를 사용함. order ID 기준 CRUD, cusomter ID 기준 조회도 가능해야 하는 정도. 

<img width="1083" alt="스크린샷 2023-05-07 오후 4 05 52" src="https://user-images.githubusercontent.com/26548454/236663074-3c8c739d-1c46-4bfe-ae5f-f4927829bb9e.png">
<img width="1082" alt="스크린샷 2023-05-07 오후 4 06 27" src="https://user-images.githubusercontent.com/26548454/236663077-1fee9f50-f0e4-43df-973c-1a32639c4171.png">

RDS 기반 Aurora일 경우, Request burst일 때 수많은 lambda function이 전부 DB에 Connection을 시도하면 DB 문제가 생길 수 있다.
- RDS Proxy 사용해서 Connection Control을 할 수 있지만, 이 경우 사용자가 RDS Proxy라는 서버를 관리해야 함.

DynamoDB는 이런 문제가 없음.
<br>

따라서 이 경우엔 DynamoDB가 사용에 보다 적합하다.

#### DynamoDB Explained

<img width="1022" alt="스크린샷 2023-05-07 오후 4 11 53" src="https://user-images.githubusercontent.com/26548454/236663294-a03ade75-9f00-4882-9407-ccd70579cc77.png">
<br>

- DynamoDB의 items는 RDBMS의 row와 유사한 개념.
  - partiton key: primary key.
  - sort key: partition key만으로 Uniqueness 충족이 어려울 경우 추가함.
  - parition key + sort key는 반드시 Unique.
- attributes는 columns와 유사한 개념.

![스크린샷 2023-05-09 오후 7 17 46](https://github.com/inspirit941/images/assets/26548454/6ae49791-b290-4dff-920b-9f96cd272e1e)
![스크린샷 2023-05-09 오후 7 19 30](https://github.com/inspirit941/images/assets/26548454/02130acc-fdaf-4b26-9aff-15416e6c9dc0)
<br>

default setting은 Provisioned: on-demand가 아님.
- RCU (Read Capacity Unit), WCU (Write Capacity Unit)이 정해져 있음.

Customized Setting 선택 후 Table Class를 결정한다.
- Standard: General-purpose table class.
- Standard-IA: Infrequently accessed data일 때 사용. store data for low cost.

![스크린샷 2023-05-09 오후 7 31 07](https://github.com/inspirit941/images/assets/26548454/2180779e-da67-4f41-845f-b0769fa020c2)
<br>

Read / Write Capacity settings에서 on-demand, provisioned 여부를 선택할 수 있다. <br>
Secondary Index를 사용해서 Full scan 없이 특정 데이터만 조회하도록 만들 수 있다. <br>
Encryption은 AWS가 보유한 key를 쓰거나, AWS managed key를 쓰거나, 사용자 고유의 key를 사용할 수 있다.

![스크린샷 2023-05-09 오후 7 49 51](https://github.com/inspirit941/images/assets/26548454/54150784-8f82-41f4-88b1-78860fedce53)
![스크린샷 2023-05-09 오후 7 51 44](https://github.com/inspirit941/images/assets/26548454/740ad1c1-d253-4dd4-bf1a-609d86cefdf7)
<br>

DynamoDB Streams: Capture item-level changes를 stream으로 전송하는 기능. stream process application에서 처리할 수 있다.

<br>

![스크린샷 2023-05-09 오후 7 52 09](https://github.com/inspirit941/images/assets/26548454/aaf7d76a-f16d-4894-9465-f8e0922d9feb)
<br>

global table
- AWS 다른 region에도 table을 배포, keep in sync.


### Building Event-Driven Architecture

![스크린샷 2023-05-09 오후 7 56 38](https://github.com/inspirit941/images/assets/26548454/421df4a6-ba89-498d-a6d9-7574207f117c)
<Br>

지금까지의 AWS 구조.
- API Gateway - Accept / validation the order request.
- Lambda - Processing.
- DynamoDB - save that order to Table.

이제 필요한 건, order service에서 호출할 downstream service.
- order service에서 특정 이벤트가 발생하면 'Fan out' 방식으로 다른 서비스에 전달될 수 있도록 Event-Driven Architecture 를 사용하는 것이 적절해보임
- https://aws.amazon.com/ko/event-driven-architecture/

<br>

![1-SEO-Diagram_Event-Driven-Architecture_Diagram b3fbc18f8cd65e3af3ccb4845dce735b0b9e2c54](https://github.com/inspirit941/images/assets/26548454/28e583bb-190a-455d-8054-c44f38afabcc)
<bR>

Event-Driven Architecture 구조
- Event Producer
- Event Router
- Event Consumer

이벤트 발생하는 컴포넌트 / 이벤트를 받는 컴포넌트가 분리되어 영향을 받지 않음. 독립적으로 Component scale out 등을 수행할 수 있음.
- Lambda와 DynamoDB는 이미 Event-Driven에 적합한 방식.

발생한 이벤트를 Downstream service에 어떻게 전달할 것인가
- 3개의 서비스에 동일한 이벤트가 전달되어야 함.

사용 가능한 프로덕트는 크게 두 가지.

<img width="1180" alt="Product-Page-Diagram_Amazon-SNS_Event-Driven-SNS-Compute@2x 03cb54865e1c586c26ee73f9dff0dc079125e9dc" src="https://github.com/inspirit941/inspirit941/assets/26548454/1a1005f6-6759-4aef-ad64-3d4a31f746e0">
<br>

#### AWS SNS

https://aws.amazon.com/ko/sns/
- Fully-Managed Serverless Messaging System with Pub/Sub
- publish - subscribe는 1:M 관계, Fan out 가능.
- Optional Filtering based on Attributes
- potential Subscriber: Lambda, SQS, kinesis, http endpoint 등등.

Message Channel의 일종인 Topic을 생성하고, topic에 전달되는 메시지는 Subscriber에게 Fan-out 되는 구조.

<img width="1039" alt="스크린샷 2023-05-14 오후 2 47 11" src="https://github.com/inspirit941/inspirit941/assets/26548454/a17f280e-9ba5-4912-80df-7dad7e67e5df">
<br>

- FIFO: Strictly preserved Order. 
  - 메시지 순서가 중요할 경우 선택
  - Exactly-Once Message Delivery
  - up to 300 publishers/sec.
- Standard: Best-effort message ordering. FIFO보다 메시지 순서 보장이 약함.

Message Queue 서비스인 SQS는 message remain in the queue until they are processed. <BR>
반면 SNS는 message send directly to the subscriber. 메시지를 제대로 전달받았느냐 아니냐는 subscriber의 문제다.

<img width="1034" alt="스크린샷 2023-05-14 오후 2 50 18" src="https://github.com/inspirit941/inspirit941/assets/26548454/a65c2f04-a98d-48de-b28b-0eed36f8b82e">
<br>

Encryption: Enabled by Default. 메시지가 도착하는 대로 암호화 진행, Delivery 전에 복호화됨.

<img width="1032" alt="스크린샷 2023-05-14 오후 2 50 59" src="https://github.com/inspirit941/inspirit941/assets/26548454/7ccc30bd-905e-4652-95a9-f179921682ec">
<br>

Policy: Who can access your topic. JSON으로 지정 가능
- topic에 메시지를 보낼 수 있는 권한은 누구인지
- topic으로부터 메시지를 Subscribe할 권한은 누구에게 있는지

<img width="982" alt="스크린샷 2023-05-14 오후 2 58 21" src="https://github.com/inspirit941/inspirit941/assets/26548454/0103cc3c-6c6e-4ed7-b7b6-fa525003aab7">
<br>

Subscription 생성 - 지원하는 서비스 / 프로토콜 확인 가능.

#### AWS EventBridge

<img width="1180" alt="Product-Page-Diagram_Amazon-EventBridge@2xa 2ef6accf0d9ff4eb0856422599406e022b552073" src="https://github.com/inspirit941/inspirit941/assets/26548454/64cdba03-5ce8-4a54-8926-b5678b5543bb">
<br>

https://aws.amazon.com/ko/eventbridge/
- Serverless Event Bus that Connects applications using events
- SNS보다 지원하는 event source / target (subscriber) 종류가 많음.
  - 서드파티 애플리케이션 / SaaS 포함.
- Message Filtering by Rules. -> SNS보다 상세한 filtering이 가능함.
  - 서비스가 받아야 하는 메시지 종류가 매우 많고, 그 많은 메시지마다 Consumer를 정확히 지정해야 할 경우 유용함.
- Schema Registry 지원
  - title, format, validation rules for event data.
  - 메시지의 structure 정의할 때 유용하다. 특히 메시지 schema 구조가 다양한 서드파티 앱일 경우.

SNS보다 기능이 많고 powerful하다고 볼 수 있으나, 요구사항을 토대로 요구수준을 유추해보면
- Event 종류는 한 가지.
- Cost / Simplicity 고려하면 SNS가 EventBridge보다 유용함.

따라서 이 경우 SNS를 선택하는 편이 좋을 것 같다.

<br>

##### EventBridge vs SNS

EventBridge: SaaS Service나 AWS Service로부터 이벤트를 받아 처리하는 용도.
- only event-based service that intergrates directly with 3rd party SaaS AWS Partners.
- 90여 개의 AWS Service에서 발생하는 이벤트 받아서 사용 가능.
- defined / JSON-based structure for events
- Rule 사용해서 특정 event forwarding하는 등의 작업 가능.
- Target으로 지정할 수 있는 서비스는 currently 15개.
  - Lambda, SQS, SNS, Kinesis Data Streams / Firehose...
- serverless -> **Limited throughput, request양에 따라 증가함.**
- latency는 0.5초 정도.

SNS: **high-throughput, low-latency messsage** that are published by other application / microservices.
- nearly unlimited throughput / high fan-out (endpoint 수천~수백만까지)
- messages are unstructured (can be in any format)
- Target으로 지정할 수 있는 서비스는 currently 6개.
  - Lambda, SQS, HTTP/S endpoint, SMS, mobile push, email
- latency는 보통 30ms
- AWS service 30여 종(EC2, S3, RDS ... )이 SNS를 지원함.

<br>

#### DynamoDB Streams

남은 과제는 DynamoDB -> SNS 로 이벤트 전달을 어떻게 할 것인가?
- DynamoDB Stream과 AWS Lambda를 사용할 수 있다.
  - DynamoDB Streams: DynamoDB Table 단위로 Enable 설정 가능.
- 테이블에 변경사항이 발생하면, event captured in an ordered flow of information (= Stream) 이 생성됨.
- 이 Stream 데이터를 trigger로 받아서, AWS SNS에 전달하는 Lambda 함수를 생성하면 된다.

captures time-ordered Sequence of item-level modification in any DynamoDB table, and stores this information n a log for **up to 24 hours**.
- DynamoDB의 변경사항을 거의 실시간으로 확인할 수 있음.
- Each stream record **appears exactly one time** in the stream.
- 비동기로 동작하므로, DynamoDB table performance는 영향을 받지 않는다.


<img width="1065" alt="스크린샷 2023-05-14 오후 2 42 51" src="https://github.com/inspirit941/inspirit941/assets/26548454/2ef16858-c7be-4bd8-b5a3-55f317e53e1b">
<br>

이렇게 만들어진 구조의 장점?
- Sending message to Downstream Service는 Order Process 바깥에서 이루어진다. **Decoupled**
- 새로운 Downstream 서비스를 추가하거나, 기존 서비스를 제거할 때도 코드 변경 없이 수행할 수 있음.

### Decoupling AWS Solutions

SNS 서비스를 도입하면서 서비스 간 Decoupling 문제는 어느 정도 해소함. <br>
하지만 latency issue with the order-acceptance component of the application 을 확인해야 한다.
- 기존 방식은 Sync 구조. -> slow, too long to complete
  - accept, validate, process, store in DB, call downstream service가 
  - 하나의 request 안에서 
  - user가 response를 받기 전에 전부 이루어진다.

<img width="1050" alt="스크린샷 2023-05-20 오후 1 29 00" src="https://github.com/inspirit941/inspirit941/assets/26548454/25033768-535f-41c8-8541-9d6a52274b56">
<br>

async architecture로의 전환.
- Storage-first pattern: API Gateway가 request accept / validate 수행 후, lambda를 바로 호출하는 게 아니라 storage로 request를 전송함.
- 사용자는 'request가 접수되었다'는 응답을 빠르게 받을 수 있고, lambda는 storage에서 새로 들어온 데이터를 확인해서 요청을 처리하는 방식.

API Gateway를 사용할 경우 이 방식이 나쁘지 않다.
- apigw 자체에서 제공하는 기능이 많으므로, offload some of the work from your backend compute layer to your API 
  - authenticate request, validate, transforming payload 같은 것들
- apigw에서 제공하는 기능을 사용하고 사용자에게 즉각 응답하는 것 - latency 감소.
- apigw에서 다른 aws service로의 연동이 쉽다. 굳이 lambda로 로직을 작성하지 않아도 가능한 것들이 많음.
  - write an item to DynamoDB
  - add a message to an SQS queue
  - publish a message to SNS
  - 등등...

따라서 store your event first, respond to your user, then your compute layer can process asynchronously.

<img width="1058" alt="스크린샷 2023-05-20 오후 1 43 17" src="https://github.com/inspirit941/inspirit941/assets/26548454/6458940c-cc67-4c55-a60b-5079bc292752">
<img width="1054" alt="스크린샷 2023-05-20 오후 1 43 31" src="https://github.com/inspirit941/inspirit941/assets/26548454/091433f3-910e-4e38-999b-080251885a82">

그렇다면 storage, 일종의 request buffer 역할을 할 컴포넌트로는 어떤 것들이 있을까?

1. DynamoDB (apigw -> lambda -> dynamoDB에서 lambda 생략)
   1. request를 DynamoDB로 저장하기 전에 custom logic (데이터 전처리 등)이 필요 없다면 괜찮은 선택지. 
   2. but 서비스 유연성이 약간 떨어진다. custom logic을 추가해야 할 경우 아키텍처 수정이 불가피하기 때문
2. SQS
   1. apigw가 queue에 request를 쌓아두고, lambda가 queue에 쌓인 request를 가져가서 처리하는 방식.
   2. lambda의 event source로 SQS가 지원되기 때문에 seamless한 통합이 가능함

강의에 사용한 Customer 예시에서는 데이터 전처리 로직이 필요하다고 함. 따라서 AWS SQS를 사용한 아키텍처로 결정함.

<img width="1042" alt="스크린샷 2023-05-20 오후 1 50 11" src="https://github.com/inspirit941/inspirit941/assets/26548454/7db02512-b05a-4a55-a286-e993e292a17a">
<br>

### AWS SQS

<img width="845" alt="스크린샷 2023-05-20 오후 1 55 02" src="https://github.com/inspirit941/inspirit941/assets/26548454/a8ecb200-f00e-4c4b-801b-479aa20a11c5">
<br>

앞서 이야기했듯, SQS와 SNS의 차이점은 message buffer 여부. 
- SQS는 process 요청이 들어오기 전까지는 message를 보관 
- SNS는 보관 없이 subscriber에게 바로 전달한다.


<img width="1031" alt="스크린샷 2023-05-20 오후 1 56 36" src="https://github.com/inspirit941/inspirit941/assets/26548454/267d494d-e2b9-4d2b-bdf7-ad2494a89b3a">
<br>

Configuration 정보
- Message size는 1KB ~ 256KB. 즉 허용되는 메시지 크기가 매우 작다. Large message일 경우 다른 solution을 사용하거나 metadata만 전송하는 식으로 활용해야 한다.
  - index값만 queue에 저장한다던가
- message retention period: 1분 ~ 14일까지.
- Receive message wait time: max amount of time that polling will wait for messages to become available to receive.
  - 최소 0, 최대 20.
  - SQS는 polling 방식임. consumer가 주기적으로 메시지 존재여부를 체크해야 한다.
  - poll 요청이 들어왔을 때, 응답까지 걸리는 시간을 조정하는 옵션.
    - low-volume queue일 경우, longer message wait time을 주면 empty queue를 polling하는 시간을 줄일 수 있다.
- visiblity timeout: length of time that a message received from a queue or by one consumer, will not be visible to the other message consumers.
  - 예컨대 같은 queue를 polling하는 consumer가 5개 있다고 하자.
  - 하나의 메시지를 5개의 consumer가 동시에 받아서 처리하는 상황을 만들지 않기 위한 옵션.
  - message is claimed from a queue, visibility timeout begins. 해당 시간동안은 다른 consumer가 해당 메시지를 받을 수 없음.
- Delivery Delay: The amount of time that Amazon SQS will delay before it delivers a message that is added to the queue.
- Enable high throughput FIFO: This feature enables high throughput for messages in the queue. 
  - Choosing this option changes the related options (deduplication scope and FIFO throughput limit) to the required settings for enabling high throughput for FIFO queues. 

<br>
<img width="1047" alt="스크린샷 2023-05-20 오후 2 25 40" src="https://github.com/inspirit941/inspirit941/assets/26548454/83266a3f-e52f-42be-93c9-a47541a42837">
<br>

Access Policy: who can send message to / receive message from a queue를 결정

<bR>

<img width="1061" alt="스크린샷 2023-05-20 오후 2 27 52" src="https://github.com/inspirit941/inspirit941/assets/26548454/26ddc6e3-2729-4da7-82b1-8bcff351bf66">
<img width="1062" alt="스크린샷 2023-05-20 오후 2 28 57" src="https://github.com/inspirit941/inspirit941/assets/26548454/eb9cd288-c564-4c66-aff9-94d0c8a49436">

<br>

- SNS Subscriptions: SQS Queue가 SNS Topic을 subscribe하도록 설정할 수 있다. 즉 SNS Topic으로 들어온 message가 SQS에 저장됨.
- Lambda Triggers: SQS message로 lambda 함수를 실행시킬 수 있음.
- Monitoring: CloudWatch와 연동. SQS Operation 관련된 정보를 볼 수 있음. 

#### Short polling vs long polling

Short polling 사용 시
- Amazon SQS samples a subset of its servers (based on a weighted random distribution) and returns messages from only those servers. 
- Thus, a particular ReceiveMessage request might not return all of your messages. 
- However, if you have fewer than 1,000 messages in your queue, a subsequent request will return your messages. 
- If you keep consuming from your queues, Amazon SQS samples all of its servers, and you receive all of your messages.
<br>

![3QKUCv46QKSEw5tKZB6Wiw_ece62d9ec28a4cfba7bf372df8d99df1_Reading1 5A](https://github.com/inspirit941/inspirit941/assets/26548454/e7bbcefb-d857-4e7f-a3ee-08ad0c64a65b)
<br>

**short polling** 적용한 상태일 때의 내부 동작방식.
- SQS에 담긴 메시지를 가져오기 위한 요청을 보냈을 때
  - 여러 대의 SQS 분산서버 중 일부를 샘플링 (weighted random distribution) 해서
  - 샘플링된 SQS 서버에 들어 있는 메시지만 리턴한다.
- 예시의 경우 MessageReceive 요청을 보냈을 때, gray server가 SQS 분산서버 중 샘플링된 서버 몇 개를 선택한 뒤, 해당 서버에 저장되어 있는 메시지를 리턴한다.
  - 샘플링된 서버들 중 메시지 E를 가진 서버가 없기 때문에, 한 번의 MessageReceive API 요청에서 E는 응답값으로 주어지지 않는다.
  - 요청을 다시 보내면 샘플링이 다시 이루어지고, 다시 샘플링된 서버 그룹에 메시지 E가 있다면 응답값으로 메시지 E가 전달된다.
  - Queue에 메시지가 1000개 이하로 남아 있다면, E는 두 번째 요청에서 반드시 응답값으로 주어지게 되어 있다고 함.

반대로, wait time for ReceiveMessage API action is greater than 0, **long polling** is in effect. 예시: [setting up long polling](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/working-with-messages.html#setting-up-long-polling)

- reduce the cost of SQS, by reducng the number of empty response / false empty response.
  - SQS가 queue의 message가 available한 상태일 때까지 대기하는 시간을 만들어주기 때문.
- 꼭 wait time만큼 대기하는 게 아니라, available message가 있을 경우 바로 응답함.


### Wrap-up: Taking this Architecture to the Next Level

최종 Architecture.

<img width="1049" alt="스크린샷 2023-05-20 오후 2 48 36" src="https://github.com/inspirit941/inspirit941/assets/26548454/6fa6d708-d102-4f8f-ab3f-5bf9e199f66e">

사용자 요구사항의 변화라던가, 현재 아키텍처 자체에서 개선할 만한 점?
- Lambda <-> DynamoDB 에서 **DynamoDB의 performance**.
  - DAX: cache layer for DynamoDB Accelerator. lambda가 DynamoDB를 매번 조회 / hit하는 대신 cache layer 적용이 가능.
    - micronsecond 단위 Latency 보장, with cost
  - DynamoDB with read capacity units.
- Lambda 최적화
  - [AWS Lambda Power Tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning): find most optimal Memory / CPU allocation for your lambda.
    - lambda는 "리소스 사용량 * 실행시간" 으로 요금이 측정됨. 그런데 어떤 경우는 더 많은 Memory를 할당받았을 때 실행시간이 줄어서 cost efficient할 수 있다.
  - **lambda layers**
    - 여러 개의 lambda function에서 사용하는 code는 재사용할 수 있도록 하는 것. like common libraries.
    - 공통로직을 바꾸려면 해당 Lambda layer만 변경하면 된다.
    - deploy faster
  - **declare variables outside the handler** / those variables can be **reused across execution environments**.
    - 예컨대 lambda에서 object를 생성하는 로직이 매번 있다면, 해당 로직은 outside of the handler로 설정할 수 있음.
  - Optimize Logging output / retention for our logs.
    - cloudwatch에 로그 전송하거나
    - [AWS Lambda PowerTools](https://awslabs.github.io/aws-lambda-powertools-python/latest/) (suite utilities for AWS Lambda functions) 
      - ease adopting the best practices for lambda. (https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
      - i.e. tracing with using like X-Ray, structured logging, creating custom metrics...
- AWS SNS
  - filtering 기능의 필요성이 커지면, SNS 대신 EventBridge 사용을 고려할 수 있다.
  - EventBridge can use SNS as one of the consumers.

## Week 1 Assignment

> A solutions architect must design a solution to help manage their customer’s containerized applications. Currently, the customer workload runs in Docker containers on top of Amazon Elastic Compute Cloud (Amazon EC2) instances and on-premises servers that run a hybrid Kubernetes cluster. The customer wants to migrate part of their hybrid Kubernetes deployment to the cloud with a minimum amount of effort, and they want to keep all the native features of Kubernetes. The customer also wants to reduce their operational overhead for managing their Kubernetes cluster. Which managed AWS service should the solutions architect suggest to best satisfy these requirements?
>
> Amazon EKS is a managed Kubernetes service that runs Kubernetes in the AWS Cloud and in on-premises data centers. In the cloud, Amazon EKS automatically manages the availability and scalability of the Kubernetes control plane nodes that are responsible for scheduling containers, managing application availability, storing cluster data, and other key tasks. 

Operational Overhead 줄인다길래 Fargate 선택했다가 틀렸음

> Amazon DynamoDB is designed for scale and performance. In most cases, the DynamoDB response times can be measured in single-digit milliseconds. However, there are certain use cases that require response times in microseconds. For these use cases, DynamoDB Accelerator (DAX) delivers fast response times for accessing eventually consistent data. Which statements about DAX are correct? (Choose THREE.)
>
> DAX is a managed caching service for Amazon DynamoDB that is compatible with the DynamoDB API. 
> Through the use of a cache like DAX, you can offload some read requests to the cache, which would save on read capacity for the table itself.
> DAX is beneficial for reads because it is a caching service. However, it is not very beneficial for write-heavy workloads.

