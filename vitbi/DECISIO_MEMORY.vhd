library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity dec_mem is
    port (CLK,reset  : in std_logic;
          WE   : in std_logic;
          RE   : in std_logic;
          --ADDR : in std_logic_vector(5 downto 0);
          DI   : in std_logic_vector(3 downto 0);
          DO   : out std_logic_vector(3 downto 0));
end dec_mem;

architecture dec_arch of dec_mem is
    type ram_type is array (0 to 15) of std_logic_vector (3 downto 0);
    signal RAM: ram_type;
	 signal inaddr,outaddr: std_logic_vector(3 downto 0); 
	 
----------------------------------------------------
component MOD16UP is
    port(CLK:in std_logic;
			reset :in std_logic;
         Q_UP : out std_logic_vector(3 downto 0));
end component;			
----------------------------------------------------
----------------------------------------------------
component MOD16DOWN is
    port(CLK:in std_logic;
			reset :in std_logic;
         Q_DOWN : out std_logic_vector(3 downto 0));
end component;			
----------------------------------------------------
begin
	downctr: MOD16DOWN port map (CLK,reset,OUTADDR);
	upctr: MOD16UP port map (CLK,reset,INADDR);
	


    process (CLK)
    begin
        if CLK'event and CLK = '1' then
		  
            if RE = '1' then
							DO <= RAM(conv_integer(outaddr+1)) ;
                elsif WE = '1' then
                    RAM(conv_integer(inADDR)) <= DI;
              
                
            end if;
        end if;
    end process;

end dec_arch;
