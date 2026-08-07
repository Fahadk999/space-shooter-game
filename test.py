health = 100
speed = 1500

def onSubmit (func):
    n = int(input("Ebter: "))

    if n == 1:
        func()
        print(health)
        print(speed)
    else:
        print("Dose Nothing")

def upgrade (health, speed):
    health += 10
    speed -= 30

while True:
    onSubmit(upgrade(health, speed))