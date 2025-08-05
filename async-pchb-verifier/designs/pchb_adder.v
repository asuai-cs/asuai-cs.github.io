// Asynchronous PCHB 4-bit adder
module pchb_adder (
    input req,
    output ack,
    input [3:0] a,
    input [3:0] b,
    output [3:0] sum,
    input en,
    input reset
);
    // Handshake controller
    always @(posedge req or posedge reset) begin
        if (reset) ack <= 0;
        else if (en) ack <= 1;
    end

    // Data path
    always @(*) begin
        if (en) sum = a + b;
        else sum = 4'b0000;
    end
endmodule