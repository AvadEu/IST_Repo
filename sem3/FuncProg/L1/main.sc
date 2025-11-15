def polacz(a: List[String], sep: String): String = {
  if a == List() then "" else
    if a.length == 1 then a.head else a.head + sep + polacz(a.tail, sep)
}


polacz(List("a", "b", "c", "2"), "-")
polacz(List("1", "2"), "-----")
polacz(List(), ".")