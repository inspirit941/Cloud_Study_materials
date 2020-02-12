# Lab
## Lab intro - deployment manager
Deployment Manager 사용해서 Template App server 굴리기

Cloud shell + 디렉토리 확인하는 거 열고

```
mkdir ~/archdp
cd ~/archdp
```
경로 생성

```yaml
resources:
- name: appserver
  type: compute.v1.instance

```
리소스 생성.

Type 보려면  `gcloud deployment-manager types list | grep v1.*instance`. List 까지만 입력하면 모든 type 볼 수 있다


yaml과 json은 상호 변환이 가능하다.

yaml에서 single Dash는 정말 중요함.
```yaml
accessConfigs:
   kind: compute#accessConfig
   type: string
   name: string
   natIP: string
```

얘는 `accessConfigs( kind:a, type:b, name:c, natIP:d )` 를 의미하고

```yaml
accessConfigs:
 - kind: compute#accessConfig
   type: string
   name: string
   natIP: string
```

얘는 `accessConfigs( [ (kind:a), (type:b), (name:c), (natIP:d) ] )` 를 의미한다.

기타 yaml 파일과 template 값 확인방법은

https://googlecoursera.qwiklabs.com/focuses/16466

여기서 보면 된다.

템플릿의 강력한 점은
```
gcloud deployment-manager deployments create development --config appserver.yaml
gcloud deployment-manager deployments create load-testing --config appserver.yaml
gcloud deployment-manager deployments create security --config appserver.yaml
gcloud deployment-manager deployments create production --config appserver.yaml
```

이 코드들로 deploy시 생각해야 할 점들을 해결할 수 있다는 것.

---
## Lab 2 : Package and deploy

https://googlecoursera.qwiklabs.com/focuses/16467
```yams
imports:
  - path: instance.jinja
  - path: install-echo.sh
    name: startup-script
resources:
  - name: instance
    type: instance.jinja
    properties:
      zone: [ZONE]
      tags:
        - http
      metadata:
        - key: echo
          value: https://storage.googleapis.com/[BUCKET]/echo-0.0.1.tar.gz
```

* tag http : tag will be applied to the instance. (해당 tag에 Firewall rule이 적용될 수 있도록)
* startup script가 boot 과정에서 실행될 수 있도록 세팅하는 부분 -> 여기서는 install-echo.sh 파일이 된다.
* metadata 부분의 key: echo 부분, value : [bucket] 부분은 앱이 처음 실행되고 booting 과정에서 접근할 곳을 말함. 여기 로직에서는 ech-0.0.1.tar.gz 파일을 해당 버킷에 생성하고, 그 버킷에서 Pip 명령어로 저 tar.gz 파일을 설치하는 식으로 진행할 예정

```jinja

{#
Copyright 2017 Google Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
#}

resources:
- name: {{ env['deployment'] }}
  type: compute.v1.instance
  properties:
    zone: {{ properties['zone'] }}
    machineType: zones/{{ properties['zone'] }}/machineTypes/{{ properties['machineType'] }}
    metadata:
      items:
        - key: deployment
          value: {{ env['deployment'] }}
        {% if imports['startup-script'] %}
        - key: startup-script
          value: |
            {{ imports['startup-script']|indent(12) }}
        {% endif %}
        {% for i in properties["metadata"] %}
        - {{ i }}
        {% endfor %}
    disks:
      - deviceName: boot
        boot: true
        autoDelete: true
        initializeParams:
          diskSizeGb: 10
          sourceImage: {{ properties['sourceImage'] }}
    networkInterfaces:
      - name: {{ ID }}-eth0
        network: {{ properties['network'] }}
        {% if properties['subnet'] %}
        subnetwork: {{ properties['subnet'] }}
        {% endif %}
        accessConfigs:
          - name: eth0
            type: ONE_TO_ONE_NAT
    serviceAccounts:
      - email: {{ properties['serviceAccount'] }}
        scopes:
          - 'https://www.googleapis.com/auth/cloud-platform'
    {% if properties['tags'] %}
    tags:
      items:
        {% for i in properties["tags"] %}
        - {{ i }}
        {% endfor %}
    {% endif %}

outputs:
  - name: url
    value: http://$(ref.{{ env['deployment'] }}.networkInterfaces[0].accessConfigs[0].natIP)
```

Instance.jinja 파일.

여기서 
```
 {% if imports['startup-script'] %}
        - key: startup-script
          value: |
            {{ imports['startup-script']|indent(12) }}
```

만약 startup-script가 있으면, make the key-value pair for the server metadata.


