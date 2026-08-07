#!/usr/bin/env python3
"""
Sincronizador Automático de PDFs do Menu de Estudos DevOps
Varre todas as pastas 'pdf/' dos 36 módulos e gera o catálogo dinâmico 'pdf/index.json'.
Basta colocar ou remover um arquivo .pdf na pasta 'pdf/' de qualquer módulo e rodar este script!
"""

import os
import json
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(base_dir, "dataset")
modules_json_path = os.path.join(dataset_dir, "modules.json")

def format_title(filename):
    name = os.path.splitext(filename)[0]
    clean = re.sub(r'[-_]+', ' ', name)
    return clean.title()

def sync():
    if not os.path.exists(modules_json_path):
        print("Erro: dataset/modules.json não encontrado!")
        return

    with open(modules_json_path, 'r', encoding='utf-8') as f:
        modules = json.load(f)

    total_modules = len(modules)
    total_pdfs = 0

    print(f"🔄 Sincronizando PDFs em {total_modules} módulos...")

    for mod in modules:
        rel_path = mod.get("path", "")
        if not rel_path:
            continue
            
        mod_dir = os.path.dirname(os.path.join(base_dir, rel_path))
        pdf_dir = os.path.join(mod_dir, "pdf")
        os.makedirs(pdf_dir, exist_ok=True)

        # Mover qualquer PDF solto na raiz do módulo para pdf/
        for f in os.listdir(mod_dir):
            if f.endswith(".pdf"):
                src = os.path.join(mod_dir, f)
                dst = os.path.join(pdf_dir, f)
                if src != dst and not os.path.exists(dst):
                    os.rename(src, dst)
                    print(f"  └─ Movido {f} para pasta pdf/")

        # Mapear arquivos .pdf existentes na pasta pdf/
        pdf_list = []
        for file in sorted(os.listdir(pdf_dir)):
            if file.endswith(".pdf"):
                pdf_list.append({
                    "title": format_title(file),
                    "file": file,
                    "description": f"Documento oficial localizado na pasta pdf/{file}"
                })

        # Escrever pdf/index.json
        index_file = os.path.join(pdf_dir, "index.json")
        with open(index_file, 'w', encoding='utf-8') as f_out:
            json.dump(pdf_list, f_out, ensure_ascii=False, indent=2)

        # Manter compatibilidade com pdfs.json legado
        legacy_file = os.path.join(mod_dir, "pdfs.json")
        with open(legacy_file, 'w', encoding='utf-8') as f_out:
            json.dump(pdf_list, f_out, ensure_ascii=False, indent=2)

        if pdf_list:
            total_pdfs += len(pdf_list)
            print(f"  ✅ {mod['name']}: {len(pdf_list)} PDF(s) catalogado(s)")

    print(f"\n🎉 Sincronização concluída! Total de {total_pdfs} PDF(s) catalogados.")

if __name__ == "__main__":
    sync()
