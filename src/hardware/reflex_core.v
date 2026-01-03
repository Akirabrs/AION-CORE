`timescale 1ns / 1ps

//////////////////////////////////////////////////////////////////////////////////
// Company: Guibral-Labs
// Engineer: Guilherme Brasil
// 
// Create Date: 03.01.2026
// Design Name: AION-CORE Reflex Layer
// Module Name: reflex_core
// Project Name: AION-CORE
// Target Devices: Xilinx Zynq-7000 (XC7Z020)
// Tool Versions: Vivado 2024.1
// Description: 
//    Layer 1 deterministic control kernel. Implements the PACC control law
//    with hard-real-time constraints (< 1us latency).
//    Includes AEGIS Safety Override logic.
//////////////////////////////////////////////////////////////////////////////////

module reflex_core #(
    parameter DATA_WIDTH = 16,
    parameter PWM_WIDTH = 12,
    parameter VELOCITY_THRESHOLD = 16'd1000  // Limite AEGIS
)(
    input wire clk,             // 100 MHz System Clock
    input wire rst_n,           // Active Low Reset
    input wire signed [DATA_WIDTH-1:0] adc_data, // Sensor Input (Z position)
    input wire [15:0] kp_gain,  // Gain form Layer 2 (Cognitive)
    input wire [15:0] kd_gain,  // Gain from Layer 2 (Cognitive)
    
    output reg signed [PWM_WIDTH-1:0] pwm_out,   // To Actuators (Coils)
    output reg safety_trigger                    // AEGIS Flag
);

    // Registradores internos (Memória Rápida)
    reg signed [DATA_WIDTH-1:0] prev_z;
    reg signed [DATA_WIDTH-1:0] velocity;
    reg signed [31:0] control_effort;
    
    // PACC Logic
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pwm_out <= 0;
            prev_z <= 0;
            velocity <= 0;
            safety_trigger <= 0;
        end else begin
            // 1. Derivador (Cálculo de Velocidade em 1 clock)
            velocity <= adc_data - prev_z;
            prev_z <= adc_data;

            // 2. Lógica AEGIS (O Guardião)
            // Se a velocidade (positiva ou negativa) for maior que o limite:
            if ((velocity > VELOCITY_THRESHOLD) || (velocity < -VELOCITY_THRESHOLD)) begin
                safety_trigger <= 1'b1;
                // Ação Reflexa Máxima (Max Negative Voltage)
                // O operador <<< aumenta a força exponencialmente (shift)
                control_effort <= -(velocity <<< 4); 
            end else begin
                safety_trigger <= 1'b0;
                // Controle Padrão (PD)
                // u = -Kp*z - Kd*v
                control_effort <= -(kp_gain * adc_data) - (kd_gain * velocity);
            end

            // 3. Output Limiter (Saturação do Atuador)
            // Converte o esforço de 32 bits para 12 bits (PWM)
            if (control_effort > 2047)
                pwm_out <= 2047;
            else if (control_effort < -2048)
                pwm_out <= -2048;
            else
                pwm_out <= control_effort[11:0];
        end
    end

endmodule
