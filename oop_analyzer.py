class OOPAnalyzer:
    def __init__(self):
        # Constructor: Initializes the analyzer's state when a new OOPAnalyzer object is created.
        self.reset()
    
    def reset(self):
        """Resets the analysis state for a new file or analysis run."""
        self.has_class = False # Flag to track if any class definition is found in the code.
        self.has_constructor = False # Flag to track if the special '__init__' method (constructor) is found.
        self.has_instance_creation = False # Flag to track if any object instances are created.
        self.has_method_call = False # Flag to track if methods are called on objects.
        self.has_attribute_access = False # Flag to track if object attributes are accessed or assigned.
        self.has_inheritance = False # Flag to track if inheritance is detected (though not fully implemented in current traversal).
        self.classes_found = [] # A list to store the names of classes defined in the code.
        self.methods_found = [] # A list to store the names of methods defined within classes.
        self.instances_found = [] # A list to store the names of classes from which instances are created.
        self.details = [] # A list to accumulate detailed findings and observations during analysis.
    
    def analyze_ast(self, ast_node):
        """Analyzes the Abstract Syntax Tree (AST) to determine if the code exhibits OOP characteristics."""
        self.reset() # Ensure the analyzer state is clean before starting a new analysis.
        self._traverse_node(ast_node) # Begin the recursive traversal of the AST from the given root node.
        return self._classify() # Classify the code based on the gathered information and return the results.
    
    def _traverse_node(self, node):
        """Recursively traverses the Abstract Syntax Tree (AST) to identify OOP patterns."""
        if isinstance(node, tuple): # Check if the current 'node' is an AST node (represented as a tuple).
            node_type = node[0] # The first element of the tuple typically indicates the type of AST node.
            
            if node_type == 'program':
                # Traverse through each statement in the top-level program.
                for stmt in node[1]:
                    self._traverse_node(stmt) # Recursively call traverse for each statement.
            
            elif node_type == 'class_def':
                self.has_class = True # Mark that a class definition has been found.
                class_name = node[1] # Extract the name of the defined class.
                self.classes_found.append(class_name) # Add the class name to the list of found classes.
                self.details.append(f"✓ Class defined: {class_name}") # Add a detailed note.
                
                # Traverse through the statements within the class body.
                class_body = node[2]
                for stmt in class_body:
                    self._traverse_node(stmt) # Recursively analyze statements inside the class.
            
            elif node_type == 'method_def':
                method_name = node[1] # Extract the name of the method.
                params = node[2] # Extract the parameters of the method.
                self.methods_found.append(method_name) # Add the method name to the list of found methods.
                
                if method_name == '__init__': # Check if the method is the constructor.
                    self.has_constructor = True # Mark that a constructor has been found.
                    self.details.append(f"✓ Constructor found: {method_name}") # Add a detailed note for the constructor.
                else:
                    self.details.append(f"✓ Method defined: {method_name}") # Add a detailed note for a regular method.
                
                # Check if the method correctly uses 'self' as its first parameter.
                if params and params[0] == 'self':
                    self.details.append(f"   - Method {method_name} uses 'self' correctly") # Add a detailed note for 'self' usage.
                
                # Traverse through the statements within the method body.
                method_body = node[3]
                for stmt in method_body:
                    self._traverse_node(stmt) # Recursively analyze statements inside the method.
            
            elif node_type == 'constructor_call':
                self.has_instance_creation = True # Mark that an instance creation has been found.
                class_name = node[1] # Extract the name of the class being instantiated.
                args = node[2] # Extract the arguments passed to the constructor.
                self.instances_found.append(class_name) # Add the class name to the list of created instances.
                self.details.append(f"✓ Instance created of: {class_name}") # Add a detailed note.
            
            elif node_type == 'function_call':
                # Distinguish between general function calls and potential constructor calls.
                func_name = node[1] # Extract the name of the function/class being called.
                args = node[2] # Extract the arguments passed to the call.
                
                # If the function name matches a defined class name, it's likely a constructor call.
                if func_name in self.classes_found:
                    self.has_instance_creation = True # Mark as instance creation.
                    self.instances_found.append(func_name) # Add to instances found.
                    self.details.append(f"✓ Possible instance created of: {func_name}") # Add a detailed note.
                else:
                    # Otherwise, it's considered a regular function call (non-OOP).
                    self.details.append(f"• Function call: {func_name}()") # Add a detailed note.
            
            elif node_type == 'method_call':
                self.has_method_call = True # Mark that a method call has been found.
                obj_name = node[1] # Extract the object on which the method is called.
                method_name = node[2] # Extract the name of the method being called.
                args = node[3] # Extract the arguments passed to the method.
                self.details.append(f"✓ Method call: {obj_name}.{method_name}()") # Add a detailed note.
            
            elif node_type == 'self_assignment':
                self.has_attribute_access = True # Mark that attribute access/assignment has occurred.
                attr_name = node[1] # Extract the attribute name.
                self.details.append(f"✓ Attribute assignment: self.{attr_name}") # Add a detailed note.
            
            elif node_type == 'self_attr':
                self.has_attribute_access = True # Mark that attribute access has occurred.
                attr_name = node[1] # Extract the attribute name.
                self.details.append(f"✓ Attribute access: self.{attr_name}") # Add a detailed note.
            
            elif node_type == 'attr_access':
                self.has_attribute_access = True # Mark that attribute access has occurred.
                obj_name = node[1] # Extract the object name.
                attr_name = node[2] # Extract the attribute name.
                self.details.append(f"✓ Attribute access: {obj_name}.{attr_name}") # Add a detailed note.
            
            elif node_type == 'attr_assignment':
                self.has_attribute_access = True # Mark that attribute assignment has occurred.
                obj_name = node[1] # Extract the object name.
                attr_name = node[2] # Extract the attribute name.
                self.details.append(f"✓ Attribute assignment: {obj_name}.{attr_name}") # Add a detailed note.
            
            # Recursively analyze other types of nodes that might contain sub-nodes.
            else:
                for item in node[1:]: # Iterate through other elements in the node tuple.
                    if isinstance(item, (list, tuple)): # Check if the item is a list (of statements) or another tuple (sub-node).
                        if isinstance(item, list): # If it's a list, iterate through its elements.
                            for sub_item in item:
                                self._traverse_node(sub_item) # Recursively traverse each sub-item.
                        else: # If it's a tuple, it's a single sub-node.
                            self._traverse_node(item) # Recursively traverse the sub-node.
    
    def _classify(self):
        """Classifies the code's OOP nature based on the detected patterns and assigns a score."""
        oop_score = 0 # Initialize the OOP score.
        reasons = [] # List to collect reasons for the OOP classification.
        
        # Criteria for OOP classification with assigned weights.
        if self.has_class: # If classes are defined.
            oop_score += 3 # Significant OOP characteristic.
            reasons.append("Defines classes")
        
        if self.has_constructor: # If constructors are found.
            oop_score += 2 # Strong OOP characteristic.
            reasons.append("Has constructor (__init__)")
        
        if self.has_instance_creation: # If object instances are created.
            oop_score += 2 # Strong OOP characteristic.
            reasons.append("Creates object instances")
        
        if self.has_method_call: # If methods are called on objects.
            oop_score += 2 # Strong OOP characteristic.
            reasons.append("Calls object methods")
        
        if self.has_attribute_access: # If object attributes are accessed or assigned.
            oop_score += 1 # Basic OOP characteristic.
            reasons.append("Accesses/assigns attributes")
        
        # Determine the final classification and confidence based on the total OOP score.
        if oop_score >= 5:
            classification = "CÓDIGO OOP" # Clearly OOP code.
            confidence = "High"
        elif oop_score >= 3:
            classification = "POSSIBLE OOP" # Might be OOP, but less comprehensive.
            confidence = "Medium"
        elif oop_score >= 1:
            classification = "BASIC OOP ELEMENTS" # Contains some OOP elements, but not fully structured.
            confidence = "Low"
        else:
            classification = "NOT OOP" # Lacks significant OOP characteristics.
            confidence = "High"
        
        return { # Return a dictionary containing the comprehensive analysis results.
            'classification': classification, # The determined OOP category.
            'confidence': confidence, # The confidence level of the classification.
            'score': oop_score, # The numerical OOP score.
            'reasons': reasons, # A list of reasons for the classification.
            'details': self.details, # All detailed findings during the traversal.
            'summary': { # A summary of key OOP elements found.
                'classes': len(self.classes_found), # Count of classes found.
                'methods': len(self.methods_found), # Count of methods found.
                'instances': len(self.instances_found), # Count of instances created.
                'has_constructor': self.has_constructor # Boolean indicating if a constructor was present.
            }
        }