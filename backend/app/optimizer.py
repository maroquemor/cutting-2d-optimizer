"""
Optimizador principal con todas las funcionalidades
"""
import numpy as np
import pulp
import time
import json
import hashlib
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io
import base64

@dataclass
class Piece:
    """Representa una pieza a cortar"""
    id: int
    width: float
    height: float
    demand: int
    name: str = ""
    area: float = 0
    
    def __post_init__(self):
        self.area = self.width * self.height
    
    def rotate(self):
        """Devuelve una versión rotada"""
        return Piece(self.id, self.height, self.width, self.demand, self.name + " (R)")

@dataclass
class Material:
    """Representa material de entrada"""
    id: int
    width: float
    height: float
    quantity: int
    name: str = ""
    area: float = 0
    
    def __post_init__(self):
        self.area = self.width * self.height

class CuttingPattern:
    """Patrón de corte individual"""
    def __init__(self, pattern_id: int, material: Material):
        self.id = pattern_id
        self.material = material
        self.pieces = []  # (piece, x, y, rotated)
        self.waste = material.area
        self.piece_counts = {}
        
    def add_piece(self, piece: Piece, x: float, y: float, rotated: bool):
        """Añade una pieza al patrón"""
        piece_width = piece.height if rotated else piece.width
        piece_height = piece.width if rotated else piece.height
        
        # Verificar que quepa
        if (x + piece_width <= self.material.width and 
            y + piece_height <= self.material.height):
            
            self.pieces.append((piece, x, y, rotated))
            self.waste -= piece.area
            
            if piece.id not in self.piece_counts:
                self.piece_counts[piece.id] = 0
            self.piece_counts[piece.id] += 1
            
            return True
        return False

