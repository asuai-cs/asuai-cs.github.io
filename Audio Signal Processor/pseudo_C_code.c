#include <xiicps.h>
#define I2C_DEVICE_ID XPAR_PS7_I2C_0_DEVICE_ID
#define WM8731_ADDR 0x1A

XIicPs I2cInstance;
u8 WriteBuffer[2];

void write_wm8731(u8 reg, u8 value) {
    WriteBuffer[0] = (reg << 1) | ((value >> 8) & 0x01);  // Register address + MSB
    WriteBuffer[1] = value & 0xFF;  // LSB
    XIicPs_MasterSendPolled(&I2cInstance, WriteBuffer, 2, WM8731_ADDR);
}

int main() {
    XIicPs_Config *ConfigPtr = XIicPs_LookupConfig(I2C_DEVICE_ID);
    XIicPs_CfgInitialize(&I2cInstance, ConfigPtr, ConfigPtr->BaseAddress);
    XIicPs_SetSClk(&I2cInstance, 100000);  // 100 kHz I2C clock
    
    // WM8731 configuration
    write_wm8731(0x0F, 0x00);  // R15: Reset
    write_wm8731(0x04, 0x10);  // R4: Enable microphone input
    write_wm8731(0x05, 0x00);  // R5: Disable high-pass filter
    write_wm8731(0x06, 0x00);  // R6: Power on all blocks
    write_wm8731(0x07, 0x0A);  // R7: I2S, 16-bit, slave mode
    write_wm8731(0x08, 0x00);  // R8: 48 kHz sampling
    write_wm8731(0x09, 0x01);  // R9: Activate codec
    
    return 0;
}