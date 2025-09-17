import unittest
from datetime import datetime, timedelta
from core_bancario import CoreBancario, Cliente, Prestamo, Pago, EstadoPrestamo, TipoPrestamo
import uuid
import os


class TestCoreBancario(unittest.TestCase):
    def setUp(self):
        self.core = CoreBancario()
        self.id_cliente = self.core.registrar_cliente(
            "María García", 
            "maria@example.com", 
            "+1234567890", 
            5000.0, 
            800
        )
    
    def test_registrar_cliente(self):
        self.assertIsNotNone(self.id_cliente)
        self.assertIn(self.id_cliente, self.core.clientes)
    
    def test_solicitar_prestamo_valido(self):
        id_prestamo = self.core.solicitar_prestamo(
            self.id_cliente, 
            TipoPrestamo.PERSONAL, 
            10000.0, 
            24
        )
        self.assertIsNotNone(id_prestamo)
        self.assertIn(id_prestamo, self.core.prestamos)
        
        prestamo = self.core.prestamos[id_prestamo]
        self.assertEqual(prestamo.estado, EstadoPrestamo.SOLICITADO)
        self.assertEqual(prestamo.monto, 10000.0)
        self.assertEqual(prestamo.tasa_interes, 8.5)  # Para score 800
    
    def test_solicitar_prestamo_monto_invalido(self):
        id_prestamo = self.core.solicitar_prestamo(
            self.id_cliente, 
            TipoPrestamo.PERSONAL, 
            -1000.0,  # Monto negativo
            24
        )
        self.assertIsNone(id_prestamo)
    
    def test_solicitar_prestamo_cliente_inexistente(self):
        id_prestamo = self.core.solicitar_prestamo(
            "cliente_inexistente", 
            TipoPrestamo.PERSONAL, 
            10000.0, 
            24
        )
        self.assertIsNone(id_prestamo)
    
    def test_aprobar_prestamo(self):
        id_prestamo = self.core.solicitar_prestamo(
            self.id_cliente, 
            TipoPrestamo.PERSONAL, 
            10000.0, 
            24
        )
        
        resultado = self.core.aprobar_prestamo(id_prestamo)
        self.assertTrue(resultado)
        
        prestamo = self.core.prestamos[id_prestamo]
        self.assertEqual(prestamo.estado, EstadoPrestamo.APROBADO)
        self.assertIsNotNone(prestamo.fecha_aprobacion)
    
    def test_desembolsar_prestamo(self):
        id_prestamo = self.core.solicitar_prestamo(
            self.id_cliente, 
            TipoPrestamo.PERSONAL, 
            10000.0, 
            24
        )
        
        self.core.aprobar_prestamo(id_prestamo)
        resultado = self.core.desembolsar_prestamo(id_prestamo)
        self.assertTrue(resultado)
        
        prestamo = self.core.prestamos[id_prestamo]
        self.assertEqual(prestamo.estado, EstadoPrestamo.DESEMBOLSADO)
        self.assertIsNotNone(prestamo.fecha_desembolso)
    
    def test_registrar_pago(self):
        id_prestamo = self.core.solicitar_prestamo(
            self.id_cliente, 
            TipoPrestamo.PERSONAL, 
            10000.0, 
            24
        )
        
        self.core.aprobar_prestamo(id_prestamo)
        self.core.desembolsar_prestamo(id_prestamo)
        
        fecha_pago = datetime.now()
        resultado = self.core.registrar_pago(id_prestamo, 500.0, fecha_pago)
        self.assertTrue(resultado)
        
        prestamo = self.core.prestamos[id_prestamo]
        self.assertEqual(prestamo.saldo, 9500.0)
        self.assertEqual(len(prestamo.pagos), 1)
    
    def test_verificar_moras(self):
        id_prestamo = self.core.solicitar_prestamo(
            self.id_cliente, 
            TipoPrestamo.PERSONAL, 
            10000.0, 
            24
        )
        
        self.core.aprobar_prestamo(id_prestamo)
        self.core.desembolsar_prestamo(id_prestamo)
        
        # Registrar un pago hace 45 días (debería estar en mora)
        fecha_pago_antiguo = datetime.now() - timedelta(days=45)
        self.core.registrar_pago(id_prestamo, 500.0, fecha_pago_antiguo)
        
        # Verificar moras
        self.core.verificar_moras()
        
        prestamo = self.core.prestamos[id_prestamo]
        self.assertEqual(prestamo.estado, EstadoPrestamo.EN_MORA)
    
    def test_guardar_y_cargar_datos(self):
        # Crear datos de prueba
        id_prestamo = self.core.solicitar_prestamo(
            self.id_cliente, 
            TipoPrestamo.PERSONAL, 
            10000.0, 
            24
        )
        self.core.aprobar_prestamo(id_prestamo)
        
        # Guardar datos
        archivo = "test_datos.json"
        self.core.guardar_datos(archivo)
        
        # Crear nuevo core y cargar datos
        core_nuevo = CoreBancario()
        core_nuevo.cargar_datos(archivo)
        
        # Verificar que los datos se cargaron correctamente
        self.assertIn(self.id_cliente, core_nuevo.clientes)
        self.assertIn(id_prestamo, core_nuevo.prestamos)
        
        prestamo = core_nuevo.prestamos[id_prestamo]
        self.assertEqual(prestamo.estado, EstadoPrestamo.APROBADO)
        self.assertEqual(prestamo.monto, 10000.0)
        
        # Limpiar archivo de prueba
        if os.path.exists(archivo):
            os.remove(archivo)
    
    def test_calcular_cuota_mensual(self):
        prestamo = Prestamo(
            str(uuid.uuid4()),
            self.id_cliente,
            TipoPrestamo.PERSONAL,
            10000.0,
            12.0,  # 12% anual
            24     # 24 meses
        )
        
        cuota = prestamo.calcular_cuota_mensual()
        # Verificar que la cuota es un valor positivo
        self.assertGreater(cuota, 0)
        # Verificar que la cuota es menor al monto del préstamo
        self.assertLess(cuota, 10000.0)


if __name__ == "__main__":
    unittest.main()