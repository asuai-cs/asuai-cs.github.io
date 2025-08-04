-- Equalizer with bin-specific processing
process(clk_100mhz, reset)
    constant NUM_BINS : integer := 256;
    type bin_array is array (0 to NUM_BINS-1) of signed(15 downto 0);
    variable fft_bins : bin_array;
    variable low_gain : signed(15 downto 0) := to_signed(16384, 16);  -- 1.0 in Q15 format
    variable mid_gain : signed(15 downto 0) := to_signed(16384, 16);
    variable high_gain : signed(15 downto 0) := to_signed(16384, 16);
begin
    if reset = '1' then
        audio_proc <= (others => '0');
    elsif rising_edge(clk_100mhz) then
        if fft_tvalid_out = '1' then
            -- Assume fft_data_out represents one bin per cycle
            for i in 0 to NUM_BINS-1 loop
                if i < 64 then  -- Low frequencies (0-3 kHz)
                    fft_bins(i) := signed(fft_data_out) * low_gain;
                elsif i < 192 then  -- Mid frequencies (3-9 kHz)
                    fft_bins(i) := signed(fft_data_out) * mid_gain;
                else  -- High frequencies (9-12 kHz)
                    fft_bins(i) := signed(fft_data_out) * high_gain;
                end if;
            end loop;
            -- Simplified: output the first bin (in practice, perform IFFT)
            audio_proc <= std_logic_vector(fft_bins(0));
        end if;
    end if;
end process;