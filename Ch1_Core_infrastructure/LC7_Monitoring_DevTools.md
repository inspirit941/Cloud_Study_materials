# Development in Cloud
GCP의 development / monitoring Tools를 소개.

- Cloud Source Repositories = Fully featured Git repositories hosted on GCP.
= keep code private to a GCP project + use IAM permissions to protect it, but not have to maintain Git instance yourself.
Git version Control 지원 - App / Compute / Kubernetes Engine 에서의development 지원.
Private Git repository 지원.
= Source viewer 지원  -> browse and view repository files from within GCP console.

Application에는 Event-driven parts가 반드시 존재한다. 예컨대 사용자가 이미지를 업로드하도록 만드는 것. 이 경우, 이 이미지를 처리하는 방법에는 여러 가지가 있다. Standard img format으로 변환하기, thumbnail into various sizes, store each in a repository 등등. 
-> 이 경우, providing compute resource가 문제일 수 있다. 얼마나 많은 리소스를 사용할지 알 수 없으므로.

Provisioning problem을 없애는 방법, 즉 single purpose function that did the necessary image manipulations & arrange for it to automatically run whenever new image uploaded.
-> Cloud Functions의 역할. 그냥 node.js에서 작동할 JS 코드를 만들고 , 어디서 이 함수가 작동할지만 configure해주면 된다. Server / runtime binary 고민할 필요 없고, 돈 낼 것도 없다. 단지 function이 작동할 때마다 돈 내면 된다. (In 100ms intervals)

Cloud function은 Cloud storage의 event, Cloud pub/sub, or in HTTP call로 작동시킬 수 있음. Microservice architecture로 만들었을 경우, Cloud function형태로 전부 구현할 수 있다. 또는, scaling 고민 없이 existing application에 적용할 수도 있다는 장점이 있다.

(-> Your code executes whenever an event triggers it, no matter whether it happens rarely or many times per second. That means you don’t have to provision compute resources to handle these operations.)

(확장성 = 많은 트래픽이 몰렸을 때 감당 가능한지. 워낙 가볍고 단순해서 여러 개 돌려도 무방함. 단순히 돌려야 해서 람다쓰는 경우 -> ex) 실시간 요청시 반환하는 api같은 거. Cold start vs Warm start… 메모리에 올려놓느냐 아니냐. 설령 안 쓰더라도 주기적으로 메모리에 값이 올라가도록 함수를 실행한다던가. (Warm start 상태가 일반적으로 더 가격이 쌈))

---
## Deployment: IaaS

GCP를 써서 Environment를 구성하는 작업은 보통 많은 작업을 수반한다. Set up computing networks & storing resources, keep track of their configurations… 이걸 스스로 다 알아서 하는 imperative approach도 있지만, figuring out the command that makes it done도 있다.
그 중에는 ‘change environment’나 ‘clone’ 같은, 거의 같은 작업을 다시 해야 하는 일들도 있기 마련이다. 이런 일들은 template 형태로 처리할 수 있다. 일종의 declarative한 선언인 셈.

-> GCP의 Deployment manager를 사용하면 된다. Infrastructure Management Service that automates the creation + management of your GCP resources.

yaml Markup file이나 Python that describes what you want the components of your environment to look like. 이 파일을 Deployment manager가 받기만 하면 된다.

---
## Monitoring: Proactive instrumentation

Monitoring lets you figure out whether the changes you made were good or bad. 운영 및 비상상황 대처에 필요한 정보를 제공하는 개념이라고 생각하면 된다.

-> Stackdriver : GCP’s Tool for monitoring, logging and diagnostics.
Infra platforms, VMs, Containers, middleware and application tier, logs, metrics and trace 등 다양한 정보를 제공한다.

Core components of Stackdriver
1. Monitoring: checks the endpoint of web applications / other internal accessible services running on your cloud environment. Uptime checks associated with URLs, groups of resources (instance, load balancers)
Visualization을 위한 Dashboard도 지원한다.
2. Logging : view, filter, search log를 지원, lets you define metrics, based on log contents that are incorporated into dashboards and alerts. Export to BigQuery, Cloud Storage, Cloud Pub/Sub. 
3. Error Reporting : tracks and groups the errors in your cloud applications. + notifies you when new error detected.
4. Trace : sample the latency of app engine applications and report Per-URL statistics.
5. Debugger : connects your applications production data to your source code. -> can inspect the state of your application at any code location in production. (일반적으로 사용하는, existing application에 로그 표시하도록 때려박는 것과 다르다고 함) Application Source code available일 때 최고의 성능을 발휘한다. (Repository 형태로 있을 때)

---



