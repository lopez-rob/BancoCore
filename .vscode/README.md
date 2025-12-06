# 🏦 Sistema Bancario Core - Pruebas Automatizadas

![Azure DevOps builds](https://img.shields.io/badge/build-passing-success)
![Azure DevOps tests](https://img.shields.io/badge/tests-24_passed-success)
![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)
![Coverage](https://img.shields.io/badge/coverage->85%25-brightgreen)

Sistema de gestión de préstamos bancarios con pruebas automatizadas y pipeline CI/CD en Azure DevOps.

## 📊 Dashboard de Calidad

| Métrica | Estado | Objetivo |
|---------|--------|----------|
| ✅ Pruebas Unitarias | 24/24 pasando | 100% |
| 📈 Cobertura de Código | >85% | >85% |
| 🔍 Análisis Estático | 0 errores | 0 |
| 🛡️ Seguridad (Bandit) | 0 vulnerabilidades | 0 |
| ⚡ Pipeline CI/CD | Automatizado | Siempre verde |

## 🚀 Características Principales

### Sistema Bancario
- ✅ Gestión completa de clientes y préstamos
- ✅ 4 tipos de préstamos: Personal, Hipotecario, Automotriz, Educativo
- ✅ 7 estados de préstamo: Solicitado, Aprobado, Rechazado, Desembolsado, En Mora, Pagado, Cancelado
- ✅ Cálculo automático de cuotas mensuales
- ✅ Sistema de pagos y detección de moras
- ✅ Persistencia de datos en JSON

### Pruebas Automatizadas
- ✅ 24 pruebas unitarias completas
- ✅ Pruebas de integración
- ✅ Pruebas de borde y casos límite
- ✅ Pruebas de persistencia de datos
- ✅ Verificación automática de moras

### Pipeline CI/CD
- ✅ Ejecución en múltiples versiones de Python (3.7-3.11)
- ✅ Reportes de cobertura de código
- ✅ Análisis estático con Pylint
- ✅ Análisis de seguridad con Bandit
- ✅ Generación automática de reportes
- ✅ Integración con Azure DevOps

## 🛠️ Instalación Rápida

### Requisitos
- Python 3.7+
- pip (gestor de paquetes)

### Instalación
```bash
# Clonar repositorio
git clone https://dev.azure.com/your-org/your-project/_git/banco-core
cd banco-core

# Instalar dependencias
pip install -r requirements.txt
pip install coverage pylint bandit pytest-azurepipelines