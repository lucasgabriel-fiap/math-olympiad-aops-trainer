#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import sys
import pyperclip
from datetime import datetime
from pathlib import Path

# ============================================
# CONFIGURAÇÃO
# ============================================
MIKTEX_PATH = r"C:\Users\Lucas\AppData\Local\Programs\MiKTeX\miktex\bin\x64"
OUTPUT_FOLDER = "diagrams"

def find_ghostscript():
    """Procura Ghostscript instalado"""
    program_files = [r"C:\Program Files", r"C:\Program Files (x86)"]
    
    for pf in program_files:
        gs_path = Path(pf) / "gs"
        if gs_path.exists():
            for version_dir in sorted(gs_path.iterdir(), reverse=True):
                if version_dir.is_dir():
                    bin_dir = version_dir / "bin"
                    if bin_dir.exists():
                        for exe in ["gswin64c.exe", "gswin32c.exe"]:
                            exe_path = bin_dir / exe
                            if exe_path.exists():
                                return str(exe_path)
    return None

def get_user_asymptote_dir():
    """Retorna diretório do usuário para módulos Asymptote (SEM PRECISAR DE ADMIN)"""
    user_asy = Path.home() / ".asy"
    user_asy.mkdir(exist_ok=True)
    return user_asy

def create_olympiad_official():
    """Cria olympiad.asy no diretório do usuário"""
    
    # SEMPRE usa diretório do usuário (não precisa de admin)
    asy_dir = get_user_asymptote_dir()
    olympiad_file = asy_dir / "olympiad.asy"
    
    if olympiad_file.exists():
        print(f"   ✅ olympiad.asy já instalado")
        print(f"   📁 Local: {olympiad_file}")
        return True
    
    print(f"   📝 Criando olympiad.asy (baseado em AoPS)...")
    print(f"   📁 Local: {olympiad_file}")
    
    # Conteúdo oficial do olympiad.asy
    olympiad_content = '''// olympiad.asy
// Asymptote Olympiad Package
// Based on AoPS (Art of Problem Solving) official package

import graph;
import geometry;

// Default settings
real markscalefactor = 0.03;
real anglescalefactor = 1.0;

// Marking angles
pen AngleArc = deepgreen;

// Point size
real dotfactor = 4;

// ============================================
// USEFUL POINTS (Table 1 from AoPS)
// ============================================

// origin: The pair (0,0)
pair origin = (0,0);

// waypoint(path p, real r): Point on path p at distance r from start
pair waypoint(path p, real r) {
    return point(p, arctime(p, r));
}

// midpoint(path p): The midpoint of path p
pair midpoint(path p) {
    return point(p, 0.5*length(p));
}

// foot(pair P, pair A, pair B): Foot of perpendicular from P to line AB
pair foot(pair P, pair A, pair B) {
    real t = dot(P-A, B-A) / dot(B-A, B-A);
    return A + t*(B-A);
}

// bisectorpoint(pair A, pair B, pair C): 
// Point on angle bisector of ∠ABC at unit distance from B
pair bisectorpoint(pair A, pair B, pair C) {
    pair U = unit(A-B);
    pair V = unit(C-B);
    return B + U + V;
}

// bisectorpoint(pair A, pair B):
// Point on perpendicular bisector of segment AB at unit distance from line AB
pair bisectorpoint(pair A, pair B) {
    pair M = (A+B)/2;
    pair perp = rotate(90)*(B-A);
    return M + unit(perp);
}

// ============================================
// TRIANGLE CENTERS
// ============================================

// Circumcenter
pair circumcenter(pair A, pair B, pair C) {
    pair M1 = (A+B)/2;
    pair M2 = (B+C)/2;
    pair P1 = M1 + rotate(90)*(B-A);
    pair P2 = M2 + rotate(90)*(C-B);
    return extension(M1, P1, M2, P2);
}

// Incenter
pair incenter(pair A, pair B, pair C) {
    real a = abs(B-C);
    real b = abs(C-A);
    real c = abs(A-B);
    return (a*A + b*B + c*C)/(a+b+c);
}

// Orthocenter
pair orthocenter(pair A, pair B, pair C) {
    return extension(A, foot(A,B,C), B, foot(B,A,C));
}

// Centroid
pair centroid(pair A, pair B, pair C) {
    return (A+B+C)/3;
}

// ============================================
// DRAWING FUNCTIONS
// ============================================

// Draw right angle mark
void rightanglemark(pair A, pair O, pair B, real size=8) {
    pair dir1 = size*unit(A-O);
    pair dir2 = size*unit(B-O);
    draw(O+dir1 -- O+dir1+dir2 -- O+dir2);
}

// Mark angle with arc
void markangle(pair A, pair O, pair B, 
               real radius=8, 
               pen p=AngleArc,
               int n=1,
               real anglefactor=1.0) {
    
    real ang1 = degrees(A-O);
    real ang2 = degrees(B-O);
    
    if (ang2 < ang1) ang2 += 360;
    
    real spacing = 2;
    for (int i = 0; i < n; ++i) {
        draw(arc(O, radius + i*spacing, ang1, ang2), p);
    }
}

// Mark segments as equal
void markscalefactor(real x) {
    markscalefactor = x;
}

// ============================================
// CIRCLES
// ============================================

// Circumcircle
path circumcircle(pair A, pair B, pair C) {
    pair O = circumcenter(A, B, C);
    real r = abs(A-O);
    return circle(O, r);
}

// Incircle
path incircle(pair A, pair B, pair C) {
    pair I = incenter(A, B, C);
    real r = abs(foot(I, A, B) - I);
    return circle(I, r);
}

// ============================================
// EXTENSIONS AND INTERSECTIONS
// ============================================

// Extend point
pair extend(pair A, pair B, real t=1.0) {
    return B + t*(B-A);
}

// Reflect point
pair reflect(pair A, pair B, pair C) {
    return 2*foot(A, B, C) - A;
}

// ============================================
// BOOLEAN TESTS (with tolerance)
// ============================================

real ps = 0.001; // tolerance

// Check if three points are collinear
bool collinear(pair A, pair B, pair C) {
    return abs(cross(B-A, C-A)) < ps;
}

// Check if four points are concyclic
bool concyclic(pair A, pair B, pair C, pair D) {
    pair O = circumcenter(A, B, C);
    return abs(abs(D-O) - abs(A-O)) < ps;
}

// Check if three lines are concurrent
bool concurrent(pair A, pair B, pair C, pair D, pair E, pair F) {
    pair P = extension(A, B, C, D);
    return collinear(P, E, F);
}

// ============================================
// DRAWING HELPERS
// ============================================

// Draw triangle
void drawtriangle(pair A, pair B, pair C, pen p=currentpen) {
    draw(A--B--C--cycle, p);
}

// Draw angle arc (simple version)
void draw_angle(pair A, pair O, pair B, real r=10, pen p=currentpen) {
    real ang1 = degrees(A-O);
    real ang2 = degrees(B-O);
    if (ang2 < ang1) ang2 += 360;
    draw(arc(O, r, ang1, ang2), p);
}
'''
    
    try:
        with open(olympiad_file, 'w', encoding='utf-8') as f:
            f.write(olympiad_content)
        
        print(f"   ✅ olympiad.asy criado com sucesso!")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao criar olympiad.asy: {e}")
        return False

