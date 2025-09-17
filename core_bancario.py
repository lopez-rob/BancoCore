"""
Core Bancario de Préstamos
Sistema de gestión de préstamos para instituciones financieras
"""
from datetime import datetime, timedelta
from enum import Enum
import json
from typing import List, Dict, Optional
import uuid


class EstadoPrestamo(Enum):
    SOLICITADO = "SOLICITADO"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"
    DESEMBOLSADO = "DESEMBOLSADO"
    EN_MORA = "EN_MORA"
    PAGADO = "PAGADO"
    CANCELADO = "CANCELADO"


class TipoPrestamo(Enum):
    PERSONAL = "PERSONAL"
    HIPOTECARIO = "HIPOTECARIO"
    AUTOMOTRIZ = "AUTOMOTRIZ"
    EDUCATIVO = "EDUCATIVO"


class Cliente:
    def __init__(self, id_cliente: str, nombre: str, email: str, telefono: str, 
                 ingresos_mensuales: float, score_crediticio: int):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.ingresos_mensuales = ingresos_mensuales
        self.score_crediticio = score_crediticio
        self.fecha_registro = datetime.now()
    
    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "ingresos_mensuales": self.ingresos_mensuales,
            "score_crediticio": self.score_crediticio,
            "fecha_registro": self.fecha_registro.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        cliente = cls(
            data["id_cliente"],
            data["nombre"],
            data["email"],
            data["telefono"],
            data["ingresos_mensuales"],
            data["score_crediticio"]
        )
        cliente.fecha_registro = datetime.fromisoformat(data["fecha_registro"])
        return cliente


