#!/usr/bin/python3
from rockingMotorcycle import RockingMotorcycleGame

if __name__ == "__main__":
    print("Start game. Rock on!!!")

    game = RockingMotorcycleGame(startVolume=90)

    try:
        game.run()
    except KeyboardInterrupt:
        game.stop()
        print("Stopped game")