def create_config_asy(gs_path):
    """Cria configuração do Asymptote"""
    config_dir = get_user_asymptote_dir()
    config_file = config_dir / "config.asy"
    
    config_content = f'''import settings;
gs="{gs_path.replace("\\", "\\\\")}";
'''
    
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    return config_file

def render_from_clipboard():
    """Renderiza código do clipboard"""
    
    print("="*70)
    print("  🎨 GERADOR DE DIAGRAMAS ASYMPTOTE - VERSÃO PROFISSIONAL")
    print("="*70)
    print()
    
    # 1. Verifica Ghostscript
    print("🔍 [1/3] Verificando Ghostscript...")
    gs_path = find_ghostscript()
    
    if gs_path:
        print(f"   ✅ Encontrado: {gs_path}")
        config_file = create_config_asy(gs_path)
        print(f"   ✅ Configuração: {config_file}")
    else:
        print("   ⚠️  Ghostscript não encontrado")
        print("   📥 Baixe em: https://ghostscript.com/releases/gsdnld.html")
    
    print()
    
    # 2. Verifica/Cria olympiad.asy
    print("🔍 [2/3] Verificando módulo olympiad.asy...")
    
    codigo = pyperclip.paste().strip()
    
    if not codigo:
        print("   ❌ Clipboard vazio!")
        print()
        print("   💡 Como usar:")
        print("   1. No site, clique em 'View Code' no diagrama")
        print("   2. Clique em 'Copy Code'")
        print("   3. Execute este script")
        return False
    
    # Verifica se precisa do olympiad
    if 'import olympiad' in codigo or 'olympiad' in codigo.lower():
        if not create_olympiad_official():
            print("   ⚠️  Falha ao criar olympiad.asy, mas vou tentar compilar...")
    else:
        print("   ℹ️  Código não usa olympiad.asy")
    
    print()
    
    # 3. Compila diagrama
    print("🎨 [3/3] Compilando diagrama...")
    
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    try:
        # Prepara código completo
        codigo_completo = f"""import graph;
import geometry;

{codigo}
"""
        
        # Nome com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_base = f"diagram_{timestamp}"
        
        # Salva arquivo
        asy_file = os.path.join(OUTPUT_FOLDER, f"{nome_base}.asy")
        with open(asy_file, 'w', encoding='utf-8') as f:
            f.write(codigo_completo)
        
        print(f"   💾 Arquivo .asy: {nome_base}.asy")
        
        # Configura ambiente
        env = os.environ.copy()
        env['PATH'] = MIKTEX_PATH + os.pathsep + env.get('PATH', '')
        env['ASYMPTOTE_TEXPATH'] = MIKTEX_PATH
        
        if gs_path:
            env['ASYMPTOTE_GS'] = gs_path
        
        # IMPORTANTE: Adiciona diretório do usuário ao path do Asymptote
        user_asy = get_user_asymptote_dir()
        env['ASYMPTOTE_DIR'] = str(user_asy)
        
        print(f"   📁 Diretório de módulos: {user_asy}")
        print(f"   ⚙️  Compilando para SVG...")
        
        # Compila
        resultado = subprocess.run(
            ['asy', '-f', 'svg', '-o', nome_base, f"{nome_base}.asy"],
            cwd=OUTPUT_FOLDER,
            capture_output=True,
            text=True,
            timeout=60,
            env=env
        )
        
        # Verifica resultado
        svg_file = os.path.join(OUTPUT_FOLDER, f"{nome_base}.svg")
        
        if os.path.exists(svg_file):
            tamanho = os.path.getsize(svg_file)
            print()
            print("="*70)
            print("✅ SUCESSO!")
            print("="*70)
            print(f"📁 Pasta: {os.path.abspath(OUTPUT_FOLDER)}")
            print(f"📄 SVG: {nome_base}.svg ({tamanho:,} bytes)")
            print(f"📄 ASY: {nome_base}.asy")
            print()
            
            # Renomear
            novo_nome = input("💾 Renomear arquivo? (Enter para manter): ").strip()
            if novo_nome:
                if not novo_nome.endswith('.svg'):
                    novo_nome_svg = novo_nome + '.svg'
                    novo_nome_asy = novo_nome + '.asy'
                else:
                    novo_nome_svg = novo_nome
                    novo_nome_asy = novo_nome.replace('.svg', '.asy')
                
                # Renomeia
                os.rename(svg_file, os.path.join(OUTPUT_FOLDER, novo_nome_svg))
                os.rename(asy_file, os.path.join(OUTPUT_FOLDER, novo_nome_asy))
                
                print(f"✅ Renomeado para: {novo_nome_svg}")
            
            return True
        else:
            print()
            print("❌ ERRO: SVG não foi gerado")
            print()
            
            if resultado.stderr:
                print("📋 Detalhes do erro:")
                print("-" * 70)
                print(resultado.stderr)
                print("-" * 70)
            
            if resultado.stdout:
                print("\n📋 Output:")
                print(resultado.stdout)
            
            print()
            print("🔧 Possíveis soluções:")
            print("  1. Verifique se olympiad.asy foi criado:")
            print(f"     {user_asy / 'olympiad.asy'}")
            print("  2. Execute: asy --version (para testar Asymptote)")
            print(f"  3. Tente compilar manualmente:")
            print(f"     cd {OUTPUT_FOLDER}")
            print(f"     asy -f svg {nome_base}.asy")
            
            return False
            
    except subprocess.TimeoutExpired:
        print("\n❌ ERRO: Timeout (60 segundos)")
        print("   O diagrama é muito complexo ou há algum problema")
        return False
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        render_from_clipboard()
    except KeyboardInterrupt:
        print("\n\n⚠️ Cancelado pelo usuário")
    
    print()
    input("Pressione Enter para sair...")