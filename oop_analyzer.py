class OOPAnalyzer:
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reinicia el análisis para un nuevo archivo"""
        self.has_class = False
        self.has_constructor = False
        self.has_instance_creation = False
        self.has_method_call = False
        self.has_attribute_access = False
        self.has_inheritance = False
        self.classes_found = []
        self.methods_found = []
        self.instances_found = []
        self.details = []
    
    def analyze_ast(self, ast_node):
        """Analiza el AST y determina si es OOP"""
        self.reset()
        self._traverse_node(ast_node)
        return self._classify()
    
    def _traverse_node(self, node):
        """Recorre recursivamente el AST"""
        if isinstance(node, tuple):
            node_type = node[0]
            
            if node_type == 'program':
                # Analizar la lista de statements
                for stmt in node[1]:
                    self._traverse_node(stmt)
            
            elif node_type == 'class_def':
                self.has_class = True
                class_name = node[1]
                self.classes_found.append(class_name)
                self.details.append(f"✓ Clase definida: {class_name}")
                
                # Analizar el cuerpo de la clase
                class_body = node[2]
                for stmt in class_body:
                    self._traverse_node(stmt)
            
            elif node_type == 'method_def':
                method_name = node[1]
                params = node[2]
                self.methods_found.append(method_name)
                
                if method_name == '__init__':
                    self.has_constructor = True
                    self.details.append(f"✓ Constructor encontrado: {method_name}")
                else:
                    self.details.append(f"✓ Método definido: {method_name}")
                
                # Verificar si tiene 'self' como primer parámetro
                if params and params[0] == 'self':
                    self.details.append(f"  - Método {method_name} usa 'self' correctamente")
                
                # Analizar el cuerpo del método
                method_body = node[3]
                for stmt in method_body:
                    self._traverse_node(stmt)
            
            elif node_type == 'constructor_call':
                self.has_instance_creation = True
                class_name = node[1]
                args = node[2]
                self.instances_found.append(class_name)
                self.details.append(f"✓ Instancia creada de: {class_name}")
            
            elif node_type == 'function_call':
                # Distinguir entre llamadas a funciones y constructores
                func_name = node[1]
                args = node[2]
                
                # Si la función tiene el mismo nombre que una clase definida, podría ser un constructor
                if func_name in self.classes_found:
                    self.has_instance_creation = True
                    self.instances_found.append(func_name)
                    self.details.append(f"✓ Posible instancia creada de: {func_name}")
                else:
                    # Es una llamada a función regular (no OOP)
                    self.details.append(f"• Llamada a función: {func_name}()")
            
            elif node_type == 'method_call':
                self.has_method_call = True
                obj_name = node[1]
                method_name = node[2]
                args = node[3]
                self.details.append(f"✓ Llamada a método: {obj_name}.{method_name}()")
            
            elif node_type == 'self_assignment':
                self.has_attribute_access = True
                attr_name = node[1]
                self.details.append(f"✓ Asignación de atributo: self.{attr_name}")
            
            elif node_type == 'self_attr':
                self.has_attribute_access = True
                attr_name = node[1]
                self.details.append(f"✓ Acceso a atributo: self.{attr_name}")
            
            elif node_type == 'attr_access':
                self.has_attribute_access = True
                obj_name = node[1]
                attr_name = node[2]
                self.details.append(f"✓ Acceso a atributo: {obj_name}.{attr_name}")
            
            elif node_type == 'attr_assignment':
                self.has_attribute_access = True
                obj_name = node[1]
                attr_name = node[2]
                self.details.append(f"✓ Asignación de atributo: {obj_name}.{attr_name}")
            
            # Recursivamente analizar otros nodos
            else:
                for item in node[1:]:
                    if isinstance(item, (list, tuple)):
                        if isinstance(item, list):
                            for sub_item in item:
                                self._traverse_node(sub_item)
                        else:
                            self._traverse_node(item)
    
    def _classify(self):
        """CClassifies if the code is OOP based on found patterns"""
        oop_score = 0
        reasons = []
        
        # Criterios para considerar OOP (con pesos)
        if self.has_class:
            oop_score += 3
            reasons.append("Define clases")
        
        if self.has_constructor:
            oop_score += 2
            reasons.append("Tiene constructor (__init__)")
        
        if self.has_instance_creation:
            oop_score += 2
            reasons.append("Crea instancias de objetos")
        
        if self.has_method_call:
            oop_score += 2
            reasons.append("Llama métodos de objetos")
        
        if self.has_attribute_access:
            oop_score += 1
            reasons.append("Accede/asigna atributos")
        
        # Clasificación
        if oop_score >= 5:
            classification = "CÓDIGO OOP"
            confidence = "Alta"
        elif oop_score >= 3:
            classification = "POSIBLEMENTE OOP"
            confidence = "Media"
        elif oop_score >= 1:
            classification = "ELEMENTOS OOP BÁSICOS"
            confidence = "Baja"
        else:
            classification = "NO ES OOP"
            confidence = "Alta"
        
        return {
            'classification': classification,
            'confidence': confidence,
            'score': oop_score,
            'reasons': reasons,
            'details': self.details,
            'summary': {
                'classes': len(self.classes_found),
                'methods': len(self.methods_found),
                'instances': len(self.instances_found),
                'has_constructor': self.has_constructor
            }
        }