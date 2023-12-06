#ifndef BPSK_SIMULATION_H_
#define BPSK_SIMULATION_H_

#include "simulation.h"

#include <cstdint>
#include <itpp/itcomm.h>

class BpskSimulation : public Simulation {

public:

    BpskSimulation(int32_t nbits = 500000, int32_t MaxIterations = 10, int32_t MaxErrors = 100);
    virtual ~BpskSimulation();

    int32_t Run(itpp::vec &EbN0dB) override;

private:
    int32_t Nbits;
    int32_t MaxIterations;
    int32_t MaxErrors;
};

#endif