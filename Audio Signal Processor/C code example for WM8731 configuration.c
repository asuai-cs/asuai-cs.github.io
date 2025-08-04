#include <xiicps.h>
#include <xparameters.h>
#include <xil_printf.h>

#define I2C_DEVICE_ID XPAR_PS7_I2C_0_DEVICE_ID
#define WM8731_ADDR 0x1A  // 7-bit I2C address

XIicPs I2cInstance;
u8 WriteBuffer[2];

int write_wm8731(u8 reg, u16 value) {
    WriteBuffer[0] = (reg << 1) | ((value >> 8) & 0x01);  // Register address + MSB
    WriteBuffer[1] = value & 0xFF;  // LSB
    return XIicPs_MasterSendPolled(&I2cInstance, WriteBuffer, 2, WM8731_ADDR);
}

int main() {
    // Initialize I2C
    XIicPs_Config *ConfigPtr = XIicPs_LookupConfig(I2C_DEVICE_ID);
    if (XIicPs_CfgInitialize(&I2cInstance, ConfigPtr, ConfigPtr->BaseAddress) != XST_SUCCESS) {
        xil_printf("I2C Initialization failed\n");
        return XST_FAILURE;
    }
    XIicPs_SetSClk(&I2cInstance, 100000);  // 100 kHz I2C clock

    // Configure WM8731 registers
    write_wm8731(0x0F, 0x000);  // R15: Reset
    write_wm8731(0x04, 0x010);  // R4: Enable microphone input
    write_wm8731(0x05, 0x000);  // R5: Disable high-pass filter
    write_wm8731(0x06, 0x000);  // R6: Power on all blocks
    write_wm8731(0x07, 0x00A);  // R7: I2S, 16-bit, slave mode
    write_wm8731(0x08, 0x000);  // R8: 48 kHz sampling, normal mode
    write_wm8731(0x09, 0x001);  // R9: Activate codec

    xil_printf("WM8731 Configured\n");
    while (1) {}  // Keep program running
    return XST_SUCCESS;
}