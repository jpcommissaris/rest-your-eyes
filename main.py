import sys
import objc
import platform
from Cocoa import (
    NSObject,
    NSApplication,
    NSStatusBar,
    NSVariableStatusItemLength,
    NSMenu,
    NSMenuItem,
    NSImage,
)
from AppKit import NSFontWeightRegular


class AppDelegate(NSObject):
    # We do not need this. Use "user defaults" instead
    def applicationSupportsSecureRestorableState_(self, app):
      return True

    def applicationDidFinishLaunching_(self, notification):
        print("🧘‍♂️ Did finish launch")
        self.is_paused = False

        # Create status bar ref.
        status_bar = NSStatusBar.systemStatusBar()
        self.status_item = status_bar.statusItemWithLength_(NSVariableStatusItemLength)
        self.status_item.setHighlightMode_(True)
        print("hello1")

        # Set up menu
        self.menu = NSMenu.alloc().init()

        # Create pause/resume item
        self.pause_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Pause", "togglePause:", "")
        self.pause_item.setTarget_(self)
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "terminate:", "")

        # Add menu items
        self.menu.addItem_(self.pause_item)
        self.menu.addItem_(NSMenuItem.separatorItem())
        self.menu.addItem_(quit_item)

        # Init state (unpaused)
        print("👁️ Initiating")
        self.updateStatusIcon()

        self.status_item.setMenu_(self.menu)
        print("👁️ Menu set")
        print("🧘‍♂️ COMPLETE")

    
    @objc.IBAction
    def togglePause_(self, sender):
        self.is_paused = not self.is_paused
        self.updateStatusIcon()

    def updateStatusIcon(self):
        symbol = "eye.slash.circle.fill" if self.is_paused else "eye.circle.fill"
        self.pause_item.setTitle_("Resume" if self.is_paused else "Pause")

        icon = NSImage.imageWithSystemSymbolName_accessibilityDescription_(symbol, None)
        icon = icon or NSImage.imageWithSystemSymbolName_accessibilityDescription_("eye", None) # backup
        config = objc.lookUpClass("NSImageSymbolConfiguration").configurationWithPointSize_weight_(18, NSFontWeightRegular)
        icon = icon.imageWithSymbolConfiguration_(config)
        icon.setTemplate_(False)

        self.status_item.button().setImage_(icon)
        print(f"👁️ Updated Menu to {'PAUSED' if self.is_paused else 'ACTIVE'} state")

if __name__ == "__main__":
    print("🫡 Booting up...")
    print("OS version:", platform.mac_ver()[0])
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    print("🚀 App launched")
    app.run()

    # How to terminate:
    # press "quit" button
    # pkill -f your_script_name.py