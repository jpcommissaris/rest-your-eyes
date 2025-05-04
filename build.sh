#!/bin/bash

echo "🧹 Cleaning old build and dist folders..."
rm -rf build dist

echo "⚙️  Building app with py2app..."
python3 setup.py py2app

echo "🧹 Stripping extended attributes..."
xattr -cr "dist/Rest Your Eyes.app"

echo "🔏 Ad-hoc signing the app..."
codesign --force --deep --sign - "dist/Rest Your Eyes.app"

echo "✅ Build complete! Find your app in dist/Rest Your Eyes.app"