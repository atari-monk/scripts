function GetHashtableFromArguments {
    param (
        [string[]]$argsArray
    )

    $paramsHashtable = @{}

    for ($i = 0; $i -lt $argsArray.Length; $i += 2) {
        $key = $argsArray[$i]
        $value = $argsArray[$i + 1]

        $key = $key.TrimStart('-')

        $paramsHashtable[$key] = $value
    }

    return $paramsHashtable
}
