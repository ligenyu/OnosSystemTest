
class RCOnosPerf4nodes:

    def __init__(self) :
        self.default = ''

    def CASE1(self,main) :
        '''
        First case is to simply check if ONOS, ZK, and RamCloud are all running properly.
        If ONOS if not running properly, it will restart ONOS once before continuing. 
        It will then check if the ONOS has a view of all the switches and links as defined in the params file.
        The test will only pass if ONOS is running properly, and has a full view of all topology elements.
        '''
        import time
        main.ONOS1.stop()
        main.ONOS2.stop()
        main.ONOS3.stop()
        main.ONOS4.stop()
        main.RamCloud1.start_coor()
        main.RamCloud1.start_serv()
        main.RamCloud2.start_serv()
        main.RamCloud3.start_serv()
        main.RamCloud4.start_serv()
        main.ONOS1.start()
        time.sleep(10)
        main.ONOS2.start()
        main.ONOS3.start()
        main.ONOS4.start()
        main.ONOS1.start_rest()
        time.sleep(5)
        test= main.ONOS1.rest_status()
        if test == main.FALSE:
            main.ONOS1.start_rest()
        main.ONOS1.get_version()
        main.log.report("Startup check Zookeeper1, RamCloud1, and ONOS1 connections")
        main.case("Checking if the startup was clean...")
        main.step("Testing startup Zookeeper")
        data =  main.Zookeeper1.isup()
        utilities.assert_equals(expect=main.TRUE,actual=data,onpass="Zookeeper is up!",onfail="Zookeeper is down...")
        main.step("Testing startup RamCloud")
        data =  main.RamCloud1.server_status()
        if data == main.FALSE:
            main.RamCloud1.stop_coor()
            main.RamCloud1.stop_serv()
            main.RamCloud2.stop_serv()
            main.RamCloud3.stop_serv()
            main.RamCloud4.stop_serv()

            time.sleep(5)
            main.RamCloud1.start_coor()
            main.RamCloud1.start_serv()
            main.RamCloud2.start_serv()
            main.RamCloud3.start_serv()
            main.RamCloud4.start_serv()
        utilities.assert_equals(expect=main.TRUE,actual=data,onpass="RamCloud is up!",onfail="RamCloud is down...")
        main.step("Testing startup ONOS")
        data = main.ONOS1.isup()
        data = data and main.ONOS2.isup()
        data = data and main.ONOS3.isup()
        data = data and main.ONOS4.isup()
        if data == main.FALSE:
            main.log.report("Something is funny... restarting ONOS")
            main.ONOS1.stop()
            main.ONOS2.stop()
            main.ONOS3.stop()
            main.ONOS4.stop()
            time.sleep(5)
            main.ONOS1.start()
            time.sleep(10)
            main.ONOS2.start()
            main.ONOS3.start()
            main.ONOS4.start()
            data = main.ONOS1.isup()
        utilities.assert_equals(expect=main.TRUE,actual=data,onpass="ONOS is up and running!",onfail="ONOS didn't start...")

    def CASE2(self,main) :
        '''
        Makes sure that the HW links are all up
        Verifies that at least one mininet host exists.
        Proves that there is actually a mininet that we are working with
        '''
        import time
        main.step("Checking if MN switches exist")
        main.log.report("Check if MN switches exist")
        #result = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
        #for i in range(2):
        #    if result == main.FALSE: 
        #        time.sleep(5)
        #        result = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
        #    else: 
        #        break
        #main.step("Verifying the result")
        #utilities.assert_equals(expect=main.TRUE,actual=result,onpass="MN switches exist",onfail="MN is missing switches and or links...")

        main.step("assigning ONOS controllers to switches")
        for i in range(25):
            if i < 3:
                j=i+1
                main.Mininet1.assign_sw_controller(sw=str(j),ip1=main.params['CTRL']['ip1'],port1=main.params['CTRL']['port1'])
                time.sleep(1)
                main.Mininet1.assign_sw_controller(sw=str(j),ip1=main.params['CTRL']['ip1'],port1=main.params['CTRL']['port1'],ip2=main.params['CTRL']['ip2'],port2=main.params['CTRL']['port2'],ip3=main.params['CTRL']['ip3'],port3=main.params['CTRL']['port3'],ip4=main.params['CTRL']['ip4'],port4=main.params['CTRL']['port4'])
            elif i >= 3 and i < 5:
                j=i+1
                main.Mininet1.assign_sw_controller(sw=str(j),ip1=main.params['CTRL']['ip2'],port1=main.params['CTRL']['port2'])
                time.sleep(1)
                main.Mininet1.assign_sw_controller(sw=str(j),ip1=main.params['CTRL']['ip1'],port1=main.params['CTRL']['port1'],ip2=main.params['CTRL']['ip2'],port2=main.params['CTRL']['port2'],ip3=main.params['CTRL']['ip3'],port3=main.params['CTRL']['port3'],ip4=main.params['CTRL']['ip4'],port4=main.params['CTRL']['port4'])
            elif i >= 5 and i < 15:
                j=i+1
                main.Mininet1.assign_sw_controller(sw=str(j),ip1=main.params['CTRL']['ip3'],port1=main.params['CTRL']['port3'])
                time.sleep(1)
                main.Mininet1.assign_sw_controller(sw=str(j),ip1=main.params['CTRL']['ip1'],port1=main.params['CTRL']['port1'],ip2=main.params['CTRL']['ip2'],port2=main.params['CTRL']['port2'],ip3=main.params['CTRL']['ip3'],port3=main.params['CTRL']['port3'],ip4=main.params['CTRL']['ip4'],port4=main.params['CTRL']['port4'])
            else:
                j=i+16
                main.Mininet1.assign_sw_controller(sw=str(j),ip1=main.params['CTRL']['ip4'],port1=main.params['CTRL']['port4'])
                time.sleep(1)
                main.Mininet1.assign_sw_controller(sw=str(j),ip1=main.params['CTRL']['ip1'],port1=main.params['CTRL']['port1'],ip2=main.params['CTRL']['ip2'],port2=main.params['CTRL']['port2'],ip3=main.params['CTRL']['ip3'],port3=main.params['CTRL']['port3'],ip4=main.params['CTRL']['ip4'],port4=main.params['CTRL']['port4'])
        main.Mininet1.get_sw_controller("s1")
        time.sleep(5)        

    def CASE3(self,main) :
        '''
        Verifies that ONOS sees the right topology... 
        '''
        import time
        main.log.report("checking if ONOS sees the right topo...") 
        main.case("TOPO check")
        main.step("calling rest calls") 
        for i in range(4):
            result = main.ONOS1.check_status(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
            time.sleep(5)
            if result == 1:
                break
        if result == 0:
            main.ONOS1.start()
            main.ONOS2.start()
            main.ONOS3.start()
            main.ONOS4.start()
            time.sleep(45)
            for i in range(4):
                result = main.ONOS1.check_status(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
                time.sleep(5)
                if result == 1:
                    break
        utilities.assert_equals(expect=1,actual=result)
       
    def CASE4(self,main) :
        '''
        This Test case: 
            - Clears out any leftover flows
            - Adds new flows into ONOS
            - Checks flows up to 10 times waiting for each flow to be caluculated and no "NOT" statements inte get_flow
        '''
        import time
        main.log.report("Deleting and adding flows")
        main.case("Taking care of these flows!") 
        main.step("Cleaning out any leftover flows...")
        main.log.info("deleting...")
        main.ONOS1.rm_flow()
       # main.ONOS1.delete_flow("all")
        main.log.info("adding...")
        t1 = time.time()
        main.ONOS1.ad_flow()
       # main.ONOS1.add_flow(main.params['FLOWDEF'])   
        main.log.info("Checking...")
        for i in range(15):
            result = main.ONOS1.check_flow()
            if result == main.TRUE: 
                t2 = time.time()
                main.log.info( 'Adding flows took %0.3f s' % (t2-t1))
                break
            time.sleep(5)
            main.log.info("Checking Flows again...")

        strtTime = time.time()
        count = 1
        i = 6
        while i < 16 :
            main.log.info("\n\t\t\t\th"+str(i)+" IS PINGING h"+str(i+25) )
            ping = main.Mininet1.pingHost(src="h"+str(i),target="h"+str(i+25))
            if ping == main.FALSE and count < 3:
                count = count + 1
                i = 6
                main.log.info("Ping failed, making attempt number "+str(count)+" in 10 seconds")
                time.sleep(10)
            elif ping == main.FALSE and count ==3:
                main.log.error("Ping test failed")
                i = 17
                result = main.FALSE
            elif ping == main.TRUE:
                i = i + 1
                result = main.TRUE
        endTime = time.time()
        if result == main.TRUE:
            main.log.info("\tTime to complete ping test: "+str(round(endTime-strtTime,2))+" seconds")
        else:
            main.log.info("\tPING TEST FAIL")

        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="flows are good",onfail="FLOWS not correct") 

        main.log.report("checking if ONOS sees the right topo...")
        main.case("TOPO check")
        main.step("calling rest calls")
        for i in range(3):
            result = main.ONOS1.check_status(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
            time.sleep(5)
            if result == 1:
                break

    def CASE5(self,main) :
        '''
        Tests a single ping 
        '''
        main.log.report("Testing a single ping")
        main.case("Testing ping...")
        ping_result = main.Mininet4.pingHost(src=main.params['PING']['source1'],target=main.params['PING']['target1'])
        utilities.assert_equals(expect=main.TRUE,actual=ping_result,onpass="NO PACKET LOSS, HOST IS REACHABLE",onfail="PACKET LOST, HOST IS NOT REACHABLE") 


    def CASE6(self,main) :
        '''
        Starts continuous pings on the Mininet nodes
        '''
        main.log.report("Starting continuous ping, then toggle a single link in the center triangle")
        import time
        import os
        main.case("Starting long ping... ") 
        main.Mininet4.pingLong(src=main.params['PING']['source1'],target=main.params['PING']['target1'])
        main.Mininet4.pingLong(src=main.params['PING']['source2'],target=main.params['PING']['target2'])
        main.Mininet4.pingLong(src=main.params['PING']['source3'],target=main.params['PING']['target3'])
        main.Mininet4.pingLong(src=main.params['PING']['source4'],target=main.params['PING']['target4'])
        main.Mininet4.pingLong(src=main.params['PING']['source5'],target=main.params['PING']['target5'])
        main.Mininet4.pingLong(src=main.params['PING']['source6'],target=main.params['PING']['target6'])
        main.Mininet4.pingLong(src=main.params['PING']['source7'],target=main.params['PING']['target7'])
        main.Mininet4.pingLong(src=main.params['PING']['source8'],target=main.params['PING']['target8'])
        main.Mininet4.pingLong(src=main.params['PING']['source9'],target=main.params['PING']['target9'])
        main.Mininet4.pingLong(src=main.params['PING']['source10'],target=main.params['PING']['target10'])
        main.step("Check that the pings are going") 
        result = main.Mininet4.pingstatus(src=main.params['PING']['source1'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source2'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source3'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source4'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source5'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source6'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source7'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source8'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source9'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source10'])
        main.step( "Link down number of iterations: " +  main.params['Iterations'] )
        for i in range(int(main.params['Iterations'])):
            main.log.info("Bringing Link down... ") 
            main.Mininet1.link(END1="s1",END2="s2",OPTION="down")
            main.log.info( "Waiting " + main.params['WaitTime'] + " seconds.... " )
            time.sleep( int(main.params['WaitTime']) )
            main.log.info("Bringing Link up... ")
            main.Mininet1.link(END1="s1",END2="s2",OPTION="up")
            main.log.info( "Waiting " + main.params['WaitTime'] + " seconds.... " )
            time.sleep( int(main.params['WaitTime']) )
        main.case("Killing remote ping processes ") 
        result =  result & main.Mininet4.pingKill() 
        utilities.assert_equals(expect=main.TRUE,actual=result) 
       

    def CASE7(self,main) :
        '''
        Processes all of the ping data and outputs raw data and an overall average
        '''
        import os
        import time
        main.log.report("Process ping data (Fail is time is >20 seconds)")
        main.case("Processing Ping data") 
        time.sleep(3) 
        #result=os.popen("/home/admin/tools/shell.sh " + main.params['Iterations']).read()
        try:
            result=os.popen("/home/admin/ONLabTest/TestON/scripts/get_reroute_times.py").read() 
            average=result.split(":")[1] 
            main.log.info( "Reroute times are... " ) 
            main.log.report( result + " seconds" ) 
            try:
                if float(average) < float(main.params['TargetTime']) :
                    test=main.TRUE
                else:
                    test=main.FALSE
            except ValueError: 
                main.log.error("Data is corrupted")
                test=main.FALSE
        except:
            main.log.report("No data")
            test=main.FALSE
        utilities.assert_equals(expect=main.TRUE,actual=test,onpass="Average is less then the target time!",onfail="Average is worse then target time... ")

    def CASE8(self,main) :
        '''
        Starts continuous pings on the Mininet nodes
        '''
        main.log.report("Start continuous pings, then toggle multiple links in center triangle")
        import time
        import os
        time.sleep(20)
        main.case("Starting long ping... ")
        main.Mininet4.pingLong(src=main.params['PING']['source1'],target=main.params['PING']['target1'])
        main.Mininet4.pingLong(src=main.params['PING']['source2'],target=main.params['PING']['target2'])
        main.Mininet4.pingLong(src=main.params['PING']['source3'],target=main.params['PING']['target3'])
        main.Mininet4.pingLong(src=main.params['PING']['source4'],target=main.params['PING']['target4'])
        main.Mininet4.pingLong(src=main.params['PING']['source5'],target=main.params['PING']['target5'])
        main.Mininet4.pingLong(src=main.params['PING']['source6'],target=main.params['PING']['target6'])
        main.Mininet4.pingLong(src=main.params['PING']['source7'],target=main.params['PING']['target7'])
        main.Mininet4.pingLong(src=main.params['PING']['source8'],target=main.params['PING']['target8'])
        main.Mininet4.pingLong(src=main.params['PING']['source9'],target=main.params['PING']['target9'])
        main.Mininet4.pingLong(src=main.params['PING']['source10'],target=main.params['PING']['target10'])
        main.step("Check that the pings are going")
        result = main.Mininet4.pingstatus(src=main.params['PING']['source1'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source2'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source3'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source4'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source5'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source6'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source7'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source8'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source9'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source10'])
        main.step( "Making topo change while flows are rerouting")
        main.step( "Link down number of iterations: " +  main.params['Iterations'] )
        for i in range(int(main.params['Iterations'])):
            main.log.info("s1-s2 link down")
            main.Mininet1.link(END1="s1",END2="s2",OPTION="down")
            main.Mininet1.link(END1="s1",END2="s3",OPTION="up")
            main.Mininet1.link(END1="s2",END2="s3",OPTION="up")

            time.sleep(5)

            main.log.info("s1-s2 link up | s1-s3 link down | s2-s3 link down")
            main.Mininet1.link(END1="s1",END2="s2",OPTION="up")
            main.Mininet1.link(END1="s1",END2="s3",OPTION="down")
            main.Mininet1.link(END1="s2",END2="s3",OPTION="down")

            main.log.info( "Waiting " + main.params['WaitTime'] + " seconds.... " )
            time.sleep( int(main.params['WaitTime']) + 60 )

        main.case("Killing remote ping processes ")
        result =  result & main.Mininet4.pingKill()
        utilities.assert_equals(expect=main.TRUE,actual=result)
        main.log.info("Make sure all links in triangle are up")
        main.Mininet1.link(END1="s1",END2="s2",OPTION="up")
        main.Mininet1.link(END1="s1",END2="s3",OPTION="up")
        main.Mininet1.link(END1="s2",END2="s3",OPTION="up")

    def CASE9(self,main) :
        '''
        Starts continuous pings on the Mininet nodes
        '''
        main.log.report("Start continuous pings, then toggle one link in center triangle and start/stop 1 ONOS node")
        import time
        import os

        time.sleep(20)
        main.case("Starting long ping... ")
        main.Mininet4.pingLong(src=main.params['PING']['source1'],target=main.params['PING']['target1'])
        main.Mininet4.pingLong(src=main.params['PING']['source2'],target=main.params['PING']['target2'])
        main.Mininet4.pingLong(src=main.params['PING']['source3'],target=main.params['PING']['target3'])
        main.Mininet4.pingLong(src=main.params['PING']['source4'],target=main.params['PING']['target4'])
        main.Mininet4.pingLong(src=main.params['PING']['source5'],target=main.params['PING']['target5'])
        main.Mininet4.pingLong(src=main.params['PING']['source6'],target=main.params['PING']['target6'])
        main.Mininet4.pingLong(src=main.params['PING']['source7'],target=main.params['PING']['target7'])
        main.Mininet4.pingLong(src=main.params['PING']['source8'],target=main.params['PING']['target8'])
        main.Mininet4.pingLong(src=main.params['PING']['source9'],target=main.params['PING']['target9'])
        main.Mininet4.pingLong(src=main.params['PING']['source10'],target=main.params['PING']['target10'])
        main.step("Check that the pings are going")
        result = main.Mininet4.pingstatus(src=main.params['PING']['source1'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source2'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source3'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source4'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source5'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source6'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source7'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source8'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source9'])
        result = result & main.Mininet4.pingstatus(src=main.params['PING']['source10'])
        main.step( "Making topo change while flows are rerouting")
        main.step( "Link down number of iterations: " +  main.params['Iterations'] )
        for i in range(int(main.params['Iterations'])):
            main.log.info("s1-s2 link down | Onos 1 down")
            main.Mininet1.link(END1="s1",END2="s2",OPTION="down")
            if i % 4 == 0:
                main.ONOS1.stop()
            elif i % 4 == 1:
                main.ONOS2.stop()
            elif i % 4 == 2:
                main.ONOS3.stop()
            else:
                main.ONOS4.stop()

            time.sleep(5)

            main.log.info("s1-s2 link up | Onos 1 back up")
            main.Mininet1.link(END1="s1",END2="s2",OPTION="up")
            if i % 4 == 0:
                main.ONOS1.start()
                main.ONOS1.isup()
            elif i % 4 == 1:
                main.ONOS2.start()
                main.ONOS2.isup()
            elif i % 4 == 2:
                main.ONOS3.start()
                main.ONOS3.isup()
            else:
                main.ONOS4.start()
                main.ONOS4.isup()

            main.log.info( "Waiting " + main.params['WaitTime'] + " seconds.... " )
            time.sleep( int(main.params['WaitTime']) )

        main.case("Killing remote ping processes ")
        result =  result & main.Mininet4.pingKill()
        utilities.assert_equals(expect=main.TRUE,actual=result)

