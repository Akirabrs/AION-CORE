// ARQUIVO: aion_fpga_twin_bus.sv
// CLASSIFICAÇÃO: SEGREDO INDUSTRIAL
module aion_fpga_twin_bus (
    input wire clk,
    input wire rst_n,
    input aion_burn_types_v1::thermal_state_t core_in,
    input wire core_valid,
    input aion_burn_types_v1::geometry_state_t edge_in,
    input wire edge_valid,
    output logic scram_alarm
);
    import aion_burn_types_v1::*;
    
    localparam q16_16_t MIN_DIST = 32'h0000_2666; // Limite 15cm

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) scram_alarm <= 1'b0;
        else begin
            // Lógica Guardian (Constitucional)
            if (edge_in.z_pos > MIN_DIST) scram_alarm <= 1'b1;
            else scram_alarm <= 1'b0;
        end
    end
endmodule
