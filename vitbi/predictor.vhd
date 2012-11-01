-- implemented full functionality of predictor
library ieee;
   use ieee.std_logic_1164.all;
    entity predictor is
        port (rst,clk,din,load:in bit;
            stateValue:in bit_vector(1 downto 0);
				outStateValue:out integer range 0 to 3;
            dout:out bit);
        end predictor;
        
        architecture arch of predictor is
            type state is (s0,s1,s2,s3);
            --- declaring states. 
            signal pr_state, n_state,min_state:state;
            signal st_changed:bit;--flag used to know whether the state has changed 
            
            begin
           ------------------------------------------------------------- 
            process(rst,clk)
                    begin
                    
                    
                        if (rst = '1')then
                            pr_state <= s0;--reseting the state to s0
                            
                            
                        elsif(clk'event and clk ='1')then
								
                            if(load ='1')then
                            
                                case stateValue is
                                 when "00"=>min_state <= s0;--here the minimum state of the 
                                 when "10"=>min_state <= s1;--decoder is used as the initial
                                 when "01"=>min_state <= s2;--state 
                                 when "11"=>min_state <= s3;
                                end case;
                            pr_state <= min_state;

                            else 
                            pr_state <= n_state;
                            
                            end if;
                            st_changed <= not st_changed;
                        end if;
   
                end process;
                -----------------------------------------------------
                        process(pr_state,st_changed,din)
								variable newState:state := s0;
                            begin
                                                                        
                                case pr_state is
                                    when s0 => 
                                        if (din = '0')then
                                        n_state <=s2;
                                            dout<='0';
														  newState:=s2;
                                        else
                                            n_state <=s0;
														  newState := s0;
                                            dout<='0';
                                        end if;
                                    when s1 =>
                                       if (din = '0')then
                                            dout <= '0';
                                            n_state <= s2;
														  newState := s2;														  
                                       else
                                            n_state <=s0;
                                            dout<='0';
														  newState := s0;
                                       end if;     
                                    when s2 =>
                                         if (din = '0')then
                                            dout <= '1';
                                            n_state <= s3;
														  newState := s3;
                                       else
                                            n_state <=s1;
														  newState := s1;
                                            dout<='1';
                                       end if;
                                    when s3 =>
                                         if (din = '0')then
                                            dout <= '1';
                                            n_state <= s3;
														  newState := s3;
                                       else
                                            n_state <=s1;
														  newState := s1;
                                            dout<='1';
                                       end if;
                                     end case;
													 
										  case newState is
												when s0=>outStateValue <= 0;--
												when s2=>outStateValue <= 1;--
												when s1=>outStateValue <= 2;--
												when s3=>outStateValue <= 3;
                                end case;

                                    end process;
                                end;
