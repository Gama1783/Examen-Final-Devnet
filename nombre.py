#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

def mostrar_datos():
    datos = {
        "nombre_completo": "Nelson Espinoza",
        "rut": "17.831.968-k"
    }
    print(json.dumps(datos, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    mostrar_datos()