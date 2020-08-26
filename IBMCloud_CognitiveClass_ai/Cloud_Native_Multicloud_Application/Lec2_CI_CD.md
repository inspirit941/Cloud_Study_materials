

## Continuous Integration / Continuous Delivery

### Continuous Integration

https://www.youtube.com/watch?v=1er2cjUq1UI

<img width="705" alt="스크린샷 2020-08-26 오후 2 04 10" src="https://user-images.githubusercontent.com/26548454/91270950-67cf7480-e7b4-11ea-9d04-49e8c0a18ea6.png">

요약
- Infrequent Merging에서 발생하는 Merge Hell 문제를 해결하고
- Constantly testable Build를 제공하는 Integration 방식


* Everybody thinks that they're doing, but it's widely misunderstood.

독립된 환경에서 일하는 두 명 이상의 개발자가, 서로의 코드 작업을 합치려 할 때를 가정.

* Old School Approach

동일한 코드를 누군가는 수정하고 / 누군가는 삭제한 상황이라면 Merge Conflict가 발생한다. 이 변경사항이 각자의 코드 로직에 영향을 끼치므로, 코드를 합칠 경우 버그 발생의 원인이 되기도 함. 코드 파일 하나만 수정해도 이렇게 되는데, 많은 개발자가 투입된 애플리케이션의 경우 문제는 더 심각해진다.

-> Merge Hell이라고 부른다.

**Merge Hell을 해결하는 방법?**

- Code base에 변경사항을 Commit하고, 다른 개발자가 작업할 때 마지막으로 변경된 사항을 pull down 후 작업하는 식. 이 경우, Last Change를 토대로 작업한다.

단, 이 방식도 단점이 명확하다.

- Whole People constantly checking in code into the code base.
- 어제 작동하는 코드가 오늘 컴파일이 안 된다거나, 어제 없었던 버그가 오늘 생기는 등 **Continuous Integration leads to continuous broken** 문제 발생.

해결책 -> 일종의 Safety Net 구축.

- 코드 변경이 생길 때마다 build / test 수행. success하지 않을 경우 관련된 팀 사람들에게 메일로 안내한다. (현재 코드 상황이 무엇인지 - broken, 누가 작업했는지 등)

매번 Build와 Test를 거치는 작업을 한다는 건, 하나의 커밋을 제대로 하기 위해서는 Build / Test가 가능할 만큼의 완성도가 필요하다는 것.

**We always have a Testable Build**


---

### Continuous Delivery

https://www.youtube.com/watch?v=2TTU5BB-k9U

<img width="702" alt="스크린샷 2020-08-26 오후 3 53 05" src="https://user-images.githubusercontent.com/26548454/91270966-6d2cbf00-e7b4-11ea-9970-879f81afd481.png">

* How do I quickly get CODE into Production? 에 관련된 문제.

1. Code를 SW로 변환해야 한다. = Build.
2. SW를 Production에 적용하기 위해 Test를 거친다. 다양한 환경에서 프로그램이 작동하는지 테스트. = QA.
3. Performance / Stage Env에 적용
4. Production에 적용.

* Continuous Delivery의 Backbone
Code -> Build -> QA -> Stage -> Production

#### Key Behavior?

1. 각각의 step마다 이루어지는 Migration.
    특히 Build -> OA -> Stage -> Production은 Auto Deploy를 지원하는 Tool이 많다.
    * how do my builds move through the Env?
    * what's the order of the Env?
    * how do I manage & govern?
    * Are there any roles for when I need to move from each step? 등등.

2. QA, Stage 과정에서의 Auto Testing. 이걸 지원하는 Tool도 따로 있음.
3. Build를 담당하는 CI server.

여기에, 보통 Stage -> Production 진행단계에서는 another level of governance가 필요함.

예컨대 코드를 깃허브에 올리면
- CI 서버에서 build & QA로 Deplot
- QA에서 Test 수행 & Stage로 Deploy
- Stage에서 또 다른 종류의 Test 수행.
이 작업은 자동화가 가능하다. 하지만 Production으로 넘어가기 전에는 Human involved. **Change Approval Board (CAB)** 단순한 작업이라 해도, 최종 확인차원에서 사람의 승인을 요구하는 경우가 많음.









