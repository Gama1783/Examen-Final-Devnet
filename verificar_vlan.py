#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

def verificar_vlan(vlan: int) -> dict:
    if 1 <= vlan <= 1005:
        rango = "normal"
    elif 1006 <= vlan <= 4094:
        rango = "extendido"
    else:
        rango = "inválido"
    return {
        "vlan": vlan,
        "resultado": rango
    }

if __name__ == "__main__":
    entrada = input("Ingrese el número de VLAN: ")
    if entrada.isdigit():
        resultado = verificar_vlan(int(entrada))
        print(json.dumps(resultado, indent=4, ensure_ascii=False))
    else:
        print(json.dumps({"error": "Entrada inválida"}, indent=4, ensure_ascii=False))