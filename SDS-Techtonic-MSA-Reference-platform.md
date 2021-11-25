## MSA Reference Platform

![스크린샷 2021-11-25 오전 9 40 50](https://user-images.githubusercontent.com/26548454/143331600-3bc375f7-50b8-4ad9-90ff-fcba34b69bbc.png)


발표자: 삼성SDS DT아키텍처그룹 임지훈 프로.


![스크린샷 2021-11-25 오전 9 43 14](https://user-images.githubusercontent.com/26548454/143331627-daf98c6f-a8d4-4721-ad79-928d94403384.png)

1. Monolitic
    - '모듈' 이라는 구성요소. 실행 시 프로세스에 Link되는 구조.
    - 모듈 간 결합도가 높은 편이며, Centralized된 DB에 모든 데이터 저장 / 수정.
    - 일정 규모 이상이 되면 구조를 바꾸거나 변화를 만들어내기 쉽지 않다.

2. MicroService
   - '서비스' 라는 단위로 구성되어 있으며, 각 서비스는 API로 통신.
   - 각각의 서비스는 독립적으로 배포 가능한 단위를 의미함
   - Loosely Coupled.




![스크린샷 2021-11-25 오전 11 54 27](https://user-images.githubusercontent.com/26548454/143371876-dda3c3a7-72d2-47ab-b424-da8190639173.png)

Cloud Native Application

- 클라우드 환경에 container화된 애플리케이션이 MicroService 형태로 구현된 애플리케이션을 의미함.
- 장점으로는 Agility, Scalability, Resiliency가 있음.


![스크린샷 2021-11-25 오전 11 56 15](https://user-images.githubusercontent.com/26548454/143372062-81f2cfe4-8e34-40a1-ab61-2fb6726a570f.png)

Agility

특정 기능을 추가한다고 가정하면
1. Monolitic
  - 신규 모듈에 기능 구현. 중앙화된 DB의 스키마 수정.
  - 배포 단위: 애플리케이션 전체
  - 따라서 Lead time (build, test, deploy에 걸리는 시간)이 길다.

2. MicroService Architecture
   - 신규 서비스를 생성해서 기존 서비스에 연결하면 되는 구조. 
   - Lead time이 상대적으로 적게 소요된다.

![스크린샷 2021-11-25 오후 12 00 45](https://user-images.githubusercontent.com/26548454/143372403-7c90e103-f7b6-4e42-9fe4-b5afc417f4f7.png)


Scalability

1. Monolitic
  - 애플리케이션 전체를 확장해야 함 - 시간, 비용소모 큼
  - RDB일 경우 확장이 쉽지 않음

2. MicroService Architecture
   - 서비스 단위로 필요한 것만 확장 가능 - 상대적으로 적은 시간, 비용소모
   - NoSQL 등 확장에 용이한 DB 사용 가능

![스크린샷 2021-11-25 오후 12 04 57](https://user-images.githubusercontent.com/26548454/143372771-9f508fed-853b-4d4c-9b67-33ec2b594608.png)


Resiliency

ex) 특정 서비스에 문제가 생겼을 경우
- 서킷 브레이커 발동. 해당 서비스가 외부로부터 받는 트래픽 차단. 서비스 안정화 작업에 돌입
- 사용자 요청에는 Fallback 형태로 안내메시지 제공, 정상화된 이후에 다시 서비스 제공.

![스크린샷 2021-11-25 오후 12 13 09](https://user-images.githubusercontent.com/26548454/143373412-e2646320-6376-4208-a644-13f244f229c8.png)

ex) 심각한 버그 발생
1. Monolitic
  - 전체 시스템 장애. 서비스 불가능

2. MicroService Architecture
   - 장애가 버그 있는 서비스에만 국한됨. 다른 서비스는 정상 동작함.



![스크린샷 2021-11-25 오후 1 45 40](https://user-images.githubusercontent.com/26548454/143381124-29c2ff5e-fc9b-4488-a1ab-fb02bf63a936.png)

그럼에도 MSA를 하기 어려운 단점

1. 복잡도 증가
2. 오픈소스 SW 활용 증가에 따르는 어려움
   - 오픈소스 간 정합성, 통합성을 고려해야 함
   - 라이선스 이슈
3. Infra 구성 변화
   - Private Cloud를 선택할 경우 해당 cloud에 맞게끔 구조 변경이 필요
   - Public cloud는 종속성 / 비용 문제
   - Hybrid / Multi cloud는 운영 복잡도의 증가

![스크린샷 2021-11-25 오후 1 48 15](https://user-images.githubusercontent.com/26548454/143381328-edddd986-374a-45ae-afb3-5f303de55215.png)

삼성SDS에서는 MSA Reference Platform을 제안한다. 내부에서는 표준 스택으로 사용하고 있음

![스크린샷 2021-11-25 오후 1 52 24](https://user-images.githubusercontent.com/26548454/143381695-20ba8785-9efa-4cae-96c9-a37e8a0f6d95.png)


1. Event Driven 아키텍처 스타일.

Saga Pattern, Message Queue, Java / Python 기반 Service 구축.

![스크린샷 2021-11-25 오후 1 52 34](https://user-images.githubusercontent.com/26548454/143381700-03b8b133-4d12-42ab-9788-b9dab4cd4c23.png)



2. 인증 / 권한관리

OpenID Connect 방식. Keycloak을 활용한 Customize / OIDC Provider.

JWT 토큰 사용.

![스크린샷 2021-11-25 오후 1 53 12](https://user-images.githubusercontent.com/26548454/143381705-fdf0a06d-5504-49d9-9868-b739387c3ff2.png)

3. Performance

grpc, NoSQL, 분산 캐시 시스템으로 성능 향상

![스크린샷 2021-11-25 오후 1 56 07](https://user-images.githubusercontent.com/26548454/143381991-70052ad5-138b-4d44-bfc8-09ab9db88d60.png)


4. Scalability, Portability

docker container 기반으로 구축 -> private / public 모두에 유연하게 적용 가능하도록 세팅

K8s의 Horizontal Pod Autoscaler 사용. 기준에 따라 자동으로 scale in / out

![스크린샷 2021-11-25 오후 1 56 15](https://user-images.githubusercontent.com/26548454/143381980-bba83363-39e9-4b91-8231-d4e24ea44cbc.png)


5. 모니터링

![스크린샷 2021-11-25 오후 1 58 59](https://user-images.githubusercontent.com/26548454/143382191-513673ff-aa06-47c6-a607-1132497b1468.png)



Implementation

![스크린샷 2021-11-25 오후 1 59 38](https://user-images.githubusercontent.com/26548454/143382285-09e4d704-157b-4806-8400-3873951c5efb.png)

- 각각의 영역에서 사용하고 있는 기술들.
- SaaS의 경우 Multi Tenancy : 논리적 격리

HPA : Horizontal Pod Autoscale을 의미하는 듯.

Backing Service HA: 이중화 / 클러스터링 가이드 제공.

![스크린샷 2021-11-25 오후 7 30 51](https://user-images.githubusercontent.com/26548454/143425186-0a2f6202-e910-4fb8-87bd-5d20114ce817.png)


Open Source Stack

![스크린샷 2021-11-25 오후 7 32 03](https://user-images.githubusercontent.com/26548454/143425396-875cd3fd-60db-4839-9eb8-39c640aada70.png)

대략 30여 개의 검증된 오픈소스 사용중. Product Validation도 추가로 수행하고 있음.
- OSS 검증
- Security 검증
- 기능 검증
- Performance 검증


![스크린샷 2021-11-25 오후 7 33 43](https://user-images.githubusercontent.com/26548454/143425639-51bedab5-d0aa-462f-8fdc-6a383fbb803b.png)


![스크린샷 2021-11-25 오후 7 35 20](https://user-images.githubusercontent.com/26548454/143425884-470ce72d-249b-45d1-be7a-7bb1f892f83c.png)


![스크린샷 2021-11-25 오후 7 37 59](https://user-images.githubusercontent.com/26548454/143426290-af0a03e5-0d6f-4d00-a896-f614e45755a6.png)

