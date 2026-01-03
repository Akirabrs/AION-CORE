`timescale 1ns / 1ps

module reflex_core_tb;

    // 1. Sinais de Teste (Inputs para o Core)
    reg clk;
    reg rst_n;
    reg signed [15:0] adc_data;       // Simula o sensor Z
    reg signed [15:0] npe_kp_suggested; // Simula o Python
    reg signed [15:0] npe_kd_suggested;
    reg npe_update_valid;

    // 2. Sinais Observados (Outputs do Core)
    wire signed [15:0] pwm_out;
    wire safety_trigger;

    // 3. Instancia o Device Under Test (DUT) - Seu módulo reflex_core
    reflex_core uut (
        .clk(clk), 
        .rst_n(rst_n), 
        .adc_data(adc_data), 
        .kp_gain(npe_kp_suggested), // Simplificação para teste direto
        .kd_gain(npe_kd_suggested),
        .pwm_out(pwm_out),
        .safety_trigger(safety_trigger)
    );

    // 4. Geração de Clock (100MHz -> 10ns período)
    always #5 clk = ~clk;

    // 5. Cenário de Teste
    initial begin
        // Inicialização
        $display("⚡ INICIANDO TESTBENCH DE HARDWARE: REFLEX CORE");
        $dumpfile("reflex_wave.vcd"); // Arquivo de onda para visualizadores
        $dumpvars(0, reflex_core_tb);
        
        clk = 0;
        rst_n = 0;
        adc_data = 0;
        npe_kp_suggested = 20;
        npe_kd_suggested = 5;
        npe_update_valid = 0;

        #100;
        rst_n = 1; // Solta o Reset
        $display("[100ns] Reset liberado. Sistema Ativo.");

        // CENÁRIO A: Plasma Estável (Erro 0)
        #100;
        adc_data = 0;
        #20;
        if (pwm_out == 0) $display("✅ PASSO 1: Plasma Zero -> PWM Zero (OK)");
        else $display("❌ ERRO 1: PWM não é zero! Valor: %d", pwm_out);

        // CENÁRIO B: Perturbação Súbita (Plasma sobe 100 unidades)
        #100;
        adc_data = 100; 
        #20; 
        // Esperado: u = -Kp*Erro = -20 * 100 = -2000
        // (Nota: O código real tem lógica derivativa, então o valor pode variar, 
        // mas deve ser negativo e forte)
        $display("[300ns] Perturbação detectada: ADC=100. PWM Output: %d", pwm_out);
        
        if (pwm_out < 0) $display("✅ PASSO 2: Reação Negativa Correta (OK)");
        else $display("❌ ERRO 2: PWM deveria ser negativo!");

        // CENÁRIO C: Atualização do NPE (Python muda os ganhos)
        #100;
        npe_kp_suggested = 50; // Python manda endurecer
        npe_update_valid = 1;
        #10;
        npe_update_valid = 0;
        $display("[500ns] Python atualizou Kp para 50.");
        
        #100;
        // Agora com Kp=50, para o mesmo erro 100, o PWM deve ser maior (-5000)
        $display("[600ns] Verificando novo ganho. PWM Output: %d", pwm_out);
        
        if (pwm_out < -2500) $display("✅ PASSO 3: Adaptação de Ganho Funcionou (OK)");
        else $display("❌ ERRO 3: Ganho não atualizou corretamente.");

        // Fim
        #100;
        $display("✨ TESTBENCH CONCLUÍDO.");
        $finish;
    end

endmodule
