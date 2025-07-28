#include <${src_path_prefix}${styled_name}/version.hpp>

#include <iostream>
#include <filesystem>
#include <stdexcept>

//#if $qml
#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QQmlComponent>
#include <QQuickWindow>
#include <QObject>
#include <QDebug>
#include <QFile>

//#end if
#include <fmt/format.h>

namespace ${cpp_namespace_prefix}${styled_name} {

namespace fs = std::filesystem;

//
// main()
//

int main(int argc, char** argv)
{
    // TODO: Insert your logic here.

//#if "corporate_tag_normalized_word" in self.keys()
//#set $macro_prefix = $corporate_tag_normalized_word.upper() + "_" + $name.upper()
//#else
//#set $macro_prefix = $name.upper()
//#end if

    std::cout << fmt::format( "{} v{}.{}.{}",
                              fs::path( argv[ 0 ] ).filename().string(),
                              ${macro_prefix}_VERSION_MAJOR,
                              ${macro_prefix}_VERSION_MINOR,
                              ${macro_prefix}_VERSION_PATCH ) << std::endl;

    for( int i=1; i < argc; ++i )
    {
        std::cout << fmt::format("argv[{}]: {}", i, argv[i] ) << std::endl;
    }
//#if $qml
    //#if "Camel" == $style
    //#set $qtapp = "qtApp"
    //#set $objurl = "objUrl"
    //#set $retvalue = "retValue"
    //#set $loadjsfilelambda = "loadJSScript"
    //#set $filenamevar = "fileName"
    //#else
    //#set $qtapp = "qt_app"
    //#set $objurl = "obj_url"
    //#set $retvalue = "ret_value"
    //#set $filenamevar = "file_name"
    //#set $loadjsfilelambda = "load_js_script"
    //#end if

    QGuiApplication ${qtapp}( argc, argv );
    QQmlApplicationEngine engine;

    const QUrl url(
        QStringLiteral( "qrc:/${camel_name}/qml/MyMainWindow.qml" ) );

    {
        // Introduce Custom JS routines to qml-engine.
        auto ${loadjsfilelambda} = []( const QString & ${$filenamevar} ) {
            QFile file( ${$filenamevar} );
            if( !file.open( QIODevice::ReadOnly | QIODevice::Text ) )
            {
                throw std::runtime_error{
                    "unable to open file: '" + ${$filenamevar}.toStdString() + "'" };
            }
            QTextStream in( &file );
            return in.readAll();
        };

        QJSValue jsValue =
            engine.evaluate( ${loadjsfilelambda}( ":/${camel_name}/js/CommonUtils.js" ) );

        if( jsValue.isError() )
        {
            qWarning().nospace()
                << "Failed to apply script: /${camel_name}/js/CommonUtils.js: line:"
                << jsValue.property( "lineNumber" ).toInt() << ":"
                << jsValue.toString();

                throw std::runtime_error{ jsValue.toString().toStdString() };
        }
    }

    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreated,
        &${qtapp},
        [ url ]( QObject * obj, const QUrl & ${objurl} ) {
            if( !obj && url == ${objurl} ) QCoreApplication::exit( -1 );
        },
        Qt::QueuedConnection );
    engine.load( url );

    const auto ${retvalue} = qtApp.exec();
    if( 0 != ${retvalue} )
    {
        qWarning() << "Application finished with error...";
    }
//#end if

    return 0;
}

}  // namespace ${cpp_namespace_prefix}${styled_name}
