from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
import switch
from ryu.app import simple_switch_stp_13 
from datetime import datetime
import socket
import time
dpid_controller_map = {
    1: 'c0',
    2: 'c0',
    3: 'c0',
    4: 'c0',
    5: 'c2',
    6: 'c2',
    7: 'c0',
    8: 'c0',
    9: 'c2',
    10: 'c0',
    11: 'c0',
    12: 'c1',
    13: 'c1',
    14: 'c1',
    15: 'c1',
    16: 'c1',
    17: 'c2',
    18: 'c2',
    19: 'c2',
}


class SimpleMonitor13(simple_switch_stp_13.SimpleSwitch13):

    def __init__(self, *args, **kwargs):

        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)
        
        # self.controller_ip = self.get_controller_ip()
        # start = datetime.now()

        # self.flow_training()

        # end = datetime.now()
        # print("Training time: ", (end-start)) 

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(10)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):

        timestamp = datetime.now()
        timestamp = timestamp.timestamp()

        # file0 = open("PredictFlowStatsfile.csv","w")
        file=""
        header=('timestamp,datapath_id,flow_id,ip_src,tp_src,ip_dst,tp_dst,ip_proto,icmp_code,icmp_type,flow_duration_sec,flow_duration_nsec,idle_timeout,hard_timeout,flags,packet_count,byte_count,packet_count_per_second,packet_count_per_nsecond,byte_count_per_second,byte_count_per_nsecond\n')
        body = ev.msg.body
        # dp=ev.msg.datapath
        # print(dp.address)
        icmp_code = -1
        icmp_type = -1
        tp_src = 0
        tp_dst = 0
        # print("hello")
        for stat in sorted([flow for flow in body if (flow.priority == 1) ], key=lambda flow:
            (flow.match['eth_type'],flow.match['ipv4_src'],flow.match['ipv4_dst'],flow.match['ip_proto'])):
        
            ip_src = stat.match['ipv4_src']
            ip_dst = stat.match['ipv4_dst']
            ip_proto = stat.match['ip_proto']
            
            if stat.match['ip_proto'] == 1:
                icmp_code = stat.match['icmpv4_code']
                icmp_type = stat.match['icmpv4_type']
                
            elif stat.match['ip_proto'] == 6:
                tp_src = stat.match['tcp_src']
                tp_dst = stat.match['tcp_dst']

            elif stat.match['ip_proto'] == 17:
                tp_src = stat.match['udp_src']
                tp_dst = stat.match['udp_dst']

            flow_id = str(ip_src) + str(tp_src) + str(ip_dst) + str(tp_dst) + str(ip_proto)
          
            try:
                packet_count_per_second = stat.packet_count/stat.duration_sec
                packet_count_per_nsecond = stat.packet_count/stat.duration_nsec
            except:
                packet_count_per_second = 0
                packet_count_per_nsecond = 0
                
            try:
                byte_count_per_second = stat.byte_count/stat.duration_sec
                byte_count_per_nsecond = stat.byte_count/stat.duration_nsec
            except:
                byte_count_per_second = 0
                byte_count_per_nsecond = 0
                
            file+=("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n"
                .format(timestamp, ev.msg.datapath.id, flow_id, ip_src, tp_src,ip_dst, tp_dst,
                        stat.match['ip_proto'],icmp_code,icmp_type,
                        stat.duration_sec, stat.duration_nsec,
                        max(0,stat.idle_timeout-stat.duration_sec), stat.hard_timeout-stat.duration_sec,
                        stat.flags, stat.packet_count,stat.byte_count,
                        packet_count_per_second,packet_count_per_nsecond,
                        byte_count_per_second,byte_count_per_nsecond))
        if len(file)==0:
            return
        dpid=ev.msg.datapath.id
        
        controller=dpid_controller_map[dpid]
        if controller=='c0':
            client_ip='127.0.0.2'
        elif controller=='c1':
            client_ip='127.0.0.3'
        else:
            client_ip='127.0.0.4'
        
        local_ip = socket.gethostbyname(socket.gethostname())
        tcp_port=9999
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((client_ip,0))
        tcp_socket.connect((local_ip, tcp_port))
         
        # Make the socket non-blocking
        tcp_socket.setblocking(False)

        # Send the flow statistics data to the server
        file_data = file
        tcp_socket.sendall(file_data.encode())

        # Check for response with a timeout
        # timeout = 5  # Timeout in seconds
        # start_time = time.time()
        
        # while True:
        #     try:
        #         # Attempt to receive data
        #         response_data = tcp_socket.recv(1024).decode()
        #         if response_data:
        #             print("Response from server:", response_data)
        #             output_filename = 'received_file.txt'
        #             if response_data!='1':
        #                 with open(output_filename, 'w') as file:
        #                     file.write(response_data)
        #             else:
        #                 with open(output_filename,'w') as file:
        #                     pass
        #             tcp_socket.close()
        #             break
        #     except BlockingIOError:
        #         # Non-blocking error, continue waiting or perform other tasks
        #         pass

        #     # Check for timeout
            
        #     if time.time() - start_time > timeout:
        #         print("Timeout: No response received within the specified time.")
        #         break
        tcp_socket.close()   
            
            
            
            
        # file0.close()
        # self.flow_predict()

    # def flow_training(self):

    #     self.logger.info("Flow Training ...")

    #     flow_dataset = pd.read_csv('Dataset.csv')

    #     # flow_dataset.iloc[:, 2] = flow_dataset.iloc[:, 2].str.replace('.', '')
    #     # flow_dataset.iloc[:, 3] = flow_dataset.iloc[:, 3].str.replace('.', '')
    #     # flow_dataset.iloc[:, 5] = flow_dataset.iloc[:, 5].str.replace('.', '')
    #     flow_datasetn=flow_dataset[['tp_src','tp_dst','ip_proto','icmp_code','icmp_type','flow_duration_sec','flow_duration_nsec','idle_timeout','hard_timeout','flags','packet_count','byte_count','packet_count_per_second','packet_count_per_nsecond','byte_count_per_second','byte_count_per_nsecond','label']]
    #     # flow_datasetn.iloc[:, 0] = flow_datasetn.iloc[:, 0].str.replace('.', '')
    #     # flow_datasetn.iloc[:, 1] = flow_datasetn.iloc[:, 1].str.replace('.', '')
    #     X_flow = flow_datasetn.iloc[:, :-1].values
    #     X_flow = X_flow.astype('float64')
    #     rus = RandomUnderSampler(random_state=42)

    #     y_flow = flow_datasetn.iloc[:, -1].values

    #     X_flow_train, X_flow_test, y_flow_train, y_flow_test = train_test_split(X_flow, y_flow, test_size=0.25, random_state=0)
        
    #     X_train_rus, y_train_rus = rus.fit_resample(X_flow_train, y_flow_train)

    #     classifier = RandomForestClassifier(n_estimators=10, criterion="entropy", random_state=0)
    #     self.flow_model = classifier.fit(X_train_rus, y_train_rus)

    #     y_flow_pred = self.flow_model.predict(X_flow_test)

    #     self.logger.info("------------------------------------------------------------------------------")

    #     self.logger.info("confusion matrix")
    #     cm = confusion_matrix(y_flow_test, y_flow_pred)
    #     self.logger.info(cm)

    #     acc = accuracy_score(y_flow_test, y_flow_pred)

    #     self.logger.info("succes accuracy = {0:.2f} %".format(acc*100))
    #     fail = 1.0 - acc
    #     self.logger.info("fail accuracy = {0:.2f} %".format(fail*100))
    #     self.logger.info("------------------------------------------------------------------------------")

