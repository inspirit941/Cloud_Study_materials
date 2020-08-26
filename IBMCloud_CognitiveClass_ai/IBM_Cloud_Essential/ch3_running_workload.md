## OpenShift

Open Source Application Platform based on Kubernetes / container tech. Allows you to run containerized application & workloads, and is powered by Kubernetes under the covers.

* Origin Kubernetes Distribution (OKD) : Open Source project that powers Openshift.
* OpenShift : Redhat이 제공하는 서비스 중 하나. 

Highly Available / Managable OpenShift Cluster를 제공함.

Fully Managed Platform
    - Automated Provisioning / Upgrades.
    - 24/7 global support
    - IBM cloud와 RedHat의 middleware와의 integration - AI, Hyperledger

<img width="1171" alt="스크린샷 2020-07-31 오후 2 17 36" src="https://user-images.githubusercontent.com/26548454/89004142-7ef97e80-d33c-11ea-8de6-4941839d3be2.png">


1. Resource Layer - Public / Private Resource 상관없이 실행이 가능함. On-prem Resource / Cloud Resource 무관
2. OS Layer - 보통은 Red Hat Enterprise Linux를 사용하지만, OKD 프로젝트 기반이면 CentOS를 사용해도 무방하다.
3. Kubernetes Layer
4. OpenShift - Kubernetes Layer 위에 설치. difficult task를 대신 처리해주는 역할. Deploying Application이나 day-to-day Operation 같은 작업을 Web Console이나 CLI로 쉽게 작업할 수 있게 해줌.


### 누가 어떻게 이득을 보게 되나?

<img width="1175" alt="스크린샷 2020-07-31 오후 2 39 26" src="https://user-images.githubusercontent.com/26548454/89004167-8de03100-d33c-11ea-8907-3ce53f645150.png">

1. Developers
이들의 핵심업무 : Write Application, Create Changes, Test, Deploy them into a cluster.

- Create a Project & Application : CLI / Web Console로 작업. Templates / Source code and Language 제공.
- Push changes to Repository (ex-Github)

이 두 가지를 제외한 나머지는 전부 OpenShift가 담당한다.

---

CLI나 Web Console로 프로젝트를 생성하면, OpenShift는 자동으로 Jenkins Job & Pipeline을 백엔드에 생성한다. Github에 코드를 푸시하면, Webhook을 작동시켜서 Jenkins job kicks off.

**Jenkins가 하는 두 가지 작업**

* Sourced Image (소스코드 기반 Docker Image) 생성. 생성된 image를 OpenShift Built-in Private Registry에 저장. 필요하다면 Public Registry에도 저장할 수 있음.
* 레지스트리에 저장하는 작업이 끝나면, Actual Cluster에 Push.

현재 Cluster에 두 개의 host가 있다고 가정하고, 저장된 image를 각각의 host에 Deploy한다고 해보자.

개발자가 소스코드를 작성하고 Repository에 Push할 경우
1. Jenkins에서 해당 소스코드를 토대로 Docker image를 생성하고, 해당 이미지를 Registry에 저장한다.
2. Actual Cluster에 해당 image를 push. 이 과정에서 Image Stream이라는 방식을 사용한다.
3. Bring down the old version, and Start the new version

Image Stream?
- Whenever a change is deteced with the image you deployed, it allows you to push those changes with no downtimes to application.

---

<img width="1086" alt="스크린샷 2020-07-31 오후 2 44 27" src="https://user-images.githubusercontent.com/26548454/89004170-8e78c780-d33c-11ea-92aa-c13b61b111eb.png">


2. Operations Engineers
이들의 핵심 업무 : Maintain a high availabilty (ensure SLA), Sustain healthy infrastructure.

- Web Console이 CLI보다 편의성이 높다.

Scale out이 필요한 상황이라면? -> Ansible Playbook 사용 가능.
- Spin up the creation of new host + bring it into cluster

https://www.youtube.com/watch?v=KTN_QBuDplo