class CuttingOptimizer2D:
    """Optimizador principal"""
    
    def __init__(self):
        self.materials = []
        self.pieces = []
        self.patterns = []
        self.substitution_patterns = []
        self.solution = None
        self.stats = {
            "total_optimizations": 0,
            "avg_waste": 0,
            "avg_time": 0
        }
        
    def add_material(self, width: float, height: float, quantity: int, name: str = ""):
        """Añadir material"""
        material_id = len(self.materials) + 1
        material = Material(material_id, width, height, quantity, name)
        self.materials.append(material)
        return material_id
    
    def add_piece(self, id: int, width: float, height: float, demand: int, name: str = ""):
        """Añadir pieza"""
        piece = Piece(id, width, height, demand, name)
        self.pieces.append(piece)
        return piece
    
    def clear(self):
        """Limpiar datos anteriores"""
        self.materials = []
        self.pieces = []
        self.patterns = []
        self.substitution_patterns = []
        self.solution = None
    
    def generate_patterns(self, max_patterns: int = 1000):
        """Generar patrones de corte"""
        # Implementación simplificada
        # En producción, usar algoritmo completo del artículo
        
        patterns = []
        pattern_id = 0
        
        for material in self.materials:
            # Ordenar piezas por área descendente
            sorted_pieces = sorted(self.pieces, key=lambda p: p.area, reverse=True)
            
            # Generar algunos patrones básicos
            # (Para producción, implementar algoritmo completo)
            
            # Patrón 1: Sin cortar (todo desperdicio)
            pattern = CuttingPattern(pattern_id, material)
            patterns.append(pattern)
            pattern_id += 1
            
            # Patrón 2: Intentar colocar la pieza más grande
            if sorted_pieces:
                largest_piece = sorted_pieces[0]
                pattern = CuttingPattern(pattern_id, material)
                
                # Intentar sin rotar
                if largest_piece.width <= material.width and largest_piece.height <= material.height:
                    pattern.add_piece(largest_piece, 0, 0, False)
                    patterns.append(pattern)
                    pattern_id += 1
                
                # Intentar rotado
                pattern = CuttingPattern(pattern_id, material)
                if largest_piece.height <= material.width and largest_piece.width <= material.height:
                    pattern.add_piece(largest_piece, 0, 0, True)
                    patterns.append(pattern)
                    pattern_id += 1
            
            # Limitar número de patrones
            if pattern_id >= max_patterns:
                break
        
        self.patterns = patterns
        return len(patterns)
    
    def solve(self) -> Dict:
        """Resolver problema de optimización"""
        start_time = time.time()
        
        # Generar patrones
        self.generate_patterns()
        
        # Crear problema de optimización
        prob = pulp.LpProblem("Cutting2D", pulp.LpMinimize)
        
        # Variables: cuántas veces usar cada patrón
        pattern_vars = {}
        for i, pattern in enumerate(self.patterns):
            pattern_vars[i] = pulp.LpVariable(f"pattern_{i}", lowBound=0, cat='Integer')
        
        # Función objetivo: minimizar desperdicio
        waste_terms = [pattern.waste * pattern_vars[i] for i, pattern in enumerate(self.patterns)]
        prob += pulp.lpSum(waste_terms)
        
        # Restricciones: satisfacer demanda
        for piece in self.pieces:
            demand_terms = []
            for i, pattern in enumerate(self.patterns):
                count = pattern.piece_counts.get(piece.id, 0)
                if count > 0:
                    demand_terms.append(count * pattern_vars[i])
            
            if demand_terms:
                prob += pulp.lpSum(demand_terms) >= piece.demand
        
        # Restricciones: disponibilidad de material
        for material in self.materials:
            material_terms = []
            for i, pattern in enumerate(self.patterns):
                if pattern.material.id == material.id:
                    material_terms.append(pattern_vars[i])
            
            if material_terms:
                prob += pulp.lpSum(material_terms) <= material.quantity
        
        # Resolver
        solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=300)
        prob.solve(solver)
        
        solve_time = time.time() - start_time
        
        # Recopilar solución
        solution = {
            "id": hashlib.md5(str(time.time()).encode()).hexdigest()[:8],
            "status": pulp.LpStatus[prob.status],
            "waste": pulp.value(prob.objective),
            "time": solve_time,
            "patterns_used": 0,
            "instructions": [],
            "summary": {}
        }
        
        # Contar patrones usados
        used_patterns = []
        for i, var in pattern_vars.items():
            if pulp.value(var) and pulp.value(var) > 0.5:
                count = int(round(pulp.value(var)))
                solution["patterns_used"] += count
                
                pattern_info = {
                    "pattern_id": i,
                    "count": count,
                    "material": self.patterns[i].material.name,
                    "waste_per_unit": self.patterns[i].waste
                }
                used_patterns.append(pattern_info)
                
                # Generar instrucciones
                pattern = self.patterns[i]
                for piece, x, y, rotated in pattern.pieces:
                    instruction = f"Cortar {piece.name} en ({x:.1f}, {y:.1f})"
                    if rotated:
                        instruction += " (rotado)"
                    solution["instructions"].append(instruction)
        
        # Actualizar estadísticas
        self.stats["total_optimizations"] += 1
        total_waste = self.stats["avg_waste"] * (self.stats["total_optimizations"] - 1)
        total_waste += solution["waste"]
        self.stats["avg_waste"] = total_waste / self.stats["total_optimizations"]
        
        total_time = self.stats["avg_time"] * (self.stats["total_optimizations"] - 1)
        total_time += solve_time
        self.stats["avg_time"] = total_time / self.stats["total_optimizations"]
        
        # Crear resumen
        total_material_area = sum(m.area * m.quantity for m in self.materials)
        total_pieces_area = sum(p.area * p.demand for p in self.pieces)
        utilization = (total_pieces_area / total_material_area) * 100 if total_material_area > 0 else 0
        
        solution["summary"] = {
            "total_material_area": total_material_area,
            "total_pieces_area": total_pieces_area,
            "material_utilization": utilization,
            "waste_percentage": 100 - utilization,
            "used_patterns": used_patterns,
            "timestamp": datetime.now().isoformat()
        }
        
        self.solution = solution
        return solution
    
    def get_stats(self):
        """Obtener estadísticas del optimizador"""
        return self.stats
    
    def generate_visualization(self, pattern_id: int = 0):
        """Generar visualización de un patrón"""
        if not self.patterns or pattern_id >= len(self.patterns):
            return None
        
        pattern = self.patterns[pattern_id]
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Dibujar material
        ax.add_patch(patches.Rectangle(
            (0, 0), pattern.material.width, pattern.material.height,
            edgecolor='black', facecolor='lightblue', alpha=0.3,
            label=f'Material: {pattern.material.width}x{pattern.material.height}'
        ))
        
        # Dibujar piezas
        colors = plt.cm.tab10(np.linspace(0, 1, len(self.pieces)))
        for piece, x, y, rotated in pattern.pieces:
            width = piece.height if rotated else piece.width
            height = piece.width if rotated else piece.height
            
            color_idx = next((i for i, p in enumerate(self.pieces) if p.id == piece.id), 0)
            
            ax.add_patch(patches.Rectangle(
                (x, y), width, height,
                edgecolor='black', facecolor=colors[color_idx], alpha=0.7,
                label=f'{piece.name} ({width}x{height})'
            ))
            
            # Añadir texto
            ax.text(x + width/2, y + height/2, piece.name,
                   ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Configurar gráfico
        ax.set_xlim(0, pattern.material.width * 1.1)
        ax.set_ylim(0, pattern.material.height * 1.1)
        ax.set_aspect('equal')
        ax.set_xlabel('Ancho (cm)')
        ax.set_ylabel('Alto (cm)')
        ax.set_title(f'Patrón de Corte - {pattern.material.name}')
        ax.grid(True, alpha=0.3)
        
        # Guardar en buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        
        # Convertir a base64
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"