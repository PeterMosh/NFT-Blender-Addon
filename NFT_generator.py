import bpy
import random



#Add props for save needed collections
bpy.types.Scene.texturesCollection = bpy.props.StringProperty()
bpy.types.Scene.lightCollection = bpy.props.StringProperty()

listOfMainColl = []
listOfSecondColl = []
listOfThirdColl = []

Barcodes = [[],[]]
#A[[Init][Collections]]
A[0].append(2)
A[0].append(1)
A[0].append(4)
A[0].append(0)
A[0].append(1)
A[1].append(2)
A[1].append(4)
A[1].append(1)

class OBJECT_OT_NFT_Generator(bpy.types.Operator):
    bl_idname = "object.nft_generator"
    bl_label = "NFT generate"
    
    def execute(self,context):
        scene = context.scene
        
        mytool = scene.NFT_prop
        print("NFT generator started")
        listOfUsed = []
        
        for init in range(1,mytool.quantity+1):
            print("Instance", init)
            ###Create new collections for new NFT instances
            new_collection = bpy.data.collections.new('Init'+str(init))
            bpy.context.scene.collection.children['Instances'].children.link(new_collection)
            # Copy objects from main collections
            for c_name in listOfMainColl:
                for obj in bpy.data.collections[c_name].objects:
                    ###Copy object
                    obj_copy = context.collection.children[c_name].objects[obj.name].copy()
                    context.collection.children['Instances'].children['Init'+str(init)].objects.link(obj_copy)
                listOfUsed.append(c_name)
            # Choose random objects from At Least One collections        
            for c_name in listOfThirdColl:
                if listOfUsed.count(c_name)==0:
                    _rand = random.randint(1,len(bpy.data.collections[c_name].objects))
                    obj_copy = context.collection.children[c_name].objects[_rand-1].copy()
                    context.collection.children['Instances'].children['Init'+str(init)].objects.link(obj_copy)
                    listOfUsed.append(c_name)
            # Choose objects from random collections
            for c_name in listOfSecondColl:
                if listOfUsed.count(c_name)==0:
                    _rand = random.randint(0,len(bpy.data.collections[c_name].objects))
                    if _rand != 0:
                        ###Copy object
                        obj_copy = context.collection.children[c_name].objects[_rand-1].copy()
                        context.collection.children['Instances'].children['Init'+str(init)].objects.link(obj_copy)
                        listOfUsed.append(c_name)
            listOfUsed.clear()
            
                    
        
        print("NFT collection was generate")
        return {'FINISHED'}
 
class VIEW3D_PT_NFT_Panel_One(bpy.types.Panel):
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "NFT Generator"
    bl_label = "NFT Generator"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        #layout.prop_search(context.object, "mychosenObject",  context.scene, "objects", text = "Main Camera")
        layout.prop(scene, "camera", text = "Main Camera")
        layout.operator('object.nft_generator',
            text='Generate NFT',
            icon='GROUP')
        row = layout.row()
        row.label(text='Generator settings')
        mytool = scene.NFT_prop
        col_main = layout.box().column(align=True)
        
        #row = layout.row()
        col_main.prop(mytool, 'quantity', text="Quantity")
        col_main.prop(mytool, 'use_background', text="Use background")
        
        split = col_main.split(factor=0.6)
        col_1 = split.column(align=True)
        col_2 = split.column(align=True)
        
        if mytool.use_background == True:
            #row = col.row(align=True)
            #row.alignment = 'LEFT'
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
            #row = col.row(align=True)
            #row.alignment = 'LEFT'
            col_1.label(text='Light Generate Mode')
            col_2.prop(mytool, 'light_mode', text="")
            if (mytool.light_mode == 'lamp') or (mytool.light_mode == 'both'):
                #row = col.row(align=True)
                #row.alignment = 'LEFT'
                col_1.label(text='Light Collection')
                col_2.prop_search(context.scene, "lightCollection",  context.scene.collection, "children", text = "")     
        '''
        layout.operator('object.nft_generator',
            text='Generate NFT',
            icon='GROUP')
        row = layout.row(align=True)
        row.prop(mytool, "nft_mode", icon='CAMERA_DATA', text="")
        row.prop(mytool, "nft_mode", icon='CONSOLE', text="")
        row.prop(mytool, "nft_mode", icon='ARMATURE_DATA', text="")
        '''
        
        
            #row.prop(mytool, "ch_MainColl", icon='CHECKBOX_HLT')
            #row.label(text=c_name)


