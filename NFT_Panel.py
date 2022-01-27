import bpy
from . import NFT_generator
from . import NFT_properties


class VIEW3D_PT_NFT_Panel_One(bpy.types.Panel):
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "NFT Generator"
    bl_label = "NFT Generator"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, "camera", text = "Main Camera")
        layout.operator('object.nft_generator',
            text='Generate NFT',
            icon='GROUP')
        row = layout.row()
        row.label(text='Generator settings')
        mytool = scene.NFT_prop
        col_main = layout.box().column(align=False)
        col_main.prop(mytool, 'quantity', text="Quantity")
        col_main.prop(mytool, 'degree', text="Degree of Difference", slider=True)
        col_main.prop(mytool, 'use_background', text="Use background")
        split = col_main.split(factor=0.6)
        col_1 = split.column(align=True)
        col_2 = split.column(align=True)
        if mytool.use_background == True:
            col_1.label(text='Backround Render Mode')
            col_2.prop(mytool, 'background_mode', text="",expand =False)
            if mytool.background_mode == 'texs':
                col_1.label(text='Background Collection')
                col_2.prop_search(context.scene, "texturesCollection",  context.scene.collection, "children", text = "") 
        col_main.prop(mytool, 'use_light', text="Use Light")
        split = col_main.split(factor=0.6)
        col_1 = split.column(align=True)
        col_2 = split.column(align=True)
        if mytool.use_light == True:
            col_1.label(text='Light Generate Mode')
            col_2.prop(mytool, 'light_mode', text="")
            if (mytool.light_mode == 'lamp') or (mytool.light_mode == 'both'):
                col_1.label(text='Light Collection')
                col_2.prop_search(context.scene, "lightCollection",  context.scene.collection, "children", text = "")     

class VIEW3D_PT_NFT_Panel_Two(bpy.types.Panel):
    bl_parent_id = "VIEW3D_PT_NFT_Panel_One"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "NFT Generator"
    bl_label = "Working collections"
    
    def draw(self, context):
        layout = self.layout    
        scene = context.scene
        mytool = scene.NFT_prop
        row = layout.row(align=True)
        row.label(text='First set not-changable collections')
        row = layout.row(align=True)
        row.label(text='Second set randomly collections')
        row = layout.row(align=True)
        row.label(text='Third set collections with at least one object in render')
        row = layout.row(align=True)
        row.prop(mytool, "hide_coll", text = "Hide Used Collections")
        col = layout.box().column(align=True)
        for coll in bpy.context.collection.children:
            c_name = coll.name
            row = col.row(align=True)
            row.alignment = 'LEFT'
            _isEnabled = isEnabled(c_name, listOfMainColl)
            #if _isEnabled: row.alert = True
            row.operator("object.reset_main_coll" if _isEnabled else "object.set_main_coll",
            icon='CHECKBOX_HLT' if _isEnabled else 'CHECKBOX_DEHLT',
            text = '',
            emboss=True,).name = c_name
            _isEnabled = isEnabled(c_name, listOfSecondColl)
            #if _isEnabled: row.alert = True
            row.operator("object.reset_second_coll" if _isEnabled else "object.set_second_coll",
            icon='CHECKBOX_HLT' if _isEnabled else 'CHECKBOX_DEHLT',
            text = '',
            emboss=True,).name = c_name
            _isEnabled = isEnabled(c_name, listOfThirdColl)
            #if _isEnabled: row.alert = True
            row.operator("object.reset_third_coll" if _isEnabled else "object.set_third_coll",
            icon='CHECKBOX_HLT' if _isEnabled else 'CHECKBOX_DEHLT',
            text = '',
            emboss=True,).name = c_name
            row.label(text=c_name)

def isEnabled(Name,List):
    for name in List:
        if name == Name: 
            return True
    return False

classesName = (
    VIEW3D_PT_NFT_Panel_One,
    VIEW3D_PT_NFT_Panel_Two
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