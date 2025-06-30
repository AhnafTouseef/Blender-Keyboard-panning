import bpy, os
from .config import *


class BL_KEY_Pan_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    key_pan_up: bpy.props.StringProperty(
        name="Pan Up Key",
        description="Key to pan the view up (e.g., 'NumpadUp', 'W', 'Space', 'LButton').",
        default="NumpadUp",
        options={'ANIMATABLE'}
    )
    key_pan_down: bpy.props.StringProperty(
        name="Pan Down Key",
        description="Key to pan the view down (e.g., 'NumpadDown', 'S').",
        default="NumpadDown",
        options={'ANIMATABLE'}
    )
    key_pan_left: bpy.props.StringProperty(
        name="Pan Left Key",
        description="Key to pan the view left (e.g., 'NumpadLeft', 'A').",
        default="NumpadLeft",
        options={'ANIMATABLE'}
    )
    key_pan_right: bpy.props.StringProperty(
        name="Pan Right Key",
        description="Key to pan the view right (e.g., 'NumpadRight', 'D').",
        default="NumpadRight",
        options={'ANIMATABLE'}
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Customize Panning Hotkeys (Windows Only)", icon='FILE_SCRIPT')
        
        # UI for Pan Up Key
        row = box.row(align=True)
        row.prop(self, "key_pan_up")
        op = row.operator("key.set_key_modal", text="Set Key")
        op.target_property = "key_pan_up"
        op.target_label = "Pan Up Key" # Pass label for better modal feedback

        # UI for Pan Down Key
        row = box.row(align=True)
        row.prop(self, "key_pan_down")
        op = row.operator("key.set_key_modal", text="Set Key")
        op.target_property = "key_pan_down"
        op.target_label = "Pan Down Key"

        # UI for Pan Left Key
        row = box.row(align=True)
        row.prop(self, "key_pan_left")
        op = row.operator("key.set_key_modal", text="Set Key")
        op.target_property = "key_pan_left"
        op.target_label = "Pan Left Key"

        # UI for Pan Right Key
        row = box.row(align=True)
        row.prop(self, "key_pan_right")
        op = row.operator("key.set_key_modal", text="Set Key")
        op.target_property = "key_pan_right"
        op.target_label = "Pan Right Key"

        row = box.row(align=True)
        row.operator("key.generate_and_recompile_script", icon='FILE_REFRESH', text="Generate & Recompile Script")
        row.operator("key.reset_keys", text="🔄️Reset Keys")

        box.separator()
        box.label(text="Important Notes:")
        box.label(text="- Use the 'Set Key' button to press your desired key.")
        row_template = box.row(align=True)
        row_template.label(text="- Other settings (speed, acceleration) can be edited in:")
        row_template.operator("wm.url_open", text=TEMPLATE_FILENAME, icon='FILE_SCRIPT').url = \
            "file://" + os.path.join(os.path.dirname(__file__), TEMPLATE_FILENAME).replace("\\", "/")

        box.label(text="- The generated script will be '%s' and compiled to '%s'." % (GENERATED_FILENAME, COMPILED_FILENAME))

