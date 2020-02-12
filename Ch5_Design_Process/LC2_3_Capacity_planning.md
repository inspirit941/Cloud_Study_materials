# Capacity Planning and Cost optimization
## Overview

Both forecasting for future demand on a system, and planning the resources for a system, depend on non-abstract large-scale design sometimes called “dimensioning”.

디자인을 할 때, 리소스를 하나 바꾸는 게 다른 쪽에 영향을 줄 수 있다. 예컨대 CPU capacity를 맞추기 위해 VM size를 바꾸면, network throughput memory and disk capacity could change as a consequence.

따라서 뭐 하나 바꾸려 할 때는 그게 미칠 영향을 종합적으로 판단해서 결정해야 하고, perform the calculations to ensure that there’s sufficient capacity for your purpose.

가장 많이들 하는 실수가 optimize away resiliency. Excess capacity를 돈 좀 아끼겠다고 팍팍하게 설정했다가 cascade failure 발생할 수도 있다.

Cost optimization -> built in to many GCP services.


## Capacity planning

핵심 질문은 ‘is there sufficient resources with reasonable certainty?’다.

이전에 설명한 개념 중 하나로 design first, dimension later가 있었다. Change Design for capacity / for better pricing 둘 중 뭐가 됐던, what benefits you’re trading for reduced cost or better capacity management.



<img width="924" alt="스크린샷 2020-02-11 오후 9 38 57" src="https://user-images.githubusercontent.com/26548454/74295932-ca67a280-4d85-11ea-9a06-8c8ff55e28c2.png">

주기적인 과정으로, 네 개의 프로세스가 반복된다.
1. forecast. 예측에 사용할 데이터가 없으면 wild guess라도 한다.
2. allocate. 어떤 resource가 필요할지 확인하고 필요한 자원을 할당받는다.
3. approve. 자원을 승인받고
4. deploy


<img width="925" alt="스크린샷 2020-02-11 오후 11 13 58" src="https://user-images.githubusercontent.com/26548454/74295934-cf2c5680-4d85-11ea-93c3-1e7ab609fd53.png">


Iterative process라고 했다.
* 지난번 예측값은 어땠는지
* 예측값과 비교해서 높은지 낮은지
* 지난 에측값과의 오차를 prediction model에 반영해서
* 다시 에측

그렇게 되면 고민할 점은 what other values should you potentially include in your forecasting estimate? 가 된다.

 

<img width="921" alt="스크린샷 2020-02-11 오후 11 17 41" src="https://user-images.githubusercontent.com/26548454/74295950-e0756300-4d85-11ea-8e6c-c6245a8273d8.png">


- Don’t mistake launch demand for sth stable, or you might actually over-provision. stabilized될 때까지는 기다려야 한다 (게임 출시 - 안정화까지의 예시) 

- N+2 server 기억해라. Overload situation 방지를 위한 최소한의 조건임. Add head room to deal with non-linearity of demand.



<img width="925" alt="스크린샷 2020-02-11 오후 11 22 15" src="https://user-images.githubusercontent.com/26548454/74295957-e4a18080-4d85-11ea-9d9d-088ef05b1902.png">

Over estimate하긴 해야 하는데, 그게 또 과하면 안 된다. 어떻게 해야 하나


Well, if you take a look at 100% of the capacity of a VM, some of it is going to be consumed by overhead right out of the box. So if you can’t test, just say 30%, you’re only going to get only 30%, especially because you don’t want to run things at 100% due to potential cascading failures.

On-premise를 Cloud로 변환하려고 할 때 유의할 점

1. on-prem에서 8 core라면, VM에서 상응하는 파워를 내려면 16 core. vCPU는 hyper thread이기 때문
2. OS image. Image performance를 잘 낼 수 있는 testing을 해보는 걸 추천. 구글 팀에서의 조사로는 GCP에서 ubuntu가 안정적인 성능을 낸다.
3. 하드웨어도 필요한 거 알아서 테스팅해봐라. 어차피 하드웨어는 뭘 고르든 가격이 같다. (프로세서 같은)


<img width="923" alt="스크린샷 2020-02-11 오후 11 30 30" src="https://user-images.githubusercontent.com/26548454/74295960-e66b4400-4d85-11ea-92d5-832ddf8aee87.png">


we are simply Enabling our software to find quotas, and we are enabling that disk to perform to that level. 만약 CPU와 disk IO간 균형이 맞지 않으면 그 지점이 bottleneck이 된다.

(Standard SSD 성능 극대화를 위해서는 4개의 CPU가 필요하다.)




<img width="923" alt="스크린샷 2020-02-11 오후 11 37 08" src="https://user-images.githubusercontent.com/26548454/74295962-e79c7100-4d85-11ea-9761-9cffb9345dab.png">

Network capacity estimation. 이건 VM의 CPU 코어 개수에 따라 좌우되는 성능이다. 2 gigs of throughput for every CPU -> allow up to 16 gig인 셈. Quota 적용할 수도 있다.

VM에서는 internal network이 반드시 더 빠르기 마련.


