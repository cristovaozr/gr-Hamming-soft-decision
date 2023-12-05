#ifndef SIMULATION_H_
#define SIMULATION_H_

#include <cstdint>

class Simulation {

public:

    Simulation();
    virtual ~Simulation();

    virtual int32_t Run() = 0;

    enum SimulationSuccess {
        E_WRONG_PARAMETER = INT32_MIN,
        E_DECODING_FAILED,

        E_SUCCESS = 0
    };
};

#endif  // SIMULATION_H_