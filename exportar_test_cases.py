"""
Genera lista de casos de prueba para Azure Test Plans
"""

print("📋 CASOS DE PRUEBA - SISTEMA BANCARIO CORE")
print("=" * 50)
print("\nTOTAL: 14 PRUEBAS AUTOMATIZADAS")
print("\n" + "=" * 50)

# Pruebas de TestCoreBancario
print("\n📁 SUITE: TestCoreBancario (Pruebas Básicas)")
print("-" * 40)
tests_basicas = [
    "test_registrar_cliente",
    "test_solicitar_prestamo_valido", 
    "test_solicitar_prestamo_monto_invalido",
    "test_solicitar_prestamo_cliente_inexistente",
    "test_aprobar_prestamo",
    "test_desembolsar_prestamo", 
    "test_registrar_pago",
    "test_verificar_moras",
    "test_guardar_y_cargar_datos",
    "test_calcular_cuota_mensual"
]

for i, test in enumerate(tests_basicas, 1):
    print(f"TC{i:02d}: {test.replace('test_', '').replace('_', ' ').title()}")

# Pruebas de TestCoreBancarioAvanzado  
print("\n📁 SUITE: TestCoreBancarioAvanzado (Pruebas Avanzadas)")
print("-" * 40)
tests_avanzadas = [
    "test_pago_completo_cambia_estado_a_pagado",
    "test_rechazar_prestamo",
    "test_capacidad_pago_limite_40_porciento", 
    "test_multiples_clientes_y_prestamos"
]

for i, test in enumerate(tests_avanzadas, 1):
    print(f"TC{i+10:02d}: {test.replace('test_', '').replace('_', ' ').title()}")

print("\n" + "=" * 50)
print("🎯 PARA AZURE TEST PLANS:")
print("1. Ve a 'Test Plans' → 'New Test Plan'")
print("2. Crea 14 casos manualmente usando los nombres TC01-TC14")
print("3. Asocia este pipeline al Test Plan")
print("=" * 50)