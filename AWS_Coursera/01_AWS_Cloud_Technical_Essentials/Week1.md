## AWS Overview and Security

기본적인 infra 구조 for Redundancy
<br>


<img width="446" alt="스크린샷 2023-04-07 오전 8 38 02" src="https://user-images.githubusercontent.com/26548454/230512723-e2e613b0-e6a1-4f81-b329-f8e29d6b34fc.png">

- Availability Zone (AZ) : Low-latency, high-speed link로 연결된 여러 개의 데이터센터의 집합. 하나의 데이터센터 전체에 문제가 생기더라도 대응 가능.
- Region : a Cluster of Availability Zones. 사용자는 Region 단위로 AWS resource를 선택할 수 있다.

<br>

<img width="967" alt="스크린샷 2023-04-07 오전 8 38 08" src="https://user-images.githubusercontent.com/26548454/230512729-3cb6a116-d5dd-455e-a0e1-d69c7394260b.png">


사용자 입장에서 Region을 선택할 때 고려할 점은 네 가지.
- Compliance : 법규준수, 준법감시, 내부통제 등 IT 서비스를 하려 할 때 서비스 외적으로 고려해야 할 조건.
- Latency : 통신에 걸리는 지연시간. 좀 쉽게 표현하면 사용자와 IT infra 사이의 거리. 거리가 멀면 통신이 오래걸리고, 가까우면 빠름.
- Price : 데이터센터가 건설된 지역의 세금과 같은 문제 때문에라도 region마다 가격이 다름.
- Service Availability : AWS는 신규 서비스를 모든 region에 동시오픈하지는 않는다. 어떤 서비스는 특정 region에서만 사용할 수 있는 등의 제약조건이 있음.

Interacting With AWS - 3 ways
- AWS Web Console
- AWs CLI Tools
- AWS SDK


## Security in the AWS Cloud

<img width="947" alt="스크린샷 2023-04-07 오전 8 38 16" src="https://user-images.githubusercontent.com/26548454/230512731-68ea8290-bff4-48dc-851d-3c2d9663bb08.png">


AWS 서비스의 보안 책임자 -> AWS (서비스 공급자) / User (사용자) 둘 다 해당함.
- Shared Responsibility Model. AWS가 보안을 담당하는 영역이 있고, 사용자가 보안을 책임져야 하는 영역이 있다.

<br>

AWS는 그림 하단의 **Security of the Cloud** 를 담당. = PM / VM이라 생각하면 될듯
- AWS Global Infrastructure (물리서버 / private fiber cables 등)
- Software Component (Compute, DB, Storage, Netoworking)
  - AWS는 이 소프트웨어 서비스들을 virtualizing layer로 관리.
- 예컨대 사용자가 VM 인스턴스를 사용할 경우
  - VM instance 자체의 availability + host machine (hypervisor)의 소프트웨어 업데이트 같은 사안은 AWS의 책임.

사용자는 **Security In the Cloud**를 담당.
- VM OS의 patch / upgrade, Configuring firewalls, 해당 리소스의 Acccess Control
- 사용자가 올린 데이터는 사용자의 책임. encrypted / secure / proper access control 여부는 사용자가 확인해야 한다.

<br>

---

<bR>

AWS에 로그인할 때 Email + Password 조합을 사용했다면 Root User 권한으로 로그인한 것. 이 계정은 모든 권한을 가지고 있다.
- 별다른 추가 인증절차가 없으면 Single-Factor Authentication.
- AWS는 Multi-Factor Authentication (MFA) 방식의 인증방식을 권장함.


### Identity and Acccess Management (IAM)

<img width="914" alt="스크린샷 2023-02-24 오후 12 36 58" src="https://user-images.githubusercontent.com/26548454/221085947-d7bf37a4-ea16-4b81-a967-55546b06e546.png">
<br>

**App Level Access Control**

