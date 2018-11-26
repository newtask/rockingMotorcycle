#!/usr/bin/python3
from rockingMotorcycle import RockingMotorcycleGame

if __name__ == "__main__":
    print("Start game. Rock on!!!")

    game = RockingMotorcycleGame(startVolume=90, changeDelta=1000, limit=0.2, imuAddress=0x1d)

    try:
        game.run()
    except KeyboardInterrupt:
        game.stop()
        print("Stopped game")
