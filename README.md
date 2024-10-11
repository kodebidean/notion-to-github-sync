El Markdown en GitHub sí funciona perfectamente cuando lo añades al archivo `README.md`. Sin embargo, las secciones que mencionan comandos de shell, como `pip install` o la creación del archivo `.env`, deben estar correctamente formateadas usando bloques de código (triple backticks) para que se visualicen como código y no como texto plano.

Voy a ajustar algunos detalles para asegurarme de que todo el contenido sea visualizado correctamente en GitHub y el Markdown funcione como se espera.

Aquí te dejo la versión corregida del `README.md`:

---

# Notion to GitHub Sync Script

Este repositorio contiene un script Python que permite sincronizar contenido de una página de Notion con un repositorio de GitHub en formato Markdown. El script es altamente configurable y permite ajustar el contenido a tus necesidades, utilizando variables de entorno para mayor seguridad.

## Requisitos

Antes de comenzar, asegúrate de tener los siguientes requisitos instalados en tu máquina:

- **Python 3.x**: Asegúrate de tener instalada una versión reciente de Python. Puedes descargarla desde [aquí](https://www.python.org/downloads/).
- **pip**: Si no lo tienes instalado, puedes instalar `pip` ejecutando: 
  ```bash
  python -m ensurepip --upgrade
  ```

## Instalación

### 1. Clonar el repositorio

Primero, clona este repositorio en tu máquina local:

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

### 2. Crear el entorno virtual (opcional pero recomendado)

Es recomendable crear un entorno virtual para mantener las dependencias del proyecto aisladas:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar las dependencias

Instala las dependencias necesarias utilizando `pip`. Estas incluyen las bibliotecas para interactuar con la API de Notion y GitHub, además de `dotenv` para manejar las variables de entorno.

```bash
pip install -r requirements.txt
```

Si no tienes un archivo `requirements.txt`, puedes ejecutar:

```bash
pip install python-dotenv notion-client PyGithub
```

### 4. Crear el archivo `.env`

El script utiliza un archivo `.env` para cargar las credenciales necesarias sin exponerlas directamente en el código.

Copia el archivo `.env.example` para crear tu archivo `.env`:

```bash
cp .env.example .env
```

Luego abre el archivo `.env` y añade tus tokens de Notion y GitHub, así como el ID de la página raíz de Notion y el nombre de tu repositorio de GitHub. El archivo `.env` debe verse así:

```bash
# NOTION
NOTION_TOKEN=tu_notion_token
NOTION_ROOT_ID=tu_notion_root_id

# GITHUB
GITHUB_TOKEN=tu_github_token
USER_REPO_NAME=tu_usuario_github/tu_nombre_repositorio
```

#### ¿Cómo obtener tu token de Notion?
1. Ve a [Notion Integrations](https://www.notion.so/my-integrations) y crea una nueva integración.
2. Copia el **Internal Integration Token** que te proporcionan.
3. Añade este token como `NOTION_TOKEN` en tu archivo `.env`.

#### ¿Cómo obtener tu token de GitHub?
1. Ve a [GitHub Tokens](https://github.com/settings/tokens) y genera un nuevo token con permisos para `repo` y `workflow`.
2. Añade este token como `GITHUB_TOKEN` en tu archivo `.env`.

#### ¿Cómo obtener el ID de la página raíz en Notion?
1. Abre tu página principal de Notion.
2. Copia el ID de la página desde la URL del navegador (es una secuencia de números y letras después de `notion.so/`).

### 5. Ejecutar el script

Una vez configurado el archivo `.env`, ya puedes ejecutar el script para sincronizar el contenido de Notion con GitHub:

```bash
python notion_github.py
```

### 6. Verificar los resultados

Después de ejecutar el script, los archivos de Markdown se crearán en tu repositorio de GitHub en la estructura que refleje las páginas de Notion.

Cada sección de Notion se convertirá en un archivo Markdown que se organizará en carpetas según la estructura de la página.

## Uso avanzado

### Personalización del script

Puedes modificar el script para ajustar la estructura de carpetas y nombres de archivo. El script ya maneja la conversión de enlaces, encabezados, listas, citas, y más.

Si necesitas personalizar más tipos de bloques, consulta la [documentación de la API de Notion](https://developers.notion.com/).

### Contribuciones

Si quieres contribuir con mejoras, siente libre de crear un **Pull Request** o abrir un **Issue** para discutir nuevas funcionalidades o correcciones.

---

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](./LICENSE) para más información.

---

### Últimos detalles

- Asegúrate de que el archivo `.gitignore` esté configurado para evitar que el archivo `.env` suba al repositorio.
- Si decides que el repositorio sea público, evita incluir información sensible en tus commits.

---

### Comentarios adicionales

- Puedes añadir un archivo `LICENSE` en tu repositorio para incluir la licencia bajo la cual compartes el código.
- Si deseas incluir ejemplos de salidas o archivos de muestra, podrías crear una carpeta `/examples` y documentar el uso del script en más detalle.

### Estructura del proyecto
Al final, tu estructura de carpetas será algo así:

```
/tu_repositorio
  - .gitignore
  - .env.example
  - notion_github.py  # El script principal
  - README.md         # Documentación del proyecto
  - LICENSE           # Licencia del proyecto (si decides incluirla)
```

---