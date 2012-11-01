
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
--library UNISIM;
--use UNISIM.VComponents.all;

entity TOP is
port (CLK, RESET: IN STD_LOGIC;
      WE,RE,load  : in std_logic;--delete after testing. this signals should be from control unit
		dout:out std_logic;-- we get the decoded data
		decisions:out std_logic_vector (3 downto 0));
end TOP;
----------------------------------------------------------
architecture Behavioralarch of TOP is

component INPUT_MEM is
    port (CLK ,reset : in std_logic;
			 --CLR	: in std_logic;
          --WE   : in std_logic;
          --EN   : in std_logic;
          --INPUT_DI   : in std_logic_vector(1 downto 0);
          INPUT_DO   : out std_logic_vector(1 downto 0));
end component;
-----------------------------------------------------------
component ACSunit is
    
		port(din : IN std_logic_vector(1 downto 0);-- data input
          RESET,CLK:IN std_logic;
			 outPM1,outPM2,outPM3,outPM4:out std_logic_vector (2 downto 0);-- path metric values
					 --dec1,dec2,dec3,dec4:out std_logic
					 decisions:out std_logic_vector (3 downto 0));--decisions of 4 ACS
end component;
-------------------------------------------------------------
component compar1 is
	PORT(A,B,C,D:in std_logic_vector(2 downto 0);
			code : out std_logic_vector(1 downto 0));
END component;
------------------------------------------------------------
component dec_mem is
    port (CLK,reset  : in std_logic;
          WE   : in std_logic;
          RE   : in std_logic;
          --ADDR : in std_logic_vector(5 downto 0);
          DI   : in std_logic_vector(3 downto 0);
          DO   : out std_logic_vector(3 downto 0));
end component;
------------------------------------------------------------
component predictor is
	port (rst,clk,din,load:in bit;
		stateValue:in bit_vector(1 downto 0);
		outStateValue:out integer range 0 to 3;
		dout:out bit);
	end component;


signal indata,cmp_op: std_logic_vector(1 downto 0);
signal outPM1,outPM2,outPM3,outPM4:std_logic_vector (2 downto 0);
signal mem_column_value : std_logic_vector (3 downto 0);
signal temp_outstate : integer range 0 to 3;

 
begin
	         memory : input_mem port map(clk,reset,indata);
			  mainacs : acsunit port map(indata,reset,clk,outPM1,outPM2,outPM3,outPM4,decisions);
			  comp_pm : compar1 port map (outPM1,outPM2,outPM3,outPM4,cmp_op);

			decision_memory : dec_mem port map(CLK,RESET,WE,RE,decisions,mem_column_value);
			  predictor1 : predictor port map(reset,clk,mem_column_value(conv_integer(cmp_op)),load,cmp_op,temp_outstate,dout);
end Behavioralarch;

