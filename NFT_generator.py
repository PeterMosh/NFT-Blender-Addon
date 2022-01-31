import bpy
import random

#Add props for save needed collections
bpy.types.Scene.texturesCollection = bpy.props.StringProperty()
bpy.types.Scene.lightCollection = bpy.props.StringProperty()

listOfMainColl = []
listOfSecondColl = []
listOfThirdColl = []

class OBJECT_OT_NFT_Generator(bpy.types.Operator):
    bl_idname = "object.nft_generator"
    bl_label = "NFT generate"
    
    def execute(self,context):
        scene = context.scene

        Barcodes = [[]]
        mytool = scene.NFT_prop
        print("NFT generator started")
        listOfUsed = []
        limit = mytool.degree
        for c_name in listOfThirdColl:
            Barcodes[0].append(c_name)
        for c_name in listOfSecondColl:
            if Barcodes[0].count(c_name)==0:
                Barcodes[0].append(c_name)
        
        for init in range(1,mytool.quantity+1):
            print("Instance", init)
            Barcodes.append([])
            repeatRand = True
            ###Create new collections for new NFT instances
            new_collection = bpy.data.collections.new('Init_'+str(init))
            bpy.context.scene.collection.children['Instances'].children.link(new_collection)
            # Copy objects from main collections
            while repeatRand:    
                repeatRand = False
                print("Generate BarCodes...")
                for c_name in listOfMainColl:
                    listOfUsed.append(c_name)
                # Choose random objects from At Least One collections        
                for c_name in listOfThirdColl:
                    if listOfUsed.count(c_name)==0:
                        _rand = random.randint(1,len(bpy.data.collections[c_name].objects))
                        listOfUsed.append(c_name)
                        Barcodes[init].append(_rand) #Add number of object inside the collection
                # Choose objects from random collections
                for c_name in listOfSecondColl:
                    if listOfUsed.count(c_name)==0:
                        _rand = random.randint(0,len(bpy.data.collections[c_name].objects))
                        listOfUsed.append(c_name)
                        Barcodes[init].append(_rand)
                
                if init != 1: 
                    print("Checking BarCodes...")
                    for r in range(1,init):
                        mismatch = 0 
                        for c in range(0,len(Barcodes[0])):
                            if Barcodes[r][c] != Barcodes[init][c]: 
                                mismatch += 1
                                
                                if mismatch > limit: 
                                    repeatRand = False
                                    break
                        #Check for double BarCode
                        if mismatch <= limit:
                            repeatRand = True
                            Barcodes[init].clear()
                            print('Match Unit', init)
                            break
                
                
                if repeatRand == False:
                    
                    #Add objs inside new collection    
                    for c_name in listOfMainColl:
                        for obj in bpy.data.collections[c_name].objects:
                            ###Copy main object
                            obj_copy = context.collection.children[c_name].objects[obj.name].copy()
                            context.collection.children['Instances'].children['Init_'+str(init)].objects.link(obj_copy)
                    # Choose random objects
                    for C, c_name in enumerate(Barcodes[0],0):
                        if Barcodes[init][C]!=0:
                            obj_copy = context.collection.children[c_name].objects[Barcodes[init][C]-1].copy()
                            context.collection.children['Instances'].children['Init_'+str(init)].objects.link(obj_copy)
                    for obj in bpy.data.collections['Init_'+str(init)].objects:
                        #Pretarget frame
                        obj.hide_viewport = True
                        obj.keyframe_insert('hide_viewport', frame=init-1)
                        obj.hide_render = True
                        obj.keyframe_insert('hide_render', frame=init-1)
                        #Target frame
                        obj.hide_viewport = False
                        obj.keyframe_insert('hide_viewport', frame=init)
                        obj.hide_render = False
                        obj.keyframe_insert('hide_render', frame=init)
                        #Next frame
                        obj.hide_viewport = True
                        obj.keyframe_insert('hide_viewport', frame=init+1)
                        obj.hide_render = True
                        obj.keyframe_insert('hide_render', frame=init+1)
                listOfUsed.clear()            
                
            print(Barcodes)
                    
        Barcodes.clear()
        print("NFT collection was generate")
        return {'FINISHED'}
#Hide used collections
def hide_Collections(self, context):
    scene = context.scene
    mytool = scene.NFT_prop
    if mytool.hide_coll == True:
        for c_name in listOfMainColl:
            bpy.data.collections[c_name].hide_viewport = True
            bpy.data.collections[c_name].hide_render = True
        for c_name in listOfSecondColl:
            bpy.data.collections[c_name].hide_viewport = True
            bpy.data.collections[c_name].hide_render = True
        for c_name in listOfThirdColl:
            bpy.data.collections[c_name].hide_viewport = True
            bpy.data.collections[c_name].hide_render = True
            
    if mytool.hide_coll == False:
        for c_name in listOfMainColl:
            bpy.data.collections[c_name].hide_viewport = False
            bpy.data.collections[c_name].hide_render = False
        for c_name in listOfSecondColl:
            bpy.data.collections[c_name].hide_viewport = False
            bpy.data.collections[c_name].hide_render = False
        for c_name in listOfThirdColl:
            bpy.data.collections[c_name].hide_viewport = False
            bpy.data.collections[c_name].hide_render = False
    
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
    

    
classesName = (
    OBJECT_OT_NFT_Set_MainColl,
    OBJECT_OT_NFT_Reset_MainColl,
    OBJECT_OT_NFT_Set_SecondColl,
    OBJECT_OT_NFT_Reset_SecondColl,
    OBJECT_OT_NFT_Set_ThirdColl,
    OBJECT_OT_NFT_Reset_ThirdColl,
    OBJECT_OT_NFT_Generator,
)

def register():
    from bpy.utils import register_class
    for cls in classesName:
        register_class(cls)
    
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classesName):
        unregister_class(cls)