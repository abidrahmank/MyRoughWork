
----------------------------------------------------
------------------CODE FOR upCOUNTER------------------
----------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity MOD16UP is
    port(CLK: in std_logic; 
		reset: in std_logic;
         Q_UP : out std_logic_vector(3 downto 0));
end MOD16UP;

architecture ARCHI_UP of MOD16UP is
    signal tmp: std_logic_vector(3 downto 0):="1111";
begin
    process (CLK) 
				--put CLR in sensitivity list ,if its used
    begin
        if (CLK'event and CLK='1') then
          if (reset='1') then
            tmp <= "1111";
          else
            tmp <= tmp + 1;
          end if;
			end if;
    end process;
	 Q_UP <= tmp;


end ARCHI_UP;

----------------------------------------------------
