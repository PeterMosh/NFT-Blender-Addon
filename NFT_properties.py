import bpy
from . import NFT_generator

class NFT_Settings(bpy.types.PropertyGroup):

    camera_name : bpy.props.EnumProperty(
        name="Camera Name",
        description="Choose Right Camera",
        items=[ ('1', "Mode 1", "one"),
                ('2', "Mode 2", "two"),
                ('3', "Mode 3", "three"),
               ]
        )
    use_background : bpy.props.BoolProperty(
        name="Use Background",
        description="Use random background in generator",
        default = True
        )
    
    background_mode : bpy.props.EnumProperty(
        name="Background Mode",
        description="Generation mode of a background",
        items=[ ('diff', "Diffuse", "Use random diffuse color"),
                ('texs', "Textures", "Use random textures background"),
                ('alpha', "Transparent", "Transparent background with alpha channel"),
               ]
        )
    degree : bpy.props.IntProperty(
        name="Degree",
        description="Degree of difference between units",
        default = 2,
        min = 1,
        max=10,
        subtype='UNSIGNED'
        )
    
    quantity : bpy.props.IntProperty(
        name="Number of Instances",
        description="Enter a Number of Instances",
        default = 10,
        min = 1,
        max=1000,
        subtype='UNSIGNED'
        )
    hide_coll : bpy.props.BoolProperty(
        name="Hide Collections",
        description="Hide Used Collections",
        update= NFT_generator.hide_Collections,
        default = False
        )
    use_light : bpy.props.BoolProperty(
        name="Use Light",
        description="Use random light in generator",
        default = True
        )
    
    light_mode : bpy.props.EnumProperty(
        name="Light Mode",
        description="Generation mode of a light",
        items=[ ('both', "Env+Lamps", "Use random Env+Lamps light"),
                ('env', "Only Env", "Use only env light"),
                ('lamp', "Lamp", "Use random Lamp light"),
               ]
        )
        
classesName = (
    NFT_Settings
)

def register():
    from bpy.utils import register_class
    for cls in classesName:
        register_class(cls)
    bpy.types.Scene.NFT_prop = bpy.props.PointerProperty(type = NFT_Settings)
    
    
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classesName):
        unregister_class(cls)
    del bpy.types.Scene.NFT_prop