import bpy
import math

class WoodGenerator:
    def __init__(self, clear_scene=True):
        if clear_scene:
            self.clear_scene()
        
    def clear_scene(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
    def create_wood_material(self, name):
        material = bpy.data.materials.new(name=name)
        material.use_nodes = True
        nodes = material.node_tree.nodes
        nodes.clear()
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.inputs['Base Color'].default_value = (0.396, 0.262, 0.129, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.8
        
        output = nodes.new('ShaderNodeOutputMaterial')
        material.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        return material
        
    def create_wood_plank(self, dimensions, location):
        width, depth, height = dimensions
        bpy.ops.mesh.primitive_cube_add(size=1, location=location, scale=(width, depth, height))
        plank = bpy.context.active_object
        plank.name = f"WoodPlank_{width}x{depth}x{height}"
        return plank
        
    def generate_stack(self, dimensions, count, spacing=0.05):
        width, depth, height = dimensions
        material = self.create_wood_material("WoodMaterial")
        
        planks = []
        rows = int(math.sqrt(count))
        cols = (count + rows - 1) // rows
        
        for i in range(count):
            row = i // cols
            col = i % cols
            
            x_offset = col * (width + spacing)
            y_offset = row * (depth + spacing)
            z_offset = height / 2
            
            location = (x_offset, y_offset, z_offset)
            plank = self.create_wood_plank(dimensions, location)
            plank.data.materials.append(material)
            planks.append(plank)
            
        return planks

def parse_dimension_string(dimension_string):
    dimensions = []
    for part in dimension_string.split('x'):
        if part.endswith('cm'):
            dimensions.append(float(part[:-2]) / 100)
        elif part.endswith('m'):
            dimensions.append(float(part[:-1]))
        else:
            dimensions.append(float(part) / 100)
    return tuple(dimensions)

class WOOD_PT_generator_panel(bpy.types.Panel):
    bl_label = "Wood Generator"
    bl_idname = "WOOD_PT_generator_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Wood Tools"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene, "wood_dimensions")
        layout.prop(scene, "wood_count")
        layout.prop(scene, "wood_spacing")
        layout.operator("object.generate_wood_operator")

class WOOD_OT_generate_wood(bpy.types.Operator):
    bl_idname = "object.generate_wood_operator"
    bl_label = "Generate Wood"
    
    def execute(self, context):
        scene = context.scene
        try:
            dimensions = parse_dimension_string(scene.wood_dimensions)
            if len(dimensions) != 3:
                self.report({'ERROR'}, "Exactly three dimensions required")
                return {'CANCELLED'}
                
            generator = WoodGenerator(clear_scene=False)
            generator.generate_stack(dimensions, scene.wood_count, scene.wood_spacing)
            
            self.report({'INFO'}, f"Generated {scene.wood_count} wood planks")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

def register():
    bpy.types.Scene.wood_dimensions = bpy.props.StringProperty(
        name="Dimensions",
        description="Wood dimensions in WxDxL format (e.g., 5cmx5cmx200cm)",
        default="5cmx5cmx200cm"
    )
    bpy.types.Scene.wood_count = bpy.props.IntProperty(
        name="Count",
        description="Number of wood planks to generate",
        default=10,
        min=1,
        max=1000
    )
    bpy.types.Scene.wood_spacing = bpy.props.FloatProperty(
        name="Spacing",
        description="Spacing between planks in meters",
        default=0.05,
        min=0.01,
        max=1.0
    )
    bpy.utils.register_class(WOOD_PT_generator_panel)
    bpy.utils.register_class(WOOD_OT_generate_wood)

def unregister():
    bpy.utils.unregister_class(WOOD_PT_generator_panel)
    bpy.utils.unregister_class(WOOD_OT_generate_wood)
    del bpy.types.Scene.wood_dimensions
    del bpy.types.Scene.wood_count
    del bpy.types.Scene.wood_spacing

if __name__ == "__main__":
    register()