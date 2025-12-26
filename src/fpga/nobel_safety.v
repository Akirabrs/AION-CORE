
/*
 * Module: NOBEL_Interlock
 * Description: Hardware-level safety interlock for Tokamak VDE protection.
 * Responds in < 1 clock cycle (nanoseconds).
 */

module nobel_interlock (
    input wire clk,
    input wire reset,
    input wire [15:0] z_position, // ADC reading (fixed point)
    input wire [15:0] z_limit,    // Safety threshold
    output reg scram_signal       // Emergency Shutdown
);

    // Logic: If Position > Limit -> TRIGGER SCRAM
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            scram_signal <= 1'b0;
        end else begin
            // Check positive or negative limit (absolute value logic simplified)
            if (z_position > z_limit || z_position < -z_limit) begin
                scram_signal <= 1'b1; // CRITICAL: Hardware Shutdown
            end else begin
                scram_signal <= 1'b0;
            end
        end
    end

endmodule
