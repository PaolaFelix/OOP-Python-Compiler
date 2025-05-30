import os
from preprocessor import preprocess_code
from parser import parser
from lexer import lexer
from oop_analyzer import OOPAnalyzer

def print_separator(title, char="=", width=50):
    """Imprime un separador con título"""
    print(f"\n{char * width}")
    print(f"{title:^{width}}")
    print(f"{char * width}")

def print_oop_analysis(analysis):
    """Imprime el análisis OOP de forma organizada"""
    print_separator("ANÁLISIS OOP")
    
    # Clasificación principal
    print(f"🎯 CLASIFICACIÓN: {analysis['classification']}")
    print(f"📊 CONFIANZA: {analysis['confidence']}")
    print(f"⭐ PUNTUACIÓN OOP: {analysis['score']}/10")
    
    # Resumen estadístico
    summary = analysis['summary']
    print(f"\n📈 RESUMEN:")
    print(f"   • Clases definidas: {summary['classes']}")
    print(f"   • Métodos encontrados: {summary['methods']}")
    print(f"   • Instancias creadas: {summary['instances']}")
    print(f"   • Tiene constructor: {'Sí' if summary['has_constructor'] else 'No'}")
    
    # Razones de la clasificación
    if analysis['reasons']:
        print(f"\n✅ CRITERIOS OOP ENCONTRADOS:")
        for reason in analysis['reasons']:
            print(f"   • {reason}")
    
    # Detalles específicos
    if analysis['details']:
        print(f"\n🔍 DETALLES DEL ANÁLISIS:")
        for detail in analysis['details']:
            print(f"   {detail}")

def analyze_file(filename, test_path):
    """Analiza un archivo individual"""
    print(f"\n{'='*80}")
    print(f"🔍 ANALIZANDO ARCHIVO: {filename}")
    print(f"{'='*80}")
    
    # Preprocesamiento
    preprocessed_code = preprocess_code(test_path)
    print_separator("CÓDIGO PREPROCESADO")
    for i, line in enumerate(preprocessed_code, 1):
        print(f"{i:2}: {line.rstrip()}")

    # Parsing
    print_separator("PARSING")
    result = parser.parse(''.join(preprocessed_code), lexer=lexer)
    
    if result is None:
        print("❌ Error en el parsing. No se pudo analizar el código.")
        return None
    
    print("✅ Parsing exitoso")
    print(f"📝 AST generado: {result}")

    # Análisis OOP
    analyzer = OOPAnalyzer()
    oop_analysis = analyzer.analyze_ast(result)
    
    # Mostrar resultados
    print_oop_analysis(oop_analysis)
    
    # Conclusión final
    print_separator("CONCLUSIÓN FINAL")
    classification = oop_analysis['classification']
    
    if classification == "CÓDIGO OOP":
        print("🎉 ¡Este código utiliza programación orientada a objetos!")
        print("   El código demuestra un uso completo de conceptos OOP.")
    elif classification == "POSIBLEMENTE OOP":
        print("🤔 Este código tiene características de OOP.")
        print("   Utiliza algunos conceptos de programación orientada a objetos.")
    elif classification == "ELEMENTOS OOP BÁSICOS":
        print("⚠️  Este código tiene elementos básicos de OOP.")
        print("   Usa algunos conceptos OOP pero de forma limitada.")
    else:
        print("❌ Este código NO es orientado a objetos.")
        print("   No utiliza los conceptos principales de OOP.")
    
    return oop_analysis

def main():
    tests_dir = 'tests'
    
    # Verificar que la carpeta tests existe
    if not os.path.isdir(tests_dir):
        print(f"❌ La carpeta '{tests_dir}' no existe.")
        return
    
    # Obtener todos los archivos .py de la carpeta tests
    python_files = [f for f in os.listdir(tests_dir) if f.endswith('.py')]
    
    if not python_files:
        print(f"❌ No se encontraron archivos Python (.py) en la carpeta '{tests_dir}'.")
        return
    
    print(f"📁 Archivos encontrados en '{tests_dir}': {len(python_files)}")
    for i, filename in enumerate(python_files, 1):
        print(f"   {i}. {filename}")
    
    # Analizar cada archivo
    results = {}
    for filename in python_files:
        test_path = os.path.join(tests_dir, filename)
        analysis = analyze_file(filename, test_path)
        if analysis:
            results[filename] = analysis
    
    # Resumen final de todos los archivos
    if results:
        print(f"\n{'='*80}")
        print(f"📊 RESUMEN FINAL DE TODOS LOS ARCHIVOS")
        print(f"{'='*80}")
        
        for filename, analysis in results.items():
            classification = analysis['classification']
            score = analysis['score']
            confidence = analysis['confidence']
            
            # Emoji según clasificación
            emoji = "🎉" if classification == "CÓDIGO OOP" else \
                   "🤔" if classification == "POSIBLEMENTE OOP" else \
                   "⚠️" if classification == "ELEMENTOS OOP BÁSICOS" else "❌"
            
            print(f"{emoji} {filename:<20} | {classification:<25} | Puntuación: {score}/10 | Confianza: {confidence}")

if __name__ == '__main__':
    main()