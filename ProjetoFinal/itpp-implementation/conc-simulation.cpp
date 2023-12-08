#include "conc-simulation.h"

#include <iostream>
#include <cstdint>
#include <itpp/itcomm.h>

using namespace itpp;

ConcSimulation::ConcSimulation(int32_t nbits, int32_t MaxIterations, int32_t MaxErrors) :
    Nbits(nbits), MaxIterations(MaxIterations), MaxErrors(MaxErrors)
{
    RNG_randomize();
}

ConcSimulation::~ConcSimulation()
{

}

int32_t ConcSimulation::Run(vec &EbN0dB)
{
    int32_t ret = E_SUCCESS;

    // vec EbN0dB = linspace(0, 4, 16);
    vec EbN0 = inv_dB(EbN0dB);

    AWGN_Channel awgn_Channel;
    BPSK bpsk;
    BERC berc;
    Reed_Solomon rs(8, 16);
    Convolutional_Code cc;
    ivec generators;
    Block_Interleaver<double> interleaver(2, 8*223);

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
    double Eb = Ec / rs.get_rate() / cc.get_rate();

    // Calculando os valores de N0 para todos os EbN0
    vec N0 = Eb*pow(EbN0, -1);

    for (int32_t p = 0; p < EbN0dB.length(); p++) {
        std::cout << "Simulando ponto " << p + 1 << " de " << EbN0dB.length() << std::endl;

        berc.clear();
        awgn_Channel.set_noise(N0(p) / 2.0);

        for (int32_t i = 0; i < this->MaxIterations; i++) {
            bvec bits, rec_bits, coded_bits, rs_coded_bits;
            bits = randb(this->Nbits);

            // Encode RS(7, 4)
            rs_coded_bits = rs.encode(bits);

            coded_bits = cc.encode(rs_coded_bits);

            // Modular BPSK
            vec trans_symbols;
            bpsk.modulate_bits(coded_bits, trans_symbols);

            // Interleaving
            vec interleaved_symbols = interleaver.interleave(trans_symbols);

            // Passar no canal AWGN
            vec rec_interleaved = awgn_Channel(interleaved_symbols);

            // Deinterleaving
            vec rec_symbols = interleaver.deinterleave(rec_interleaved);

            // Decodificação CC -- soft decision
            bvec decoded_bits, rs_decoded_bits;
            rs_decoded_bits = cc.decode(rec_symbols);

            // Decode RS(7, 4)
            bvec cw_isvalid;
            rs.decode(rs_decoded_bits, decoded_bits, cw_isvalid);

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

    std::ofstream csvfile("conc.csv");

    std::cout << "Concatenado ***** Resultado final: " << std::endl;
    std::cout << "ber, ebn0db" << std::endl;
    csvfile << "ber, ebn0db" << std::endl;
    for (int32_t i = 0; i < ber.length(); i++) {
        std::cout << ber(i) << ", " << EbN0dB(i) << std::endl;
        csvfile << ber(i) << ", " << EbN0dB(i) << std::endl;
    }

    csvfile.close();

    return ret;
}