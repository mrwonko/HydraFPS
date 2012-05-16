bl_info = {
    "name": "HydraFPS Level",
    "author": "Willi Schinmeyer",
    "version": (0, 0, 1),
    "blender": (2, 6, 3),
    "location": "File > Export > HydraFPW level",
    "description": "Export HydraFPS level file. Caution: Faces with no material won't be exported!",
    "category": "Import-Export"}

import bpy

VERSION = 0
IDENT = "HFPSLVL\0"

matrixFormat = "[[{mat[0][0]}, {mat[0][1]}, {mat[0][2]}, {mat[0][3]}], "
matrixFormat += "[{mat[1][0]}, {mat[1][1]}, {mat[1][2]}, {mat[1][3]}], "
matrixFormat += "[{mat[2][0]}, {mat[2][1]}, {mat[2][2]}, {mat[2][3]}], "
matrixFormat += "[{mat[3][0]}, {mat[3][1]}, {mat[3][2]}, {mat[3][3]}]]"

entityStart = "{\n"
propertyFormat = "\t\"{}\" \"{}\"\n"
entityEnd = "}\n"

class Entity:
    def __init__(self, errorFunc):
        self.properties = {}
        self.classname = False
        self.reportError = errorFunc
        
    def loadFromObject(self, obj):
        # read user properties
        for key, value in obj.items():
            key = key.lower()
            try:
                value = str(value) #this unfortunately pretty much always works, hard to filter invalid values this way
                if key in {"_rna_ui", "cycles_visibility"}:
                    pass #ignore those
                elif key == "classname":
                    self.classname = value;
                else:
                    self.properties[key] = value
            except:
                pass
        if not self.classname:
            self.reportError("Entity object \"{}\" has no classname property! (This error should be impossible since it should be treated as geometry then!)".format(obj.name))
            return False
        # get transformation matrix
        self.properties["matrix_world"] = matrixFormat.format(mat = obj.matrix_world)
        return True
    
    def saveToFile(self, file):
        file.write(entityStart.encode())
        file.write(propertyFormat.format("classname", self.classname).encode())
        for key, value in self.properties.items():
            file.write(propertyFormat.format(key, value).encode())
        file.write(entityEnd.encode())
        return True

class LevelExporter:
    def __init__(self, errorFunc):
        self.reportError = errorFunc
        
    def export(self, filename):
        # We work on layer 0
        prevLayer0State = bpy.context.scene.layers[0]
        # read objects
        if not self.readObjects():
            bpy.context.scene.layers[0] = prevLayer0State
            return
        bpy.context.scene.layers[0] = prevLayer0State
        # save to file
        with open(filename, "wb") as file:
            self.saveToFile(file)
            file.close()
            return
        self.reportError("Could not open \"{}\" for writing!".format(filename))
        
    def readObjects(self):
        self.entities = []
        self.geometryObjectsByMaterial = {}
        # go through all objects
        for obj in bpy.data.objects:
            # objects with a custom property "classname" are entities
            if "classname" in obj:
                if not self.readEntity(obj):
                    return False
            # other mesh entities are geometry
            elif obj.type == 'MESH':
                if not self.readGeometry(obj):
                    return False
        return True
    
    def readEntity(self, obj):
        ent = Entity(self.reportError)
        if not ent.loadFromObject(obj):
            return False;
        self.entities.append(ent)
        return True
        
    def readGeometry(self, obj):
        if bpy.context.mode != 'OBJECT':
            self.reportError("Must be in Object Mode to export!")
            return False
            
        bpy.ops.object.select_all(action='DESELECT')
        
        # select object, making sure its visible and on the correct layer
        objHidden = obj.hide
        objLayer0 = obj.layers[0]
        obj.hide = False
        obj.layers[0] = True
        obj.select = True
        
        # create duplicate (works by selection)
        bpy.ops.object.duplicate()
        dupObj = bpy.context.active_object
        
        # restore previous object state
        obj.hide = objHidden
        obj.layers[0] = objLayer0
        
        # enter edit mode
        bpy.ops.object.editmode_toggle()
        mesh = obj.data
        
        # Enter face selection mode
        #todo
        
        # triangulate
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris()
        bpy.ops.mesh.select_all(action='DESELECT')
        
        # we're about to create lots of objects - we won't be able to tell which unless we remember the previous ones.
        prevObjs = bpy.objects[:]
        
        # go through material slots
        # but caution: materials may be used multiple times!
        processedMaterials = []
        for materialIndex, material in enumerate(obj.material_slots):
            # only process each material once (may be in multiple slots)
            if material not in processedMaterials:
                # select all slots with this material
                for materialIndex2 in range(materialIndex, len(obj.material_slots)):
                    material2 = obj.material_slots[materialIndex2]
                    if material2 == material:
                        obj.active_material_index = materialIndex
                        bpy.ops.object.material_slot_select()
                # separate these
                bpy.ops.mesh.separate()
                
                processedMaterials.append(material)
        
        newObjs = bpy.objects[:]
        for oldObj in prevObjs:
            newObjs.remove(oldObj)
        del prevObjs
        
        # delete object
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.delete()
        
        # process new material separated objects (newObjs)
        #todo
        
        return True
    
    def saveToFile(self, file):
        # save header
        file.write(IDENT.encode())
        import struct
        file.write(struct.pack("I", VERSION)) #todo: add numsurfaces (and more?)
        # save surfaces
        #todo
        # save entities
        for ent in self.entities:
            if not ent.saveToFile(file):
                return False
        return True

class HFPSLVLExport(bpy.types.Operator):
    """Export to the HydraFPS Level file format"""

    bl_idname = "export_scene.hfps_lvl"
    bl_label = "Export HydraFPS Level"

    filepath = bpy.props.StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        #Append .hlvl
        filepath = bpy.path.ensure_ext(self.filepath, ".hlvl")
        
        def report_error(msg):
            self.report({'ERROR'}, msg)
        
        #ctx = bpy.context
        #bpy.context = context
        exporter = LevelExporter(report_error)
        exporter.export(filepath)
        #bpy.context = ctx
        
        return {"FINISHED"}

    def invoke(self, context, event):
        if not self.filepath:
            self.filepath = bpy.path.ensure_ext(bpy.data.filepath, ".hlvl")
        WindowManager = context.window_manager
        WindowManager.fileselect_add(self)
        return {"RUNNING_MODAL"}

def menu_func(self, context):
    self.layout.operator(HFPSLVLExport.bl_idname, text="HydraFPS Level")


def register():
    bpy.utils.register_module(__name__)

    bpy.types.INFO_MT_file_export.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.INFO_MT_file_export.remove(menu_func)


if __name__ == "__main__":
    register()
