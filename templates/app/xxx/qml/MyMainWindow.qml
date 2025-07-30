import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls

Window {
    width: 600
    height: 400
    visible: true
    color: "whitesmoke"

    FontLoader {
        id: blocks3x3Font
        source: "qrc:/@{names.camel}/fonts/blocks-3x3-monospaced.ttf"
        onStatusChanged: {
            if (status == FontLoader.Ready) {
                console.log("blocks-3x3-monospaced loaded successfully");
            } else if (status == FontLoader.Error) {
                console.log("Error loading blocks-3x3-monospaced font");
            }
        }
    }

    Dialog {
        anchors.centerIn: parent

        id: helloDialog
        modal: true
        title: qsTr("@{names.camel} app")
        standardButtons: Dialog.Ok

        contentItem: Label {
            text: qsTr("Hello!")
            font.pixelSize: 16
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    MyButton {
        anchors.centerIn: parent
        color: "yellow"
        text: "Click me"
        onClicked: {
            console.log("Button clicked!");
            helloDialog.open();
        }
    }



    Text {
        anchors.topMargin: 4
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top

        // Using CommonUtils.js
        text: "Big number: " + myPrettyNumber( 281308 * 1171 * 7 )

        // Using cystom font:
        font.family: blocks3x3Font.name
        font.pixelSize: 32
    }

    Image {
        anchors.right: parent.right
        anchors.bottom: parent.bottom

        // Using Images.
        source: "qrc:/@{names.camel}/images/sample_image.png"
    }
}
