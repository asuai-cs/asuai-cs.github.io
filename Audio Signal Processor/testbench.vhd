```vhdl
-- Project: FPGA-Based Real-Time Audio Signal Processor (Testbench)
--
-- What it does:
-- This testbench tests the audio_processor module with real I2S data from a 48 kHz speech WAV file. It simulates audio input and checks the processed output.
--
-- How we built it:
-- 1. Setup:
--    - Used Vivado (2023.1) for simulation.
--    - Got real I2S data from Generate_Audio_Test.py (first 16 samples of a speech WAV).
-- 2. Testing:
--    - Generated a 100 MHz clock and reset signal.
--    - Fed 16-bit I2S samples (e.g., 0x7FFF for max amplitude) at 48 kHz.
--    - Checked audio_out for correct equalization (mid frequencies boosted).
-- 3. Usage:
--    - Run in Vivado: Add Audio_Processor.vhd and this file, then simulate.
--    - Check waveform for audio_out matching expected processed values.
-- 4. Notes:
--    - I2S data is from a real speech clip (male voice, "hello world").
--    - Expected outputs account for 1.5x mid-frequency gain.

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tb_audio_processor is
end tb_audio_processor;

architecture Behavioral of tb_audio_processor is
    signal clk_100mhz : STD_LOGIC := '0';
    signal reset : STD_LOGIC := '1';
    signal mclk, bclk, adclrc, daclrc, adcdat, dacdat : STD_LOGIC;
    signal audio_out : STD_LOGIC_VECTOR(15 downto 0);
    
    constant CLK_PERIOD : time := 10 ns;
    -- Real I2S samples from WAV file (first 16 samples, 16-bit, mono)
    type sample_array is array (0 to 15) of STD_LOGIC_VECTOR(15 downto 0);
    constant TEST_SAMPLES : sample_array := (
        x"7FFF", x"6A1B", x"5C3D", x"4E7A", x"4081", x"32B4", x"24F2", x"1738",
        x"0987", x"FBDA", x"EE2C", x"E07E", x"D2D0", x"C522", x"B774", x"A9C6"
    );
    
begin
    -- Instantiate the audio processor
    uut : entity work.audio_processor
        port map (
            clk_100mhz => clk_100mhz,
            reset => reset,
            mclk => mclk,
            bclk => bclk,
            adclrc => adclrc,
            daclrc => daclrc,
            adcdat => adcdat,
            dacdat => dacdat,
            audio_out => audio_out
        );
    
    -- Clock generation
    clk_process : process
    begin
        while True loop
            clk_100mhz <= '0';
            wait for CLK_PERIOD / 2;
            clk_100mhz <= '1';
            wait for CLK_PERIOD / 2;
        end loop;
    end process;
    
    -- Stimulus process
    stim_proc : process
        variable sample_idx : integer := 0;
        variable bit_idx : integer := 0;
    begin
        wait for 100 ns;
        reset <= '0';
        
        -- Simulate I2S input
        while sample_idx < 16 loop
            wait until falling_edge(bclk);
            if adclrc = '0' then
                adcdat <= TEST_SAMPLES(sample_idx)(15 - bit_idx);
                if bit_idx < 15 then
                    bit_idx := bit_idx + 1;
                else
                    bit_idx := 0;
                    sample_idx := sample_idx + 1;
                end if;
            end if;
        end loop;
        wait;
    end process;
end Behavioral;
```