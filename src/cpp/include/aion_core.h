
/**
 * @file aion_core.h
 * @brief C++ Implementation of AION MPC Controller for Embedded Systems
 * @author Guilherme Brasil (Akira)
 */

#ifndef AION_CORE_H
#define AION_CORE_H

#include <vector>
#include <cmath>

class AIONController {
public:
    AIONController(float dt, float max_voltage);
    float compute_control(float z_pos, float z_vel);
    void update_model(float error);

private:
    float dt_;
    float max_voltage_;
    float integral_error_;
    // Simplified MPC gains for embedded (pre-computed)
    const float K_p = -50.0;
    const float K_d = -10.0;
    const float K_i = -2.0;
};

#endif // AION_CORE_H
