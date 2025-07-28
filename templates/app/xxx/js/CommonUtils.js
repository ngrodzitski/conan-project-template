function myPrettyNumber(n) {
    if (n !== undefined)
        return n.toLocaleString(Qt.locale("en-US"), "f", 0);

    return "";
}
