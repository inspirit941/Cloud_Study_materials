# Module 설명 - App Engine
## intro to App Engine
Compute Engine / Kubernetes Engine -> 전부 compute infrastructure에 관련된 것들이었다. Choose infra in which your applications runs. VM = Compute Engine, Containers = Kubernetes Engines.

Infra 자체에 신경쓰기 싫은 경우? App code에만 집중하기 위해 존재하는 게 App Engine이다.

App Engine = PaaS. It manages HW, Networking Infrastructure required to run your code. App Engine을 code에만 심어 놓으면, 나머지는 App Engine이 알아서 한다. 
It provides you with a built-in services that many web applications need. NoSQL DB, in-memory caching, load balancing, health checking, logging and authenticating user에 이르기까지.

Amount of traffic에 따라 automated scaling도 지원한다. Provision / maintain용 서버도 따로 없고, 그냥 쓴 만큼 내면 됨. 이런 특성 때문에, 예측이 불가능하고 변동이 심한 Web / Mobile application에 좋다. 
2 environments selection; standard / flexible.

---
## App Engine Standard Environment

simpler than Flexible Env and offers Fine-grained auto scale. 둘 다 free daily usage quota for the use of some service를 제공하지만, standard는 ‘low utilization application might be able to run with no charge’. 구글에서 제공하는 SDK로 미리 App testing을 해볼 수 있다.

App Engine’s executable binary = Runtime. Standard Env를 사용할 경우, Google이 제공하는 Runtime을 사용한다. Specified version of Java, PHP, python, Go언어를 지원함. App Engine에서 사용할 수 있는 API와 라이브러리도 제공. 보통은 이 정도 제공으로도 충분하다.
-> 만약 위에 명시된 언어가 아니면, Standard는 쓰기 어렵다. Flexible 써라.

It enforces restrictions on your code by making it run in a so-called ‘Sandbox’. HW & OS & Physical location of server it runs - all independent하게 만드는 SW construct라고 보면 된다. 

이 Sandbox라는 특성 때문에 fine-grained scale / manage가 가능함. 
몇 가지 제한점
- Application Can’t write to the local file system. Persistent data preserving을 위해서는 DB service를 사용해야 한다.
- All requests your application receives has a 60 sec timeout.
- can’t install arbitrary 3rd party SW
-> 이 제한을 수용할 수 없다면, Flexible Env로 넘어가야 한다.

사용예시
1. App Engine SDK로 로컬에서 개발 및 Testing 진행
2. 준비되었다면, SDK를 사용해 deploy 수행
3. Each App Engine application runs in a GCP project. + App Engine Automatically provisions server instances, scales and load balances them.
4. Application can use Dedicated API (NoSQL DB, caching of data, search, logging, task queue나 schedule 같은, 사용자의 request와는 별도로 실행되어야 하는 로직까지도)

---
## App Engine Flexible Environment

Standard Model에서 요구하는 sandbox 형식이 맞지 않을 경우 고려할 수 있는 선택지. It lets you specify the Container your App Engine runs in. 즉 Compute Engine VM의 Docker Container를 사용할 수 있게 해준다. App Engine은 이 Compute Engine machine을 관리해주는 것.
보통 health check & heal 지원, geographical region choice, critical backward-compatible updates to their OS를 제공함.

Standard runtime을 사용한다. 따라서 App Engine의 Data store, memcached, task queue 등의 기능도 사용할 수 있음.

Standard와의 비교 표 제시.
- instance startup: Standard는 ms 단위로 훨씬 빠르다. Flexible의 경우 minutes 단위.
- 대신, Flexible에서 지원하는 기능 중 standard에서는 불가능한 것들이 많다. SSH access, local disk writing, 3rd party binary support는 standard에서는 불가능하지만 flexible에서는 지원하며, Network access도 standard는 App Engine service를 통해서만 가능한 반면 Flexible은 application can call to the network without going through App Engine.
- Standard에서 completely idle application은 No charge. (둘 다 free daily quota는 존재한다!)

Kubernetes와의 차이점
- Language Support : anything in Kubernetes / Flexible, Java & Python & Go & Php in Standard
- Service model : Kubernetes = Hybrid, App Engines = PaaS
- Primary Use case : Container-based workload in Kubernetes, Web / Mobile Application & Container-based workload in Flexible, Web / Mobile Application in Standard.

따라서 standard는 for people who want the service to take maximum control of their Application’s deployment and scaling. Kubernetes == Full flexibility of Kubernetes. Flexible is somewhere in between.

App Engine treats containers as a mean to an end, whereas containers are a fundamental Org principle in Kuberntes.

---
## Cloud Endpoints and Apigee Edge

일종의 interface that abstracts away needless details. API 자체를 수정해야 할 경우에는 보통 Version change를 진행함. 이전 버전에는 없는 기능이 새 버전에 추가되는 등, 버전에 따른 변동이나 변화는 있기 마련. 

Supporting API는 상당히 중요한 일로, GCP는 2 API management tools를 제공한다.

- Cloud Endpoints
Expose API, 허가된 사람들만 API에 접근 가능하도록 지정하고 싶은 경우, monitor & usage log가 필요한 경우 사용할 수 있다.
Easy to deploy proxy in front of your SW service, and It provides an API console to wrap up those capabilities in an easy-to-manage inferface.
Supports applications running in the GCP’s compute platforms. 즉 App Engine Flexible Env, Kubernetes Engine, Compute Engine에 전부 사용 가능하며, clients (Android, IOS, JS)도 취사선택 가능하다.

- Apigee edge
= helps you secure and monetize API proxies.
Business problems에 좀 더 focusing 된 형태. Rate limiting, quotas, analytics 등. 보통 다른 SW에 service를 제공하는 업체가 사용한다.
Backend Service가 반드시 GCP에 종속될 필요는 없기 때문에, engineers often use it when they are ‘taking apart’ a legacy application. 제공하는 서비스를 한 번에 옮기는 위험을 감수하는 대신, Apigee로 peel off its service one by one, standing up microservices to implement each in turn.

“<실습 필요>”