EC2에 띄워져 있는 서비스 (예컨대 Employee management service)에서 내가 특정 작업을 수행하려면 보통 로그인을 해야 한다. 
- 즉 사용자가 띄운 애플리케이션에 접근하기 위한 Access Control이 필요.

<br>

**Api Call Authentication**

서비스 로직상 EC2 인스턴스가 S3 Storage에서 데이터를 Read / Write해야 한다고 가정하면
- EC2 인스턴스가 S3 인스턴스에 Read / Write 요청을 보낼 수 있는지도 Access Control이 필요하다.

<br>

**Access to AWS Account**

그렇다면 어떤 권한을 가진 사용자가
- EC2 / S3 서비스를 발급받고 통신할 수 있게 네트워크 세팅을 하고
- EC2 <-> S3 서비스가 Read / Write 권한을 가질 수 있도록 설정을 해야 한다.

root user는 이 권한을 전부 가지고 있지만, 모든 관리자가 root user 권한이 있는 계정을 쓰는 건 바람직하지 않다.
- 각자가 필요로 하는 권한이 보통은 정해져 있기 마련. 예컨대 애플리케이션 개발자와 네트워크 엔지니어는 관리할 리소스가 다름.

<br>

AWS는 IAM (Identity and Access Management) 서비스를 사용해서, 앞서 언급한 세 가지 Access Control 중 두 가지를 담당하고 있다.
- Access to AWS Account
- Credentials used to sign API calls made to AWS services.

Application Level의 access control은 관리하지 않는다.

#### IAM brief structure

IAM은 User를 생성할 수 있다. -> Authentication 담당.
- User: Access Control이 필요한 모든 형태의 사용자.
- Authentication: Verifying if someone is who they say they are.
  - proper credential로 로그인하면 Authentication은 충족되기 때문.

IAM Policy는 해당 User가 특정 Action을 수행할 권한이 있는지 체크한다. -> Authorization 담당.
- Authorization: 인증된 사용자가 특정 Action을 수행할 권한이 있는지 체크하는 것.
  - Permission Control what you can / cannot do. (Grant or Deny)
  - 일반적으로 Action은 "AWS API call" 을 뜻함.

<br>

