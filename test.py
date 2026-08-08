health = 100
speed = 1500

def onSubmit (func, *args):
    global health, speed 
    health, speed = func(*args)



def upgrade (h, s):
    return h + 10, s - 100

onSubmit(upgrade, health, speed)
print(health, speed)