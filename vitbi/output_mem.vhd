----------------------------------------------------------------------------------
--THE FOLLOWING IS THE CODE FOR 16X 1 MEM , WHICH CAN BE USED AS OUTRAM, WHICH CAN BE 
--WRITTEN AND READ ACCORDING TO THE CONDITION IN WriteEnable PIN
--
------------------------------------------------------------------------------------
--library IEEE;
--use IEEE.STD_LOGIC_1164.ALL;
--use IEEE.NUMERIC_STD.ALL;
--use IEEE.STD_LOGIC_UNSIGNED.all;
--library UNISIM;
--use UNISIM.VComponents.all;
--
--
--entity OUTPUT_ MEM is
--    port (CLK  : in std_logic;
--          WE   : in std_logic;
--          EN   : in std_logic;
--          OUTADDR : in std_logic_vector(3 downto 0);
--          OUTPUT_DI   : in std_logic;
--          OUTPUT_DO   : out std_logic);
--end OUTPUT_ MEM;
--
--architecture syn of OUTPUT_ MEM is
--    type OUTRAM_type is array (15 downto 0) of std_logic;
--    signal OUTRAM: OUTRAM_type;
--begin
--
--    process (CLK)
--    begin
--        if CLK'event and CLK = '1' then
--            if EN = '1' then
--                if WE = '1' then
--                    OUTRAM(conv_integer(OUTADDR)) <= OUTPUT_DI;
--                end if;
--                OUTPUT_DO <= OUTRAM(conv_integer(OUTADDR)) ;
--            end if;
--        end if;
--    end process;
--
--end syn;
-------------------------------------------------------------
-------------------------------------------------------------



library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use IEEE.STD_LOGIC_UNSIGNED.all;
--library UNISIM;
--use UNISIM.VComponents.all;

----------------------------------------------------
entity OUTPUT_MEM is
    port (CLK  : in std_logic;
			 --CLR	: in std_logic;
          --WE   : in std_logic;
          --EN   : in std_logic;
          --OUTPUT_DI   : in std_logic_vector(1 downto 0);
          OUTPUT_DO   : out std_logic);
end OUTPUT_MEM;
----------------------------------------------------



architecture outp_memarch of OUTPUT_MEM is
    type OUTRAM_type is array (0 TO 15) of std_logic;
	 signal OUTADDR: std_logic_vector (3 downto 0);
    signal OUTRAM: OUTRAM_type:=   ('1',
										'0',
										'1',
										'1',
										'0',
										'1',
										'1',
										'1',
										'1',
										'1',
										'1',
										'0',
										'0',
										'1',
										'0',
										'0'); 
----------------------------------------------------
component MOD16DOWN is
    port(CLK:in std_logic;
			--CLR :in std_logic;
         Q_DOWN : out std_logic_vector(3 downto 0));
end component;			
----------------------------------------------------
begin
counter1: MOD16DOWN port map (CLK,OUTADDR);----GIVE CLR IN SENSITIVITY LIST IF IT IS USED IN THE CIRCUIT

    process (CLK)
    begin
        if CLK'event and CLK = '1' then
            --if EN = '1' then
               --- if WE = '1' then
                  --  OUTRAM(conv_integer(OUTADDR)) <= OUTPUT_DI;----(uncomment if used as OUTRAM)
                --end if;
                OUTPUT_DO <= OUTRAM(conv_integer(OUTADDR-1)) ;
           --- end if;
        end if;
    end process;
	 
end outp_memarch;
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

