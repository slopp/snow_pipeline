
function transform(line) {
    var values = JSON.parse(line)
    // remove bad fields
    delete values["archive"]
    delete values["Parks-n-Pipes"]
    var jsonString = JSON.stringify(values);
    return jsonString;
}