# Laboratorio de Seguridad: Ataque de Secuestro de Root Bridge mediante STP Spoofing

**Autor:** Wilfri Solano Frias  
**Matrícula:** 2024-2364    

---

## 1. Objetivo del Laboratorio
El objetivo de este laboratorio es conocer las vulnerabilidades y peligros reales de la falta de autenticación en los protocolos de topología lógica de Capa 2 (Spanning Tree Protocol). Se analiza cómo un atacante puede explotar la confianza implícita del switch ante paquetes BPDU entrantes para alterar la jerarquía de la red LAN y forzar una re-convergencia no autorizada.

---

## 2. Objetivo del Script
Inyectar de forma continua (cada 2 segundos) tramas de datos crudas modificadas que emulen ser Unidades de Datos de Protocolo de Puente (BPDUs) legítimas. El script configura una prioridad de raíz y emisor de `0x0000` (máxima prioridad posible) para obligar al switch a transferirle el rol de "Root Bridge" y centralizar el tráfico de la red.

### 2.1. Requisitos para utilizar la herramienta
* **Sistema Operativo:** Kali Linux.
* **Lenguaje:** Python 3.x.
* **Librerías/Dependencias:** Scapy (módulos de infraestructura base: `Dot3`, `LLC`, `STP`, `sendp`).
* **Entorno de Red:** La interfaz del atacante debe estar cableada hacia un puerto del switch que tenga Spanning Tree activo en la VLAN 1, que admita tramas IEEE 802.3 estándar y se ejecute con privilegios de administrador (`sudo`).

### 2.2. Parámetros Usados
El script admite y manipula las siguientes variables y campos estructurales:

**Definición y Capa Ethernet (Líneas 4 y 9)**
* `interfaz="eth0"`: Especifica el adaptador de red en Kali Linux conectado al entorno virtual de GNS3.
* `dst="01:80:c2:00:00:00"`: Dirección Multicast estándar de la IEEE reservada exclusivamente para el tráfico de STP clásico.
* `src=mac_atacante`: Dirección MAC física simulada por el atacante para identificar el puente falso en la red.

**Campos de la Capa STP (Líneas 12-15)**
* `bpdutype=0x00`: Representa estructuralmente una BPDU de Configuración válida.
* `rootid` / `bridgeid = 0x0000`: Prioridad forzada a 0 (el valor con mayor preferencia jerárquica para los equipos Cisco).
* `rootmac`: Dirección MAC que se promociona a sí misma como la raíz absoluta de toda la topología LAN.

---

## 3. Documentación del Funcionamiento del Script
El programa ejecuta un bucle infinito estructurado con la función `sendp()` y un temporizador `time.sleep(2)`. El script arma en memoria una trama combinando la encapsulación LLC (`dsap=0x42`, `ssap=0x42`) exigida por el estándar y los parámetros modificados de Spanning Tree.

Al inyectar esta BPDU por el puerto de acceso del switch, la infraestructura recibe una notificación que afirma que existe un puente con una prioridad superior (Prioridad 0). En un entorno desprotegido, el switch se ve obligado a recalcular su algoritmo de árbol de expansión (STA), cambiando el estado de sus puertos y nombrando de forma errónea al host de Kali Linux como la nueva raíz de toda la topología.

---

## 4. Documentación de la Red

### 4.1. Topología
* **Descripción:** Escenario virtualizado en GNS3 para evaluar el comportamiento del algoritmo de árbol de expansión ante la inyección fraudulenta de tramas de control en puertos de usuario.
* **VLANs Configuradas:** VLAN 1 (Nativa / Por defecto).
* **Direccionamiento IP:**
  * **Segmento de Red:** `192.168.124.0` / `255.255.255.0`
  * **Estación Atacante (Kali Linux):** Dirección MAC configurada dinámicamente en el script (Interfaz `eth0`).
* **Interfaces Clave (SWI2):**
  * `Ethernet0/0`: Conectado hacia el switch principal de la infraestructura (SWI3).
  * `Ethernet0/2`: Conectado directamente a la estación del atacante Kali Linux.

---

## 5. Contramedidas (Mitigación)

### 5.1 Implementación de BPDU Guard (Protección Perimetral de STP)
Para neutralizar el ataque de secuestro de topología desde la infraestructura de red del switch, se aplican directivas de protección perimetral de Spanning Tree directamente en la interfaz física conectada al usuario/atacante (`Ethernet0/2`). Al activar BPDU Guard, el switch apagará de forma automática cualquier puerto de acceso si este recibe una sola trama BPDU.

SWI2# configure terminal
SWI2(config)# interface Ethernet0/2
SWI2(config-if)# switchport mode access
SWI2(config-if)# spanning-tree portfast disable
SWI2(config-if)# spanning-tree bpduguard enable

6. Evidencias
6.1. Demostración en Video

En el siguiente enlace se encuentra el video demostrativo donde se visualiza la topología con la ejecución del ataque y la aplicación de la contramedida:

https://www.youtube.com/watch?v=3rqnjT8LNZ8&list=PLGfNWxn7Di3BhsEEifmTJKXP4_U9fla7P&index=1

6.2. Capturas de Pantalla

A. Diseño de la Topología en GNS3 

<img width="421" height="420" alt="imagen" src="https://github.com/user-attachments/assets/d791a439-6877-47b8-b393-2d4f3aa74a6e" />

B. Actual root del stp antes del ataque 

<img width="660" height="411" alt="imagen" src="https://github.com/user-attachments/assets/1b49cb85-dd1f-4d62-83d6-b8bc281b566e" />

C. Ejecución del Script en Kali Linux

<img width="412" height="92" alt="imagen" src="https://github.com/user-attachments/assets/75b67881-7e39-4fc1-82a6-fb62ecff1e62" />

D.

<img width="696" height="409" alt="imagen" src="https://github.com/user-attachments/assets/59692975-6d97-4a29-8f43-90c19589a8c4" />

E. Aplicación de Contramedidas 

<img width="384" height="24" alt="imagen" src="https://github.com/user-attachments/assets/145da102-70bd-4814-9b84-c6d5bd9857ad" />

<img width="380" height="15" alt="imagen" src="https://github.com/user-attachments/assets/e4e2cbe5-589b-488b-873d-b62d75ade97b" />

respuesta del sw ante el ataque
<img width="841" height="89" alt="imagen" src="https://github.com/user-attachments/assets/79912989-b7ed-46fd-acb5-166da716f9e5" />
