"""
Script utilitario de inicialización (Seeder).
Crea los registros iniciales requeridos para la primera autenticación en la API:
- Área: Dirección General
- Cargo: Administrador de Sistema / Administrador
- Empleado: Administrador Sistema (email: admin@sistema.com, pass: Admin123!)
"""
import sys
import os

# Asegurar que 'src' esté en el sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from shared.infrastructure.database.connection import DatabaseConnection
from shared.infrastructure.security.security import get_password_hash
from modules.catalogos.infrastructure.persistence import AreaRepositoryAdapter, CargoRepositoryAdapter
from modules.catalogos.domain.entities import Area, Cargo
from modules.personal.infrastructure.persistence import EmpleadoRepositoryAdapter
from modules.personal.domain.entities import Empleado


def seed():
    print("🌱 Iniciando proceso de seeding inicial...")

    area_repo = AreaRepositoryAdapter()
    cargo_repo = CargoRepositoryAdapter()
    empleado_repo = EmpleadoRepositoryAdapter()

    try:
        # 1. Crear Área "Dirección General"
        area = area_repo.get_by_nombre("Dirección General")
        if not area:
            new_area = Area(nombre="Dirección General")
            area = area_repo.add(new_area)
            print(f"✅ Área creada: 'Dirección General' (ID: {area.id})")
        else:
            print(f"ℹ️ Área ya existente: 'Dirección General' (ID: {area.id})")

        # 2. Crear Cargos ("Administrador de Sistema" y "Administrador")
        cargo_admin_sys = cargo_repo.get_by_nombre("Administrador de Sistema")
        if not cargo_admin_sys:
            cargo_admin_sys = cargo_repo.add(Cargo(nombre="Administrador de Sistema"))
            print(f"✅ Cargo creado: 'Administrador de Sistema' (ID: {cargo_admin_sys.id})")
        else:
            print(f"ℹ️ Cargo ya existente: 'Administrador de Sistema' (ID: {cargo_admin_sys.id})")

        cargo_admin = cargo_repo.get_by_nombre("Administrador")
        if not cargo_admin:
            cargo_admin = cargo_repo.add(Cargo(nombre="Administrador"))
            print(f"✅ Cargo creado: 'Administrador' (ID: {cargo_admin.id})")
        else:
            print(f"ℹ️ Cargo ya existente: 'Administrador' (ID: {cargo_admin.id})")

        # 3. Crear Empleado Administrador
        admin_email = "admin@sistema.com"
        admin_emp = empleado_repo.get_by_email(admin_email)
        if not admin_emp:
            hashed_pw = get_password_hash("Admin123!")
            new_emp = Empleado(
                nombre="Administrador Sistema",
                email=admin_email,
                idArea=area.id,
                activo=True,
                password_hash=hashed_pw
            )
            admin_emp = empleado_repo.add_with_cargos(new_emp, [cargo_admin_sys.id, cargo_admin.id])
            print(f"✅ Empleado Admin creado con éxito:")
            print(f"   - Email: {admin_email}")
            print(f"   - Contraseña: Admin123!")
            print(f"   - ID Empleado: {admin_emp.id}")
        else:
            print(f"ℹ️ Empleado Admin ya existente (Email: {admin_email}, ID: {admin_emp.id})")

        print("\n🎉 Seeding completado exitosamente. ¡Ya puedes autenticarte!")

    except Exception as e:
        print(f"❌ Error durante el seeding de base de datos: {e}")
        raise


if __name__ == "__main__":
    seed()