<img width="922" alt="스크린샷 2020-02-11 오후 11 39 50" src="https://user-images.githubusercontent.com/26548454/74295963-e8350780-4d85-11ea-9429-bfa905ea5c66.png">


이건 어떤 종류의 throughput이 적용될지에 따라 다르다. Photo app의 예시에서 어떤 건 high throughput, 다른 건 high disk IO 였던 것처럼. 따라서 business logic의 어떤 부분이 어떤 effect일지를 이해하고 있어야 함.


<img width="925" alt="스크린샷 2020-02-11 오후 11 42 04" src="https://user-images.githubusercontent.com/26548454/74295965-e8cd9e00-4d85-11ea-8b6c-bf0495d5f7bc.png">


Performance benchmark의 표준으로 쓰이길 바라며 구글이 만든 오픈소스.

GCP의 경우 achieve efficiency at scale 형태로 디자인되어 있다. Single server 하나 테스트하고 gcp 느리다고 매도하진 말아달라



<img width="926" alt="스크린샷 2020-02-11 오후 11 44 31" src="https://user-images.githubusercontent.com/26548454/74296044-24686800-4d86-11ea-8656-82c15a6942cb.png">
 
‘얼마나 많은 자원이 estimation을 충족하기 위해 필요할 것인가’. 

Ratio of resources to capacity라고 이해하면 된다. 
you have to kind of ask your questions, and you’ll estimate what capacity is required, based on our forecast. How do we validate those estimates, we’re going to do so with load testing. 이렇게 얻은 데이터로 ‘이 정도 성능을 내려면 얼마의 자원이 필요하겠구나’ 산정하는 것

<img width="923" alt="스크린샷 2020-02-11 오후 11 46 51" src="https://user-images.githubusercontent.com/26548454/74296051-292d1c00-4d86-11ea-997b-fbd5331f85c1.png">



<img width="927" alt="스크린샷 2020-02-11 오후 11 47 48" src="https://user-images.githubusercontent.com/26548454/74296053-29c5b280-4d86-11ea-8bb6-4bf9320b0006.png">

그리고 뭐 항상 그렇듯, 자원 더 받는 거 말고 다른 대안은 없었는지 고민해야 한다. Adjust code라던가, 좋은 알고리즘이라던가, caching을 써본다던가. Dataflow로 ETL 프로세싱을 넘겨버린다던가… alternative service가 있지는 않은지 등등.


데이터 토대로 예측하고 산정한 결과물이면 approve될 거다.


<img width="919" alt="스크린샷 2020-02-11 오후 11 50 17" src="https://user-images.githubusercontent.com/26548454/74296055-2a5e4900-4d86-11ea-9209-914b4acda90e.png">


사용자에게 deploy하기 전까지 다각도로 test하는 게 중요함. integrity를 제공하는 게 목적인 만큼, bottleneck을 찾아내고 최대한 painless하게 만들어야 한다.

<img width="921" alt="스크린샷 2020-02-12 오전 12 00 04" src="https://user-images.githubusercontent.com/26548454/74296056-2b8f7600-4d86-11ea-9256-771751ca0f9c.png">



## Price

Design choice can influence price.


<img width="925" alt="스크린샷 2020-02-12 오전 12 08 28" src="https://user-images.githubusercontent.com/26548454/74296057-2b8f7600-4d86-11ea-833c-0f0dc7e83b08.png">

구글 측에서 제공하는 기본적인 price optimizing 방법.

VM의 경우 standard template의 설정을 선택한 뒤 optimize memory, cpus, gpu 등을 변경할 수 있다.

Machine type에 따른 discount나 sustained-use discount, instance discount 등등. Pre-pay 이후 사용량에 따른 use discount도 존재한다. (1 ~ 3년 쓰겠다고 하면 할인해주는 것)

Preemptive VM은 가격 면에서 좋은 선택지다.

<img width="924" alt="스크린샷 2020-02-12 오전 12 13 54" src="https://user-images.githubusercontent.com/26548454/74296058-2c280c80-4d86-11ea-91ca-888abe47688c.png">


HDD냐 SSD냐 차이. 


<img width="924" alt="스크린샷 2020-02-12 오전 12 14 24" src="https://user-images.githubusercontent.com/26548454/74296060-2cc0a300-4d86-11ea-903e-640884881386.png">


Multi zone이면, same region의 서로 다른 zone 간 통신은 원래 fee가 청구된다. (Egress 비용) 이 통신을 위해 필요한 비용이 따로 없으므로 1페니 per gig. 인터넷으로 egress할 경우 $0.08 per gig.

CDN, dedicated network connectivity to google (partner이거나 private이거나…) 상관없이 50% discount.

different region으로의 통신은 standard egress 취급 (intercontinental과 동일하다). 물론 intercontinental 이 약간 더 비싸긴 하지만.


<img width="920" alt="스크린샷 2020-02-12 오전 12 18 10" src="https://user-images.githubusercontent.com/26548454/74296130-5a0d5100-4d86-11ea-8dbf-72786d78622e.png">


Same Zone에서의 instance 통신이면, 최대 16gig이지만 그거 넘어서도 가능하긴 하다. Optimized 빡세게 하고 network driver 활용해서