![스크린샷 2023-04-03 오후 10 05 29](https://user-images.githubusercontent.com/26548454/229518412-3d9bbb93-255d-4ca0-a9a5-2d617ea6b9a5.png)
<br>

IAM Policy는 json 형식.
- Effect: Allow or Deny 둘 중 하나
- Action: AWS API call. 예시의 경우 EC2-related action 전체를 말함.
- Resource: Action을 허용할 리소스 이름을 지정할 수 있다.
- Condition: Further Restrict actions

![스크린샷 2023-04-04 오전 7 23 55](https://user-images.githubusercontent.com/26548454/229640186-2d74c77a-5947-448e-a23f-a35f77c7d78b.png)

IAM Policy를 group에도 지정할 수 있다. Group은 IAM user의 집합. 
- Group에 policy를 부여하면, Group에 소속된 User는 전부 해당 Policy가 적용된다.

그 외에도 AWS가 권장하는 IAM 사용 방식
- Set up MFA for the root user, root user로 로그인해서 IAM user를 생성한다.
- root user로는 로그아웃하고, IAM user로 로그인한다.
  - IAM user를 가지고 IAM Group / User / Policy를 구축한다.

root user에는 IAM Policy를 부여할 수 없지만, IAM User는 Policy를 부여할 수 있기 때문.
<Br>

![스크린샷 2023-04-04 오후 8 30 32](https://user-images.githubusercontent.com/26548454/229778415-f1c4271f-dc11-4cde-90fc-c1e8e3978576.png)
<br>

"EC2 Instance가 AWS S3에 signed API Call 보내는 로직" 에서는 어떻게 Access Management를 관리하나?
- 이런 경우엔 **Role-based Access Control** 을 사용해야 한다.

<br>

#### Role based Access in AWS

![스크린샷 2023-04-06 오후 9 49 00](https://user-images.githubusercontent.com/26548454/230383373-aa18b043-dc3c-43ff-9b3d-e8bfaf380cd9.png)
<br>

IAM Role : Identity that can be assumed by someone or something who needs temporary access to AWS credentials.
- AWS API call은 signed & authenticated 된 상태여야 함.
  - signing : AWS가 요청을 보내는 쪽의 identity를 확인하고, security process를 통과하면서 'request is legit' 상태임을 확신하는 것.
    - **IAM User의 경우 Access Key(id) / Secret Access Key가 쓰임.**
    - signing request를 수행해야 하는 Service인 경우 (i.e. EC2 request to S3) IAM Role을 사용하면 된다.

- IAM User는 Username / password 외에도 static credential로 access key / secret access key가 있음.
- IAM Role의 경우
  - No static Login Credentials (username, password 개념이 없음)
  - Programmatically acquired, temporary in nature, automatically expire and rotated 

<br>

![스크린샷 2023-04-06 오후 9 53 37](https://user-images.githubusercontent.com/26548454/230384343-953c2e51-4ebc-408b-9540-1f5f1ccd4de3.png)
<br>


- EC2를 발급받고 실행할 때 기본적으로 IAM Role이 부여된다.
- EC2 위에서 동작하는 Application은 EC2 instance에 부여된 IAM Role을 사용해서 Temporary credential을 발급받는다.
- API Call에 temporary credential을 사용한다.

<bR>

![스크린샷 2023-04-07 오전 7 53 50](https://user-images.githubusercontent.com/26548454/230508363-04fb9a4d-4571-41dc-bf6b-295c94a8f720.png)
<br>

- IAM Role을 생성할 때 첫 화면. 어느 서비스 / 리소스에 IAM Role을 부여할 것인지 선택할 수 있다.
- 예시의 경우 EC2가 IAM Role을 부여받아야 하므로 EC2 선택.

<bR>

![스크린샷 2023-04-07 오전 7 54 42](https://user-images.githubusercontent.com/26548454/230508368-637983ff-8dd2-48e0-ad17-cdc9cf5c73fb.png)
<br>

- 해당 IAM Role에는 어떤 policy를 부여할 것인지 선택한다.
- 예시의 경우 EC2는 DynamoDB와 S3에 접근해야 하므로, 각 서비스의 FullAccess를 선택한다.
  - AWS가 생성해둔 predefined policy도 있고, 사용자가 직접 policy를 생성할 수도 있다.

<br>

![스크린샷 2023-04-07 오전 7 55 31](https://user-images.githubusercontent.com/26548454/230508376-d19a00f9-41d5-4867-8ba1-ec62af554967.png)
<br>

- tags: billing / resource management 등 사용자가 필요한 용도에 맞게 쓸 수 있는 key-value pairs.

<br>

![스크린샷 2023-04-07 오전 7 59 06](https://user-images.githubusercontent.com/26548454/230508769-f2c5e909-c4ae-44d4-b5c8-03a35fe1747e.png)

- 이름 정하고 생성하면 됨.

<br>

두 개의 서비스가 같은 Region에 있다고 바로 통신할 수 있는 게 아니다.
- AWS의 서로 다른 서비스끼리 연결해야 할 때 IAM Role이 필요함. 많이 보게 될 거임.

<br>

![스크린샷 2023-04-07 오전 8 02 21](https://user-images.githubusercontent.com/26548454/230509092-be263aba-958f-4229-ba8a-8c35b4c2ffef.png)
<br>

이미 External Identity Provider를 사용해서 employee management를 하고 있는 경우
- 수많은 직원에게 전부 IAM User를 부여하는 방식은 효율적이지 않음.
- 이미 External Identity Provider를 사용하고 있는 Federate User의 경우에도 IAM Role을 사용할 수 있다. 
  - Federate User가 IAM Role을 받아야 접근할 수 있는 Resource를 구성하는 식.
  - 인증 절차를 단순화하기 위해 AWS SSO도 지원하고 있다


