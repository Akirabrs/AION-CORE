// ARQUIVO: aion_burn_types_v1.sv
timescale 1ns/1ps
package aion_burn_types_v1;
    // Q16.16: Formato padrão para física
    typedef logic signed [31:0] q16_16_t;
    // Q2.14: Para geometria fina
    typedef logic signed [15:0] q2_14_t;

    typedef struct packed {
        q16_16_t temp_keV;
        q16_16_t p_alpha;
        q16_16_t beta_pol;
    } thermal_state_t;

    typedef struct packed {
        q16_16_t z_pos;
        q2_14_t kappa;
        q2_14_t delta;
    } geometry_state_t;
endpackage
