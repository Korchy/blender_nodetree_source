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

The "Material", "World" and "Compositing" nodes are supported.

Current add-on version
-
1.0.1.

Blender versions
-
2.83

Location and call
-
“3D Viewport” window – N-panel – the “NodeTree Source” tab

Installation
-
- Download the *.zip archive with the add-on distributive.
- The “Preferences” window — Add-ons — Install… — specify the downloaded archive.

Version history
-
1.0.1.
- Fixed bug with groups in compositor
- Fixed bug with tabulation in Mapping nodes sources

1.0.0.
- This release.
