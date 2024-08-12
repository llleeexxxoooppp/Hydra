"""Hydra initialization module."""

bl_info = {
	"name": "Hydra",
	"author": "Ondrej Vlcek",
	"version": (1, 2, 0),
	"blender": (4, 0, 0),
	"location": "View3D > Sidebar > Hydra Tab",
	"description": "Blender addon for hydraulic erosion using textures.",
	"warning": "Requires external dependencies. See Preferences below.",
	"doc_url": "",
	"category": "Mesh",
	"support": "COMMUNITY",
}
"""Blender Addon information."""

_hydra_invalid:bool = False
"""Helper flag. `False` if ModernGL is found."""

def checkModernGL():
	"""Checks :mod:`moderngl` installation and sets the addon invalid flag."""
	global _hydra_invalid
	try:
		import moderngl
	except:
		print("ModernGL not found.")
		_hydra_invalid = True

checkModernGL()

# ------------------------------------------------------------
# Init:
# ------------------------------------------------------------

import bpy
from Hydra import startup

if not _hydra_invalid:
	from Hydra import common, opengl
	from Hydra.addon import get_exports, properties
	_classes = get_exports()
else:
	from Hydra.addon.preferences import get_exports
	_classes = get_exports()

# ------------------------------------------------------------
# Register:
# ------------------------------------------------------------

def register():
	"""Blender Addon register function.
	Creates :data:`common.data` object and calls initialization functions.
	Adds settings properties to `Scene`, `Object` and `Image` Blender classes."""
	from bpy.props import PointerProperty

	global _hydra_invalid
	global _classes

	for cls in _classes:
		bpy.utils.register_class(cls)

	if not _hydra_invalid:
		common.data = common.HydraData()

		try:
			common.data.init_context()
			opengl.init_context()
			startup.invalid = False
		except Exception as e:
			print(f"Failed to initialize OpenGL context: {e}")
			startup.invalid = True

		bpy.types.Object.hydra_erosion = PointerProperty(type=properties.ErosionGroup)
		bpy.types.Image.hydra_erosion = PointerProperty(type=properties.ErosionGroup)

def unregister():
	"""Blender Addon unregister function.
	Removes UI classes, settings properties and releases all resources."""
	global _hydra_invalid
	global _classes
	
	for cls in reversed(_classes):
		bpy.utils.unregister_class(cls)

	if not _hydra_invalid:
		del bpy.types.Object.hydra_erosion
		del bpy.types.Image.hydra_erosion

		common.data.free_all()
		common.data = None

# ------------------------------------------------------------

if __name__ == "__main__":
	register()
