import sys
import objc
import platform
from Cocoa import (
    NSObject,
    NSApplication,
    NSStatusBar,
    NSVariableStatusItemLength,
    NSImage,
    NSTextField,
    NSMakeRect,
    NSFont,
    NSTimer,
    NSView,
    NSButton,
    NSColor,
    NSUserNotificationCenter,
)
from AppKit import NSFontWeightRegular, NSPopover, NSViewController, NSMenu
import Quartz
import UserNotifications


# todo make customizable
time = 20 * 60


class HoverButton(NSButton):
    def mouseEntered_(self, event):
        self.layer().setBackgroundColor_(NSColor.selectedMenuItemColor().CGColor())
        self.layer().setCornerRadius_(6.0)
        self.layer().setMasksToBounds_(True)

    def mouseExited_(self, event):
        self.layer().setBackgroundColor_(Quartz.CGColorCreateGenericRGB(0, 0, 0, 0))
        self.layer().setCornerRadius_(0)
        self.layer().setMasksToBounds_(True)

    # -- STYLING --


def style_as_menu_button(btn):
    btn.setBordered_(False)
    btn.setBezelStyle_(0)  # Flat
    btn.setFont_(NSFont.menuFontOfSize_(13))
    btn.setAlignment_(16)  # Left align

    btn.setWantsLayer_(True)
    btn.layer().setBackgroundColor_(Quartz.CGColorCreateGenericRGB(0, 0, 0, 0))

    tracking = (
        objc.lookUpClass("NSTrackingArea")
        .alloc()
        .initWithRect_options_owner_userInfo_(
            btn.bounds(),
            0x01 | 0x10 | 0x20,  # mouseEnteredAndExited | activeAlways | inVisibleRect
            btn,
            None,
        )
    )
    btn.addTrackingArea_(tracking)


def style_as_menu_divider(view: NSView, width=196, height=1):
    view.setFrame_(NSMakeRect(0, 0, width, height))
    view.setWantsLayer_(True)
    view.layer().setBackgroundColor_(NSColor.separatorColor().CGColor())
    return view


def send_timer_finished_notification():
    content = UserNotifications.UNMutableNotificationContent.alloc().init()
    content.setTitle_("⏰ Time's Up!")
    content.setBody_("Time to rest your eyes 👁️💤")
    content.setSound_(UserNotifications.UNNotificationSound.defaultSound())

    trigger = UserNotifications.UNTimeIntervalNotificationTrigger.triggerWithTimeInterval_repeats_(
        1, False
    )
    request = (
        UserNotifications.UNNotificationRequest.requestWithIdentifier_content_trigger_(
            "rest_timer_done", content, trigger
        )
    )
    print("👁️💤 Sending notification")
    center = UserNotifications.UNUserNotificationCenter.currentNotificationCenter()
    center.addNotificationRequest_withCompletionHandler_(request, None)


