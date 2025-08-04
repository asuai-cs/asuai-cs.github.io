```sdc
# Project: Neural Network Accelerator on Custom ASIC (Synthesis Constraints)
#
# What it does:
# This SDC file sets timing constraints for synthesizing the nn_accelerator module. It ensures the design meets a 100 MHz clock for a TSMC 65nm process.
#
# How we built it:
# 1. Setup:
#    - Created for Synopsys Design Compiler.
#    - Used TSMC 65nm library settings.
# 2. Constraints:
#    - Set 100 MHz clock (10 ns period).
#    - Added 2 ns input/output delays (20% of period).
#    - Set 1.2V supply and 25°C temperature.
# 3. Usage:
#    - Load in Design Compiler: `read_sdc constraints.sdc`.
#    - Synthesize: `compile -map_effort high`.
#    - Check timing.rpt for violations.
# 4. Notes:
#    - Adjust delays if timing fails.
#    - Add multicycle paths for complex operations if needed.

# Clock definition
create_clock -name clk -period 10 [get_ports clk]  # 100 MHz

# Input/output delays
set_input_delay 2 -clock clk [all_inputs]
set_output_delay 2 -clock clk [all_outputs]

# Operating conditions
set_operating_conditions -library typical -voltage 1.2 -temp 25

# Drive strength and load
set_driving_cell -lib_cell INVX1 [all_inputs]
set_load 0.05 [all_outputs]
```