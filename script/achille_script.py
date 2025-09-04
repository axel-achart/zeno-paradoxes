speed_achille = 10
speed_tortoise = speed_achille/2
position_achille = 0
position_tortoise = 100
iteration = 0
total_time = 0

def move_ach_to_tort(position_achille,position_tortoise,speed_achille,speed_tortoise,iteration,total_time):
    length_achille_to_tortoise = position_tortoise - position_achille
    position_achille = position_tortoise
    time_spent = length_achille_to_tortoise/speed_achille
    position_tortoise = position_tortoise + time_spent * speed_tortoise
    iteration+=1
    total_time = total_time + time_spent
    print(f"Achille : {position_achille}m\nTortue : {position_tortoise}m\nIterations : {iteration}\nTotal time : {total_time}s")
    return position_tortoise,position_achille,iteration,total_time


def move_achille(position_achille,speed_achille):
    position_achille = position_achille + speed_achille
    return position_achille

def move_tortoise(position_tortoise,speed_tortoise):
    position_tortoise = position_tortoise + speed_tortoise
    return position_tortoise

def race(position_achille,speed_achille,position_tortoise,speed_tortoise,iteration,total_time):
    position_achille = move_achille(position_achille,speed_achille)
    position_tortoise = move_tortoise(position_tortoise,speed_tortoise)
    iteration += 1
    total_time +=1
    print(f"Achille : {position_achille}m\nTortoise : {position_tortoise}m\nIterations : {iteration}\nTotal Time : {total_time}s")
    return position_tortoise,position_achille,iteration,total_time

def run(position_achille,position_tortoise,speed_achille,speed_tortoise,iteration,total_time):
    answer = input("Do you want to make Achille catch back the tortoise (1) or do you want to make them run at their pace (2)")
    if answer == "1":
        while position_achille<position_tortoise:
            position_tortoise,position_achille,iteration,total_time = move_ach_to_tort(position_achille,position_tortoise,speed_achille,speed_tortoise,iteration,total_time)
        position_achille = 0
        position_tortoise = 100
        iteration = 0
        total_time = 0

    elif answer == "2":
        while position_achille<position_tortoise:
            position_tortoise,position_achille,iteration,total_time=race(position_achille,speed_achille,position_tortoise,speed_tortoise,iteration,total_time)
        position_achille = 0
        position_tortoise = 100
        iteration = 0
        total_time = 0

    run(position_achille,position_tortoise,speed_achille,speed_tortoise,iteration,total_time)

run(position_achille,position_tortoise,speed_achille,speed_tortoise,iteration,total_time)