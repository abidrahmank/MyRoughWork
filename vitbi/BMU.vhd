	----------------------------------------------------------------------------------
-- Group :  12VL_01F_15F_22F
-- Engineer: ABID K., MUHAMMED ASIF K.T., SANOOP V.L.
-- 
-- Create Date:    14:08:21 09/04/2012 
-- Design Name: 	VITERBI DECODER
-- Module Name:   BRANCH METRIC UNIT 
-- Target Devices: XILINX SPARTAN 3E
-- Code Versions: 1.0.1
-- Description: Includes entities for 4:1 MUX and Branch Metric Unit
--
-- Dependencies: None
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: To be implemented in FPGA
--
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.std_logic_unsigned.all;

-- Declaring 4:1 MUX

entity MUX is
port(reset: in std_logic;
dataIn  : IN std_logic_vector(1 downto 0);
A,B,C,D : IN std_logic_vector(1 downto 0);
dataOut : OUT std_logic_vector(1 downto 0)
);
end MUX;

architecture MUX_ARCH of MUX is

begin
process(A,B,C,D,dataIn,reset)
variable TEMP:std_logic_vector(1 downto 0);
begin
		if (reset='1') then
			TEMP:="00";
			
		ELSE
			case dataIn is
				when "00" =>TEMP:=A;
				when "01" =>TEMP:=B;
				when "10" =>TEMP:=C;
				when "11" =>TEMP:=D;
				when others => null;
			end case;
		end if;	
dataOut <= TEMP;
end process;
end MUX_ARCH;

-- finished MUX declaration

-------------------------------------------------------------------
--------------------   BRANCH METRIC UNIT -------------------------
-------------------------------------------------------------------

-- INPUT: 
	--din : received bit stream (2 bits at a time)
	
-- OUTPUTS:
	-- W : the branch metric w.r.t input '00'
	-- X : the branch metric w.r.t input '01'
	-- Y : the branch metric w.r.t input '10'
	-- Z : the branch metric w.r.t input '11'

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.std_logic_unsigned.all;

entity BMU is 
	port (CLK,reset: IN STD_LOGIC;
		din : IN std_logic_vector(1 downto 0);
		W,X,Y,Z : OUT std_logic_vector(1 downto 0) 
	); 
end BMU;

architecture BMU_ARCH of BMU is 

--	component INPUT_MEM
--			
--					port (CLK,reset  : in std_logic;
--					 --CLR	: in std_logic;
--					 --WE   : in std_logic;
--					 --EN   : in std_logic;
--					 --INPUT_DI   : in std_logic_vector(1 downto 0);
--					 INPUT_DO   : out std_logic_vector(1 downto 0));
--	end component;
	
	component MUX
		port (reset: in std_logic;
				dataIn,A,B,C,D:IN std_logic_vector(1 downto 0);
				dataOut : OUT std_logic_vector(1 downto 0)
				);
		end component;
--		signal inputdata: std_logic_vector(1 downto 0) ;
		
	begin
			
--		inputmem: INPUT_MEM port map (CLK,reset,inputdata);
		M1: MUX port map (reset,din,"00","01","01","10",W);
		M2: MUX port map (reset,din,"01","00","10","01",X); 
		M3: MUX port map (reset,din,"01","10","00","01",Y);
		M4: MUX port map (reset,din,"10","01","01","00",Z);
	

	end BMU_ARCH;



