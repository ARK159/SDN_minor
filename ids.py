import joblib

model=joblib.load('RFC')
import numpy as np

import socket
sv_count={}
dest_addresses = ['127.0.0.2', '127.0.0.3', '127.0.0.4']
dest_ports = 8888

local_ip = socket.gethostbyname(socket.gethostname())
tcp_host = local_ip  # Replace with the actual IP address of your device
tcp_port = 9999  # Replace with the desired port number

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((tcp_host, tcp_port))
tcp_server.listen()

print(f"Listening for incoming connections on {tcp_host}:{tcp_port}")

while True:
    conn, addr = tcp_server.accept()
    # print(f"Connection established with {addr}")

    data = conn.recv(8024).decode()
    conn.close()
    data_lines = data.split('\n')
    data_lines=data_lines[:-1]
    list_of_lists = []


    for line in data_lines:
        values = line.split(',')
        # Convert values to appropriate data types if needed
        values = [v for v in values]
        list_of_lists.append(values)
    
    # print(list_of_lists)
    result = []
    indices=[7,8,9,10,11,12,13,14,15,16,17,18,19,20]

    for sublist in list_of_lists:
        result.append([sublist[index] for index in indices])
    
    x=np.array(result)
    # print(x)
    # for i in range(len(x)):
    #     x[i][0]=x[i][0].replace('.','')
        # x[i][3]=x[i][3].replace('.','')
        # x[i][5]=x[i][5].replace('.','')
    x=x.astype('float64')
    
    y=model.predict(x)
    legitimate=0
    ddos=0
    j=0
    response_data=""
    flag=0
    # print(y)
    for i in y:
        if i==0:
            legitimate+=1
        else:
            print("there is a attack")
            ddos+=1
            frame=list_of_lists[j]
            # print(frame)
            victim=frame[5]
            source=frame[3]
            dpid=frame[1]
            # print(frame)
            print(victim,dpid)
            if victim in sv_count:
                flag=1
                break
            else:
                sv_count[victim]=1
            response_data=f"{victim},{source},{dpid}"
            
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.bind(('127.0.1.1',12345))
            for dest_address in dest_addresses:
                dest_server = (dest_address, dest_ports)
                client_socket.sendto(response_data.encode(), dest_server)
                print(f"Sent message to {dest_address}")
            client_socket.close()
            flag=1
            break

        j+=1
    if flag==0:
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.bind(('127.0.1.1',12345))
        for dest_address in dest_addresses:
                dest_server = (dest_address, dest_ports)
                client_socket.sendto("1".encode(), dest_server)
                print(f"Sent message to {dest_address}")
        client_socket.close()
    
    
    

        # if len(predict_flow_dataset):
        #     # predict_flow_dataset.iloc[:, 2] = predict_flow_dataset.iloc[:, 2].str.replace('.', '')
        #     # predict_flow_dataset.iloc[:, 3] = predict_flow_dataset.iloc[:, 3].str.replace('.', '')
        #     # predict_flow_dataset.iloc[:, 5] = predict_flow_dataset.iloc[:, 5].str.replace('.', '')
            
            
        #     predict_flow_datasetn=predict_flow_dataset[['tp_src','tp_dst','ip_proto','icmp_code','icmp_type','flow_duration_sec','flow_duration_nsec','idle_timeout','hard_timeout','flags','packet_count','byte_count','packet_count_per_second','packet_count_per_nsecond','byte_count_per_second','byte_count_per_nsecond']]
        #     # predict_flow_datasetn.iloc[:, 0] = predict_flow_datasetn.iloc[:, 0].str.replace('.', '')
        #     # predict_flow_datasetn.iloc[:, 1] = predict_flow_datasetn.iloc[:, 1].str.replace('.', '')
        #     X_predict_flow = predict_flow_datasetn.iloc[:, :].values
        #     X_predict_flow = X_predict_flow.astype('float64')
            
        #     y_flow_pred = self.flow_model.predict(X_predict_flow)

        #     legitimate_trafic = 0
        #     ddos_trafic = 0

        #     for i in y_flow_pred:
        #         if i == 0:
        #             legitimate_trafic = legitimate_trafic + 1
        #         else:
        #             ddos_trafic = ddos_trafic + 1
        #             victim = predict_flow_dataset.iloc[i, 5]
        #             print(victim)
                    
                    
                    
                    

        #     self.logger.info("------------------------------------------------------------------------------")
        #     if (legitimate_trafic/len(y_flow_pred)*100) > 80:
        #         self.logger.info("legitimate trafic ...")
        #     else:
        #         self.logger.info("ddos trafic ...")
        #         self.logger.info("victim is host: h{}".format(victim))

        #     self.logger.info("------------------------------------------------------------------------------")
            
        #     file0 = open("PredictFlowStatsfile.csv","w")
            
        #     file0.write('timestamp,datapath_id,flow_id,ip_src,tp_src,ip_dst,tp_dst,ip_proto,icmp_code,icmp_type,flow_duration_sec,flow_duration_nsec,idle_timeout,hard_timeout,flags,packet_count,byte_count,packet_count_per_second,packet_count_per_nsecond,byte_count_per_second,byte_count_per_nsecond\n')
        #     file0.close()
        # else:
        #     print("DataNotReady")

    
