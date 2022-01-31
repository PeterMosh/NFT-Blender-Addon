import sys

bl_info = {
    'name': 'NFT Generator',
    'author': "Petr Moshkantsev",
    'category': 'All',
    'version': (0, 0, 2),
    'blender': (2, 93, 7)
}

debug = 0 # 0 (ON) or 1 (OFF)
 
modules = ["NFT_Generator", "NFT_Panel", "NFT_properties"]
 
for mod in modules:
    try:
        exec("from . import {mod}".format(mod=mod))
    except Exception as e:
        print(e)
 
def register():
    
    import importlib
    for mod in modules:
        try:
            if debug:
                exec("importlib.reload({mod})".format(mod=mod))
            exec("{mod}.register()".format(mod=mod))
        except Exception as e:
            print(e)
 
def unregister():
    for mod in modules:
        try:
            exec("{mod}.unregister()".format(mod=mod))
        except Exception as e:
            print(e)
            
if __name__ == "__main__":
    register()