"""
Exporta pruebas de Python a formato para Azure Test Plans
"""
import inspect
import unittest
import sys

def exportar_casos_prueba():
    casos = []
    
    # Importar módulo de pruebas dinámicamente
    sys.path.insert(0, '.')
    try:
        import test_core_bancario
    except ImportError as e:
        print(f"❌ Error importando pruebas: {e}")
        return []
    
    print("📋 CASOS DE PRUEBA PARA AZURE TEST PLANS")
    print("=" * 60)
    
    # Buscar todas las clases que heredan de unittest.TestCase
    for nombre_clase, clase in inspect.getmembers(test_core_bancario, inspect.isclass):
        if issubclass(clase, unittest.TestCase) and nombre_clase != 'TestCase':
            print(f"\n📁 CLASE: {nombre_clase}")
            print("-" * 40)
            
            for nombre_metodo, metodo in inspect.getmembers(clase, predicate=inspect.isfunction):
                if nombre_metodo.startswith('test_'):
                    # Obtener docstring o generar descripción
                    doc = metodo.__doc__ or "Prueba del sistema bancario"
                    # Limpiar docstring
                    doc = ' '.join(doc.split())
                    
                    print(f"✅ {nombre_metodo}")
                    print(f"   📝 {doc}")
                    print(f"   🏷️ Categoría: {nombre_clase}")
                    print()
                    
                    casos.append({
                        "id": nombre_metodo,
                        "titulo": nombre_metodo.replace('test_', '').replace('_', ' ').title(),
                        "descripcion": doc,
                        "clase": nombre_clase,
                        "pasos": [
                            f"Ejecutar método: {nombre_metodo}()",
                            "Verificar que todas las aserciones pasen",
                            "Resultado esperado: Prueba exitosa"
                        ]
                    })
    
    print(f"\n🎯 TOTAL: {len(casos)} casos de prueba listos para importar")
    print("\n📝 PARA IMPORTAR EN AZURE TEST PLANS:")
    print("1. Ve a 'Test Plans' → 'New Test Plan'")
    print("2. Nombre: 'Sistema Bancario Core'")
    print("3. Crea los siguientes casos:")
    
    for i, caso in enumerate(casos, 1):
        print(f"\n{i}. {caso['titulo']}")
        print(f"   Descripción: {caso['descripcion']}")
        print(f"   Categoría: {caso['clase']}")
    
    return casos

if __name__ == "__main__":
    exportar_casos_prueba()