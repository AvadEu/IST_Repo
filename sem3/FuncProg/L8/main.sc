def printAll(args: Any*): Unit = {
  if (args.isEmpty) {
    ()
  } else {
    val head = args.head
    val typeName = head.getClass.getSimpleName

    println(s"$typeName: $head")

    printAll(args.tail*)
  }
}

printAll(1, "hello", 3.14)

printAll(true, false, true)

printAll(List(1, 2), Some("value"))

printAll(Nil)