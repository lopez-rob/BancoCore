#!/usr/bin/env python3
"""
Script para analizar cobertura de código localmente
"""
import subprocess
import sys
import os

def ejecutar_pruebas():
    """Ejecuta todas las pruebas y calcula cobertura"""
    print("🧪 EJECUTANDO ANÁLISIS DE COBERTURA")
    print("=" * 50)
    
    # 1. Ejecutar pruebas con cobertura
    print("\n1️⃣ Ejecutando pruebas con cobertura...")
    resultado = subprocess.run(
        ['python3', '-m', 'pytest', 
         '--cov=core_bancario',
         '--cov-report=term',
         '--cov-report=html',
         'test_core_bancario.py'],
        capture_output=True,
        text=True
    )
    
    print(resultado.stdout)
    if resultado.stderr:
        print("Errores:", resultado.stderr)
    
    # 2. Contar pruebas
    print("\n2️⃣ Contando pruebas...")
    pruebas = subprocess.run(
        ['python3', '-m', 'pytest', '--collect-only'],
        capture_output=True,
        text=True
    )
    num_pruebas = len([l for l in pruebas.stdout.split('\n') if '<Function test_' in l])
    print(f"✅ Total pruebas encontradas: {num_pruebas}")
    
    # 3. Calcular líneas de código
    print("\n3️⃣ Analizando código...")
    with open('core_bancario.py', 'r') as f:
        lineas_codigo = len(f.readlines())
    with open('test_core_bancario.py', 'r') as f:
        lineas_pruebas = len(f.readlines())
    
    print(f"📄 Líneas de código: {lineas_codigo}")
    print(f"🧪 Líneas de pruebas: {lineas_pruebas}")
    print(f"📈 Ratio pruebas/código: {lineas_pruebas/lineas_codigo:.2f}:1")
    
    # 4. Verificar que todo funciona
    print("\n4️⃣ Verificación final...")
    subprocess.run(['python3', '-c', """
from core_bancario import CoreBancario, TipoPrestamo
from datetime import datetime

print("   • CoreBancario importado: ✓")
print("   • Clases disponibles: ✓")
print("   • Sistema listo para usar: ✓")
    """])
    
    print("\n" + "=" * 50)
    print("🎯 ANÁLISIS COMPLETADO")
    return resultado.returncode == 0

if __name__ == "__main__":
    if ejecutar_pruebas():
        print("\n✅ Todo funciona correctamente")
        print("\n📊 Para ver reporte HTML de cobertura:")
        print("   open htmlcov/index.html  # En Mac")
        print("   o revisa la carpeta 'htmlcov/'")
    else:
        print("\n❌ Hubo errores en la ejecución")
        sys.exit(1)