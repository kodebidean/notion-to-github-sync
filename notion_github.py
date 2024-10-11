import os
from dotenv import load_dotenv
from notion_client import Client
from github import Github

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Autenticación Notion y GitHub
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
USER_REPO_NAME = os.getenv('USER_REPO_NAME')

# Inicialización de Notion y GitHub clients
notion = Client(auth=NOTION_TOKEN)
github = Github(GITHUB_TOKEN)
repo = github.get_repo(USER_REPO_NAME)

# Función para obtener todo el contenido de una page de Notion (bloques)
def get_notion_page_content(page_id):
    blocks = notion.blocks.children.list(block_id=page_id).get("results")
    return blocks

# Convertir los bloques de Notion en formato Markdown
def convert_to_markdown(blocks):
    markdown_content = ""
    
    def process_blocks(blocks):
        nonlocal markdown_content
        for block in blocks:
            block_type = block["type"]
            
            # Registro para ver el tipo de bloque y contenido
            print(f"Procesando bloque tipo: {block_type}")

            if block_type == "paragraph":
                if "rich_text" in block["paragraph"]:
                    for t in block["paragraph"]["rich_text"]:
                        # Verificar si es un texto o una mención
                        if t.get("type") == "text":
                            text_content = t["text"].get("content", "")
                            # Si contiene un enlace, mostrarlo como enlace Markdown
                            if t["text"].get("link"):
                                url = t["text"]["link"]["url"]
                                markdown_content += f"[{text_content}]({url})"
                            else:
                                markdown_content += text_content
                        elif t.get("type") == "mention":
                            mention_type = t["mention"]["type"]
                            if mention_type == "page":
                                page_id = t["mention"]["page"]["id"]
                                markdown_content += f"[Mención a page](https://www.notion.so/{page_id})"
                            elif mention_type == "user":
                                user_name = t["mention"]["user"].get("name", "Usuario mencionado")
                                markdown_content += f"@{user_name}"
                                markdown_content += "\n\n"
            elif block_type == "heading_1":
                heading = ''.join([t.get("text", {}).get("content", "") for t in block["heading_1"]["rich_text"]])
                markdown_content += "# " + heading + "\n\n"
                if block.get("has_children", False):
                    heading_1_children = notion.blocks.children.list(block_id=block["id"]).get("results")
                    process_blocks(heading_1_children)

            elif block_type == "heading_2":
                heading = ''.join([t.get("text", {}).get("content", "") for t in block["heading_2"]["rich_text"]])
                markdown_content += "## " + heading + "\n\n"
                if block.get("has_children", False):
                    heading_2_children = notion.blocks.children.list(block_id=block["id"]).get("results")
                    process_blocks(heading_2_children)

            elif block_type == "heading_3":
                heading = ''.join([t.get("text", {}).get("content", "") for t in block["heading_3"]["rich_text"]])
                markdown_content += "### " + heading + "\n\n"
                if block.get("has_children", False):
                    heading_3_children = notion.blocks.children.list(block_id=block["id"]).get("results")
                    process_blocks(heading_3_children)

            elif block_type == "bulleted_list_item":
                text = ''.join([t.get("text", {}).get("content", "") for t in block["bulleted_list_item"]["rich_text"]])
                markdown_content += "- " + text + "\n"
            elif block_type == "numbered_list_item":
                text = ''.join([t.get("text", {}).get("content", "") for t in block["numbered_list_item"]["rich_text"]])
                markdown_content += "1. " + text + "\n"
            elif block_type == "to_do":
                text = ''.join([t.get("text", {}).get("content", "") for t in block["to_do"]["rich_text"]])
                checked = block["to_do"]["checked"]
                markdown_content += f"- [{'x' if checked else ' '}] {text}\n"
            elif block_type == "toggle":
                text = ''.join([t.get("text", {}).get("content", "") for t in block["toggle"]["rich_text"]])
                markdown_content += "<details>\n<summary>" + text + "</summary>\n\n"
                if block.get("has_children", False):
                    toggle_children = notion.blocks.children.list(block_id=block["id"]).get("results")
                    process_blocks(toggle_children)
                markdown_content += "</details>\n\n"
            elif block_type == "quote":
                text = ''.join([t.get("text", {}).get("content", "") for t in block["quote"]["rich_text"]])
                markdown_content += "> " + text + "\n\n"
            elif block_type == "divider":
                markdown_content += "---\n\n"
            elif block_type == "callout":
                icon = block["callout"]["icon"]["emoji"] if block["callout"]["icon"] else ""
                text = ''.join([t.get("text", {}).get("content", "") for t in block["callout"]["rich_text"]])
                markdown_content += f"> {icon} {text}\n\n"
            elif block_type == "code":
                language = block["code"]["language"]
                code_text = ''.join([t.get("text", {}).get("content", "") for t in block["code"]["rich_text"]])
                markdown_content += f"```{language}\n{code_text}\n```\n\n"
            elif block_type == "image":
                image_url = block["image"]["file"]["url"]
                markdown_content += f"![Image]({image_url})\n\n"
            elif block_type == "file":
                file_url = block["file"]["file"]["url"]
                markdown_content += f"[File]({file_url})\n\n"
            elif block_type == "video":
                if "file" in block["video"]:
                    video_url = block["video"]["file"]["url"]
                elif "external" in block["video"]:
                    video_url = block["video"]["external"]["url"]
                else:
                    video_url = "No disponible"
                markdown_content += f"[Video]({video_url})\n\n"
            elif block_type == "bookmark":
                # Procesar enlaces de GitHub u otros como enlaces Markdown
                url = block["bookmark"]["url"]
                markdown_content += f"[Enlace]({url})\n\n"
            elif block_type == "embed":
                embed_url = block["embed"]["url"]
                markdown_content += f"[Embed]({embed_url})\n\n"
            elif block_type == "link_to_page":
                linked_page_id = block["link_to_page"]["page_id"]
                markdown_content += f"[Linked Page](https://www.notion.so/{linked_page_id})\n\n"
            elif block_type == "synced_block":
                markdown_content += "Synced Block\n\n"
            elif block_type == "child_page":
                title = block["child_page"]["title"]
                markdown_content += f"# {title}\n\n"
            else:
                markdown_content += f"<!-- Bloque no soportado: {block_type} -->\n\n"
    
    process_blocks(blocks)
    return markdown_content






