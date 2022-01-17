# NodeTree Source
Blender 3D add-on for converting material nodes into python source code and storing it in the library.

Add-on functionality
-
When you click on the "Material to Text" button the current material node tree source code is created and shown in the "Text Editor" window.

<img src="https://b3d.interplanety.org/wp-content/upload_content/2020/07/prevew_01_1200x600-400x200.jpg"><p>

You can copy this code, or save it to a file, and then paste or open it in any other Blender project. Executing this code, by clicking the “Run Script” button, the same material will be created in the project.

The “NodeTree Source” add-on has the library into which you can save the materials source code. To save the material sources to the local library, click the “Material to Library” button. Saved materials can be used from the library immediately.

<img src="https://b3d.interplanety.org/wp-content/upload_content/2020/07/prevew_02_1200x600-400x200.jpg"><p>

If you want to distribute your materials to other users, the “NodeTree Source” material library can be compiled into a separate add-on. Specify the path and click the “Distribute Library as Add-on” button. The complete archive with an add-on that includes the entire library of materials will be created. Users just need to download the add-on you provided and install it, after which they can immediately use the materials you provide.

Important
-
The local materials library is stored in the add-on directory. If you need to temporarily remove or reinstall the add-on, be sure to back up the library in a separate place on the disk first. After reinstalling the addon, the library can be restored simply by copying it to the "nodetree_source_library" directory of the add-on.

The "Material", "World", "Geometry Nodes", "Lights" and "Compositing" nodes are supported.

Current add-on version
-
1.2.4.

Blender versions
-
2.93, 3.0, 3.1

Location and call
-
“3D Viewport” window – N-panel – the “NodeTree Source” tab

Installation
-
- Download the *.zip archive with the add-on distributive.
- The “Preferences” window — Add-ons — Install… — specify the downloaded archive.

Version history
-
1.2.4.
- Fixed issue with some symbols in materials names

1.2.3.
- Fixed issue with materials from the Adobe Substance add-on

- 1.2.2.
- Fixed issue with node groups node trees input-output nodes
- Fixed issue with Frame node

1.2.1.
- Fixed issue with node groups input-output nodes

1.2.0.
- Added Geometry Nodes support
- Minimum Blender compatibility increased to 2.93 for supporting Geometry Nodes

1.1.0.
- Added nodes support for lights

1.0.2.
- Some improvements in bl_types conversion and with indents (deep)

1.0.1.
- Fixed the bug with groups in compositor
- Fixed the bug with tabulation in Mapping nodes sources
- Add "hide" node property to processing
- Fixed ColorRamp node

1.0.0.
- This release.