class VIEW3D_PT_NFT_Panel_Two(bpy.types.Panel):
    bl_parent_id = "VIEW3D_PT_NFT_Panel_One"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "NFT Generator"
    bl_label = "Working collections"

    
    
    def draw(self, context):
        layout = self.layout    
        
        row = layout.row(align=True)
        row.label(text='First set not-changable collections')
        row = layout.row(align=True)
        row.label(text='Second set randomly collections')
        row = layout.row(align=True)
        row.label(text='Third set collections with at least one object in render')
        
        col = layout.box().column(align=True)
        
        for coll in bpy.data.collections:
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



#MAIN RENDER NOT-CHANGEBLE COLLECTIONS

class OBJECT_OT_NFT_Set_MainColl(bpy.types.Operator):
    bl_idname = "object.set_main_coll"
    bl_label = "NFT generate"
    
    name : bpy.props.StringProperty(
    name = 'Name of Collection ',
    default = ''
    )
    
    def execute(self,context):
        listOfMainColl.append(self.name)
        print("+", self.name)
        print('MainColl ',listOfMainColl)
        return {'FINISHED'} 

class OBJECT_OT_NFT_Reset_MainColl(bpy.types.Operator):
    bl_idname = "object.reset_main_coll"
    bl_label = "NFT generate"
    
    name : bpy.props.StringProperty(
    name = 'Name of Collection ',
    default = ''
    )
    
    def execute(self,context):
        listOfMainColl.remove(self.name)
        print("-", self.name)    
        print('MainColl ',listOfMainColl)
        return {'FINISHED'} 
    
#SECOND RANDOMLY COLLECTIONS

class OBJECT_OT_NFT_Set_SecondColl(bpy.types.Operator):
    bl_idname = "object.set_second_coll"
    bl_label = "NFT generate"
    
    name : bpy.props.StringProperty(
    name = 'Name of Collection ',
    default = ''
    )
    
    def execute(self,context):
        listOfSecondColl.append(self.name)
        print("+", self.name)
        print('SecondColl ',listOfSecondColl)
        return {'FINISHED'} 

class OBJECT_OT_NFT_Reset_SecondColl(bpy.types.Operator):
    bl_idname = "object.reset_second_coll"
    bl_label = "NFT generate"
    
    name : bpy.props.StringProperty(
    name = 'Name of Collection ',
    default = ''
    )
    
    def execute(self,context):
        listOfSecondColl.remove(self.name)
        print("-", self.name)    
        print('SecondColl ',listOfSecondColl)
        return {'FINISHED'} 

#THIRD AT-LEAST-ONE COLLECTIONS

class OBJECT_OT_NFT_Set_ThirdColl(bpy.types.Operator):
    bl_idname = "object.set_third_coll"
    bl_label = "NFT generate"
    
    name : bpy.props.StringProperty(
    name = 'Name of Collection ',
    default = ''
    )
    
    def execute(self,context):
        listOfThirdColl.append(self.name)
        print("+", self.name)
        print('ThirdColl ',listOfThirdColl)
        return {'FINISHED'} 

class OBJECT_OT_NFT_Reset_ThirdColl(bpy.types.Operator):
    bl_idname = "object.reset_third_coll"
    bl_label = "NFT generate"
    
    name : bpy.props.StringProperty(
    name = 'Name of Collection ',
    default = ''
    )
    
    def execute(self,context):
        listOfThirdColl.remove(self.name)
        print("-", self.name)    
        print('ThirdColl ',listOfThirdColl)
        return {'FINISHED'} 
    
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
    quantity : bpy.props.IntProperty(
        name="Number of Instances",
        description="Enter a Number of Instances",
        default = 10,
        min = 1,
        max=1000,
        subtype='UNSIGNED'
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
'''
    ch_MainColl : bpy.props.BoolVectorProperty(
        name = "Enable collection",
        description = "Choose collection for render",
        default = (False,False,False,False,False,False,False,False,False,False),
        size = len(bpy.data.collections),
        get=get_array,
        set=set_array
        )'''



    
classesName = (
    NFT_Settings,
    OBJECT_OT_NFT_Set_MainColl,
    OBJECT_OT_NFT_Reset_MainColl,
    OBJECT_OT_NFT_Set_SecondColl,
    OBJECT_OT_NFT_Reset_SecondColl,
    OBJECT_OT_NFT_Set_ThirdColl,
    OBJECT_OT_NFT_Reset_ThirdColl,
    OBJECT_OT_NFT_Generator,
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
    
if __name__ == "__main__":
    register()
    
