#include "cc-simulation.h"

#include <iostream>
#include <cstdint>
#include <itpp/itcomm.h>

using namespace itpp;

CcSimulation::CcSimulation(int32_t nbits, int32_t MaxIterations, int32_t MaxErrors) :
    Nbits(nbits), MaxIterations(MaxIterations), MaxErrors(MaxErrors)
{
    RNG_randomize();
}

CcSimulation::~CcSimulation()
{

}

int32_t CcSimulation::Run(vec &EbN0dB)
{
    int32_t ret = E_SUCCESS;

    vec EbN0 = inv_dB(EbN0dB);
    ivec generators;

    AWGN_Channel awgn_Channel;
    BPSK bpsk;
    BERC berc;
    Convolutional_Code cc;

    generators.set_size(3, false);
    generators(0) = 0133;
    generators(1) = 0145;
    generators(2) = 0175;
    int32_t constraint_length = 7;
    cc.set_generator_polynomials(generators, constraint_length);

    vec ber;
    ber.set_size(EbN0dB.length(), false);
    ber.clear();

    // Determinar Eb a partir de Ec
    double Ec = 1.0;
    double Eb = Ec / cc.get_rate();

    // Calculando os valores de N0 para todos os EbN0
    vec N0 = Eb*pow(EbN0, -1);

    for (int32_t p = 0; p < EbN0dB.length(); p++) {
        std::cout << "Simulando ponto " << p + 1 << " de " << EbN0dB.length() << std::endl;

        berc.clear();
        awgn_Channel.set_noise(N0(p) / 2.0);

        for (int32_t i = 0; i < this->MaxIterations; i++) {
            bvec bits, rec_bits, coded_bits;
            bits = randb(this->Nbits);
            // Encode CC
            coded_bits = cc.encode(bits);
            vec trans_symbols;
            // Modular BPSK
            bpsk.modulate_bits(coded_bits, trans_symbols);
            // Passar no canal AWGN
            vec rec_symbols = awgn_Channel(trans_symbols);
            // Decode CC -- soft decision
            bvec decoded_bits;
            decoded_bits = cc.decode(rec_symbols);

            berc.count(bits, decoded_bits);
            double err_rate = berc.get_errorrate();
            if (err_rate == 0.0) err_rate = 1e-8;
            ber(p) = err_rate;
            if (berc.get_errors() > this->MaxErrors) {
                std::cout << "Saindo do ponto " << p + 1 << " com " << berc.get_errors() << " erros." << std::endl;
                break;
            }

        }
    }

    std::ofstream csvfile("cc.csv");

    std::cout << "CC ***** Resultado final: " << std::endl;
    std::cout << "ber, ebn0db" << std::endl;
    csvfile << "ber, ebn0db" << std::endl;
    for (int32_t i = 0; i < ber.length(); i++) {
        std::cout << ber(i) << ", " << EbN0dB(i) << std::endl;
        csvfile << ber(i) << ", " << EbN0dB(i) << std::endl;
    }

    csvfile.close();

    return ret;
}