#include "bpsk-simulation.h"

#include <iostream>
#include <cstdint>
#include <itpp/itcomm.h>

using namespace itpp;

BpskSimulation::BpskSimulation(int32_t nbits, int32_t MaxIterations, int32_t MaxErrors) :
    Nbits(nbits), MaxIterations(MaxIterations), MaxErrors(MaxErrors)
{
    RNG_randomize();
}

BpskSimulation::~BpskSimulation()
{

}

int32_t BpskSimulation::Run()
{
    vec EbN0dB = linspace(0, 4, 16);
    vec EbN0 = inv_dB(EbN0dB);

    AWGN_Channel awgn_Channel;
    BPSK bpsk;
    BERC berc;

    vec ber;
    ber.set_size(EbN0dB.length(), false);
    ber.clear();

    // Calculando os valores de N0 para todos os EbN0
    vec N0 = pow(EbN0, -1);

    for (int32_t p = 0; p < EbN0dB.length(); p++) {
        std::cout << "Simulando ponto " << p + 1 << " de " << EbN0dB.length() << std::endl;

        berc.clear();
        awgn_Channel.set_noise(N0(p) / 2.0);

        for (int32_t i = 0; i < this->MaxIterations; i++) {
            bvec rec_bits, bits = randb(this->Nbits);
            vec trans_symbols;
            // Modular BPSK
            bpsk.modulate_bits(bits, trans_symbols);
            // Passar no canal AWGN
            vec rec_symbols = awgn_Channel(trans_symbols);
            // Demodular BPSK
            bpsk.demodulate_bits(rec_symbols, rec_bits);
            berc.count(bits, rec_bits);
            ber(p) = berc.get_errorrate();
            if (berc.get_errors() > this->MaxErrors) {
                std::cout << "Saindo do ponto " << p + 1 << " com " << berc.get_errors() << " erros." << std::endl;
                break;
            }
        }
    }

    std::cout << "Resultado final: " << std::endl;
    std::cout << "ber, ebn0db" << std::endl;
    for (int32_t i = 0; i < ber.length(); i++) {
        std::cout << ber(i) << ", " << EbN0dB(i) << std::endl;
    }

    return SimulationSuccess::E_SUCCESS;
}