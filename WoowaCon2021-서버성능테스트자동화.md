## 서버 성능테스트, 클릭 한 번으로 끝내볼 수 있을까?

배민서비스개발팀 김덕수

![스크린샷 2021-12-04 오후 3 23 32](https://user-images.githubusercontent.com/26548454/144700034-f015c7a2-82f0-49fd-b266-697d5498fdb6.png)


전제사항
1. 클라우드 환경. CLI로 클라우드 서버를 조작할 수 있어야 함
2. 서버 자원을 시각화할 수 있고, 모니터링할 수 있는 수단을 갖추고 있음.


서버 성능테스트? API 요청이 많은 상황에서 서버가 어떻게 동작하는지 확인하기 위해 수행하는 테스트. 목적에 따라 성능테스트 / stress test / 부하 테스트 등 용어가 다르지만, 세분화된 용어 정의는 이 발표에서 중요하지 않으므로 '성능테스트'로 통일.

![스크린샷 2021-12-04 오후 3 25 17](https://user-images.githubusercontent.com/26548454/144700089-7adbc02e-5553-4168-b104-5582bf17a835.png)

- 요청을 얼마나 잘 처리하는가?

![스크린샷 2021-12-04 오후 3 25 30](https://user-images.githubusercontent.com/26548454/144700086-8dd7dc00-54d8-44cc-bb3b-06043c31e045.png)

- 병목현상이 되는 지점은?

가상의 클라이언트를 만들고, 서버 부하를 발생시켜서 상황을 관측한다.


![스크린샷 2021-12-04 오후 3 28 22](https://user-images.githubusercontent.com/26548454/144700153-6b0cab4b-cce7-476a-9f23-f87483867e21.png)

트래픽 많이 들어오는 게 무서운 서비스... 사전에 확인하기 위해서.

![스크린샷 2021-12-04 오후 3 29 10](https://user-images.githubusercontent.com/26548454/144700200-7c8ce1ab-3cbc-4ddc-b5f3-990a44d791ab.png)


![스크린샷 2021-12-04 오후 3 29 28](https://user-images.githubusercontent.com/26548454/144700199-3b967018-741e-4239-8cb0-a4be08d6779c.png)

가상 클라이언트를 생성하는 부분은 자동화가 잘 되어 있는 편이다.

![스크린샷 2021-12-04 오후 3 29 34](https://user-images.githubusercontent.com/26548454/144700198-4a33badd-0592-45b5-8c74-697f42f50a12.png)

![스크린샷 2021-12-04 오후 3 29 41](https://user-images.githubusercontent.com/26548454/144700197-ad8fe5ff-5005-4bba-a224-8ee7dd414d2a.png)

테스트 환경을 세팅하고, 모니터링한 결과를 기록하는 일이 고됨.


![스크린샷 2021-12-04 오후 5 59 43](https://user-images.githubusercontent.com/26548454/144703811-71276e1e-1b9e-4e9d-81c0-462c5b0d0de1.png)


---

성능테스트 과정의 도식화

![스크린샷 2021-12-04 오후 6 00 40](https://user-images.githubusercontent.com/26548454/144703829-1a66cb3b-4a8c-419f-991f-481f23d76062.png)

1. 사전작업
   - input : 어느 부분에 어떻게 부하를 줄 것인지.
   - output : 시스템은 어떤 결과를 내야 하는지.

![스크린샷 2021-12-04 오후 6 03 29](https://user-images.githubusercontent.com/26548454/144703900-4a4418f6-3d83-4bea-affa-8ee0184885b3.png)

2. 테스트 환경 구축
   - 서버 개수 / 스펙 결정
   - Scale 조절작업


![스크린샷 2021-12-04 오후 6 03 42](https://user-images.githubusercontent.com/26548454/144703923-31c2c378-8aed-41cd-828e-18cc0e68b763.png)

3. 성능테스트 생성, 수행

![스크린샷 2021-12-04 오후 6 04 50](https://user-images.githubusercontent.com/26548454/144703942-bf487bd4-8ed5-4659-856e-9ebabea8c729.png)

4. 모니터링 보드의 지표 관측, 기록

![스크린샷 2021-12-04 오후 6 04 57](https://user-images.githubusercontent.com/26548454/144703941-6fcb6170-1701-4b09-9e85-894d853e494a.png)

5. 결과 확인
    - 요청 처리는 잘 이루어졌는지
    - 시스템은 기대하던 대로 동작했는지

![스크린샷 2021-12-04 오후 6 06 10](https://user-images.githubusercontent.com/26548454/144703976-ca82f1e7-107c-4c6d-9770-3d416278f099.png)

필요하다면 반복시행이 가능하도록.


---


이 파이프라인에는 두 가지 성격이 혼합되어 있음.

![스크린샷 2021-12-04 오후 6 07 23](https://user-images.githubusercontent.com/26548454/144704004-bbbced87-632e-4d45-bd71-f3d9e9226982.png)

- 개발자가 집중해야 하는 부분은 시나리오 구상, 테스트결과 분석이다.


![스크린샷 2021-12-04 오후 6 07 37](https://user-images.githubusercontent.com/26548454/144704009-f60170c3-ea9c-448e-922b-575ea969dcca.png)

- 하지만 여기에 쏟는 시간이 생각보다 많이 걸림.
- 자동화가 가능하다면 자동화해야 하지 않을까?


어떻게 해결할까??

![스크린샷 2021-12-04 오후 6 10 09](https://user-images.githubusercontent.com/26548454/144704105-33273763-ef04-43f2-8f13-c9c1c3e734b7.png)

- nGrinder, AWS CLI, Jenkins 사용.
  - HTTP 요청으로 테스트 생성 / 수행
  - CLI로 인프라 제어
  - Groovy Script로 jenkins에 사용.

환경 세팅

![스크린샷 2021-12-04 오후 6 13 23](https://user-images.githubusercontent.com/26548454/144704205-a59e383c-b55a-4973-8ebd-4ada4455cd65.png)

테스트 시나리오 / 테스트 스크립트까지 준비되었다고 가정하면

1. 성능테스트 환경구축 시작
   - ASG (AutoScaling Group) 사용해서 인스턴스를 추가하거나 replica 노드를 증가시키는 작업 등을 수행
   - nGrinder Agent 세팅
   - health check 확인.


![스크린샷 2021-12-04 오후 6 16 42](https://user-images.githubusercontent.com/26548454/144704293-fc59ae86-3b7d-43d6-8fc3-4f33117087eb.png)

2. nGrinder에 API 요청. 신규테스트 생성 / 실행
    - 인스턴스에 부하
    - Jenkins는 테스트 시간 측정

![스크린샷 2021-12-04 오후 6 18 37](https://user-images.githubusercontent.com/26548454/144704360-a4268a74-e4e7-41a1-9244-94c1a2ee3f4c.png)

3. 테스트 완료되면 Notification은 슬랙 메시지로 전송.

![스크린샷 2021-12-04 오후 6 19 19](https://user-images.githubusercontent.com/26548454/144704379-a75e65bc-cf0a-491e-8112-cd40d30d9a11.png)

4. 리소스 정리.


nGrinder 테스트 -> 수행결과는 nGrinder에서 제공하는 레포트 사용, 인프라 모니터링은 그라파나 사용.


![스크린샷 2021-12-04 오후 6 22 38](https://user-images.githubusercontent.com/26548454/144704467-98417a5d-3141-4672-9717-9026b5955a3d.png)

- 테스트 input, output을 빠르게 확인할 수 있으며
- 결과가 기록되어 언제든 확인할 수 있다는 것.


![스크린샷 2021-12-04 오후 6 24 20](https://user-images.githubusercontent.com/26548454/144704499-a563717b-ebe8-47d3-a33d-61e7c867ed73.png)


![스크린샷 2021-12-04 오후 6 24 52](https://user-images.githubusercontent.com/26548454/144704519-1102f8c6-82da-4ed4-94bb-0a18ed81f696.png)


![스크린샷 2021-12-04 오후 6 24 59](https://user-images.githubusercontent.com/26548454/144704523-cf0f69df-a163-4e98-94a6-6c1a1a1e954d.png)


![스크린샷 2021-12-04 오후 6 25 46](https://user-images.githubusercontent.com/26548454/144704533-95932768-6682-48b5-83ce-beba9f686b9b.png)


![스크린샷 2021-12-04 오후 8 07 15](https://user-images.githubusercontent.com/26548454/144707197-c87429ec-7517-4e41-b059-6b495bf59f44.png)

방법은 여러 가지가 있다. 

'어떻게 해당 기능을 수행하도록 할 것인가'가 더 중요하다.

---

![스크린샷 2021-12-04 오후 8 07 43](https://user-images.githubusercontent.com/26548454/144707227-ee797e1d-cee9-431a-bb38-2cfdc416cb42.png)


![스크린샷 2021-12-04 오후 8 07 51](https://user-images.githubusercontent.com/26548454/144707225-a1749d90-bf31-4bf8-9738-872a7656ea92.png)

- 자동화하는 건 좋지만, 모든 시스템에 전부 유용하게 사용될 수 있는 영역은 아님.
- 비용을 들여서 구축할 만큼 자주 사용하고, 그럴만한 가치가 있을 때 유용함.

![스크린샷 2021-12-04 오후 8 08 03](https://user-images.githubusercontent.com/26548454/144707223-96ba9552-7915-4c0f-a324-38e5bd290383.png)

- 발표 기준으로 개발된 지 3개월 된 프로덕트로, 실험 단계라고 보고 있음.
- 다양한 시나리오 테스트 / 장애상황 시뮬레이션하면서 기록하면 자산이 될 것이라 생각함.



