module reflex_core (
    input wire clk, rst_n, 
    input wire signed [15:0] z_pos, z_vel,
    output reg signed [15:0] u_out
);
    // AEGIS Logic: Guardian Mode
    always @(posedge clk) begin
        if (z_vel > 50 || z_vel < -50) 
            u_out <= -2000; // Safety Trigger
        else 
            u_out <= -(z_pos * 10 + z_vel * 5); // Normal PACC Control
    end
endmodule
