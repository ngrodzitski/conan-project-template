import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls

Button {
    // Enable a simple access to button color
    property color color: "gray"
    palette.button: color
}
