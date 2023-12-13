#include <iostream>

#include "simulation.h"
#include "bpsk-simulation.h"
#include "rs-simulation.h"
#include "cc-simulation.h"
#include "conc-simulation.h"

int main(int argc, char **argv)
{
    std::cout << "NASA Deep Space Network simulator" << std::endl;

    std::cout << "Serão simulados os seguintes canais:" << std::endl;
    std::cout << "\t* Canal BPSK AWGN" << std::endl;
    std::cout << "\t* Reed-Solomon RS(255, 223) sobre canal BPSK AWGN" << std::endl;
    std::cout << "\t* Código convolucional CC (R=0.5,K=7) sobre BPSK AWGN" << std::endl;
    std::cout << "\t* Código concatenado RS(255, 223) com CC(R=0.5, K=7) BPSK AWGN" << std::endl;

    itpp::vec EbN0dB = itpp::linspace(0, 8, 16);

    BpskSimulation bpsk_sim(1000000);
    RsSimulation rs_sim(8*223*561); // m * k * NumCodewords
    CcSimulation cc_sim(1000000);
    ConcSimulation conc_sim(8*223*561);

    int32_t st;

    st = bpsk_sim.Run(EbN0dB);
    if (st != Simulation::E_SUCCESS) {
        std::cout << "Erro na execução da simulação do BPSK!" << std::endl;
    }

    st = rs_sim.Run(EbN0dB);
    if (st != Simulation::E_SUCCESS) {
        std::cout << "Erro na execução da simulação do ReedSolomon!" << std::endl;
    }

    st = cc_sim.Run(EbN0dB);
    if (st != Simulation::E_SUCCESS) {
        std::cout << "Erro na execução da simulação do Código Convolucional!" << std::endl;
    }

    st = conc_sim.Run(EbN0dB);
    if (st != Simulation::E_SUCCESS) {
        std::cout << "Erro na execução da simulação do Código Concatenado!" << std::endl;
    }

    exit:
    return 0;
}