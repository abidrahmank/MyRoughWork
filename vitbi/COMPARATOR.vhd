-- comparator calculate state with minimum path metric from final path metric sum

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity comparator is
    port(A,B : in  std_logic_vector(2 downto 0);
		 CODE_A, CODE_B : in  std_logic_vector(1 downto 0);
         CMP : out std_logic_vector(2 downto 0);
		 CODE_OUT : out std_logic_vector(1 downto 0));
end comparator ;

architecture COMPARCH of comparator is
begin

    CMP <= A when A <= B else B;
	CODE_OUT <= CODE_A when A<=B else CODE_B;

end COMPARCH;
-------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity comparator2 is
    port(A,B : in  std_logic_vector(2 downto 0);
		 CODE_A, CODE_B : in  std_logic_vector(1 downto 0);
		 CODE_OUT : out std_logic_vector(1 downto 0));
end comparator2 ;

architecture COMPARCH of comparator2 is
begin

	CODE_OUT <= CODE_A when A<=B else CODE_B;

end COMPARCH;
-------------------------------------------------

--------------------------------------------------------
------------------- Original comparator ----------------
----------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

ENTITY COMPAR1 IS
	PORT(A,B,C,D:in std_logic_vector(2 downto 0);
			CODE : out std_logic_vector(1 downto 0));
END ENTITY;
-----------------------------------------------------
architecture COMPAR1_ARCH OF COMPAR1 IS

signal ab,cd : std_logic_vector(2 downto 0);
signal code_ab,code_cd : std_logic_vector(1 downto 0);

COMPONENT comparator is
    port(A,B : in  std_logic_vector(2 downto 0);
		 CODE_A, CODE_B : in  std_logic_vector(1 downto 0);
         CMP : out std_logic_vector(2 downto 0);
		 CODE_OUT : out std_logic_vector(1 downto 0));
end component ;

COMPONENT comparator2 is
    port(A,B : in  std_logic_vector(2 downto 0);
		 CODE_A, CODE_B : in  std_logic_vector(1 downto 0);
		 CODE_OUT : out std_logic_vector(1 downto 0));
end COMPONENT ;

BEGIN
	C1: comparator port map (A,B,"00","01",AB,CODE_AB);
	C2: comparator port map (C,D,"10","11",CD,CODE_CD);
	C3: comparator2 port map (AB,CD,CODE_AB,CODE_CD,CODE);
END;

		