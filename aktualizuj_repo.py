import os
import hashlib
import xml.etree.ElementTree as ET
import xml.dom.minidom  # Dodane do ładnego formatowania XML

def generate_repo_files():
    """Generuje addons.xml i addons.xml.md5 na podstawie folderów wtyczek."""
    addons_root = ET.Element("addons")
    
    # Pomijamy foldery, które nie są wtyczkami (śmieci systemowe i gitowe)
    ignore_dirs = {'__pycache__', '.git', '.github', '.idea', 'venv', 'env'}
    folders = [f for f in os.listdir('.') if os.path.isdir(f) and f not in ignore_dirs and not f.startswith('.')]
    
    print(f"🔍 Skanowanie folderów w poszukiwaniu wtyczek: {folders}")
    
    found_addons = 0
    for folder in folders:
        xml_path = os.path.join(folder, "addon.xml")
        if os.path.exists(xml_path):
            try:
                # Czytamy addon.xml każdej wtyczki
                tree = ET.parse(xml_path)
                addons_root.append(tree.getroot())
                print(f"✅ Dodano do indeksu repozytorium: {folder}")
                found_addons += 1
            except Exception as e:
                print(f"❌ Błąd w {xml_path}: {e}")

    if found_addons == 0:
        print("⚠️ Nie znaleziono żadnych plików addon.xml w podfolderach. Upewnij się, że uruchamiasz skrypt w głównym folderze GitHuba!")
        return

    # 1. Zapisujemy ładnie sformatowany addons.xml
    # Używamy minidom, żeby XML był czytelny (wcięcia i nowe linie) - zapobiega to błędom parsowania w Kodi
    xml_string = ET.tostring(addons_root, encoding='utf-8')
    parsed_xml = xml.dom.minidom.parseString(xml_string)
    pretty_xml = parsed_xml.toprettyxml(indent="    ")

    # Usuwamy puste linie, które minidom czasem sztucznie dodaje
    pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])

    with open("addons.xml", "w", encoding="utf-8") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n")
        # Pomijamy pierwszą linię z pretty_xml, bo minidom dodaje własną deklarację, a my chcemy naszą z "standalone"
        f.write(pretty_xml.split('\n', 1)[1] + '\n')

    # 2. Generujemy sumę kontrolną MD5 (Kodi jej wymaga!)
    with open("addons.xml", "rb") as f:
        md5_hash = hashlib.md5(f.read()).hexdigest()
    
    with open("addons.xml.md5", "w") as f:
        f.write(md5_hash)
        
    print(f"\n🚀 GOTOWE! Wygenerowano czytelny addons.xml (zawiera {found_addons} wtyczek) oraz addons.xml.md5.")
    print("Teraz wrzuć wszystkie pliki (razem ze spakowanymi ZIP-ami) na GitHuba.")

if __name__ == "__main__":
    generate_repo_files()