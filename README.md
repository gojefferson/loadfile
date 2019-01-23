# loadfile
Convert .DAT load files to CSV or JSON

Usage: loadfile [OPTIONS] SOURCE DEST

  Converts a .DAT formatted loadfile to CSV or JSON.

  SOURCE: the the file you wish to convert

  DEST: the directory where the converted file will be created.

  The converted file will have the same name as the original file, with
  either .csv or .json added at the end.

Options:
  -j, --json  Whether to convert to JSON, rather than CSV (the default)
  --help      Show this message and exit.
  
