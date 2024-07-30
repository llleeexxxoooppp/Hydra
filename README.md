# Hydra - GPU Erosion in Blender

![2048 by 2048 vertex mountain range](./github/img/main_banner.webp)

Setup guide
===========

To install this project, download the latest [Release](https://github.com/ozikazina/Hydra/releases) and import the **zip** file into Blender add-ons, then activate it.

This project requires external dependencies (~5 MB), which can be downloaded with a provided button in the preferences. Executing this command will probably require elevated privileges. If the installation fails, launch Blender as an administrator and try again. If it succeeds, restart the app normally.

The add-on page will indicate whether the dependencies are installed.

If you are on Linux and get a `Failed to initialize OpenGL context` exception, try to switch to X11.

Manual dependency installation or update
----------------------------

Go to your Blender installation directory and to the version you want to use. Then navigate to the `python\bin` directory. As an example for Windows:

`C:\Program Files\Blender Foundation\Blender {Version}\{Version}\python\bin`

Once there, open this folder in the command line and install ModernGL through the Python executable:

`python.exe -m pip install --upgrade moderngl>=5.10.0`

or

`./python -m pip install --upgrade moderngl>=5.10.0`

ModernGL **version 5.10 or higher is required to work with Wayland**.

Uninstallation
------------

To uninstall the project, go to the add-ons tab and press remove. Removing the ModernGL library needs to be done manually.

Go to the Python folder specified above in the [Manual ModernGL installation](#manual-moderngl-installation) section and execute:

`python.exe -m pip uninstall moderngl`

or

`./python -m pip uninstall moderngl`

Add-on usage and principles
===========

This add-on supports erosion for individual **objects** and **images**. It can be found in the right side panel in **3D&nbsp;View** and **Image&nbsp;Editor** windows in the Hydra tab.

The add-on works by converting Blender objects and images into [internal heightmaps](#heightmaps-and-applying-results). These heightmaps have the resolution of the original image or a chosen resolution for objects. Resolution can drastically change the size and shape of resulting features:

| **256x256 px** | **512x512 px** |
| :--: | :--: |
| ![256 by 256 pixel heightmap example](./github/img/example_256.webp) | ![512 by 512 pixel heightmap example](./github/img/example_512.webp) |

- Once erosion starts, the resolution becomes locked. To pick a different resolution you first have to clear existing heightmaps for the current object.

- If the height of the object changes (e.g. you apply Scale) or the resolution of the original image changes, then you should first clear existing heightmaps.

- Objects with overlapping geometry are supported, but the resulting heightmap might create unwanted deformations when applied back to the object.

Heightmaps and applying results
----------

The add-on creates two internal heightmaps - **Source** and **Result**.

- `Source` - Starting point for erosion.
- `Result` - Result of erosion. It is automatically previewed.

Choosing different parameters and eroding again will start erosion from the Source map, giving the option to test different settings. To use the Result map as a starting point, use:
 - **Set & Continue** - which sets *Result* as *Source* and starts erosion - or
 - **Set as Source**

The *Result* map can be applied in the following ways using buttons in the *Heightmaps* subtab:

### Object options

<table>
<thead>
    <th width=100px>Type</th>
    <th>Description</th>
</thead>
<tr><td align="right"><code>Image</code></td><td>
        Creates a Blender image of the resulting heightmap.
</td></tr>
<tr><td align="right"><code>Nodes</code></td><td>
    Applies erosion as a Geometry Nodes group.
</td></tr>
<tr><td align="right"><code>Modifier</code></td><td>
    Applies erosion as a Displace modifier.
</td></tr>
<tr><td align="right"><code>Displacement</code></td><td>
    Adds a displacement map to the first material slot. Creates material if necessary.
</td></tr>
<tr><td align="right"><code>Bump</code></td><td>
    Adds a bump map to the first material slot. Creates material if necessary.
</td></tr>
<tr><td align="right"><code>Mesh</code></td><td>
    Applies modifiers to the mesh. Available if the preview or modifier option was chosen.
</td>

</tr></table>

### Image options

<table>
<thead>
    <th width=100px>Type</th>
    <th>Description</th>
</thead>
<tr><td align="right"><code>Image</code></td><td>
        Creates a new Blender image of the resulting heightmap. Unlike the image preview, this image won't be erased by launching erosion.
</td></tr>
<tr><td align="right"><code>To&nbsp;Original</code></td><td>
    Writes the resulting heightmap to the original image.
</td></tr>
</table>

Water erosion
=============

The main focus of this add-on is water erosion, where the flow of water carves material away and deposits it lower down. Two types of water erosion are implemented: particle-based and pipe-based.

Both types have a **Simulation resolution** slider, which allows the user to simulate erosion at different scales. It is recommended to start at **512x512** pixels for large-scale features.

Both types also support variable hardness in the **Advanced** settings.

Particle-based erosion
----------------------

Particle-based erosion simulates water using particles moving across the terrain. It is stable for almost any terrain and resolution, but aggressive settings can sometimes produce errors around borders.

The number of particles simulated is fixed and **doesn't change with the heightmap resolution**. It can be increased for higher resolutions using the **Iterations** property.

![Particle-based water erosion example.](./github/img/example_particle.webp)

It has the following parameters:

| Parameter | Description |
| --: | -- |
| `Iterations` | Number of iterations to perform. Increases the number of particles simulated. |
| `Lifetime` | Number of steps a particle can take in an iteration. |
| `Smoothness` | Creates smoother and finer surface features. |
| `Deposition` | Strength of sedimentation. Can be used to disable sedimentation. |
| `Capacity` | Particle material capacity. Increases erosion strength. |
| `Acceleration` | Defines how strongly slopes affect particle movement. Increases erosion strength. |
| `Drag` | Slows down particle movement. Low drag creates larger streaks. |

### Parameter examples

| | |
| :--: | :--: |
| High capacity | High lifetime |
| ![Higher capacity](./github/img/params_capacity.webp) | ![Higher lifetime](./github/img/params_lifetime.webp) |
| High smoothness | Low drag |
| ![High smoothness](./github/img/params_smooth.webp) | ![Low drag](./github/img/params_drag.webp) |

Pipe-based erosion
------------------

Pipe-based erosion creates more subtle sand-like terrains, but it is more difficult to set up and can be unstable. If the resulting terrain has ugly peaks, try decreasing capacity, iteration count, or increasing hardness.

![Pipe-based water erosion example.](./github/img/example_pipe.webp)

> When eroding images the effects of erosion can be hard to see in the resulting image. You can use the [Landscape](#landscape-generation) tab to see the results better.

It has the following parameters:

| Parameter | Description |
| --: | -- |
| `Iterations` | Number of iterations to perform. |
| `Hardness` | Concentrates erosion to larger streams. |
| `Capacity` | Increases erosion strength. |
| `Rain` | Low values bring out more detail. Higher values create larger gulleys. |

### Parameter examples

| | |
| :--: | :--: |
| Original | High hardness + High Iterations |
| ![Original](./github/img/params_mei_original.webp) | ![Higher hardness, high iterations](./github/img/params_mei_hardness.webp) |
| Low rain + High hardness | High rain + Low capacity |
| ![Low rain, high hardness](./github/img/params_mei_low_rain.webp) | ![High rain, low capacity](./github/img/params_mei_rain.webp) |

### Water source

Pipe-based erosion can use a **texture as a water source** in the **Advanced** settings. Water is otherwise added evenly across the entire terrain.

| Source | Result |
| :--: | :--: |
| ![Original](./github/img/mei_water_src.webp) | ![Result](./github/img/mei_water_res.webp) |

Thermal erosion
===============

The add-on similarly supports thermal erosion, where steep surfaces cause material to slide down. It produces smooth slopes with a specified maximum angle. It can also be used to fix extreme peaks and gulleys produced by aggressive water erosion.

![Thermal erosion example.](./github/img/example_thermal.webp)

Snow simulation
===============

The add-on offers a simple snow simulation, where a thin layer of material is placed on the terrain and moved by gravity. It can be used to simulate snow, sand, or gravel deposits or to fill deep gulleys.

![Snow simulation example.](./github/img/example_snow.webp)

Snow simulation also outputs a texture with the resulting snow placement.

![Snow texture example.](./github/img/example_snow2.webp)

Extras - Color transport
=========

Color transport takes an image and moves colors around based on the flow of water.

![Color transport example](./github/img/example_color.webp)

Similarly to water erosion, color transport has two solvers with different characteristics: particle-based and pipe-based.

### Particle-based color transport

| | |
| :--: | :--: |
| Default | High lifetime / Strength |
| ![Default color transport example](./github/img/color_default.webp) | ![High lifetime example](./github/img/color_high_lifetime.webp) |
| Low acceleration / Strength | Low detail |
| ![Low acceleration example](./github/img/color_low_accel.webp) | ![Low detail example](./github/img/color_low_detail.webp) |

### Pipe-based color transport

| | |
| :--: | :--: |
| High evaporation | Low detail |
| ![High evaporation example](./github/img/color_mei_high_evap.webp) | ![Low detail example](./github/img/color_mei_low_detail.webp) |
| High flow speed | High rain |
| ![High flow speed example](./github/img/color_mei_high_flow.webp) | ![High rain example](./github/img/color_mei_high_rain.webp) |

Extras - Flow
=========

The output texture of this operation stores paths of flowing particles. Some particle settings are shared with water erosion.

| Default | Low drag |
| :--: | :--: |
| ![Flow map example](./github/img/flow_default.webp) | ![Low drag flow map example](./github/img/flow_low_drag.webp) |

Heightmap generation
====================

Heightmaps can be generated directly at an arbitrary resolution. Cached heightmaps can also be directly exported in this tab. The following types of heightmaps can be generated:
| Type | Descripion |
| --: | -- |
| `Normalized` | Heights are scaled to the range \[0,1\]. |
| `Proportional` | Vertical angles are preserved. |
| `Local size` | Equal to object height without scale applied. |
| `World size` | Equal to world height. |

Landscape generation
====================
The image viewer tab also has a utility to generate landscapes directly from heightmaps. It is placed at the 3D cursor and a 3D View is automatically opened to view it.

![Landscape generation example](./github/img/landscape.webp)

Future plans
============
 - Water source texture for particle-based erosion
 - Simple planetary erosion
 - CUDA acceleration
 - Unified node-based UI (hopefully one day)

License
=======

This project is released under the MIT license. It is also a Bachelor's thesis implementation for the Brno University of Technology, other limitations may therefore apply.