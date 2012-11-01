----------------------------------------------------
-------CODE FOR INRAM(COMMENTED TO WORK AS A ROM)-----
----------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use IEEE.STD_LOGIC_UNSIGNED.all;
--library UNISIM;
--use UNISIM.VComponents.all;

----------------------------------------------------
entity INPUT_MEM is
    port (CLK ,reset : in std_logic;
			 --CLR	: in std_logic;
          --WE   : in std_logic;
          --EN   : in std_logic;
          --INPUT_DI   : in std_logic_vector(1 downto 0);
          INPUT_DO   : out std_logic_vector(1 downto 0));
end INPUT_MEM;
----------------------------------------------------



architecture inp_memarch of INPUT_MEM is
    type INRAM_type is array (0 TO 15) of std_logic_vector (1 downto 0);
	 signal INADDR: std_logic_vector (3 downto 0);
    signal INRAM: INRAM_type:=   ("11",
										"10",
										"11",
										"11",
										"01",
										"01",
										"11",
										"11",
										"10",
										"11",
										"11",
										"01",
										"01",
										"11",
										"00",
										"00"); 
----------------------------------------------------
component MOD16UP is
    port(CLK:in std_logic;
			reset :in std_logic;
         Q_UP : out std_logic_vector(3 downto 0));
end component;			
----------------------------------------------------
begin
	counter: MOD16UP port map (CLK,reset,INADDR);----GIVE CLR IN SENSITIVITY LIST IF IT IS USED IN THE CIRCUIT

   process (CLK,reset)
	 
    begin
				if (reset='1') then
				
					INPUT_DO <= "00" ;
				
				elsif CLK'event and CLK = '1' then
            
				--if EN = '1' then
               --- if WE = '1' then
                  --  INRAM(conv_integer(INADDR)) <= INPUT_DI;----(uncomment id used as INRAM)
                --end if;
                INPUT_DO <= INRAM(conv_integer(INADDR+1)) ;
           --- end if;
			  --end if;
        end if;
    end process;
	 
end inp_memarch;
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------