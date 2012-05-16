bl_info = {
    "name": "HydraFPS Level",
    "author": "Willi Schinmeyer",
    "version": (0, 0, 1),
    "blender": (2, 6, 3),
    "location": "File > Export > HydraFPW level",
    "description": "Export HydraFPS level file",
    "category": "Import-Export"}

import bpy

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
                if key in {"_RNA_UI", "cycles_visibility"}:
                    pass #ignore those
                elif key == "classname":
                    self.classname = value;
                else:
                    self.properties[key] = value
        if not self.classname:
            self.reportError("Entity object \"{}\" has no classname property! (This error should be impossible since it should be treated as geometry then!)".format(obj.name))
            return False
        # get transformation matrix
        self.properties["matrix_world"] = matrixFormat.format(mat = obj.matrix_world)
        return True
    
    def saveToFile(self, file):
        file.write(entityStart)
        file.write(propertyFormat.format("classname", self.classname);
        for key, value in self.properties.items():
            file.write(propertyFormat.format(key, value))
        file.write(entityEnd)
        return True

class LevelExporter:
    def __init__(self, errorFunc):
        self.reportError = errorFunc
        
    def export(self, filename):
        if not self.readObjects():
            return
        
    def readObjects(self)
        self.entities = []
        # go through all objects
        for obj in bpy.data.objects:
            # objects with a custom property "classname" are entities
            if "classname" in obj:
                if not self.readEntity(obj):
                    return
            # other mesh entities are geometry
            elif obj.type == 'MESH':
                if not self.readGeometry(obj):
                    return
    
    def readEntity(self, obj):
        ent = Entity(self.reportError)
        if not ent.loadFromObject(obj):
            return False;
        self.entities.append(ent)
        return True
        
    def readGeometry(self, obj):
        mesh = obj.data
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
        
        exporter = LevelExporter(report_error)
        exporter.export(filepath)
        
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