태그가 여러 개 있으면 iterate로 불러오는 것
```
tags:
      items:
        {% for i in properties["tags"] %}
        - {{ i }}
        {% endfor %}
```

#### Schema 파일

Why not develop and debug that template once, and then use it whenever an instance is needed. No one would need to write their own instance template.

The main value of the schema is it tells users of your template how they can interact with it. The schema defines a set of rules that the configuration file (the YAML file) must meet if it wants to use the template. And Deployment Manager checks and enforces those rules.

일종의 template용 API인 셈.

### Quiz

*How does a microservices design complicate business logic ?*
-> Key business logic is implemented as cross-services communications.

*Which GCP platform services are identified as useful for the 12-factor principle of “store configuration information in the environment”?*
-> Cloud storage, metadata server (config info 저장할 수 있는 곳들)

*What tradeoff occurs with the 12-factor principle of “store state information in the environment”?*
-> State information is more reliable when stored locally on a server if you use SSD.

*What advice is given on horizontal scaling design?*
-> Prefer small stateless servers. Keep servers simple, do one thing well

*What reason is given for the design advice to “design first and dimension later”?*
-> trying to optimize cost or size (dimension) before the design is fully developed = can lead to confusion and ambiguities in the design process.




---
## Data layer Quiz

*What does Data Integrity mean?*
-> user has access to their data and the data persists without being corrupted or lost.


---
## Adding Load balancer

https://googlecoursera.qwiklabs.com/focuses/16468

Health check를 허용하는 firewall rule을 생성해 줘야 한다.


---
## Presentation layer Quiz

*What is the difference between a proxied and a pass-through load balancer?*
-> proxied load balancer terminates the incoming connection and initiates a separate connection, a pass-through redirects traffic without terminating it.


*Which form of load balancing enables you to load balance behind an IP address that is only accessible to instances within your Virtual Private Cloud (VPC)?*
-> internal load balancer.

*What is the service provided by a third party (such as an ISP) that enables you to connect another cloud directly to your Google cloud resources to create hybrid cloud solutions?*
-> dedicated interconnect.


---
## Resiliency, scalability, Disaster recovery Quiz

*What is a correlated failure?*
-> Group of related items fail at the same time. The group is a failure group.

*How can a design to improve reliability through failover create an opportunity for overload failure?*
-> if growth occurs, and the capacity is not increased to accommodate the new greater load during failover.


*What is it called when you are trying to make a system more reliable by adding retries and it creates the opportunity for an overload failure?*
-> Positive feedback cycle overload failure.


*What is the recommended action to help cope with failure that involves Objectives and Indicators?*
-> incorporate failure planning including a margin of safety and scheduled downtime into the SLOs and SLIs.

*Why is DNS recommended for business continuity and disaster recovery?*
-> you can use it to redirect client requests to an alternative backup service by changing DNS definition.

*What is a cascading failure?*
-> when, due to an overload failure, the system seeks additional resources and spreads the overload until the system loses integrity.


---
## Design for security Quiz

*What does “pervasive defense in depth” mean?*
-> segregation of duties. Google handle sth, others are your responsibility.

*In most network devices such as a firewall, the network is subject to overload of the capacity of the interface. What is the overload capacity of a firewall in Google’s network?*
-> 구글의 firewall은 virtual. SW-defined다. No physical interface to be overloaded.


*Which edge features of Google’s networking provide automatic protections against Distributed Denial of Service attacks (DDoS) ?*
-> TCP/SSL proxy, Global load balancing, Cloud CDN

*Which of the following describes Cross-project VPC network peering?*
-> projects that are isolated in separate VPCs, but using network peering they can communicate over a private address space.

*What is the “principle of least privilege” as it relates to IAM Policies?*
-> grant roles at the smallest scope needed for individual or service account to be functional with the services they require.


---
## Capacity and Optimization Quiz

*What are three methods for reducing the price of virtual machines (VMs) in GCP?*
-> sustained use discount, committed use discount, preemptible VM

*What are the steps in the capacity planning cycle?*
-> forecast, allocate, approve, deploy


---

## Deployment and incident Response lab

https://googlecoursera.qwiklabs.com/focuses/16469



---
## Deployment and Incident Response Quiz

*What is the key advice presented about GCP deployment?*
-> automate everthing you can, bcz launch and release automation has an influence over reliability.

*What is the difference between black box monitoring and white box monitoring?*
-> blackbox monitoring : monitor only external observable. White box monitoring : monitor the system’s internal events.

*From the bottom up, what are the first three layers in the Site Reliability Engineering pyramid?*
-> Monitoring, incident response, postmortem & root cause analysis



#컴퓨터공학쪽지식/Coursera/GCP/ch5_infra_design_process/lab