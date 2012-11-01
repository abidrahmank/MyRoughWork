library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
--------------------------------------------------------------
entity ACSunit is
    
     
		port (din : IN std_logic_vector(1 downto 0);-- data input
          RESET,CLK:IN std_logic;
			 outPM1,outPM2,outPM3,outPM4:out std_logic_vector (2 downto 0);-- path metric values
					--- dec1,dec2,dec3,dec4:out std_logic
					decisions:out std_logic_vector (3 downto 0));--decisions of 4 ACS
end ACSunit;
---------------------------------------------------------------    
    architecture arch_ACSunit of ACSunit is
        
        component BMU
	         port (CLK,reset: in std_logic;
		                din : IN std_logic_vector(1 downto 0);
		            W,X,Y,Z : OUT std_logic_vector(1 downto 0)); 
		  end component;
		
		  component ACS
	    
	         port (PMU,PMD:in std_logic_vector (2 downto 0);
                  BMU,BMD:in std_logic_vector (1 downto 0);
		           DECISION:OUT std_logic;
		          RESET,CLK:IN std_logic;
		                 PM:OUT std_logic_vector (2 downto 0));
		      
		   end component;
		   
		   signal PM1,PM2,PM3,PM4:std_logic_vector (2 downto 0);--path metric values
         signal pr_PM1,pr_PM2,pr_PM3,pr_PM4:std_logic_vector (2 downto 0);--previous path metric values
		   signal BM1,BM2,BM3,BM4:std_logic_vector (1 downto 0);--branch metric values
		   signal reg1,reg2,reg3,reg4:std_logic_vector(2 downto 0);--registers to store pm values
			signal dec1,dec2,dec3,dec4:std_logic;
	--------------------------------------------------------------------------	      
        begin
            
           bmUnits:BMU port map(CLK,reset,din,BM1,BM2,BM3,BM4); -- calling branch metric units
            ACS1:ACS port map(pr_PM1,pr_PM3,BM1,BM4,dec1,RESET,CLK,PM1);-- calling acs units  
            ACS2:ACS port map(pr_PM1,pr_PM3,BM4,BM1,dec2,RESET,CLK,PM2);
            ACS3:ACS port map(pr_PM2,pr_PM4,BM2,BM3,dec3,RESET,CLK,PM3);
            ACS4:ACS port map(pr_PM2,pr_PM4,BM3,BM2,dec4,RESET,CLK,PM4);
				decisions(0) <= dec1;
				decisions(1) <= dec2;
				decisions(2) <= dec3;
				decisions(3) <= dec4;
				
          
          process(CLK,RESET,reg1,reg2,reg3,reg4)
              begin
           if(reset = '1')then
		
			            pr_PM1  <= "000";-- resetting the previous path metric
			            pr_PM2  <= "000";-- values to 000
			            pr_PM3  <= "000";
			            pr_PM4  <= "000";
			  elsif (clk'event and clk = '0')then
			            pr_PM1  <= reg1; -- reading previous path metric values from 
			            pr_PM2  <= reg2; -- registers and assigning them to corresponding
			            pr_PM3  <= reg3; -- signals
			            pr_PM4  <= reg4;
			            
								 
			   end if;
			                
			                end process;
			                
			   process (PM1,PM2,PM3,PM4)
			       begin
			           reg1    <= PM1; -- saving path metric values to registers  
			           reg2    <= PM2;
			           reg3    <= PM3;
			           reg4    <= PM4;
						  outPM1    <= PM1; -- taking path metric values to out put ports 
			           outPM2    <= PM2;
			           outPM3    <= PM3;
			           outPM4    <= PM4;
			           end process;
			                    
             
        end arch_ACSunit;
            