class AppDelegate(NSObject):
    def applicationSupportsSecureRestorableState_(self, app):
        return True

    def applicationDidFinishLaunching_(self, notification):
        print("🧘‍♂️ Did finish launch")
        self.is_paused = False

        # Create status bar item
        self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(
            NSVariableStatusItemLength
        )
        self.status_item.button().setTarget_(self)
        self.status_item.button().setAction_("togglePopover:")

        # Initialize timer values
        self.time_remaining = time
        self.timer = (
            NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                1.0, self, "updateTimer:", None, True
            )
        )

        # Build the popover and its content
        self.createPopover()
        print("👁️ Popover ready")
        # Init state
        self.updateStatusIcon()
        print("👁️ Init state")

    def updateStatusIcon(self):
        symbol = "eye.slash.circle.fill" if self.is_paused else "eye.circle.fill"
        icon = NSImage.imageWithSystemSymbolName_accessibilityDescription_(symbol, None)
        config = objc.lookUpClass(
            "NSImageSymbolConfiguration"
        ).configurationWithPointSize_weight_(18, NSFontWeightRegular)
        icon = icon.imageWithSymbolConfiguration_(config)
        icon.setTemplate_(False)
        self.status_item.button().setImage_(icon)

    def createPopover(self):
        self.popover = NSPopover.alloc().init()
        self.popover.setBehavior_(1)  # Transient
        self.popover.setAnimates_(True)

        # View Controller
        controller = NSViewController.alloc().init()

        # Container view
        container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, 210, 100))

        # Timer label
        self.timer_text_field = NSTextField.alloc().initWithFrame_(
            NSMakeRect(12, 60, 196, 24)
        )
        self.timer_text_field.setBezeled_(False)
        self.timer_text_field.setDrawsBackground_(False)
        self.timer_text_field.setEditable_(False)
        self.timer_text_field.setSelectable_(False)
        self.timer_text_field.setFont_(NSFont.menuFontOfSize_(13))
        self.timer_text_field.setAlignment_(0)
        self.timer_text_field.setStringValue_(f"Eyes will rest in...{10 * ' '} 20:00")
        container.addSubview_(self.timer_text_field)

        # Pause/resume button
        self.pause_button = HoverButton.alloc().initWithFrame_(
            NSMakeRect(10.5, 40, 190.5, 24)
        )
        self.pause_button.setTitle_(" Pause ")
        self.pause_button.setTarget_(self)
        self.pause_button.setAction_("togglePause:")
        style_as_menu_button(self.pause_button)
        container.addSubview_(self.pause_button)

        divider = NSView.alloc().init()
        style_as_menu_divider(divider)
        divider.setFrameOrigin_((8, 35))
        container.addSubview_(divider)

        # Reset button
        self.reset_button = NSButton.alloc().initWithFrame_(NSMakeRect(14, 5, 80, 24))
        self.reset_button.setTitle_("Reset")
        self.reset_button.setTarget_(self)
        self.reset_button.setAction_("toggleReset:")
        # self.reset_button.setHidden_(True)
        style_as_menu_button(self.reset_button)
        container.addSubview_(self.reset_button)

        # Quit button
        self.quit_button = NSButton.alloc().initWithFrame_(NSMakeRect(166, 5, 80, 24))
        self.quit_button.setTitle_("Quit")
        self.quit_button.setTarget_(self)
        self.quit_button.setAction_("terminate:")
        style_as_menu_button(self.quit_button)
        container.addSubview_(self.quit_button)

        controller.setView_(container)
        self.popover.setContentViewController_(controller)

    @objc.IBAction
    def togglePopover_(self, sender):
        if self.popover.isShown():
            self.popover.performClose_(sender)
        else:
            self.popover.showRelativeToRect_ofView_preferredEdge_(
                self.status_item.button().bounds(),
                self.status_item.button(),
                3,  # NSMaxYEdge
            )
            # 👇 Force popover to accept events
            NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
            self.popover.contentViewController().view().window().makeKeyWindow()

    @objc.IBAction
    def togglePause_(self, sender):
        self.is_paused = not self.is_paused
        self.pause_button.setTitle_(" Resume " if self.is_paused else " Pause ")
        # self.reset_button.setHidden_(not self.is_paused)
        self.updateStatusIcon()

    @objc.IBAction
    def toggleReset_(self, sender):
        self.time_remaining = time
        self.is_paused = False
        self.pause_button.setTitle_(" Pause ")
        self.updateStatusIcon()

    @objc.IBAction
    def updateTimer_(self, _):
        if not self.is_paused and self.time_remaining > 0:
            self.time_remaining -= 1

        minutes, seconds = divmod(self.time_remaining, 60)
        time_str = f"Eyes will rest in... {10 * ' '}{minutes:02}:{seconds:02}"
        self.timer_text_field.setStringValue_(time_str)

        if self.time_remaining == 0 and self.timer:
            self.time_remaining = time + 20
            send_timer_finished_notification()

    @objc.IBAction
    def terminate_(self, sender):
        NSApplication.sharedApplication().terminate_(self)
        # pkill -f main.py


if __name__ == "__main__":
    print("🫡 Booting up...")
    print("OS version:", platform.mac_ver()[0])
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    print("🚀 App launched")
    app.run()
