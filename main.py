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
from Foundation import NSTimer


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

        # Setup timer
        self.time_remaining = 20 * 60  # 20 minutes in seconds

        self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1.0,                
            self,               
            "updateTimer:",     
            None,
            True                # repeats
        )

        # Timer item
        padded = f"Eyes will rest in...{' ' * 10}20:00"
        self.timer_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(padded, "noop:", "")

        # Conditional divider
        self.divider1 = NSMenuItem.separatorItem()
        self.divider1.setTarget_(self)
        self.divider1.setHidden_(True)

        # Pause resume item
        self.pause_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Pause", "togglePause:", "")
        self.pause_item.setTarget_(self)

        # Reset item
        self.reset_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Reset", "toggleReset:", "")
        self.reset_item.setTarget_(self) 
        self.reset_item.setHidden_(True)
 

        # Quit item
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "terminate:", "")

        # Add menu items
        self.menu.addItem_(self.timer_item)
        self.menu.addItem_(self.divider1)
        self.menu.addItem_(self.pause_item) 
        self.menu.addItem_(self.reset_item)
        self.menu.addItem_(NSMenuItem.separatorItem())
        self.menu.addItem_(quit_item)

        # Init state (unpaused)
        print("👁️ Initiating")
        self.updateStatusIcon()

        self.status_item.setMenu_(self.menu)
        print("👁️ Menu set")
        print("🧘‍♂️ COMPLETE")

    @objc.IBAction
    def noop_(self, sender):
        pass
    
    @objc.IBAction
    def togglePause_(self, sender):
        self.is_paused = not self.is_paused
        self.updateStatusIcon()
        self.resetClock()
    
    @objc.IBAction
    def toggleReset_(self, sender):
        self.is_paused = False
        self.updateStatusIcon()

    @objc.IBAction
    def updateTimer_(self, _):
        if self.time_remaining > 0:
            self.time_remaining -= 1
        else:
            self.timer.invalidate()
            self.timer = None

        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        time_str = f"{minutes:02d}:{seconds:02d}"

        # Update the menu item
        padded = f"Eyes will rest in...{' ' * 10}{time_str}"
        self.timer_item.setTitle_(padded)

    def updateStatusIcon(self):
        symbol = "eye.slash.circle.fill" if self.is_paused else "eye.circle.fill"
        self.pause_item.setTitle_("Resume" if self.is_paused else "Pause")

        icon = NSImage.imageWithSystemSymbolName_accessibilityDescription_(symbol, None)
        icon = icon or NSImage.imageWithSystemSymbolName_accessibilityDescription_("eye", None) # backup
        config = objc.lookUpClass("NSImageSymbolConfiguration").configurationWithPointSize_weight_(18, NSFontWeightRegular)
        icon = icon.imageWithSymbolConfiguration_(config)
        icon.setTemplate_(False)

        self.status_item.button().setImage_(icon)
        self.reset_item.setHidden_(not self.is_paused)
        self.divider1.setHidden_(not self.is_paused)
        print(f"👁️ Updated Menu to {'PAUSED' if self.is_paused else 'ACTIVE'} state")

    def resetClock(self): 
        pass

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