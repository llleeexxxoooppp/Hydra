"""Module specifying settings for Hydra."""

import bpy
from bpy.props import (
	BoolProperty,
	FloatProperty,
	IntProperty,
	IntVectorProperty,
	StringProperty,
	EnumProperty)

from Hydra import common

#-------------------------------------------- Settings

class ErosionGroup(bpy.types.PropertyGroup):
	"""Individual settings for objects and images."""
	height_scale: FloatProperty(
		name="Height scale", default=1
	)
	"""Height scaling factor after normalization. Value of 1 means same scale as heightmap width."""

	scale_ratio: FloatProperty(
		name="Scale ratio", default=1
	)
	"""Ratio of Y to X scales for non-uniform images."""

	org_scale: FloatProperty(
		name="Original height scaling", default=1
	)
	"""Original height scaling to use with modifiers, which affect it."""

	org_width: FloatProperty(
		name="Original width", default=1,
	)
	"""Original object width for correct angle calculations."""

	img_size: IntVectorProperty(
		default=(1024,1024),
		name="Heightmap size",
		min=32,
		max=4096,
		description="To erode objects, they are first converted into heightmaps. This property defines the heightmap resolution. Once erosion occurs this resolution is set and can only be reset by clearing cached heightmaps",
		size=2
	)

	tiling: EnumProperty(
		name="Tiling",
		default="none",
		description="Tiling mode for the texture",
		items=(
			("none", "None", "No tiling", 0),
			("x", "X", "Tiling along the X direction (image width)", 1),
			("y", "Y", "Tiling along the Y direction (image height)", 2),
			("xy", "XY", "Tiling in both directions", 3),
		),
	)

	advanced: BoolProperty(
		default=False,
		name="Advanced",
		description="Show advanced settings"
	)
	
	#------------------------- Erosion
	
	erosion_solver: EnumProperty(
		default="particle",
		items=(
			("particle", "Particle", "Creates long meandering paths. Stable for most terrains", 0),
			("pipe", "Pipe", "Smoother large-scale erosion. Partially unstable", 1),
		),
		name="Erosion solver",
		description="Solver type for erosion"
	)

	erosion_subres: FloatProperty(
		default=50.0,
		min=10, max=200.0,
		soft_max=100.0,
		subtype="PERCENTAGE",
		name="Simulation resolution",
		description="Percentage of heightmap resolution to simulate at. Lower resolution creates larger features and speeds up simulation time. Simulating at 512x512 is a good starting point for erosion"
	)

	erosion_hardness_src: StringProperty(
		name="Hardness",
		description="Terrain hardness texture. Pure white won't be eroded at all, pure black will erode the most"
	)

	erosion_invert_hardness: BoolProperty(
		default=False,
		name="Invert hardness",
		description="Inverts the hardness map. Black will be eroded the least, white the most"
	)
	
	#------------------------- Particle

	part_iter_num: IntProperty(
		default=50,
		min=1, max=1000,
		name="Iterations",
		description="Number of simulation iterations"
	)
	
	part_lifetime: IntProperty(
		default=25,
		min=1, max=300,
		soft_max=100,
		name="Lifetime",
		description="Number of steps a particle will take per iteration"
	)
	
	part_acceleration: FloatProperty(
		default=50.0,
		min=1.0, soft_max=100.0, max=500.0,
		subtype="PERCENTAGE",
		name="Acceleration",
		description="Influence of the surface on motion"
	)

	part_lateral_acceleration: FloatProperty(
		default=100.0,
		min=1.0, soft_max=200.0, max=300.0,
		subtype="PERCENTAGE",
		name="Lateral Acceleration",
		description="Influence of the surface on side to side acceleration"
	)
	
	part_drag: FloatProperty(
		default=25.0,
		min=0.0, max=99.0,
		subtype="PERCENTAGE",
		name="Drag",
		description="Drag applied to the particle. Lower values lead to larger streaks"
	)

	part_deposition: FloatProperty(
		default=75.0,
		min=0.0, max=100.0,
		subtype="PERCENTAGE",
		name="Deposition",
		description="Defines how fast sediment can deposit. A value of 0 means only erosion occurs"
	)
	
	part_fineness: FloatProperty(
		default=10.0,
		min=1.0, soft_max=100.0, max=200.0,
		subtype="PERCENTAGE",
		name="Smoothness",
		description="Higher values smooth erosion, but may create unwanted patterns"
	)
	
	part_capacity: FloatProperty(
		default=25.0,
		min=1.0, soft_max=100.0, max=200.0,
		subtype="PERCENTAGE",
		name="Capacity",
		description="Sediment capacity of the particle. High capacity leads to deeper grooves"
	)
	
	part_max_change: FloatProperty(
		default=100.0,
		min=0.1, max=100.0,
		subtype="PERCENTAGE",
		name="Max change",
		description="Maximum amount of material that can be added or removed at once. Lower values prevent large spikes and help with high capacity simulations"
	)

	#------------------------- Mei

	mei_iter_num: IntProperty(
		default=100,
		min=1, max=1000,
		name="Iterations",
		description="Number of iterations, each over the entire image"
	)

	mei_rain: FloatProperty(
		default=25,
		min=1, max=100.0,
		subtype="PERCENTAGE",
		name="Rain",
		description="Amount of rain per iteration"
	)

	mei_capacity: FloatProperty(
		default=50,
		min=1, max=100.0,
		subtype="PERCENTAGE",
		name="Capacity",
		description="Erosion capacity of water per cell"
	)

	mei_hardness: FloatProperty(
		default=50,
		min=0, soft_max=100, max=400,
		subtype="PERCENTAGE",
		name="Hardness",
		description="Hardness of the terrain. Higher values lead to less erosion. Also a multiplier for the hardness map"
	)

	mei_water_src: StringProperty(
		name="Water",
		description="Water source image texture. Pure white will spawn the most water, black will spawn none"
	)

	mei_invert_water: BoolProperty(
		default=False,
		name="Invert water",
		description="Inverts the water map. White will spawn no water, black will spawn the most"
	)
	
	mei_randomize: BoolProperty(
		default=False,
		name="Randomize",
		description="Spawns random drops of water on the terrain. This effectively decreases the amount of water spawned"
	)

	mei_max_depth: FloatProperty(
		default=10,
		min=0.01, max=100,
		name="Max Depth",
		description="Maximum depth of at which erosion can occur. Can help with very deep bodies of water"
	)

	#------------------------- Thermal
	
	thermal_iter_num: IntProperty(
		default=100,
		min=1, max=3000, soft_max=1000,
		name="Iterations",
		description="Number of iterations of thermal erosion"
	)

	thermal_angle: FloatProperty(
		default=1.047198,
		min=0.174533, max=1.48353,
		subtype="ANGLE",
		name="Angle",
		description="Maximum angle the surface can have in degrees"
	)

	thermal_strength: FloatProperty(
		default=100,
		min=0, max=200, soft_max=100,
		subtype="PERCENTAGE",
		name="Strength",
		description="Strength of each iteration"
	)

	thermal_solver: EnumProperty(
		default="both",
		items=(
			("both", "All", "Move material both in XY and diagonal directions", 0),
			("cardinal", "Cardinal", "Only move material in XY directions", 1),
			("diagonal", "Diagonal", "Only move material on diagonals", 2),
		),
		name="Direction",
		description="Solver neighborhood type"
	)

	thermal_stride: IntProperty(
		default=1,
		min=1, max=10,
		name="Stride",
		description="Stride size in pixels. Higher values make low angle erosion faster"
	)

	thermal_stride_grad: BoolProperty(
		default=False,
		name="Gradual stride",
		description="Periodically halves stride for smoother erosion"
	)

	#------------------------- Snow

	snow_add: FloatProperty(
		default=50,
		min=1, max=100.0,
		subtype="PERCENTAGE",
		name="Snow amount",
		description="Relative amount of snow added to the object"
	)

	snow_iter_num: IntProperty(
		default=500,
		min=1, max=3000, soft_max=1000,
		name="Iterations",
		description="Number of iterations of snow simulation"
	)

	snow_angle: FloatProperty(
		default=0.663225,
		min=0.174533, max=1.48353,
		subtype="ANGLE",
		name="Angle",
		description="Maximum surface angle the snow can have in degrees"
	)

	snow_output: EnumProperty(
		default="both",
		items=(
			("both", "All", "Generate both a texture and a displacement", 0),
			("texture", "Texture", "Only generate a snow texture", 1),
			("displacement", "Displacement", "Only displace the surface", 2),
		),
		name="Output type",
		description="Snow output type"
	)

	#------------------------- Extras
	
	extras_type: EnumProperty(
		default="color",
		items=(
			("flow", "Flow", "Creates a map of flow concentration", 0),
			("color", "Color", "Transports color in the direction of water flow", 1),
		),
		name="Type",
		description="Type of texture to generate"
	)

	flow_iter_num: IntProperty(
		default=200,
		min=1, max=1000, soft_max=500,
		name="Iterations",
		description="Number of iterations of flow simulation"
	)

	flow_brightness: FloatProperty(
		default=50,
		min=1.0, max=100,
		subtype="PERCENTAGE",
		name="Flow contrast",
		description="Higher values lead to brighter flow maps and thicker streaks"
	)

	color_solver: EnumProperty(
		default="particle",
		items=(
			("particle", "Particle", "Creates sharper paths of color", 0),
			("pipe", "Pipe", "Creates even blotches of color", 1)
		),
		name="Solver",
		description="Solver type for color transport"
	)

	color_iter_num: IntProperty(
		default=100,
		min=1, max=500, soft_max=1000,
		name="Iterations",
		description="Number of iterations of color simulation"
	)

	color_mixing: FloatProperty(
		default=50,
		min=1, max=100.0,
		subtype="PERCENTAGE",
		name="Color strength",
		description="Defines how strongly sediment colors the surface. 100% directly paints the color of the sediment onto the surface"
	)

	color_src: StringProperty(
		name="Color",
		description="Color image texture"
	)

	color_rain: FloatProperty(
		default=10,
		min=1, max=100.0,
		subtype="PERCENTAGE",
		name="Rain",
		description="Amount of rain per iteration. Small values focus more on small details in geometry"
	)

	color_evaporation: FloatProperty(
		default=1,
		min=1, max=99.0,
		subtype="PERCENTAGE",
		name="Evaporation",
		description="Amount of water evaporated per iteration. Low values focus transport on concentrated flows, high values spread more evenly across the terrain geometry"
	)

	color_detail: FloatProperty(
		default=50,
		min=1, soft_max=100.0, max=200,
		subtype="PERCENTAGE",
		name="Detail",
		description="Lower values create simpler patterns"
	)

	color_acceleration: FloatProperty(
		default=50,
		min=1, soft_max=100.0, max=200,
		subtype="PERCENTAGE",
		name="Acceleration",
		description="Higher values lead to longer streaks"
	)

	color_lifetime: IntProperty(
		default=50,
		min=1, max=300,
		soft_max=100,
		name="Lifetime",
		description="Number of steps a particle will take per iteration"
	)

	color_speed: FloatProperty(
		default=25,
		min=1.0, soft_max=100.0, max=200,
		subtype="PERCENTAGE",
		name="Flow speed",
		description="Higher values lead to faster transport of material"
	)

	#------------------------- Utils

	is_generated: BoolProperty(name="Is generated", description="Prevents resource allocation for generated objects")

	map_result: StringProperty(name="Result map", description="Result heightmap")
	map_source: StringProperty(name="Source map", description="Source heightmap")
	map_base: StringProperty(name="Base map", description="Base heightmap")

	heightmap_gen_type: EnumProperty(
		default="proportional",
		items=(
			("normalized", "Normalized", "Scales heightmap to the range [0,1], 1 (white) being highest", 0),
			("proportional", "Proportional", "Preserves vertical angles", 1),
			("local", "Local size", "Preserves object height (without object scale applied)", 2),
			("world", "World size", "Preserves world height", 3),
		),
		name="Heightmap type",
		description="Heightmap generation type"
	)
	"""Heightmap generation type."""

	heightmap_gen_size: IntVectorProperty(
		default=(1024,1024),
		name="Heightmap size",
		min=16,
		max=4096,
		description="Image size for direct heightmap generation",
		size=2
	)
	"""Image size for direct heightmap generation."""

	gen_subscale: IntProperty(
		default=2,
		name="Subscale",
		min=1, max=16,
		description="Resolution divisor for landscape generation"
	)
	"""Resolution divisor for landscape generation"""
	
	#------------------------- Funcs
	
	def get_size(self):
		return tuple(self.img_size)

def get_exports()->list:
	return [
		ErosionGroup
	]
