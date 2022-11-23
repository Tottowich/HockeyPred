from testingfunctions import *

def main():
    Pitsburgh, Vancouver = rand_games(N=1000)
    print(Pitsburgh)
    Pitsburgh.plot("average")
    (Pitsburgh.total()-Vancouver.total()).plot()


if __name__ == '__main__':
    main()