# def flow_predict(self):
#         predict_flow_dataset = pd.read_csv('PredictFlowStatsfile.csv')
#         if len(predict_flow_dataset):
#             # predict_flow_dataset.iloc[:, 2] = predict_flow_dataset.iloc[:, 2].str.replace('.', '')
#             # predict_flow_dataset.iloc[:, 3] = predict_flow_dataset.iloc[:, 3].str.replace('.', '')
#             # predict_flow_dataset.iloc[:, 5] = predict_flow_dataset.iloc[:, 5].str.replace('.', '')
            
            
#             predict_flow_datasetn=predict_flow_dataset[['tp_src','tp_dst','ip_proto','icmp_code','icmp_type','flow_duration_sec','flow_duration_nsec','idle_timeout','hard_timeout','flags','packet_count','byte_count','packet_count_per_second','packet_count_per_nsecond','byte_count_per_second','byte_count_per_nsecond']]
#             # predict_flow_datasetn.iloc[:, 0] = predict_flow_datasetn.iloc[:, 0].str.replace('.', '')
#             # predict_flow_datasetn.iloc[:, 1] = predict_flow_datasetn.iloc[:, 1].str.replace('.', '')
#             X_predict_flow = predict_flow_datasetn.iloc[:, :].values
#             X_predict_flow = X_predict_flow.astype('float64')
            
#             y_flow_pred = self.flow_model.predict(X_predict_flow)

#             legitimate_trafic = 0
#             ddos_trafic = 0

#             for i in y_flow_pred:
#                 if i == 0:
#                     legitimate_trafic = legitimate_trafic + 1
#                 else:
#                     ddos_trafic = ddos_trafic + 1
#                     victim = predict_flow_dataset.iloc[i, 5]
#                     print(victim)
                    
                    
                    
                    

#             self.logger.info("------------------------------------------------------------------------------")
#             if (legitimate_trafic/len(y_flow_pred)*100) > 80:
#                 self.logger.info("legitimate trafic ...")
#             else:
#                 self.logger.info("ddos trafic ...")
#                 self.logger.info("victim is host: h{}".format(victim))

#             self.logger.info("------------------------------------------------------------------------------")
            
#             file0 = open("PredictFlowStatsfile.csv","w")
            
#             file0.write('timestamp,datapath_id,flow_id,ip_src,tp_src,ip_dst,tp_dst,ip_proto,icmp_code,icmp_type,flow_duration_sec,flow_duration_nsec,idle_timeout,hard_timeout,flags,packet_count,byte_count,packet_count_per_second,packet_count_per_nsecond,byte_count_per_second,byte_count_per_nsecond\n')
#             file0.close()
#         else:
#             print("DataNotReady")

    