class Pago:
    def __init__(self, id_pago: str, id_prestamo: str, monto: float, fecha_pago: datetime):
        self.id_pago = id_pago
        self.id_prestamo = id_prestamo
        self.monto = monto
        self.fecha_pago = fecha_pago
        self.fecha_registro = datetime.now()
    
    def to_dict(self):
        return {
            "id_pago": self.id_pago,
            "id_prestamo": self.id_prestamo,
            "monto": self.monto,
            "fecha_pago": self.fecha_pago.isoformat(),
            "fecha_registro": self.fecha_registro.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        pago = cls(
            data["id_pago"],
            data["id_prestamo"],
            data["monto"],
            datetime.fromisoformat(data["fecha_pago"])
        )
        pago.fecha_registro = datetime.fromisoformat(data["fecha_registro"])
        return pago


class Prestamo:
    def __init__(self, id_prestamo: str, id_cliente: str, tipo: TipoPrestamo, 
                 monto: float, tasa_interes: float, plazo_meses: int, 
                 fecha_aprobacion: Optional[datetime] = None, 
                 fecha_desembolso: Optional[datetime] = None):
        self.id_prestamo = id_prestamo
        self.id_cliente = id_cliente
        self.tipo = tipo
        self.monto = monto
        self.tasa_interes = tasa_interes
        self.plazo_meses = plazo_meses
        self.saldo = monto
        self.estado = EstadoPrestamo.SOLICITADO
        self.fecha_solicitud = datetime.now()
        self.fecha_aprobacion = fecha_aprobacion
        self.fecha_desembolso = fecha_desembolso
        self.pagos: List[Pago] = []
    
    def calcular_cuota_mensual(self) -> float:
        # Fórmula para calcular la cuota mensual: (P * r * (1 + r)^n) / ((1 + r)^n - 1)
        # donde P es el monto del préstamo, r es la tasa de interés mensual, n es el número de cuotas
        tasa_mensual = self.tasa_interes / 12 / 100
        cuota = (self.monto * tasa_mensual * (1 + tasa_mensual)**self.plazo_meses) / ((1 + tasa_mensual)**self.plazo_meses - 1)
        return round(cuota, 2)
    
    def aprobar(self):
        if self.estado == EstadoPrestamo.SOLICITADO:
            self.estado = EstadoPrestamo.APROBADO
            self.fecha_aprobacion = datetime.now()
            return True
        return False
    
    def rechazar(self):
        if self.estado == EstadoPrestamo.SOLICITADO:
            self.estado = EstadoPrestamo.RECHAZADO
            return True
        return False
    
    def desembolsar(self):
        if self.estado == EstadoPrestamo.APROBADO:
            self.estado = EstadoPrestamo.DESEMBOLSADO
            self.fecha_desembolso = datetime.now()
            return True
        return False
    
    def registrar_pago(self, monto: float, fecha_pago: datetime) -> bool:
        if self.estado != EstadoPrestamo.DESEMBOLSADO and self.estado != EstadoPrestamo.EN_MORA:
            return False
        
        if monto <= 0 or monto > self.saldo:
            return False
        
        id_pago = str(uuid.uuid4())
        pago = Pago(id_pago, self.id_prestamo, monto, fecha_pago)
        self.pagos.append(pago)
        self.saldo -= monto
        
        if self.saldo <= 0:
            self.estado = EstadoPrestamo.PAGADO
        
        return True
    
    def verificar_mora(self):
        if self.estado == EstadoPrestamo.DESEMBOLSADO and self.pagos:
            ultimo_pago = max(self.pagos, key=lambda p: p.fecha_pago)
            dias_desde_ultimo_pago = (datetime.now() - ultimo_pago.fecha_pago).days
            
            if dias_desde_ultimo_pago > 30:  # Más de 30 días sin pagar
                self.estado = EstadoPrestamo.EN_MORA
    
    def to_dict(self):
        return {
            "id_prestamo": self.id_prestamo,
            "id_cliente": self.id_cliente,
            "tipo": self.tipo.value,
            "monto": self.monto,
            "tasa_interes": self.tasa_interes,
            "plazo_meses": self.plazo_meses,
            "saldo": self.saldo,
            "estado": self.estado.value,
            "fecha_solicitud": self.fecha_solicitud.isoformat(),
            "fecha_aprobacion": self.fecha_aprobacion.isoformat() if self.fecha_aprobacion else None,
            "fecha_desembolso": self.fecha_desembolso.isoformat() if self.fecha_desembolso else None,
            "pagos": [pago.to_dict() for pago in self.pagos]
        }
    
    @classmethod
    def from_dict(cls, data):
        prestamo = cls(
            data["id_prestamo"],
            data["id_cliente"],
            TipoPrestamo(data["tipo"]),
            data["monto"],
            data["tasa_interes"],
            data["plazo_meses"],
            datetime.fromisoformat(data["fecha_aprobacion"]) if data["fecha_aprobacion"] else None,
            datetime.fromisoformat(data["fecha_desembolso"]) if data["fecha_desembolso"] else None
        )
        prestamo.saldo = data["saldo"]
        prestamo.estado = EstadoPrestamo(data["estado"])
        prestamo.fecha_solicitud = datetime.fromisoformat(data["fecha_solicitud"])
        prestamo.pagos = [Pago.from_dict(pago_data) for pago_data in data["pagos"]]
        return prestamo


class CoreBancario:
    def __init__(self):
        self.clientes: Dict[str, Cliente] = {}
        self.prestamos: Dict[str, Prestamo] = {}
        self.pagos: Dict[str, Pago] = {}
    
    def registrar_cliente(self, nombre: str, email: str, telefono: str, 
                         ingresos_mensuales: float, score_crediticio: int) -> str:
        id_cliente = str(uuid.uuid4())
        cliente = Cliente(id_cliente, nombre, email, telefono, ingresos_mensuales, score_crediticio)
        self.clientes[id_cliente] = cliente
        return id_cliente
    
    def solicitar_prestamo(self, id_cliente: str, tipo: TipoPrestamo, monto: float, 
                          plazo_meses: int) -> Optional[str]:
        if id_cliente not in self.clientes:
            return None
        
        cliente = self.clientes[id_cliente]
        
        # Reglas básicas de aprobación
        if monto <= 0 or plazo_meses <= 0:
            return None
        
        # Calcular tasa de interés basada en score crediticio
        if cliente.score_crediticio >= 800:
            tasa_interes = 8.5  # 8.5% anual
        elif cliente.score_crediticio >= 700:
            tasa_interes = 12.0  # 12% anual
        elif cliente.score_crediticio >= 600:
            tasa_interes = 15.5  # 15.5% anual
        else:
            tasa_interes = 20.0  # 20% anual (mayor riesgo)
        
        # Verificar capacidad de pago
        cuota_estimada = (monto * (tasa_interes / 100 / 12)) / (1 - (1 + tasa_interes / 100 / 12) ** -plazo_meses)
        if cuota_estimada > cliente.ingresos_mensuales * 0.4:  # No más del 40% de ingresos
            return None
        
        id_prestamo = str(uuid.uuid4())
        prestamo = Prestamo(id_prestamo, id_cliente, tipo, monto, tasa_interes, plazo_meses)
        self.prestamos[id_prestamo] = prestamo
        
        return id_prestamo
    
    def aprobar_prestamo(self, id_prestamo: str) -> bool:
        if id_prestamo not in self.prestamos:
            return False
        
        prestamo = self.prestamos[id_prestamo]
        return prestamo.aprobar()
    
    def rechazar_prestamo(self, id_prestamo: str) -> bool:
        if id_prestamo not in self.prestamos:
            return False
        
        prestamo = self.prestamos[id_prestamo]
        return prestamo.rechazar()
    
    def desembolsar_prestamo(self, id_prestamo: str) -> bool:
        if id_prestamo not in self.prestamos:
            return False
        
        prestamo = self.prestamos[id_prestamo]
        return prestamo.desembolsar()
    
    def registrar_pago(self, id_prestamo: str, monto: float, fecha_pago: datetime) -> bool:
        if id_prestamo not in self.prestamos:
            return False
        
        prestamo = self.prestamos[id_prestamo]
        return prestamo.registrar_pago(monto, fecha_pago)
    
    def obtener_estado_prestamo(self, id_prestamo: str) -> Optional[EstadoPrestamo]:
        if id_prestamo not in self.prestamos:
            return None
        
        return self.prestamos[id_prestamo].estado
    
    def obtener_prestamos_cliente(self, id_cliente: str) -> List[Prestamo]:
        return [prestamo for prestamo in self.prestamos.values() if prestamo.id_cliente == id_cliente]
    
    def obtener_prestamos_por_estado(self, estado: EstadoPrestamo) -> List[Prestamo]:
        return [prestamo for prestamo in self.prestamos.values() if prestamo.estado == estado]
    
    def verificar_moras(self):
        for prestamo in self.prestamos.values():
            prestamo.verificar_mora()
    
    def guardar_datos(self, archivo: str):
        datos = {
            "clientes": {id: cliente.to_dict() for id, cliente in self.clientes.items()},
            "prestamos": {id: prestamo.to_dict() for id, prestamo in self.prestamos.items()}
        }
        
        with open(archivo, 'w') as f:
            json.dump(datos, f, indent=2)
    
    def cargar_datos(self, archivo: str):
        try:
            with open(archivo, 'r') as f:
                datos = json.load(f)
            
            self.clientes = {id: Cliente.from_dict(cliente_data) for id, cliente_data in datos["clientes"].items()}
            self.prestamos = {id: Prestamo.from_dict(prestamo_data) for id, prestamo_data in datos["prestamos"].items()}
        except FileNotFoundError:
            print("Archivo no encontrado. Iniciando con datos vacíos.")
        except Exception as e:
            print(f"Error al cargar datos: {e}")


# Ejemplo de uso y pruebas
if __name__ == "__main__":
    # Crear instancia del core bancario
    core = CoreBancario()
    
    # Registrar cliente
    id_cliente = core.registrar_cliente(
        nombre="Juan Pérez",
        email="juan@example.com",
        telefono="+1234567890",
        ingresos_mensuales=3000.0,
        score_crediticio=750
    )
    
    print(f"Cliente registrado con ID: {id_cliente}")
    
    # Solicitar préstamo
    id_prestamo = core.solicitar_prestamo(
        id_cliente=id_cliente,
        tipo=TipoPrestamo.PERSONAL,
        monto=10000.0,
        plazo_meses=24
    )
    
    print(f"Préstamo solicitado con ID: {id_prestamo}")
    
    # Aprobar préstamo
    if core.aprobar_prestamo(id_prestamo):
        print("Préstamo aprobado")
    else:
        print("No se pudo aprobar el préstamo")
    
    # Desembolsar préstamo
    if core.desembolsar_prestamo(id_prestamo):
        print("Préstamo desembolsado")
    else:
        print("No se pudo desembolsar el préstamo")
    
    # Registrar pago
    fecha_pago = datetime.now() - timedelta(days=15)  # Hace 15 días
    if core.registrar_pago(id_prestamo, 500.0, fecha_pago):
        print("Pago registrado exitosamente")
    else:
        print("No se pudo registrar el pago")
    
    # Obtener estado del préstamo
    estado = core.obtener_estado_prestamo(id_prestamo)
    print(f"Estado del préstamo: {estado.value if estado else 'No encontrado'}")
    
    # Guardar datos
    core.guardar_datos("datos_bancarios.json")
    print("Datos guardados exitosamente")
    
    # Cargar datos (simulación)
    core2 = CoreBancario()
    core2.cargar_datos("datos_bancarios.json")
    print("Datos cargados exitosamente")
    
    # Verificar estado después de cargar
    estado = core2.obtener_estado_prestamo(id_prestamo)
    print(f"Estado del préstamo después de cargar: {estado.value if estado else 'No encontrado'}")