let joinStr lista =
  List.map (fun (s1, s2, s3, s4) -> s1 ^ s2 ^ s3 ^ s4) lista;;


joinStr [("a","b","c","d");("1","2","3","4");("x","y","z","w")];;
joinStr [];;
joinStr [("hello"," ","world","!");("foo","bar","baz","qux")];;