# Subir archivos a GitHub (crea carpetas y sube archivos)
def upload_to_github(file_path, content):
    try:
        file = repo.get_contents(file_path)
        repo.update_file(file.path, "Actualización desde Notion", content, file.sha)
    except:
        repo.create_file(file_path, "Nuevo archivo desde Notion", content)

# Recoger todas las subpages (secciones o pages) dentro de una page
def get_subpages(page_id):
    # Obtener todos los bloques dentro de la page
    blocks = notion.blocks.children.list(block_id=page_id).get("results")
    
    # Filtrar solo los bloques que son subpages
    subpages = [block for block in blocks if block["type"] == "child_page"]
    
    # Retornar las subpages con su ID y título
    return [{"page_id": subpage["id"], "title": subpage["child_page"]["title"]} for subpage in subpages]

# Función principal para sincronizar el contenido
def sync_notion_to_github():
    # ID de la ruta raíz de notion
    NOTION_ROOT_ID = os.getenv('NOTION_ROOT_ID')

    # Obtener las pages (subpages) dentro de la raíz de tu proyecto Notion
    pages = get_subpages(NOTION_ROOT_ID)

    for page in pages:
        # Crear carpeta para la page
        folder_path = page["title"].replace(' ', '_') + "/"
        
        # Obtener las secciones (sub-subpages) dentro de la page
        subpages = get_subpages(page["page_id"])
        
        for subpage in subpages:
            # Obtener el contenido de la seccion (sub-subpage)
            blocks = get_notion_page_content(subpage["page_id"])
            markdown_content = convert_to_markdown(blocks)
            
            # Crear archivo Markdown para la seccion dentro de la carpeta de la page
            file_name = f"{folder_path}{subpage['title'].replace(' ', '_')}.md"
            upload_to_github(file_name, markdown_content)

if __name__ == "__main__":
    sync_notion_to_github()
