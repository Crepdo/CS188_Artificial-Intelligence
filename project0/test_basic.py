# This is what a comment looks like
from importlib import reload #reload for modules imported
fruits = ['apples', 'oranges', 'pears', 'bananas']
for fruit in fruits:
    print(fruit + ' for sale')

fruitPrices = {'apples': 2.00, 'oranges': 1.50, 'pears': 1.75}
for fruit, price in fruitPrices.items():
    if price < 2.00:
        print('%s cost %f a pound' % (fruit, price))
    else:
        print(fruit + ' are too expensive!')

for case in list((map(lambda x: x*x,[1,2,3]))):
    print(case)

nums=[1,2,3]
plusOneNums = [x+1 for x in nums]
oddNums=[x for x in nums if x%2 ==1]
print(oddNums)
oddNumsPlusOne = [x+1 for x in nums if x%2 ==1]
print(oddNumsPlusOne)

def buyFruit(fruit,numPounds):
    if fruit not in fruitPrices :
        print('fail')
    else:
        cost = fruitPrices[fruit]*numPounds
        print("That'll be %f please" % (cost))

def qsort(list):
    if list == []: return []
    pivot = list[0]
    l = qsort([x for x in list[1:] if x < pivot])
    u = qsort([x for x in list[1:] if x >= pivot])
    return l + [pivot] + u

class FruitShop:

    def __init__(self, name, fruitPrices):
        """
            name: Name of the fruit shop

            fruitPrices: Dictionary with keys as fruit
            strings and prices for values e.g.
            {'apples': 2.00, 'oranges': 1.50, 'pears': 1.75}
        """
        self.fruitPrices = fruitPrices
        self.name = name
        print('Welcome to %s fruit shop' % (name))

    def getCostPerPound(self, fruit):
        """
            fruit: Fruit string
        Returns cost of 'fruit', assuming 'fruit'
        is in our inventory or None otherwise
        """
        if fruit not in self.fruitPrices:
            return None
        return self.fruitPrices[fruit]

    def getPriceOfOrder(self, orderList):
        """
            orderList: List of (fruit, numPounds) tuples

        Returns cost of orderList, only including the values of
        fruits that this fruit shop has.
        """
        totalCost = 0.0
        for fruit, numPounds in orderList:
            costPerPound = self.getCostPerPound(fruit)
            if costPerPound != None:
                totalCost += numPounds * costPerPound
        return totalCost

    def getName(self):
        return self.name


if __name__ == '__main__':
    buyFruit('apples',2.4)
    buyFruit('coconuts',2)
    print(qsort([]))

shopName = 'the Berkeley Bowl'
fruitPrices = {'apples': 1.00, 'oranges': 1.50, 'pears': 1.75}
berkeleyShop = FruitShop(shopName, fruitPrices)
applePrice = berkeleyShop.getCostPerPound('apples')
print(applePrice)
print('Apples cost $%.2f at %s.' % (applePrice, shopName))

otherName = 'the Stanford Mall'
otherFruitPrices = {'kiwis': 6.00, 'apples': 4.50, 'peaches': 8.75}
otherFruitShop = FruitShop(otherName, otherFruitPrices)
otherPrice = otherFruitShop.getCostPerPound('apples')
print(otherPrice)
print('Apples cost $%.2f at %s.' % (otherPrice, otherName))
print("My, that's expensive!")

class Person:
    population = 0

    def __init__(self, myAge):
        self.age = myAge
        Person.population += 1

    def get_population(self):
        return Person.population

    def get_age(self):
        return self.age
p1 = Person(12)
temp=p1.get_population()
print(temp)
p2 = Person(63)
print(p2.get_population())
Person.population=0 #static refresh
p3 = Person(63)
print(p2.get_population())
#singleton