----------------------------------------------------
--------------CODE FOR DOWNCOUNTER------------------
----------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity MOD16DOWN is
    port(
	   CLK: in std_logic; 
	 reset : in std_logic;
         Q_DOWN : out std_logic_vector(3 downto 0));
end MOD16DOWN;

architecture ARCHI_DOWN of MOD16DOWN is
    signal tmp: std_logic_vector(3 downto 0):="0000";
begin
    process (CLK,reset) 
				--put CLR in sensitivity list ,if its used
    begin
        if (CLK'event and CLK='1') then
          if (reset='1') then
            tmp <= "0000";
				else
            tmp <= tmp - 1;
          end if;
			end if;
    end process;
	 Q_DOWN <= tmp;


end ARCHI_DOWN;

----------------------------------------------------

