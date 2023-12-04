#include <iostream>

#include "simulation.h"
#include "bpsk-simulation.h"

int main(int argc, char **argv)
{
    std::cout << "NASA Deep Space Network simulator" << std::endl;

    std::cout << "Serão simulados os seguintes canais:" << std::endl;
    std::cout << "\t* Canal BPSK AWGN" << std::endl;
    std::cout << "\t* Reed-Solomon RS(255, 223) sobre canal BPSK AWGN" << std::endl;
    std::cout << "\t* Código convolucional CC (R=0.5,K=7) sobre BPSK AWGN" << std::endl;
    std::cout << "\t* Código concatenado RS(255, 223) com CC(R=0.5, K=7) BPSK AWGN" << std::endl;

    BpskSimulation bpsk_sim;

    int32_t st = bpsk_sim.Run();
    if (st != Simulation::E_SUCCESS) {
        std::cout << "Erro na execução da simulação BPSK!" << std::endl;
        goto exit;
    }

    exit:
    return 0;
}