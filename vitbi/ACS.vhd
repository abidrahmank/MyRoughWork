----------------------------------------------------------------------------------------------------
-- ACS unit calculate path metric value at each clock cycles.
-- it takes previous path metrics and branch metrics of the branches converging to a particular node.
-- New path metric will be lowest of the two path metric calculated.
-- when both path metrics are same, upper path will be selected.
-- Decision - gives 0 when new path metric calculated is sum of PMD and BMD.
--			     gives 1 when new path metric calculated is sum of PMU and BMU.
--            gives one when both are equal.
-- --------------------------------------------------------------------------------------------------   

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

	entity ACS is
	    
	   port (PMU,PMD:in std_logic_vector (2 downto 0); -- previous path metric values
            BMU,BMD:in std_logic_vector (1 downto 0); -- branch metric values
		      DECISION:OUT std_logic;                   -- decision
		      RESET,CLK:IN std_logic;
		      PM:OUT std_logic_vector (2 downto 0));    -- new path metric calculated
		 
	END ACS;
	
	architecture archi of ACS is
				
	 begin

      
		PROCESS (CLK,RESET)
		    
			variable sum1,sum2,pmVar:std_logic_vector(2 downto 0);
			variable decisionSig:std_logic;
			
			
			BEGIN
			    if (reset = '1')then
			        pm <= "000";
			       decision <= '1';
			    elsif(clk'event and clk = '1')then
			       sum1 := pmu + bmu;
			       sum2 := pmd + bmd;
			    
			       if (sum1 <= sum2)then
			                 pmVar := sum1;
			           decisionSig :='1';
			        
			       else
			                 pmVar := sum2;
			           decisionSig := '0';
			        
			       end if;
			       
			       decision <= decisionSig;
			        
			       pm <= pmVar;
				       
			      
			       end if;
			                
			                
		END PROCESS;
		 
 END archi;