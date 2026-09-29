import abc
from typing import Any, Dict


class ResourceAdapter(abc.ABC):
    @abc.abstractmethod
    def resolve(self, path: str) -> Any:
        pass

    @abc.abstractmethod
    def register(self, name: str, resource_info: Any) -> None:
        pass



class FileAdapter(ResourceAdapter):
    def __init__(self):
        self._file_table: Dict[str, str] = {}

    def register(self, name: str, resource_info: str) -> None:
        self._file_table[name] = resource_info  # resource_info = physical path

    def resolve(self, path: str) -> str:
        return self._file_table.get(path, f"Error: Archivo '{path}' no encontrado.")



class ProcessAdapter(ResourceAdapter):
    def __init__(self):
        self._process_table: Dict[str, int] = {}

    def register(self, name: str, resource_info: int) -> None:
        self._process_table[name] = resource_info  # resource_info = PID

    def resolve(self, path: str) -> Any:
        pid = self._process_table.get(path)
        return f"Process PID: {pid}" if pid else f"Error: Proceso '{path}' no hallado."



class ServiceAdapter(ResourceAdapter):
    def __init__(self):
        self._service_table: Dict[str, str] = {}

    def register(self, name: str, resource_info: str) -> None:
        self._service_table[name] = resource_info  # resource_info = IP:Port

    def resolve(self, path: str) -> Any:
        endpoint = self._service_table.get(path)
        return f"Service Endpoint: {endpoint}" if endpoint else f"Error: Servicio '{path}' no activo."



class MemoryAdapter(ResourceAdapter):
    def __init__(self):
        self._memory_table: Dict[str, str] = {}

    def register(self, name: str, resource_info: str) -> None:
        self._memory_table[name] = resource_info  # resource_info = Memory Address Offset

    def resolve(self, path: str) -> Any:
        addr = self._memory_table.get(path)
        return f"Memory Segment Address: {addr}" if addr else f"Error: Bloque '{path}' invalido."


# --- CORE SIN (Sistema de Nombrado Integral) ---
class SistemaNombradoIntegral:
    def __init__(self):
        self._adapters: Dict[str, ResourceAdapter] = {
            "file": FileAdapter(),
            "process": ProcessAdapter(),
            "service": ServiceAdapter(),
            "memory": MemoryAdapter()
        }

    def registrar_recurso(self, uri: str, info_tecnica: Any) -> None:
        # URI format: sin://<resource_type>/<name>
        prefix, path = self._parse_uri(uri)
        if prefix in self._adapters:
            self._adapters[prefix].register(path, info_tecnica)
            print(f"[SIN OK] Recurso '{uri}' registrado correctamente.")
        else:
            print(f"[SIN ERROR] Tipo de recurso '{prefix}' no soportado.")

    def resolver_recurso(self, uri: str) -> Any:
        prefix, path = self._parse_uri(uri)
        if prefix in self._adapters:
            return self._adapters[prefix].resolve(path)
        return f"[SIN ERROR] Esquema de nombrado no soportado: '{prefix}'"

    def _parse_uri(self, uri: str):
        if not uri.startswith("sin://"):
            raise ValueError("URI invalida. Debe comenzar con 'sin://'")
        clean_uri = uri.replace("sin://", "")
        parts = clean_uri.split("/", 1)
        return parts[0], parts[1] if len(parts) > 1 else ""


# --- EJECUCIÓN Y PRUEBA DEL SISTEMA ---
if __name__ == "__main__":
    sin = SistemaNombradoIntegral()

    # 1. Registro de Recursos Hetrogéneos
    sin.registrar_recurso("sin://file/docs/informe.pdf", "/var/data/storage/block_982.dat")
    sin.registrar_recurso("sin://process/worker-node-1", 4120)
    sin.registrar_recurso("sin://service/auth-api", "192.168.1.50:8080")
    sin.registrar_recurso("sin://memory/buffer-pool", "0x7FFF5FBFF040")

    print("\n--- RESOLUCIÓN DE NOMBRES EN EL SIN ---")
    # 2. Resolución de Recursos mediante Interfaz Única
    print("file    ->", sin.resolver_recurso("sin://file/docs/informe.pdf"))
    print("process ->", sin.resolver_recurso("sin://process/worker-node-1"))
    print("service ->", sin.resolver_recurso("sin://service/auth-api"))
    print("memory  ->", sin.resolver_recurso("sin://memory/buffer-pool"))