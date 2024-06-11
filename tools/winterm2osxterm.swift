#!/usr/bin/env swift

import Foundation
import AppKit

func convertColorToNSData(red: CGFloat, green: CGFloat, blue: CGFloat, alpha: CGFloat = 1.0) -> Data {
    let color = NSColor(calibratedRed: red, green: green, blue: blue, alpha: alpha)
    return try! NSKeyedArchiver.archivedData(withRootObject: color, requiringSecureCoding: false)
}

func windowsToMacColorScheme(windowsJSONPath: String, macPlistPath: String) {
    let fileManager = FileManager.default

    guard let data = fileManager.contents(atPath: windowsJSONPath),
          let jsonObject = try? JSONSerialization.jsonObject(with: data, options: []),
          let scheme = jsonObject as? [String: Any] else {
        print("Failed to read or parse the JSON file.")
        return
    }

    guard let schemeName = scheme["name"] as? String else {
        print("Failed to get scheme name.")
        return
    }

    let colors = scheme

    // Map Windows Terminal color scheme keys to macOS Terminal color keys
    let colorMapping: [String: String] = [
        "background": "BackgroundColor",
        "foreground": "TextColor",
        "black": "ANSIBlackColor",
        "blue": "ANSIBlueColor",
        "brightBlack": "ANSIBrightBlackColor",
        "brightBlue": "ANSIBrightBlueColor",
        "brightCyan": "ANSIBrightCyanColor",
        "brightGreen": "ANSIBrightGreenColor",
        "brightPurple": "ANSIBrightMagentaColor",
        "brightRed": "ANSIBrightRedColor",
        "brightWhite": "ANSIBrightWhiteColor",
        "brightYellow": "ANSIBrightYellowColor",
        "cyan": "ANSICyanColor",
        "green": "ANSIGreenColor",
        "purple": "ANSIMagentaColor",
        "red": "ANSIRedColor",
        "white": "ANSIWhiteColor",
        "yellow": "ANSIYellowColor"
    ]

    var macScheme: [String: Any] = [
        "name": schemeName,
        "type": "Window Settings",
        "ProfileCurrentVersion": 2.04
    ]

    for (windowsKey, macKey) in colorMapping {
        if let colorValue = colors[windowsKey] as? String {
            // Convert the color value from #RRGGBB to macOS Terminal format (r, g, b, a)
            let r = CGFloat(Int(colorValue.prefix(3).suffix(2), radix: 16)!) / 255.0
            let g = CGFloat(Int(colorValue.prefix(5).suffix(2), radix: 16)!) / 255.0
            let b = CGFloat(Int(colorValue.suffix(2), radix: 16)!) / 255.0
            let colorData = convertColorToNSData(red: r, green: g, blue: b)
            macScheme[macKey] = colorData
        }
    }

    // Write the macOS Terminal color scheme to a plist file
    let plistURL = URL(fileURLWithPath: macPlistPath)
    let plistData = try! PropertyListSerialization.data(fromPropertyList: macScheme, format: .xml, options: 0)
    try! plistData.write(to: plistURL)

    print("Converted scheme '\(schemeName)' to macOS Terminal format.")
}

// Example usage
let arguments = CommandLine.arguments
if arguments.count < 2 {
    print("Usage: ./script.swift <windows_terminal_schemes.json>")
    exit(1)
}

let windowsJSONPath = arguments[1]
let windowsJSONURL = URL(fileURLWithPath: windowsJSONPath)
if !FileManager.default.fileExists(atPath: windowsJSONPath) {
    print("File not found: \(windowsJSONPath)")
    exit(1)
}

let macPlistPath = windowsJSONURL.deletingLastPathComponent().deletingLastPathComponent()
    .appendingPathComponent("mac")
    .appendingPathComponent(windowsJSONURL.deletingPathExtension().deletingPathExtension().lastPathComponent + ".terminal")
    .path

windowsToMacColorScheme(windowsJSONPath: windowsJSONPath, macPlistPath: macPlistPath)
