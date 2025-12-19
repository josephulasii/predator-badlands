
from simulation import Simulation


def main():
    simulation = Simulation()

    while simulation.turncount < 20:
        simulation.run_turn()
        simulation.display()
        
        if simulation.dek.is_alive() == False:
            print("Dek has been killed")
            break

        if simulation.adversary.is_alive() == False:
            print("Dek has Killed The Boss" )
            break


    
        


if __name__ == "__main__":
    main()