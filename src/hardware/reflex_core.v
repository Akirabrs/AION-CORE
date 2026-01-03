`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: Guibral-Labs
// Engineer: Guilherme Brasil
// Design Name: AION-CORE Reflex Layer
// Module Name: reflex_core
// Target Devices: Xilinx Zynq-7000 (XC7Z020)
// Description: Layer 1 deterministic control kernel (< 1us latency).
//////////////////////////////////////////////////////////////////////////////////

module reflex_core #(
    parameter DATA_WIDTH = 16,
    parameter PWM_WIDTH = 12,
    parameter VELOCITY_THRESHOLD = 16'd1000
)(
    input wire clk,
    input wire rst_n,
    input wire signed [DATA_WIDTH-1:0] adc_data,
    input wire [15:0] kp_gain,
    input wire [15:0] kd_gain,
    output reg signed [PWM_WIDTH-1:0] pwm_out,
    output reg safety_trigger
);
    reg signed [DATA_WIDTH-1:0] prev_z;
    reg signed [DATA_WIDTH-1:0] velocity;
    reg signed [31:0] control_effort;
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pwm_out <= 0; prev_z <= 0; velocity <= 0; safety_trigger <= 0;
        end else begin
            velocity <= adc_data - prev_z;
            prev_z <= adc_data;

            if ((velocity > VELOCITY_THRESHOLD) || (velocity < -VELOCITY_THRESHOLD)) begin
                safety_trigger <= 1'b1;
                control_effort <= -(velocity <<< 4); 
            end else begin
                safety_trigger <= 1'b0;
                control_effort <= -(kp_gain * adc_data) - (kd_gain * velocity);
            end

            if (control_effort > 2047) pwm_out <= 2047;
            else if (control_effort < -2048) pwm_out <= -2048;
            else pwm_out <= control_effort[11:0];
        end
    end
endmodule
