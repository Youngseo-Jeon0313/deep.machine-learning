class GA:

//GA(유전알고리즘)라는 클래스를 만든다.

def __init__(self, tourmanager):

self.tourmanager = tourmanager //초기 값으로 tourmanager를 다시 받고,

self.mutationRate = 0.015

self.tournamentSize = 5 //토너먼트 크기는 5다.

self.elitism = True

def evolvePopulation(self, pop):

//지금까지 모아 놓은 경로들을 진화시키겠다.

newPopulation = Population(self.tourmanager, pop.populationSize(), False)

//새로운 경로 / 세대는 열성. . . (여기 해석 불가. 아마도 경로 둘을 조합해 다시 또 새로운 세대를 만들어주는 역할인 듯!

elitismOffset = 0 //elitism상쇄라는 변수에 0을 넣어준다.

if self.elitism:   //방금 진화를 시켰는데도, 만약 elitism이 True라면 --우성이라면?

newPopulation.saveTour(0, pop.getFittest()) //새로운세대 변수에

elitismOffset = 1  //그리고 elitismOffset이라는 변수에 다시 1을 넣어준다.

for i in range(elitismOffset, newPopulation.populationSize()):

parent1 = self.tournamentSelection(pop) //부모1에는 tournament형식으로 넣어준다. (이 때 tournament형식이란 무작위로 개인을 선택해서 최고를 뽑는다)

parent2 = self.tournamentSelection(pop) //부모2도 tournament형식으로 넣어준다.

child = self.crossover(parent1, parent2) 그리고 자식은 parent1과 parent2로 걸러진 상태에서 다시 crossover(꼬리를 서로 change해서 더 최고를 뽑는 방법) 방식 선택.

newPopulation.saveTour(i, child)

//

for i in range(elitismOffset, newPopulation.populationSize()):

self.mutate(newPopulation.getTour(i))

//새로운 파생함수를 만들어준다. (경로를 찾자!)

return newPopulation

def crossover(self, parent1, parent2): //crossover 방법을 사용해서 더 효과적인 방안을 찾고자 한다.

child = Tour(self.tourmanager)  //Tour함수에 tourmanager를 넣어서 자식으로 만들어준다.

startPos = int(random.random() * parent1.tourSize()) //startPos는 부모1의 사이즈에 random만큼을 곱해주고..

endPos = int(random.random() * parent1.tourSize()) //endPos도 똑같이 한다.

for i in range(0, child.tourSize()): //이제 루프를 돌린다.

if startPos < endPos and i > startPos and i < endPos:  //자식에 있는 i들을 검사할 때 i가 startPos와 endPos 사이에 있다면

child.setCity(i, parent1.getCity(i)) //자식에는 setCity함수를 대입

elif startPos > endPos: //start position 이 end position보다 클 때는

방금 위에 코드랑 같은 맥락임 - 순서만 다를 뿐

if not (i < startPos and i > endPos):

child.setCity(i, parent1.getCity(i))

for i in range(0, parent2.tourSize()): //

if not child.containsCity(parent2.getCity(i)):

for ii in range(0, child.tourSize()):

if child.getCity(ii) == None:

child.setCity(ii, parent2.getCity(i))

break

return child

def mutate(self, tour):

for tourPos1 in range(0, tour.tourSize()):

if random.random() < self.mutationRate:

tourPos2 = int(tour.tourSize() * random.random())

city1 = tour.getCity(tourPos1)

city2 = tour.getCity(tourPos2)

tour.setCity(tourPos2, city1)

tour.setCity(tourPos1, city2)

def tournamentSelection(self, pop):

tournament = Population(self.tourmanager, self.tournamentSize, False)

for i in range(0, self.tournamentSize):

randomId = int(random.random() * pop.populationSize())

tournament.saveTour(i, pop.getTour(randomId))

fittest = tournament.getFittest()

return fittest

진화 - 선택 과정

한 세대에서 다음 세대로 전해지는 해의 후보가 되는 해들을 선택한다. 선택방법은 토너먼트 형식이었다. 첫 세대는 parent1, parent2로 tournament로 돌려 뽑아 최적해를 선정한 후, 그 둘을 이번에는 crossover 방법을 이용해(꼬리를 서로 change해서 더 최고를 뽑는 방법)

이후 startposition은 parent1 경로 사이즈에 random으로 뽑은 위치값들을 곱해주고, endposition은 parent2 경로 사이즈에 random으로 뽑은 위치값들을 곱해준다.

이제 child값은 0부터 child의 경로 사이즈까지를 루프로 돌려주는데, 그 과정에서 child 경로의 사이즈가 startposition과 endposition사이에 있어야 getcity함수로 채택해 적합도와 거리를 측정할 수 있도록 실행한다. 이 때 적합도(fitness)는 당연하게도 거리에 반비례한다.

이 과정에서 변이가 나오는 것을 표현하기도 한다. 변이 연산은 주어진 해의 유전자 내의 유전 인자의 순서 혹은 값이 임의로 변경되어 다른 해로 변형되는 연산이다. 우성과 우성이 교배했는데 열성이 나오는 것이라고 생각하면 된다. 그래서 약간의 확률로 변이 연산을 수행해 ㅜ면 전체 세대가 함께 지역 최적해에 빠져드는 경우를 방지하기 위한 주요한 기법이다. 또한 해집단의 다양성을 높여준다. 이 코드에서는 tourPos1, tourPos2 등으로 지정해 주었다.

이런 진화/변이의 과정을 통해서 만들어진 새로운 해를 해집단에 추가하고 열성을 가려내서 제외시키는 연산을 대치라고 한다. 이 알고리즘에서는 True False등을 이용해 ㅜ성과 열성을 표현했는데, python문법 중 True *True = True/ True*False =False를 이용하였다고 볼 수 있다.

이렇게 해서 fittest한 경로를 결정해 낸다.